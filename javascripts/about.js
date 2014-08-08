$(document).ready(function() {
	
	$('.btn').button();

	$('input.prettyCheckable').each(function(){
		$(this).prettyCheckable();
	});

	$("#download_button").click(function() {

		$('input.prettyCheckable').each(function(){
			alert($(this))
		});

		variable = 'yield';
		if ($("#yield").is(":checked") == true) {
			variable = 'yield';
		}
    	
    	if ($("#production").is(":checked") == true) {
			variable = 'production';
    	}
    	
    	if ($("#harvested_area").is(":checked") == true) {
			variable = 'harvested_area';
    	}

    	if ($("#physical_area").is(":checked") == true) {
			variable = 'physical_area';
    	}

	});
});