$(function(){
	var page = 206337;
	$.ajax({
		url: 'http://127.0.0.1:5000/editCount/api/v1.0/article/',
		type: 'GET',
		dataType: 'json',
	})
	.done(function( data ) {
		//console.log( data["Usha_Meena"] );
		//console.log(data.object);
		var values;
		$.each( data, function( key, val ) {
			values = val;
		});
		var count = 1, articleData, totalEdit = 0;
  		// $.each(values, function(key, val) {
  		// 	 /* iterate through array or object */
  		// 	 console.log(key + val);
  		// 	 if (key === 'timestamp')
  		// 	 	continue;
  		// 	 key = key.replace('_', ' ')
  		// 	 articleData = "<tr><td> " + count + " </td> <td>" + key+ "</td> <td>" + val+ "</td> </tr>";
  		// 	 $('#articleData').append(articleData);
  		// 	 count = count + 1;
  			// });

		for ( var key in values){
			if (key === 'timestamp')
				continue;
			val = values[key];
			totalEdit = totalEdit + val;
			key = key.replace(/\_/g,' ');
			articleData = "<tr><td> " + count + " </td> <td>" + key+ "</td> <td>" + val + "</td> </tr>";
			$('#articleData').append(articleData);
			count = count + 1;
		}

		$('#totalEdit').text('Total Edit : ' + totalEdit);

	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
});
