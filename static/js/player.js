// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
var videoIds;
function onYouTubeIframeAPIReady() {
    videoIds = getVideoIds()
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        //find the first video id
        videoId: videoIds[getHashFromUrl()],
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

// 4. The API will call this function when the video player is ready.

function onPlayerReady(event) {
    event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
/*
var done = false;
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
        setTimeout(stopVideo, 6000);
        done = true;
    }
}
function stopVideo() {
    player.stopVideo();
}
*/
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
        videoIds.push(videos[i].innerText);
    }
    return videoIds;
}

function getHashFromUrl(){
    if(window.location.hash) {
      return window.location.hash.substring(1); //Puts hash in variable, and removes the # character
      // hash found
    } else {
      return 0
    }
}

function openNewUrl(videoNumber){
    var a = window.location.protocol + "//" + window.location.hostname + (window.location.port?":"+window.location.port:"") + window.location.pathname + "#" + videoNumber;
    window.location.href = a;
    window.location.reload();
}