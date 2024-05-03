$(document).ready(function() {
    document.querySelector(".path").style.animation = "swipe-dot 2s 0.5s infinite";
    document.querySelector(".hand-icon").style.animation = "swipe-hand 2s infinite";
    $('#swipeOverlay').on('mousemove', function(){
        setTimeout(() => {
            $(this).css('z-index', '-1')            
        }, 200);
    })
    $('#swipeOverlay').on('touchstart', function(){
        $(this).css('z-index', '-1')            
    })
});