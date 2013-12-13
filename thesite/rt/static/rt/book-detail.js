
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
			loadingHtml: '<div class="isloading text-center">喵小咪正在努力搬运新评论中T_T。。。</div>',
			debug: true,
			autoTriggerUntil: 1,
			nextSelector: 'a.scroll-next:last',
			padding: 10,
			callback: function(){
				if($('a.scroll-next:last').length == 0){
					$('#comment-panel').append('<button class="btn btn-default btn-default btn-block" disabled="disabled"><span class="glyphicon glyphicon-ok"></span> 该书的所有评论都已经加载完毕喵=w=～</button>');
				}
			}
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
					$('#fixbookinfo-warning > strong').text($.trim($(this).text()));
					$('#fixbookinfo-warning').removeClass('hidden');
					return false;
				} else {
					$('#fixbookinfo-warning').addClass('hidden');
					$(this).removeClass('has-error');
				}
			});
		});

		// the form used for fixing book info
		$('#makemycomment-submit').click(function(){
			var herr = false;
			$('#makemycomment-form > .form-group').each(function(){
				var txt = $(this).find('input, textarea').val();
				console.log($.trim($(this).find('.control-label').text()) + ':' + txt);
				if(!txt || !txt.length){
					// empty
					$(this).addClass('has-error');
					$('#makemycomment-warning > strong').text($.trim($(this).text()));
					$('#makemycomment-warning').removeClass('hidden');
					herr = true;
					return false;
				} else {
					$('#makemycomment-warning').addClass('hidden');
					$(this).removeClass('has-error');
				}
			});

			if(herr)
				return false;

			// check all radio
			var rate = $("input[name='optionsRadios']:checked").val();
			console.log('rate:' + rate);
			if(rate && (rate >= 1 && rate <= 5)){
				$('#makemycomment-warning').addClass('hidden');
				$(this).removeClass('has-error');
				console.log('meow');
			} else {
				// didn't rate
				$(this).addClass('has-error');
				$('#makemycomment-warning > strong').text($.trim($("label[for='inputRate']").text()));
				$('#makemycomment-warning').removeClass('hidden');
				return false;
			}

			var isSpoiler = $('#isSpoiler').is(':checked');
			console.log('isSpoiler:' + isSpoiler);
		});
		

}); // end ready funtion