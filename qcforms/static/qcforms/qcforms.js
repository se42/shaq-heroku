// GET private resource from S3
// The .src attribute for element_ID should already be set
// to the base (i.e. not signed) URL of the resource
function retrieve_private_S3_resource(element_ID){
	var resource_url = document.getElementById(element_ID).src;
	get_signed_GET_request(element_ID, resource_url);
}

function get_signed_GET_request(element_ID, resource_url){
	var xhr = new XMLHttpRequest();
	// var amz_sign_s3 must be defined in script on HTML page
	xhr.open("GET", amz_sign_s3+"?resource_url="+resource_url);
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200){
				var response = JSON.parse(xhr.responseText);
				// get_and_update_resource(element_ID, response.signed_request);
				document.getElementById(element_ID).src = response.signed_request;
			}
			else{
				alert("Could not get signed URL.");
			}
		}
	};
	xhr.send();
}

// function get_and_update_resource(element_ID, signed_request){
// 	var xhr = new XMLHttpRequest();
// 	xhr.open("GET", signed_request);
// 	xhr.onload = function() {
// 		if (xhr.status === 200) {
// 			document.getElementById(element_ID).src = signed_request;
// 		}
// 	};
// 	xhr.onerror = function() {
// 		alert("Could not retrieve file.");
// 	};
// 	xhr.send();
// }


// function upload_private_S3_resource() {

// }