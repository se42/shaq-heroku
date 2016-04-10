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

$(document).ready(function(){
	var image_previews = $(".image-previews");
	for (var i = 0; i < image_previews.length; i++) {
		get_s3_resource(image_previews[i], amz_sign_s3);
	}
	var image_inputs = $(".image-inputs");
	for (var i = 0; i < image_inputs.length; i++) {
		image_inputs[i].onchange = startS3Upload(image_inputs[i]);
	}
})


function startS3Upload(input_element) {
	var files = input_element.files;
	var file = files[0];
	if(file == null){
		alert("No file selected.");
	}
	else{
		var folder = "int-nc-form";
		upload_private_S3_resource(file, folder, function_to_update_page_elements);
	}
}

function function_to_update_page_elements(url) {
	alert("Unsigned URL: " + url);
}

