// GET private image resource for thumbnails
$(document).ready(function() {
	$(".image-previews").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
});
