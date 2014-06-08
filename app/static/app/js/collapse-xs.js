$size = ""; //Current size of the window
$prev_size = ""; //Previous size of the window

$(window).load(
    function() {
        //Get the initial window size - breakpoint at 768px (bootstrap xs breakpoint)
        $size = ($(window).width() >= 768) ? "full" : "mobile";
        $prev_size = $size;
    
        //Toggle the initial collapse (for mobile devices or small browser windows)
        toggleCollapse();
    }
);

//If a computer user is resizing their browser window
$(window).resize(
    function(){
        //Get the current size
        $size = ($(window).width() >= 768) ? "full" : "mobile";
        
        //If the size has changed
        if($size != $prev_size) {
            toggleCollapse();
        }
        
        //Store previous size
        $prev_size = $size;
    }
);

//Expand if size is full, collapse if size is mobile
toggleCollapse = function() {
    //Expand the collapse to make sure it is always visible
    if($size == "full") {
        $(".collapse-xs").height("auto");
        $(".collapse-xs").addClass("in");
    }
    //Collapse the collapse for mobile
    else {
        $(".collapse-xs").removeClass("in");
        
        //Make sure the chevron points the correct direction.
        $span = $(document).find(".visible-xs-icon");
        
        if($span.hasClass("glyphicon-chevron-down")) {
            $span.removeClass("glyphicon-chevron-down");
            $span.addClass("glyphicon-chevron-up");
        }
    }
}

//Rotates the chevron icon in the expand link to indicate expanded/collapsed
rotateChevron = function($this) {
    $span = $this.find(".visible-xs-icon");
    
    if($span.hasClass("glyphicon-chevron-up")) {
        $span.removeClass("glyphicon-chevron-up");
        $span.addClass("glyphicon-chevron-down");
    }
    else {
        $span.removeClass("glyphicon-chevron-down");
        $span.addClass("glyphicon-chevron-up");
    }
}