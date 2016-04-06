document.body.onload = function(){
	var url = document.getElementById("preview").src;
	get_signed_GET_request(url);
}

function get_signed_GET_request(resource_url){
	var xhr = new XMLHttpRequest();
	// var sign_s3_GET_url is defined in a script at the bottom of the
	// template to allow for the use of Django URL template tags
	xhr.open("GET", sign_s3_GET_url+"?resource_url="+resource_url);
	xhr.onreadystatechange = function(){
		if(xhr.readyState === 4){
			if(xhr.status === 200){
				var response = JSON.parse(xhr.responseText);
				get_resource(response.signed_request, response.url);
			}
			else{
				alert("Could not get signed URL.");
			}
		}
	};
	xhr.send();
}

function get_resource(signed_request, url){
	var xhr = new XMLHttpRequest();
	xhr.open("GET", signed_request);
	xhr.onload = function() {
		if (xhr.status === 200) {
			document.getElementById("preview").src = signed_request;
		}
		else{
				alert("Special error."+xhr.status);
			}
	};
	xhr.onerror = function() {
		alert("Could not retrieve file.");
	};
	xhr.send();
}
