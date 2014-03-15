$(function(){
	var ajax_call = function(){
		$.ajax({
			url: '/editCount/api/v1.0/article/',
			type: 'GET',
			dataType: 'json',
		})
		.done(function( data ) {
			
			var articles = data['articles'];
			var participants = data['participants'];
  			
  			$('#articleData,#userData').find('tr').remove();

			
			var articleTotal = addData(articles,'#articleData','https://en.wikipedia.org/wiki/');
			var participantTotal = addData(participants,'#userData','https://en.wikipedia.org/wiki/Special:Contributions/');
			
			$('#totalArticleCount').text(articleTotal['count']-1);
			$('#totalEditCount').text(articleTotal['total']);
			$('#totalUserCount').text(participantTotal['count']-1);

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

var addData = function (dict,table,hrefBase){
	var val ,total = 0, count = 1;
	for ( var key in dict){
				val = dict[key];
				total += val;
				var name = key.replace(/\_/g,' ');
				var href =  hrefBase + key;
				articleData = "<tr><td> " + count + " </td> <td> <a target = '_blank' href="+ href +">" + name+ "</a></td> <td>" + val + "</td> </tr>";
				$(table).append(articleData);
				count = count + 1;
			}
	return {'total': total,'count' : count};
};
