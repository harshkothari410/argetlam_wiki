$(function(){
	
	var articleTable = $('#articleDataTable').DataTable({
		"lengthMenu": [[ 25, -1 ], [ 25, "All" ]],
		"pagingType": "simple_numbers"
	});
	var userTable = $('#userDataTable').DataTable({
		"lengthMenu": [[ 25, -1 ], [ 25, "All" ]],
		"pagingType": "simple_numbers"
	});
	var ajax_call = function(){
		$.ajax({
			url: '/editCount/api/v1.0/article/',
			type: 'GET',
			dataType: 'json',
		})
		.done(function( data ) {
			var articles = data['articles'];
			var participants = data['participants'];
  			
			articleTable.clear();
			userTable.clear();
			
			var articleTotal = addData(articles,'#articleData','https://en.wikipedia.org/wiki/',articleTable);
			var participantTotal = addData(participants,'#userData','https://en.wikipedia.org/wiki/Special:Contributions/',userTable);
			
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

var addData = function (dict,tableBody,hrefBase,table){
	var val ,total = 0, count = 1;
	for ( var key in dict){
		val = dict[key];
		total += val;
		var name = key.replace(/\_/g,' ');
		var href =  hrefBase + key;
		rowData = [count, "<a target = '_blank' href="+ href +">" + name+ "</a>", val];
		table.row.add(rowData);
		count = count + 1;
	}
	table.draw(false);
	return {'total': total,'count' : count};
};
