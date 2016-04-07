QUnit.test("Unsigned URL returns HTTP status 403", function(assert) {
	var original_url = document.getElementById("test-unsigned").src;
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


QUnit.test("Target src is updated to properly signed URL", function(assert) {
	var reference_url = document.getElementById("test-reference").src;
	var original_url = document.getElementById("test-preview").src;
	var done = assert.async();

	get_private_S3_resource("test-preview", amz_sign_s3);

	function check_urls() {
		var updated_url = document.getElementById("test-preview").src;
		assert.ok(updated_url.indexOf(original_url) === 0, "Updated URL begins with original base URL.");
		assert.ok(updated_url.indexOf("AWSAccessKeyId") > -1, "Updated URL contains AWSAccessKeyId.");
		assert.ok(updated_url.indexOf("Expires") > -1, "Updated URL contains Expires.");
		assert.ok(updated_url.indexOf("Signature") > -1, "Updated URL contains Signature.");
		done();
	}

	// Give get_private_S3_resource 2 seconds to run
	setTimeout(check_urls, 2000);
});


