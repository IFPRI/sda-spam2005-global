console.log('This would be the main JS file.');

jQuery(document).ready(function( $ ) {
	$('.btn').button();
	// Retrieve country list
	//<optgroup label="group 1">
	$.getJSON("countries_Europe.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#countries").append(newOption);
		});

	$.getJSON("countries_Asia.json", function(data) {
		$.each(data, function(i, item) {
			var newOption = $('<option/>');
			newOption.html(item['name_cntr']);
			newOption.attr('value', item['iso3']);
			$("#countries").append(newOption);
		});

		$("#countries").select2({
			placeholder: "Select one or more countries",
			allowClear: true,
		});
		$("#crops").select2({
			placeholder: "Select crop(s)",
			allowClear: true,
		});
		$("#technologies").select2({
			header: "Select technologies",
			allowClear: true,
		});
		$("#file_format").select2({
			header: "Select a format",
			allowClear: true,
		});
	});

	// Download data
	$("#download_button").click(function() {
	variable = 'yield';
	if (jQuery("#yield").is(":checked") == true) {
		variable = 'yield';
	}
    	if (jQuery("#production").is(":checked") == true) {
		variable = 'prod';
    	}
    	if (jQuery("#harvested_area").is(":checked") == true) {
		variable = 'harvested';
    	}
    	if (jQuery("#value_of_production").is(":checked") == true) {
		variable = 'vop';
    	}
	// uncomment this when ready to download whole countries
	variable = variable + '_all';
    	
    	var format = "csv";
   	if ($('#file_format').val()) {
   		format = $('#file_format').val();
   	}
        var crops = [];
        var cropsSelected = $('#crops option:selected');
	
	var techSelected = $('#technologies option:selected');
	jQuery.each(techSelected, function(i, item) {
		crop_suffix = $(item).attr('value');
        	$.each(cropsSelected, function(i, item) {
			crops.push($(item).attr('value') + crop_suffix);
		})
        })

        if (crops.length == 0) {
            alert("Select a crop");
            return false;
        }

        var fields = "iso3,x,y,prod_level,unit,cell5m,rec_type," + crops.join(',');

    	var countries = $('#countries').val();
    	if (jQuery('#countries').val()) {
    		var countries = $('#countries').val().join(",");
    	} else {
    		alert("Select a country");
    		return false;
    	}

	//alert(countries);
	//alert(fields);
	//alert(variable);

        var date = Date.now();
    	var filename = 'spam2005_' + date;
	params = {
		//page: 1, // comment this when ready to download whole countries
		// api_key: "4e78c23fe0c7a1263a87cc9261df1bca228daac0",
		iso3: countries,
		fields: fields,
		format: format,
		// filename: filename,
	}
	var url = "http://api.mapspam.info/" + variable + "/?" + $.param(params);
    	//alert(url);
	console.log(url);
    	window.open(url, "_blank");

        // download metadata file - description of the downloaded variables
        /* Jawoo said not to download metadata file for now
        var dbQueryMeta = "SELECT varcode, unit, varlabel, vartitle, vardesc, year, version, cat1, cat2, aggtype, aggfun, dauthor, citation, sources FROM vi where varcode in ('" +  crops_meta.join("', '") + "') and published = '1' and tbname = '" + tableName +"'";
        var filenameMeta = filename + '_meta';
        //alert(dbQueryMeta);
        paramsMeta = {
            page: 1,
            // api_key: "4e78c23fe0c7a1263a87cc9261df1bca228daac0",
            fields: fields,
            format: "csv",
        }
	var meta_url = "http://api.mapspam.info/yield/?" + + "?" +  $.param(paramsMeta);
        window.open(meta_url, "_blank");*/

  	});
});
//http://api.mapspam.info/yield/?page=1&iso3=MWI,GHA&fields=iso3,x,y,prod_level,cell5m,unit,whea&format=csv
