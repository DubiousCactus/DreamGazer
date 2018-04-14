/*
 * index.js
 * Copyright (C) 2018 transpalette <transpalette@translaptop>
 *
 * Distributed under terms of the MIT license.
 */

window.onload = function () {
    var BACKEND_URL = 'http://localhost:5000';
    var photos = [
        BACKEND_URL + '/images/image1.jpg',
        BACKEND_URL + '/images/image2.jpg',
        BACKEND_URL + '/images/image3.jpg',
        BACKEND_URL + '/images/image4.jpg',
        BACKEND_URL + '/images/image5.jpg',
        BACKEND_URL + '/images/image6.jpg',
        BACKEND_URL + '/images/image7.jpg',
        BACKEND_URL + '/images/image8.jpg',
        BACKEND_URL + '/images/image9.jpg',
        BACKEND_URL + '/images/image10.jpg'
    ];
    var screen = {};
    var image = {};
    var previousClock = null;
    var i = 0;
    var read = false;
    var coords = new Array(photos.length);
    var interval = 25; //ms

    $('#start_calibration').click(function (e) {
        $('#header').slideUp("slow", function () {
            //$('#placeholder').fadeOut('fast');
            $('#show').fadeOut('fast');
            $('.calibration').slideDown("slow");
        });
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "assets/webgazer.js.";
        document.getElementsByTagName("head")[0].appendChild(script);

        StartCalibration();  // CNC added
        window.open("calibrationinstructions.html", "", "width=450,height=450");
    });

    $('#start_show').click(function (e) {
        $('#header').slideUp("slow", function () {
            //$('#placeholder').fadeIn('fast');
            $('#show').fadeIn('fast');
            $('.gaze').slideDown("slow");
            setTimeout(slideShow, 3000);
        });
    });

    function getScreenInfo() {
        screen.width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
        screen.height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    }

    function getImageInfo() {
        image.offsetX = $('.gaze').offset().left;
        image.offsetY = $('.gaze').offset().top;
        image.width = $('.gaze').width();
        image.height = $('.gaze').height();
    }

    function setListener() {
        webgazer.setRegression('ridge') /* currently must set regression and tracker */
            .setTracker('clmtrackr')
            .setGazeListener(function (data, clock) {
                if (data == null) {
                    return;
                }
                //if (read && (previousClock == null || (clock - previousClock) >= interval)) {
                    if (typeof coords[i] == 'undefined') {
                        coords[i] = [];
                    }

                    coords[i].push({
                        'x': data.x,
                        'y': data.y
                    });
                //}
            })
            .begin()
            .showPredictionPoints(true); /* shows a square every 100 milliseconds where current prediction is */
    }

    function slideShow() {
        $('.gaze').attr('src', photos[i]).fadeIn('slow')
        getScreenInfo();
        getImageInfo();
        read = true;
        window.setInterval(changeImage, 10000);
    }

    function sendData() {
        var json = {
            "screenWidth": screen.width,
            "screenHeight": screen.height,
            "imgWidth": image.width,
            "imgHeight": image.height,
            "imgOffsetX": image.offsetX,
            "imgOffsetY": image.offsetY,
            "coordinates": coords[i]
        };

        console.log(json);

        $.ajax({
            type: 'POST',
            url: BACKEND_URL + '/api/' + i,
            contentType: 'application/json',
            data: JSON.stringify(json),
            success: function (data) {
                console.log(data);
            }
        });

    }

    function submit() {
        $.get(BACKEND_URL + '/api/mosaic', function (data) {
            console.log(data);
            photos = [];
            obj = JSON.parse(data);
            obj.forEach(function(mosaicUrl) {
                photos.push(BACKEND_URL + mosaicUrl);
            });
            i = 0; //Reset slideshow
        });
    }

    function changeImage() {
        if (i >= photos.length) {
            submit();
            return;
        }

        read = false;
        sendData();
        $('.gaze').fadeOut('slow');
        $('.gaze').attr('src', photos[i++]).fadeIn('slow')
        read = true;
    }

    function StartCalibration() {
        document.getElementById("Accuracy").innerHTML = "<a>Not yet Calibrated</a>";
        ClearCalibration();
        PopUpInstruction();
    }

    setTimeout(setListener, 300);
};
