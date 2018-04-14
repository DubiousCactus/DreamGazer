/*
 * index.js
 * Copyright (C) 2018 transpalette <transpalette@translaptop>
 *
 * Distributed under terms of the MIT license.
 */
  
window.onload = function() {
  var photos = [
      'https://placehold.it/850x850',
      'https://placehold.it/850x850',
      'https://placehold.it/850x850',
      'https://placehold.it/850x850',
      'https://placehold.it/850x850',
      'https://placehold.it/850x850',
      'https://placehold.it/850x850',
      'https://placehold.it/850x850',
  ];

  var BACKEND_URL = 'http://localhost:5000';
  var screen = {};
  var image = {};
  var previousClock = null;
  var i = 0;
  var read = false;
  var coords = new Array(photos.length);
  var interval = 25; //ms

   $('#start').click(function(e) {
     $('#header').slideUp("slow", function() {
	 $('#placeholder').fadeOut('fast');
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
	.setGazeListener(function(data, clock) {
	  if (read && (previousClock == null || (clock - previousClock) >= interval)) {
	    if (typeof coords[i] == 'undefined') {
	      coords[i] = [];
	      console.log(coords);
	    }

	    coords[i].push(data);
	  }
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

    $.post(BACKEND_URL + '/api/' + i, json, function(data) {
      console.log(data);
    });

  }

  function submit() {
    $.get(BACKEND_URL + '/api/mozaique', function(data) {
      console.log(data);
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
  
  setTimeout(setListener, 300);
};
