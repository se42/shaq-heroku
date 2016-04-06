// GET private image resource for thumbnail if issue_image_url exists
(function() {
	document.body.onload = function() {
		var url_field = document.getElementById("id_issue_image_url");
		if (url_field.hasAttribute("value")) {
			document.getElementById("preview").src = url_field.value;
			retrieve_private_S3_resource("preview");
		};
	};
})();

// Monitor file_input file input object for changes to initiate PUT sequence
(function() {
    document.getElementById("file_input").onchange = function(){
        var files = document.getElementById("file_input").files;
        var file = files[0];
        if(file == null){
            alert("No file selected.");
        }
        else{
            get_signed_request(file);
        }
    };
})();

// S3 direct uploads per https://devcenter.heroku.com/articles/s3-upload-python
function get_signed_request(file){
	var xhr = new XMLHttpRequest();
	// var amz_sign_s3 is defined in a script at the bottom of the
	// template to allow for the use of Django URL template tags
	xhr.open("GET", amz_sign_s3+"?file_name="+file.name+"&file_type="+file.type+"&folder=int-nc-form");
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200){
				var response = JSON.parse(xhr.responseText);
				upload_file(file, response.signed_request, response.url);
			}
			else{
				alert("Could not get signed URL.");
			}
		}
	};
	xhr.send();
}

function upload_file(file, signed_request, url){
	var xhr = new XMLHttpRequest();
	xhr.open("PUT", signed_request);
	xhr.onload = function() {
		if (xhr.status === 200) {
			document.getElementById("id_issue_image_url").value = url;
			document.getElementById("preview").src = url;
			retrieve_private_S3_resource("preview");
		}
	};
	xhr.onerror = function() {
		alert("Could not upload file.");
	};
	xhr.send(file);
}

