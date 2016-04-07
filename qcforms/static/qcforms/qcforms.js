// The .src attribute for element_ID should already be set
// to the base (i.e. not signed) URL of the resource
function get_private_S3_resource(element_ID){
	var resource_url = document.getElementById(element_ID).src;
	var xhr = new XMLHttpRequest();
	// var amz_sign_s3 must be defined in script on HTML page
	xhr.open("GET", amz_sign_s3+"?resource_url="+resource_url);
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200){
				var response = JSON.parse(xhr.responseText);
				document.getElementById(element_ID).src = response.signed_request;
			}
			else{
				alert("Could not get signed URL.");
			}
		}
	};
	xhr.send();
}


// Core function to PUT a file into a folder within the project's S3 bucket
// cFunc takes URL as an argument and is the function to execute when the process is complete
function upload_private_S3_resource(file, folder, cFunc) {
	var xhr = new XMLHttpRequest();
	// var amz_sign_s3 is defined in script on HTML page
	xhr.open("GET", amz_sign_s3+"?file_name="+file.name+"&file_type="+file.type+"&folder="+folder);
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200){
				var response = JSON.parse(xhr.responseText);
				upload_file(file, response.signed_request, response.url, cFunc);
			}
			else{
				alert("Could not get signed URL.");
			}
		}
	};
	xhr.send();
}

function upload_file(file, signed_request, url, cFunc){
	var xhr = new XMLHttpRequest();
	xhr.open("PUT", signed_request);
	xhr.onload = function() {
		if (xhr.status === 200) {
			cFunc(url);
		}
	};
	xhr.onerror = function() {
		alert("Could not upload file.");
	};
	xhr.send(file);
}
