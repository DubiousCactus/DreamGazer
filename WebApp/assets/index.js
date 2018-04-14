/*
 * index.js
 * Copyright (C) 2018 transpalette <transpalette@translaptop>
 *
 * Distributed under terms of the MIT license.
 */
// Global var.
var BACKEND_URL = 'http://localhost:5000';
var photos = [
    BACKEND_URL + '/images/johnny850x850.jpg',
    BACKEND_URL + '/images/clint850x850.jpg',
    BACKEND_URL + '/images/clooney850x850.jpg',
    BACKEND_URL + '/images/martin2850x850.jpg',
    BACKEND_URL + '/images/martin850x850.jpg',
];
var screen = {};
var image = {};
var previousClock = null;
var i = 0;
var read = false;
var coords = new Array(photos.length);
var interval = 25; //ms


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
    $.get(BACKEND_URL + '/api/mozaique', function (data) {
        console.log(data);
    });
}

window.onload = function () {
    
    $('#start_calibration').click(function (e) {
        $('#header').slideUp("slow", function () {
            //$('#placeholder').fadeOut('fast');
            $('#show').fadeOut('fast');
            $('.calibration').slideDown("slow");
        });

        StartCalibration();
    });

    function setListener() {
        webgazer.setRegression('ridge') /* currently must set regression and tracker */
            .setTracker('clmtrackr')
            .setGazeListener(function (data, clock) {
                if (data == null) {
                    return;
                }
                if (read && (previousClock == null || (clock - previousClock) >= interval)) {
                    if (typeof coords[i] == 'undefined') {
                        coords[i] = [];
                    }

                    coords[i].push({
                        'x': data.x,
                        'y': data.y
                    });
                }
            })
            .begin()
            .showPredictionPoints(true); /* shows a square every 100 milliseconds where current prediction is */
    }
    setTimeout(setListener, 300);
};
