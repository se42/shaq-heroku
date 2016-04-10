// GET private image resource for thumbnails
(function () {
	var previews = document.body.onload.getElementsByClassName("image-previews");
	for (var i = previews.length - 1; i >= 0; i--) {
		get_s3_resource(previews[i], amz_sign_s3);
	}
})();
