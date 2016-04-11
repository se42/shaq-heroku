$(document).ready(function() {
	$(".image-previews").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
});


$(".image-col").each(function() {
	$(this).children(".image-inputs").change(function() {
		var file = this.files[0];
		var folder = "int-nc-form";
		var previewElement = $(this).next()[0];
		if (file != null) {
			upload_private_S3_resource(file, folder, function(url) {
				previewElement.src = url;
				get_s3_resource(previewElement, amz_sign_s3);
			});
		}
	});
});
