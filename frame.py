import cv2
from match import Match


class Frame:

    def __init__(self):
        self.match = Match()

    def read_video(self, video):
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()

        while success:
            success, image = vidcap.read()
            if(success):
                result = self.match.match_image(image)
                if result['found'] == True:
                    return result

        match_result = {}
        match_result['found'] = False
        match_result['file'] = ''

        return match_result
