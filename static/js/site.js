
function isMobileDevice(){
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

function isAutoPlay(){
    if (docCookies.hasItem("autoplay")){
        return (docCookies.getItem("autoplay") == "true");
    } else{
        docCookies.setItem("autoplay", "false");
        return false;
    }
}

if (isMobileDevice()){
    $("#onlyDesktop").addClass("hidden")
}

$("[name='my-checkbox']").bootstrapSwitch();
$('input[name="my-checkbox"]').bootstrapSwitch('state', isAutoPlay());

$('input[name="my-checkbox"]').on('switchChange.bootstrapSwitch', function(event, state) {
    docCookies.setItem("autoplay", state.toString());
});