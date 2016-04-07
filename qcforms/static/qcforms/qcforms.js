function get_private_S3_resource(element_ID, signature_url){
	/*
	The .src attribute for element_ID should already be set to the
	base (i.e. not signed) URL of the resource.  The variable
	signature_url is the URL to the server-side view that will produce
	the signed URL to be sent to S3 and can be defined using a URL
	template tag on the corresponding HTML page.
	*/
	var resource_url = document.getElementById(element_ID).src;
	var xhr = new XMLHttpRequest();
	xhr.open("GET", signature_url+"?resource_url="+resource_url);
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
// next_func takes URL as an argument and is the function to execute when the process is complete
function upload_private_S3_resource(file, folder, next_func) {
	var xhr = new XMLHttpRequest();
	// var amz_sign_s3 is defined in script on HTML page
	xhr.open("GET", amz_sign_s3+"?file_name="+file.name+"&file_type="+file.type+"&folder="+folder);
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200){
				var response = JSON.parse(xhr.responseText);
				upload_file(file, response.signed_request, response.url, next_func);
			}
			else{
				alert("Could not get signed URL.");
			}
		}
	};
	xhr.send();
}

function upload_file(file, signed_request, url, next_func){
	var xhr = new XMLHttpRequest();
	xhr.open("PUT", signed_request);
	xhr.onload = function() {
		if (xhr.readyState === 4 && xhr.status === 200) {
			next_func(url);
		}
	};
	xhr.onerror = function() {
		alert("Could not upload file.");
	};
	xhr.send(file);
}
