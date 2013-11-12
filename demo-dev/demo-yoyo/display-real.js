var cq;

/* 
 * remember to write load code here
 */

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	console.log(e.target);
	cq = e.target;
	console.log(e.relatedTarget);
})

$( document ).ready(function() { 
    $('#magic').hover(
        function(){
            $(document).find('#usertable').slideDown(250); //.fadeIn(250)
			$('#userborrow').addClass("panelloding");
			setTimeout(function(){
			  $('#userborrow').removeClass("panelloding");
			}, 2000);
        },
        function(){
			setTimeout(function(){
				  $(document).find('#usertable').slideUp(250); //.fadeOut(205)
			}, 3000);
        }
    );
});