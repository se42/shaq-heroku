// // GET private image resource for thumbnail if issue_image_url exists
// (function() {
// 	document.body.onload = function() {
// 		var url_field = document.getElementById("id_issue_image_url");
// 		if (url_field.hasAttribute("value")) {
// 			document.getElementById("preview").src = url_field.value;
// 			get_private_S3_resource("preview", amz_sign_s3);
// 		};
// 	};
// })();

// // Monitor file_input file input object for changes to initiate PUT sequence
// (function() {
// 	document.getElementById("file_input").onchange = function(){
// 		var files = document.getElementById("file_input").files;
// 		var file = files[0];
// 		if(file == null){
// 			alert("No file selected.");
// 		}
// 		else{
// 			// get_signed_request(file);
// 			var folder = "int-nc-form";
// 			upload_private_S3_resource(file, folder, update_form_page_elements);
// 		}
// 	};
// })();

// // pass this function into upload_private_S3_resource to work with
// // the file's UN-signed URL when upload is complete
// function update_form_page_elements(url) {
// 	document.getElementById("id_issue_image_url").value = url;
// 	document.getElementById("preview").src = url;
// 	get_private_S3_resource("preview", amz_sign_s3);
// }

// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------

// (function() {
// 	document.body.onload = function() {
// 		// for each img element in the image-preview-panel div, call
// 		// get_s3_resource on the img element with amz_sign_s3 url
// 		var imagePanels = document.getElementById("image-preview-panel").children;
// 		for (var i = imagePanels.length - 1; i >= 0; i--) {
// 			var imgElement = imagePanels[i].getElementsByTagName("img")[0];
// 			get_s3_resource(imgElement, amz_sign_s3);
// 			var imgInput = imagePanels[i].getElementsByTagName("input")[0];
// 			imgInput.onchange = startS3Upload(imgInput.id);
// 		}
// 	};
// })();

// (function() {
// 	document.getElementById("add-image-button").onclick = function() {
// 		// Code to create a new image select thumbnail/preview element
// 		// as well as a new hidden input for the actual image_url input.
// 		// Don't forget to update the TOTAL_FORMS count too.
// 		// Also, this shouldn't work/should be hidden if there is an undefined image input/url
// 		// 
// 		// 1 - create the hidden url input fields
// 		// 2 - run the standard create_image_input_preview function
// 	};
// })();


(function() {
	document.body.onload = function() {
		var imageInputGroups = $(".image-input-group");
		for (var i = 0; i < imageInputGroups.length; i++) {
			var previewImage = imageInputGroups[i].getElementsByTagName("img")[0];
			var imageInput = imageInputGroups[i].getElementsByTagName("input")[0];
			get_s3_resource(previewImage, amz_sign_s3);
			imageInput.addEventListener("change", function() {
				startS3Upload(imageInput.id, function() {
					get_s3_resource(previewImage, amz_sign_s3);
				});
			});
		}
	};
})();

// (function() {
// 	document.body.onload = function() {
// 		var imagePreviews = $(".image-previews");
// 		for (var i = 0; i < imagePreviews.length; i++) {
// 			get_s3_resource(imagePreviews[i], amz_sign_s3);
// 		}
// 	};
// })();

// (function() {
// 	var imageInputs = $(".image-inputs");
// 	for (var i = 0; i < imageInputs.length; i++) {
// 		var imageInputID = imageInputs[i].id;
// 		imageInputs[i].addEventListener("change", function() {
// 			startS3Upload(imageInputID, function() {
// 				get_s3_resource("the_associated_preview");
// 			});
// 		});
// 	}
// })();


function startS3Upload(imageInputID, nextFunction) {
	var inputElement = document.getElementById(imageInputID);
	var files = inputElement.files;
	var file = files[0];
	if(file != null){
		var folder = "int-nc-form";
		upload_private_S3_resource(file, folder, nextFunction);
	}
}


