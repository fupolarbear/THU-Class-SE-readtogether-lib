var cq;

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
	console.log(e.target);
	cq = e.target;
	console.log(e.relatedTarget);
})