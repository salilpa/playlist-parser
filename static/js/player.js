// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
var videoIds;

// 4. The API will call this function when the video player is ready.

function onPlayerReady(event) {
    if ($('input[name="my-checkbox"]').bootstrapSwitch('state')){
        event.target.playVideo();
    }
}

function onPlayerStateChange(event) {
    if(event.data === 0) {
        currentItem = player.getVideoData().video_id;
        nextIndex = videoIds.indexOf(currentItem) + 1;
        if (nextIndex+1 != 0 && typeof (videoIds[nextIndex]) != "undefined" ){
            openNewUrl(nextIndex);
        }
    }
}

function getVideoIds() {
    var videoIds = [];
    videos = $(".hidden.videoId");
    videosLength = videos.length;
    for (var i=0; i<videosLength; i++){
        videoIds.push(videos[i].innerHTML);
    }
    return videoIds;
}

function getHashFromUrl(){
    if(window.location.hash) {
      return parseInt(window.location.hash.substring(1));
    } else {
      return 0
    }
}

function openNewUrl(videoNumber){
    var a = window.location.protocol + "//" + window.location.hostname + (window.location.port?":"+window.location.port:"") + window.location.pathname + "#" + videoNumber.toString();
    window.location.href = a;
    window.location.reload();
}

function activeClass(obj_name,index){
    $($(obj_name)[index]).addClass("active")
}

function uiChanges(videoIds, hash){
    activeClass("a.thumbnail",hash);
    setNextPrevious(videoIds,hash, ".previous", "#previous", true);
    setNextPrevious(videoIds,hash, ".next", "#next", false);
}

function setNextPrevious(videoIds, hash, class_name, id_name, previous){
    if (previous == true){
        if (hash <= 0 || hash > videoIds.length) {
            $(class_name).addClass("disabled");
        }
        else {
            $(id_name).on("click", function(){openNewUrl(hash-1)})
        }
    } else {
        if (hash >= videoIds.length-1 || hash < -1){
            $(class_name).addClass("disabled");
        }
        else {
            $(id_name).on("click", function(){openNewUrl(hash+1)})
        }
    }
}

function getVideo(index, videoIds){
    var index = parseInt(index);
    if ((index >= 0) && (index < videoIds.length)){
        return videoIds[index];
    } else{
        return "dQw4w9WgXcQ";
    }
}

function onYouTubeIframeAPIReady() {
    videoIds = getVideoIds()
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        //find the first video id
        videoId: getVideo(getHashFromUrl(), videoIds),
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
    uiChanges(videoIds, parseInt(getHashFromUrl()));
}