function openCamera(id) {
    $('#' + id).fadeIn();
    $('html').addClass('openModal');
}

function closeCamera(id) {
    $('#' + id).fadeOut();
    $('html').removeClass('openModal');
}

$(document).ready(function () {

    const img = document.querySelector('#screenshot-img');
    const video = document.querySelector('#player');
    const button = document.querySelector('#capture');
    const canvas = document.createElement('canvas');

    button.onclick = function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        let src = canvas.toDataURL('image/jpeg');
        blob = dataURItoBlob(src);
        const data = new FormData();
        data.append('photo', blob);
        $('.cameraOverlay').addClass('loader');
        axios.post('/api/image/recog', data).then(function (data) {
            debugger
            $('.cameraOverlay').removeClass('loader');
            $('#success-animation').attr('src', 'images/gf_24.gif')
            console.log(JSON.stringify(data))
        }, function (err) {
            $('.cameraOverlay').removeClass('loader');
            $('#success-animation').attr('src', 'images/gf_24.gif')
            console.log(JSON.stringify(err))
        })

    };

    const player = document.getElementById('player');

    const constraints = {
        video: {
            facingMode: {
                exact: "environment"
            }
        }
    };

    navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
            player.srcObject = stream;
        }).catch(err => {
            alert('cant access camera')
            var source = document.createElement('source');
            source.setAttribute('src', 'images/test_video.mp4');
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