var cq;

/* 
 * remember to write load code here
 */

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	console.log(e.target);
	cq = e.target;
	console.log(e.relatedTarget);
});



$( document ).ready(function() { 
	/*
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
	*/

    csrftoken = getCookie('csrftoken');

    $('#magic').click(function(){
    	csrftoken = getCookie('csrftoken');

    	var curl = $('#find-user-url').val();
    	var search = $('#find-user-input').val();

    	$('#find-user-tbody').load(curl+search, function(){
    		$('.choose-user').click(function(){
				var uid = $(this).attr('userid');
				var uname = $(this).attr('username');
				$('#display-username').html(uname);
				$('#borrow-book-uid').val(uid);
				$('#find-user-tbody').html('');
				$('#borrow-book-tbody').html('');
				return false;
			});
    	});
    	return false;
    });

    $('#magic-borrow').click(function(){
    	var curl = $('#borrow-book-url').val();
    	var uid = $('#borrow-book-uid').val();
    	var bid = $('#borrow-book-bid').val();

    	if(!bid){
    		alert('empty book id!');
    		return false;
    	}

    	csrftoken = getCookie('csrftoken');
    	$.post(
    		'/borrow/' + bid + '/u' + uid + '/',
    		{'csrfmiddlewaretoken':csrftoken},
    		function(data){
    			var obj = $.parseJSON(data);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong> msg: <strong>' + obj.message
							+ '</strong> uid: <strong>' + uid 
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong>借出成功！'
							+ '</strong> uid: <strong>' + uid 
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				}
				$('#borrow-book-tbody').append(txt);
				$('#borrow-book-bid').val('');
    		}
    	);
    });

	$('#magic-return').click(function(){
		var bid = $('#return-book-bid').val();

    	if(!bid){
    		alert('empty book id!');
    		return false;
    	}

    	csrftoken = getCookie('csrftoken');
    	$.post(
    		'/return/' + bid + '/',
    		{'csrfmiddlewaretoken':csrftoken},
    		function(data){
    			var obj = $.parseJSON(data);
    			var txt = null;
				if(obj.status == 'Error'){
					txt = '<tr><td><div class="alert alert-danger"><strong>Error!</strong> ' 
							+ 'err: <strong>' + obj.err 
							+ '</strong> msg: <strong>' + obj.message
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				} else if(obj.status == 'OK'){
					txt = '<tr><td><div class="alert alert-success">' 
							+ '<strong>还书成功！'
							+ '</strong> bid: <strong>' + bid
							+ '</strong></div></td></tr>';
				}
				$('#return-tbody').append(txt);
				$('#return-book-bid').val('');
    		}
    	);
	});

}); // end of window