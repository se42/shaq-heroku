$(document).ready(function() {
	$(".image-preview").each(function() {
		get_s3_resource(this, amz_sign_s3);
	});
	setImageColOnChange();
});


// $(".image-col").each(function() {
// 	var previewElement = $(this).children(".image-preview")[0];
// 	var imageUrlInput = $(this).children(".form-group").children("input")[0];
// 	$(this).children(".image-input").change(function() {
// 		var file = this.files[0];
// 		var folder = "int-nc-form";
// 		if (file != null) {
// 			upload_private_S3_resource(file, folder, function(url) {
// 				previewElement.src = url;
// 				get_s3_resource(previewElement, amz_sign_s3);
// 				imageUrlInput.value = url;
// 			});
// 		}
// 	});
// });


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
	var x = totalForms.value;
	totalForms.value++;
	$("#image-panel").append("<div class=\"image-col col-xs-12 col-sm-6 col-md-4\">"
				+ "<input class=\"image-input\" type=\"file\"/>"
				+ "<img class=\"image-preview img-responsive img-thumbnail\" "
				+ "src=\"http://placehold.it/200x200\"></div>");
	/*
	2 - add new image-col div
	3 - add new image-input file input
	4 - add new image-preview img element
	5 - create new form-group div with label/input elements for url field
	6 - create new hidden input for id_intncimage_set-x-id with no value
		--> you should be able to determine the next x from the management_form data
	7 - create new hidden input for id_intncimage_set-x-report with
		value = {{ image_form.report.id }} or whatever it is
	8 - increment management_form TOTAL_FORMS count value
	9 - disable this button if there is an empty image input/url field available
	*/
});

