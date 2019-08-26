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
            readableResponse(JSON.parse(request.response))
        } else {
            formResponse.innerHTML = "Error " + request.status + " occurred when trying to process your submission.<br \/>";
        }
        formSubmitButton.disabled = false
    };

    request.send(formData);
    return request
}

function readableResponse(response) {
    if (response.search_type == 'closest_town_match') {
        closestTownMatch(response)
    } else if (response.search_type == 'closest_town_loose_match') {
        closestTownLooseMatch(response)
    }
}

function closestTownMatch(response) {
    return formResponse.innerHTML = `${parseDistance(response)} ${parseCount(response)} ` +
                                    `${parsePrice(response)}`
}

function closestTownLooseMatch(response) {
    return formResponse.innerHTML = `We couldn't find a match with your exact search ` +
                                    `criteria, so we removed some of the optional requirements.` +
                                    `${parseDistance(response)} ${parseCount(response)} ` +
                                    `${parsePrice(response)}`
}

function parseDistance(response) {
    // search_distance is in meters
    if (response.search_distance >= 1000) {
        return `The closest area that we found a listing for, is ${response.town}.`
    } else {
        return `We've found a listing within the area of ${response.town}.`
    }
}

function parseCount(response) {
    if (response.count > 1) {
        return `We found more than one listing for your search criteria, ` +
               `so we took an average of the listings.`
    } else {
        return `We only found one listing with your search criteria, ` +
               `so it may be harder to find a similar offer.`
    }
}

function parsePrice(response) {
    if (response.count > 1) {
        return `The listed average price is ${response.price} and price per sq/ft ` +
               `is ${response.price_per_sq_ft}.`
    } else {
        return `The listed price is ${response.price}, and price per sq/ft ` +
               `is ${response.price_per_sq_ft}.`
    }
}


form.addEventListener('submit', function (event) {
    formSubmission()
    event.preventDefault()
}, false);

// form.addEventListener('keypress', function(event) {
// 	if (event.key === 'Enter') {
// 		formSubmission()
// 		event.preventDefault();
// 	}
// }, false);
