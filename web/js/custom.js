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
    const button = document.querySelector('#capture');
    const canvas = document.createElement('canvas');
    const player = document.getElementById('player');

    button.onclick = function () {
        canvas.width = player.videoWidth;
        canvas.height = player.videoHeight;
        canvas.getContext('2d').drawImage(player, 0, 0);
        let src = canvas.toDataURL('image/jpeg');
        blob = dataURItoBlob(src);
        const data = new FormData();
        data.append('photo', blob);
        $('.loader').addClass('show');
        axios.post('https://websdk.affle.co/image/api/image/recog', data).then(function (response) {
            $('.loader').removeClass('show');
            let data = response.data;
            if (data.found) {
                $('#success-animation').attr('src', 'images/sprite_24.gif')
                setTimeout(function () {
                    window.location.assign('https://www.sprite.com')
                }, 15000)
            } else {
                alert('Can not recognize the image. Please try again')
            }
            console.log(JSON.stringify(data))
        }, function (err) {
            $('.loader').removeClass('show');
        })

    };


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