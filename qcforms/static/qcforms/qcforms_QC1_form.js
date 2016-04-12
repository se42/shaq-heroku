$(document).ready(function() {
	$(".image-preview").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
	setImageColOnChange();
});


function setImageColOnChange() {
	$(".image-col").each(function() {
	var previewElement = $(this).children(".image-preview")[0];
	var imageUrlInput = $(this).children("input")[0];
	var spinSpan = $(this).children(".spin-span");
	$(this).children(".image-input-btn").children(".image-input").change(function() {
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
	$("#image-panel").append("<div class=\"image-col col-xs-12 col-sm-6 col-md-4\">"
				+ "<button class=\"btn btn-default btn-block image-input-btn\">Change Image"
				+ "<input id=\"image-input-"+nextSetID+"\" class=\"image-input\" "
				+ "type=\"file\" accept=\"image/*\"/>"
				+ "</button>"
				+ "<img class=\"image-preview img-responsive img-thumbnail\" "
				+ "src=\"https://placehold.it/500?text=NewImage\">"
				+ "<input id=\"id_intncimage_set-"+nextSetID+"-image_url\" maxlength=\"200\" "
				+ "name=\"intncimage_set-"+nextSetID+"-image_url\" type=\"hidden\" />"
				+ "<input id=\"id_intncimage_set-"+nextSetID+"-id\" "
				+ "name=\"intncimage_set-"+nextSetID+"-id\" type=\"hidden\" />"
				+ "<input id=\"id_intncimage_set-"+nextSetID+"-report\" "
				+ "name=\"intncimage_set-"+nextSetID+"-report\" type=\"hidden\" />"
				+ "</div>");
	setImageColOnChange();
	$("#add-image-button").attr("disabled", "disabled");
	var newImageFieldID = "image-input-"+nextSetID;
	var newImageField = document.getElementById(newImageFieldID);
	newImageField.scrollIntoView();
	window.scrollBy(0, -70);
	newImageField.onchange = function() {
		if (reportID > 0) {
			document.getElementById("id_intncimage_set-"+nextSetID+"-report").value = reportID;
		}
		totalForms.value++;
		$("#add-image-button").attr("disabled", null);
	};
});

