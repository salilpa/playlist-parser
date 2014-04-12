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

