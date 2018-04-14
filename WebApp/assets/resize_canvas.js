/**
* This function occurs on resizing the frame
* clears the canvas & then resizes it (as plots have moved position, can't resize without clear)
*/

function resizeCanvas() {
    var canvas = document.getElementById('plotting_canvas');
    if (canvas != null) {
        canvas.style.width = window.innerWidth + 'px';
        setTimeout(function () {
            canvas.style.height = window.innerHeight + 'px';
        }, 0);
    //canvas.width = window.innerWidth;
    //canvas.height = window.innerHeight;
    }
};

window.onresize = resizeCanvas;
resizeCanvas();
