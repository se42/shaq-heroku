// GET private image resource for thumbnails
// (function () {
// 	document.body.onload = function () {
// 		var previews = document.getElementsByClassName("image-previews");
// 		for (var i = previews.length - 1; i >= 0; i--) {
// 			get_s3_resource(previews[i], amz_sign_s3);
// 		}
// 	}
// })();

$(document).ready(function() {
	$(".image-previews").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
});
