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


$(document).ready(function() {
	$(".image-previews").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
});

$(".image-inputs").change(function() {
	var file = this.files[0];
	var folder = "int-nc-form";
	if (file != null) {
		upload_private_S3_resource(file, folder, function(url) {
			alert("The url is: " + url);
			$(this).next().attr("src", url);
			get_s3_resource($(this).next()[0], amz_sign_s3);
		});
	}
});




