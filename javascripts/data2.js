console.log('This would be the main JS file.');

jQuery(document).ready(function( $ ) {
	$('.btn').button();
	// Retrieve country list
	//<optgroup label="group 1">

	$.getJSON("data/countries_Asia.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#asia").append(newOption);
		});
	});

	$.getJSON("data/countries_Canada.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#canada").append(newOption);
		});
	});

	$.getJSON("data/countries_Europe.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#europe").append(newOption);
		});
	});

	$.getJSON("data/countries_Latin_and_Central_America.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#lac").append(newOption);
		});
	});

	$.getJSON("data/countries_Middle_East.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#mideast").append(newOption);
		});
	});

	$.getJSON("data/countries_Northern_Africa.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#nafrica").append(newOption);
		});
	});

	$.getJSON("data/countries_Oceania.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#oceania").append(newOption);
		});
	});

	$.getJSON("data/countries_Russia.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#russia").append(newOption);
		});
	});

	$.getJSON("data/countries_Sub-Saharan_Africa.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#ssa").append(newOption);
		});
	});

	$.getJSON("data/countries_United_States.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#usa").append(newOption);
		});
	});

	$("#countries").select2({
		placeholder: "Select one or more countries",
		allowClear: true,
	});

	$("#crops").select2({
		placeholder: "Select one or more crops",
		allowClear: true,
	});

	$("#technologies").select2({
		placeholder: "Select one or more technologies",
		allowClear: true,
	});

	$("#file_format").select2({
		placeholder: "Select the download format",
		allowClear: true,
	});

	// Download data
	$("#download_button").click(function() {
		
		variable = 'yield';
		
		if ($("#yield").is(":checked") == true) { variable = 'yield'; }
    	if ($("#harvested_area").is(":checked") == true) { variable = 'harvested'; }
    	if ($("#production").is(":checked") == true) { variable = 'prod'; }
    	if ($("#physical_area").is(":checked") == true) { variable = 'area'; }
    	
		var crops = [];
        var cropsSelected = $('#crops option:selected');
        var techSelected = $('#technologies option:selected');
        var countrieSelected = $('#countries option:selected');
        
        if (cropsSelected.size() == 0 | techSelected.size() == 0) {alert("Please select at least one crop."); return false; }
        if (countrieSelected.size() == 0) {alert("Please select at least one country."); return false; }

		$.each(techSelected, function(i, item) {
			crop_suffix = $(item).attr('value');
        	$.each(cropsSelected, function(i, item) {
				crops.push($(item).attr('value') + crop_suffix);
			});
        });

    	var countries = $('#countries').val();
    	if (jQuery('#countries').val()) {
    		var countries = $('#countries').val().join(",");
    	}

        var fields = crops.join(',');

		if ($('#file_format').val()) { format = $('#file_format').val(); }

		params = {
			iso3: countries,
			fields: fields,
			format: format,
		}
		
		var url = "http://api.mapspam.info/" + variable + "/?" + $.param(params);
		window.open(url, "_blank");
		
    });

});