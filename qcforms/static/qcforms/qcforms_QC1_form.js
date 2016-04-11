$(document).ready(function() {
	$(".image-preview").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
});


$(".image-col").each(function() {
	var previewElement = $(this).children(".image-preview")[0];
	var imageUrlInput = $(this).children(".form-group").children("input")[0];
	$(this).children(".image-input").change(function() {
		var file = this.files[0];
		var folder = "int-nc-form";
		if (file != null) {
			upload_private_S3_resource(file, folder, function(url) {
				previewElement.src = url;
				get_s3_resource(previewElement, amz_sign_s3);
				imageUrlInput.value = url;
			});
		}
	});
});


$("#add-image-button").click(function() {
	alert("Button to add a new image-col div!");
});

