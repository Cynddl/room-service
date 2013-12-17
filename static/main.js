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

		$.post($(this).attr('action'), $(this).serializeArray(), function(json) {
			$('#room-list').empty();
			$('#room-list').append('<h2>Salles disponibles</h2>');

			$.each(json.rooms, function(id, room){
				$('#room-list').append('<div class="room">' + room[1] + '</div> ');
			});
		}, 'json');
	});
});