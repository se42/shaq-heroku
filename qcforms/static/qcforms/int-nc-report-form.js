document.body.onload = function() {myFunc()};

function myFunc() {
	var x = document.getElementById("id_report_date");
	x.type = "date";
}


// S3 direct uploads per https://devcenter.heroku.com/articles/s3-upload-python
(function() {
	document.getElementById("file_input").onchange = function(){
		var files = document.getElementById("file_input").files;
		var file = files[0];
		if (file == null){
			alert("No file selected.");
		}
		else{
			get_signed_request(file);
		}
	};
})();

function get_signed_request(file){
	var xhr = new XMLHttpRequest();
	// sign_s3_url is defined in a script at the bottom of the template
	// to allow for the use of Django URL template tags
	xhr.open("GET", sign_s3_url+"?file_name="+file.name+"&file_type="+file.type);
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
	// xhr.setRequestHeader('x-amz-acl', 'public-read');
	xhr.onload = function() {
		if (xhr.status === 200) {
			document.getElementById("preview").src = url;
			document.getElementById("id_issue_image_url").value = url;
		}
	};
	xhr.onerror = function() {
		alert("Could not upload file.");
	};
	xhr.send(file);
}
