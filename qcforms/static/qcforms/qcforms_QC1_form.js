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

(function() {
	document.body.onload = function() {
		// for each img element in the image-preview-panel div, call
		// get_s3_resource on the img element with amz_sign_s3 url
		var imagePanel = document.getElementById("image-preview-panel").children;
		for (var i = imagePanel.length - 1; i >= 0; i--) {
			var imgElement = imagePanel[i].getElementsByTagName("img");
			get_s3_resource(imgElement[0], amz_sign_s3);
		}
	};

	document.getElementById("add-image-button").onclick = function() {
		// Code to create a new image select thumbnail/preview element
		// as well as a new hidden input for the actual image_url input.
		// Don't forget to update the TOTAL_FORMS count too.
		// 
		// 1 - create the hidden url input fields
		// 2 - run the standard create_image_input_preview function
	};
})();


