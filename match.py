import cv2
import glob
from operator import itemgetter
import os

FLANN_INDEX_KDTREE = 0


class Match:
    ref_images = []
    sift = None
    flann = None

    def __init__(self):
        self.sift = cv2.xfeatures2d.SIFT_create()

        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

        for img_itr_file in glob.glob("ref_image/*.*"):

            img_cv_itr = cv2.imread(img_itr_file, 0)

            kp,  img_cv_itr_desc = self.sift.detectAndCompute(img_cv_itr, None)

            img_obj = {}

            img_obj['img_desc'] = img_cv_itr_desc
            img_obj['file_name'] = img_itr_file

            self.ref_images.append(img_obj)

    def match_image(self, image_to_find):

        # cv2.imshow('image', image_to_find)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # image_to_find_resized_scaled = cv2.resize(
        #     image_to_find, (0, 0), fx=0.5, fy=0.5)

        # newx, newy = image_to_find_resized_scaled.shape[1] / \
        #     2, image_to_find_resized_scaled.shape[0]/2

        # image_to_find_resized_final = cv2.resize(
        #     image_to_find_resized_scaled, (newx, newy), fx=0.5, fy=0.5)

        kp2, image_to_find_resized_final_desc = self.sift.detectAndCompute(
            image_to_find, None)

        results = []

        for ref_image in self.ref_images:

            matches = self.flann.knnMatch(
                ref_image['img_desc'], image_to_find_resized_final_desc, 2)

            good = []
            for m, n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)

            obj = {}
            obj['file_name'] = ref_image['file_name']
            obj['score'] = len(good)

            if len(good) >= 10:
                results.append(obj)

        sorted_result = sorted(results, key=itemgetter('score'), reverse=True)

        match_result = {}
        match_result['found'] = False
        match_result['file'] = ''

        if len(sorted_result) > 0:
            match_result['found'] = True
            match_result['file'] = os.path.basename(
                sorted_result[0]['file_name'])

        return match_result
