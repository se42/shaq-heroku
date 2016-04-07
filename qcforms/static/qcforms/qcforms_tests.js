QUnit.test("Test 403 response from private resource", function(assert) {
	var original_url = document.getElementById("test-preview").src;
	var done = assert.async();

	var xhr = new XMLHttpRequest();
	xhr.open("GET", original_url);
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			assert.ok(xhr.status == 403, "Original URL returns 403 Http response.");
			done();
		}
	};
	xhr.send();
});


QUnit.test("Test URL updates", function(assert) {
	var reference_url = document.getElementById("test-reference").src;
	var original_url = document.getElementById("test-preview").src;
	var done = assert.async();

	get_private_S3_resource("test-preview", amz_sign_s3);

	function check_urls() {
		var updated_url = document.getElementById("test-preview").src;
		console.log("Reference URL: " + reference_url);
		console.log("Original URL: " + original_url);
		console.log("Updated URL:  " + updated_url);
		assert.ok(updated_url.indexOf(original_url) === 0, "Updated URL begins with original base URL.");
		assert.ok(updated_url.indexOf("AWSAccessKeyId") > -1, "Updated URL contains AWSAccessKeyId.");
		assert.ok(updated_url.indexOf("Expires") > -1, "Updated URL contains Expires.");
		assert.ok(updated_url.indexOf("Signature") > -1, "Updated URL contains Signature.");
		done();
	}

	setTimeout(check_urls, 2000);
});

