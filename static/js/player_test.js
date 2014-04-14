test( "hello test", function() {
    ok( 1 == "1", "Passed!" );
});

test("getVideo", function() {
    function correctVideo(index, videos, expected) {
        equal(getVideo(index, videos), expected);
    }

    correctVideo("3", ["hjdfjvhdbvb"], "dQw4w9WgXcQ");
    correctVideo(3, ["hjdfjvhdbvb"], "dQw4w9WgXcQ");
    correctVideo("0", ["hjdfjvhdbvb"], "hjdfjvhdbvb");
    correctVideo(0, ["hjdfjvhdbvb"], "hjdfjvhdbvb");
    correctVideo("0",[], "dQw4w9WgXcQ");
    correctVideo(0,[], "dQw4w9WgXcQ");
    correctVideo(-1,["hjdfjvhdbvb"], "dQw4w9WgXcQ");
});

test("getVideoIds", function(){
    var correct_videoIds = ["hHUbLv4ThOo", "Y8ygKnBtKAk", "xKkb13IU_DE"];
    var extracted_videoIds = getVideoIds();
    equal(extracted_videoIds.toString(), correct_videoIds.toString());
});

test("getHashFromUrls", function(){
    window.location.hash = "23"
    currentHash = getHashFromUrl();
    equal(currentHash, 23);
    window.location.hash = "-1"
    currentHash = getHashFromUrl();
    equal(currentHash, -1);
});

test("activeClass", function(){
    activeClass("a.thumbnail",1);
    ok($($("a.thumbnail")[1]).addClass("active"));
});

test("setNextPrevious", function(){
    var videoIds = getVideoIds();
    setNextPrevious(videoIds,0,".previous","#previous", true);
    setNextPrevious(videoIds,0,".next","#next", false);
    ok($(".previous").hasClass("disabled"));
    ok(!($(".next").hasClass("disabled")));
    $(".previous").removeClass("disabled");
    setNextPrevious(videoIds,2,".previous","#previous", true);
    setNextPrevious(videoIds,2,".next","#next", false);
    ok(!($(".previous").hasClass("disabled")));
    ok($(".next").hasClass("disabled"));
    $(".next").removeClass("disabled");
    setNextPrevious(videoIds,4,".previous","#previous", true);
    setNextPrevious(videoIds,4,".next","#next", false);
    ok($(".next").hasClass("disabled"));
    ok($(".previous").hasClass("disabled"));
});