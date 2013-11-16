
$(document).ready(
	function() {
		$('#ordingModal').on('shown.bs.modal', function () {
			console.log("modal");
		});
	}
);

//var hehe, m;
function callording(obj, bid) {
	//hehe = obj;
	var list = $(obj).parent().parent().children().not($(obj).parent().parent().children().last());
	
	var content = $('#ordingModal').find('#ording-info');
	content.html('');
	$.each(list, function(i,val) {
    	content.html(content.html() + $(val).html() + " ");
    	//console.log(i + $(val).html());
    	//hehe = val;
	});
	
	$('#ordingModal').find("#book-id-info").html(bid);
	
	$('#ordingModal').modal('show');
}