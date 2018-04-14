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

   $('#start').click(function(e) {
     $('#header').slideUp("slow", function() {
	 $('#placeholder').fadeOut('fast');
	 $('.gaze').slideDown("slow");
	setInterval(slideShow, 3000);
     });
   });

    var gazing = false;
    var i = 0;

    function setListener() {
	webgazer.setRegression('ridge') /* currently must set regression and tracker */
	  .setTracker('clmtrackr')
	  .setGazeListener(function(data, clock) {
	       //console.log(data); [> data is an object containing an x and y key which are the x and y prediction coordinates (no bounds limiting) <]
	       //console.log(clock); [> elapsed time in milliseconds since webgazer.begin() was called <]
	  })
	  .begin()
	  .showPredictionPoints(true); /* shows a square every 100 milliseconds where current prediction is */
    }


    function slideShow() {
	changeImage();
	window.setInterval(changeImage, 10000);
    }

    function changeImage() {
	$('.gaze').fadeOut('slow');
	$('.gaze').attr('src', photos[i++]).fadeIn('slow')
    }
  
    setTimeout(setListener, 300);
};
