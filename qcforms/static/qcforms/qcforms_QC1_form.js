$(document).ready(function() {
	$(".image-preview").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
	setImageColOnChange();
});


function setImageColOnChange() {
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
}


$("#add-image-button").click(function() {
	var totalForms = document.getElementById("id_intncimage_set-TOTAL_FORMS");
	var nextSetID = totalForms.value;
	totalForms.value++;
	$("#image-panel").append("<div class=\"image-col col-xs-12 col-sm-6 col-md-4\">"
				+ "<input id=\"image-input-"+nextSetID+"\" class=\"image-input\" type=\"file\"/>"
				+ "<img class=\"image-preview img-responsive img-thumbnail\" "
				+ "src=\"https://placehold.it/200x200\">"
				+ "<div class=\"form-group\">"
				+ "<label class=\"control-label\" for=\"id_intncimage_set-"
				+ nextSetID+"-image_url\">Image url</label>"
				+ "<input class=\"form-control\" id=\"id_intncimage_set-"
				+ nextSetID+"-image_url\" maxlength=\"200\" name=\"intncimage_set-"
				+ nextSetID+"-image_url\" placeholder=\"Image url\" "
				+ "required=\"required\" title=\"\" type=\"url\" />"
				+ "</div>"
				+ "<input id=\"id_intncimage_set-"+nextSetID+"-id\" "
				+ "name=\"intncimage_set-"+nextSetID+"-id\" type=\"hidden\" />"
				+ "<input id=\"id_intncimage_set-"+nextSetID+"-report\" "
				+ "name=\"intncimage_set-"+nextSetID+"-report\" type=\"hidden\" />"
				+ "</div>");
	if (reportID > 0) {
		document.getElementById("id_intncimage_set-"+nextSetID+"-report").value = reportID;
	}
	setImageColOnChange();
	$("#add-image-button").attr("disabled", "disabled");
	var newImageFieldID = "image-input-"+nextSetID;
	var newImageField = document.getElementById(newImageFieldID);
	newImageField.onchange = function() {
		$("#add-image-button").attr("disabled", null);
	};
});

