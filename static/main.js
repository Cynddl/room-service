$(function(){

	// Date and time inputs
	$('.datepicker').pickadate({
		formatSubmit: 'yyyy-mm-dd',
		hiddenSuffix: '_raw'
	});
	$('.timepicker').pickatime({
		format: 'HH:i'
	});

	$('form[name=reservation]').submit(function(ev) {
		ev.preventDefault();

		var data = $(this).serializeArray();

		// jQuery.each( data, function( i, field ) {
		// 	if (field['name'] == 'date') {
		// 		field['value'] = $('input[name="date"]').pickadate('picker').get('select', 'yyyy-mm-dd');
		// 		console.log(field);
		// 	}
		// });
		console.log(data);

		$.post($(this).attr('action'), data, function(json) {
			console.log(json);
		}, 'json');
	});
});
