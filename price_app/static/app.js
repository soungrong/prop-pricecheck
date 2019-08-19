var input = document.getElementById('pac-input');

var options = {
	types: ['geocode'],
	componentRestrictions: {country: 'my'},
}

autocomplete = new google.maps.places.Autocomplete(input, options);

// autocomplete.getPlace().geometry.location.lat()
// autocomplete.getPlace().geometry.location.lng()
// JSON.stringify(autocomplete.getPlace().geometry.location.toJSON())
