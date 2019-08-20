var input = document.getElementById('location');

var options = {
	types: ['geocode'],
	componentRestrictions: {country: 'my'},
}

autocomplete = new google.maps.places.Autocomplete(input, options);

// autocomplete.getPlace().geometry.location.lat()
// autocomplete.getPlace().geometry.location.lng()


// Form Submission
var form = document.querySelector("form[name='pricecheck']")
var formSubmitButton = document.querySelector("form[name='pricecheck'] input[type='submit']")
var formResponse = document.getElementById('form-response')

function formSubmission() {
	form.reportValidity();
    formResponse.innerHTML = "Processing your submission.";
    formSubmitButton.disabled = true

	let formData = new FormData(form);
	let location = JSON.stringify(autocomplete.getPlace().geometry.location.toJSON())
	formData.append('geometry', location)

    let request = new XMLHttpRequest();
    request.open("POST", "/", true);
    request.onload = function (oEvent) {
        if (request.status == 200) {
			formResponse.innerHTML = request.response;
        } else {
            formResponse.innerHTML = "Error " + request.status + " occurred when trying to process your submission.<br \/>";
        }
        formSubmitButton.disabled = false
    };

    request.send(formData);
}

form.addEventListener('submit', function (event) {
	formSubmission()
    event.preventDefault();
}, false);

form.addEventListener('keypress', function(event) {
	if (event.key === 'Enter') {
		formSubmission()
		event.preventDefault();
	}
}, false);
