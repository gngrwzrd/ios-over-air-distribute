$(document).ready(function() {
	if(isIOSDevice()) {
		$(".desktop").hide();
		$(".mobile").show();
	}
});

function isIOSDevice() {
	return navigator.userAgent.match(/(iPad|iPhone|iPod)/g);
}

function onInstall() {
	setTimeout(function(){
		$(".gohome").show();
	},2000);
}