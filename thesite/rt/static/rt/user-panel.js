var cq;

/* 
 * remember to write load code here
 */

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	console.log(e.target);
	cq = e.target;
	console.log(e.relatedTarget);
})



$(document).ready(
	function(){

		$('.reborrow-button').click(function(){
			var uid = $(this).attr('uid');
			var bid = $(this).attr('bid');
			var curl = $(this).attr('curl');

			var that = this;

			csrftoken = getCookie('csrftoken');
			$.post(
				curl,
				{
					'csrfmiddlewaretoken' : csrftoken,
				},
				function(data){
					console.log('get reborrow data: ' + data);
					var obj = $.parseJSON(data);
					if(obj.status == 'Error'){
						alert('噢哟！ ' + 'Error: ' + obj.err + ' Message: ' + obj.message);
						$(that).removeClass('btn-default');
						$(that).addClass('btn-danger');
						$(that).text("续借失败");
						$(that).attr("disabled", "disabled");
					} else if(obj.status == 'OK'){
						$(that).removeClass('btn-default');
						$(that).addClass('btn-success');
						$(that).text("续借成功");
						$(that).attr("disabled", "disabled");
					}
				}
			);
		});
	}
);