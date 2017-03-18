
function videosetup(elementid, aspectRatio){

	var myPlayer = videojs(elementid);

    function resizeVideoJS(){

      // Get the parent element's actual width
      //var width = document.getElementById('signbody').offsetWidth;
      // Set width to fill parent element, Set height
      //myPlayer.dimensions(width, width * aspectRatio);
    }

    myPlayer.ready(function(){
        resizeVideoJS(); // Initialize the function
        window.onresize = resizeVideoJS; // Call the function on resize

        myPlayer.removeChild("bigPlayButton");

    	myPlayer.on('fullscreenchange', function(){
    		if(myPlayer.isFullscreen()) {
    			myPlayer.removeClass("vjs-static-controls");
    		} else {
    			myPlayer.addClass("vjs-static-controls");
    		}
    	});
     });
}


function uploadModalSetup() {
    'use strict';

    // UPLOAD CLASS DEFINITION
    // ======================

    var dropZone = document.getElementById('drop-zone');
    var uploadForm = document.getElementById('js-upload-form');

    var startUpload = function(files) {
        console.log(files)
    }

    uploadForm.addEventListener('submit', function(e) {
        var uploadFiles = document.getElementById('js-upload-files').files;
        e.preventDefault()

        startUpload(uploadFiles)
    })

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files)
    }

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    }

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    }

};
