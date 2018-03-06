$(document).ready(function () {

    const img = document.querySelector('#screenshot-img');
    const video = document.querySelector('#player');
    const canvas = document.createElement('canvas');

    video.onclick = function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        img.src = canvas.toDataURL('image/jpeg');
        blob = dataURItoBlob(img.src);
        const data = new FormData();
        data.append('photo', blob)
        axios.post('/api/image/recog', data).then(function (data) {
            alert(JSON.stringify(data))
        }, function (err) {
            alert(JSON.stringify(err))
        })

    };

    const player = document.getElementById('player');

    const constraints = {
        video: {
            width: {
                min: 720,
                ideal: 1280,
                max: 1280
            },
            height: {
                min: 776,
                ideal: 720,
                max: 720
            }
        }
    };

    navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
            player.srcObject = stream;
        }).catch(err => {
            var source = document.createElement('source');
            source.setAttribute('src', '/tenplate/test.mp4');
            player.appendChild(source);
            player.play();
        })

    function dataURItoBlob(dataURI) {
        var binary = atob(dataURI.split(',')[1]);
        var array = [];
        for (var i = 0; i < binary.length; i++) {
            array.push(binary.charCodeAt(i));
        }
        return new Blob([new Uint8Array(array)], {
            type: 'image/jpeg'
        });
    }
});