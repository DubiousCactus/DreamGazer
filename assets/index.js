/*
 * index.js
 * Copyright (C) 2018 transpalette <transpalette@translaptop>
 *
 * Distributed under terms of the MIT license.
 */
(function(){
  'use strict';
  
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
		   //setListener();
		   setTimeout(slideShow, 3000);
	   });
   });

   	var gazing = false;
   	var i = 0;

	function setListener() {
		console.log('setting listener');
		webgazer.setGazeListener(function(data, elapsedTime) {
			if (data == null)
				return;

			/*if (!gazing) {*/
				//console.log('gazing');
				////slideShow();
				//gazing = true;
			/*}*/

			var xprediction = data.x; //these x coordinates are relative to the viewport
			var yprediction = data.y; //these y coordinates are relative to the viewport
			console.log(xprediction);
		}).begin();
	}


	function slideShow() {
		console.log('slideshow');
		changeImage();
		window.setInterval(changeImage, 10000);
	}

	function changeImage() {
		webgazer.pause();
		$('.gaze').fadeOut('slow');
		$('.gaze').attr('src', photos[i++]).fadeIn('slow')
		webgazer.resume();
	}
})();
