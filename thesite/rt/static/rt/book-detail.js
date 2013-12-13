
//var hehe, m;
//var hehe;
function callording(obj, bid) {
	//hehe = obj;
	var list = $(obj).parent().parent().children().not($(obj).parent().parent().children().last());
	
	var content = $('#ordingModal').find('#ording-info');
	content.html('');
	$.each(list, function(i,val) {
    	content.html(content.html() + $(val).html() + "  ");
    	//console.log(i + $(val).html());
    	//hehe = val;
	});
	
	$('#ordingModal').find("#book-id-info").html(bid);
	$('#ordingModal').find("#ording-book-id").val($(obj).attr('myurl'));
	
	$('#ordingModal').modal('show');
}

function doording(bid){
	console.log("bid:" + bid);
}


$(document).ready(
	function() {

		$('#comment-panel').jscroll({
			debug: true,
			autoTriggerUntil: 1,
			//nextSelector: 'a.scroll-next:last'
		});

		csrftoken = getCookie('csrftoken');

		$('#ordingModal').on('shown.bs.modal', function () {
			console.log("finish display modal");
		});

		$('#ordingModal').find(".alert").hide();

		$('#ording-button').click(function(){
			var burl = $('#ordingModal').find("#ording-book-id").val();
			console.log("get-burl:" + burl);

			$.post(
				burl,
				{
					csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
				},
				function(res){
					var got = eval("(" + res + ")");
					if(got.status == "OK"){
						$('#ordingModal').find(".alert-success").show();
						setTimeout(
							function(){
								$('#ordingModal').find(".alert").hide();
								$('#ordingModal').modal('hide');
							},
							1200
						);
					} else {
						$('#ordingModal').find(".alert-danger").find("#detailed-alert").html(got.err);
						$('#ordingModal').find(".alert-danger").show();
						setTimeout(
							function(){
								$('#ordingModal').find(".alert").hide();
								$('#ordingModal').modal('hide');
							},
							2000
						);
					}
				}
			);
		});

		// the form used for fixing book info
		$('#fixbookinfo-submit').click(function(){
			$('#fixbookinfo-form > .form-group').each(function(){
				var txt = $(this).find('input').val();
				console.log(txt);
				if(!txt || !txt.length){
					// empty
					$(this).addClass('has-error');
					$('#fixbookinfo-warning > b').text($.trim($(this).text()));
					$('#fixbookinfo-warning').removeClass('hidden');
					return false;
				} else {
					$('#fixbookinfo-warning').addClass('hidden');
					$(this).removeClass('has-error');
				}
			});
		});

		

}); // end ready funtion