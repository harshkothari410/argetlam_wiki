$(function(){
	var ajax_call = function(){
		$.ajax({
			url: '/editCount/api/v1.0/article/',
			type: 'GET',
			dataType: 'json',
		})
		.done(function( data ) {
			var values;
			$.each( data, function( key, val ) {
				values = val;
			});
			var count = 1, articleData, totalEdit = 0;
  			
  			$('#articleData').find('tr').remove();

			for ( var key in values){
				if (key === 'timestamp')
					continue;
				val = values[key];
				totalEdit = totalEdit + val;
				var name = key.replace(/\_/g,' ');
				var href = "https://en.wikipedia.org/wiki/" + key;
				articleData = "<tr><td> " + count + " </td> <td> <a target = '_blank' href="+ href +">" + name+ "</a></td> <td>" + val + "</td> </tr>";
				$('#articleData').append(articleData);
				count = count + 1;
			}
			$('#totalArticleCount').text(count-1);
			$('#totalEditCount').text(totalEdit);

		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	};
	ajax_call();
	setInterval(ajax_call, 1000*60*3);
});
