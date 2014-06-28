$size = ""; //Current size of the window
$prev_size = ""; //Previous size of the window

$(window).load(
    function() {
        //Get the initial window size - breakpoint at 768px (bootstrap xs breakpoint)
        $size = ($(window).width() >= 768) ? "full" : "mobile";
        $prev_size = $size;

        //Toggle the initial collapse (for mobile devices or small browser windows)
        toggleCollapse();

        //Set the initial state for the navbar positioning
        if($size == "full") {
            $('.navbar-slide').css('position', 'static');
        }
        else {
            $('.navbar-slide').css('position', 'fixed');
        }

        //Set the behavior for .navbar-toggle
        $('.navbar-toggle').click(function() {
            //If the nav is collapsed, show the correct menu and
            //slide the nav out
            if($('.navbar-slide').width() == 0) {
                $($(this).data('target')).show();
                $('.navbar-slide').animate({width: "40%"}, 500);
            }
            //If the nav is not collapsed and the toggle for the
            //currently shown menu is pressed, hide the navbar-slider
            //and then hide the menus
            else if($($(this).data('target')).css('display') == "block") {
                $('.navbar-slide').animate({width: "0%"}, 500, function(){
                        $('.navbar-collapse').hide();
                });
            }
            //If the nav is not collapsed, and the toggle for the other menu
            //is pressed, hide the current menu and display the other
            else {
                $($(this).data('target')).slideDown(500);
                $('.navbar-collapse').not($(this).data('target')).slideUp(500);
            }
        });
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

            //Make sure the .navbar-slide has the appropriate width
            //Hide the collapses
            if($size == "full") {
                $('.navbar-slide').css('position', 'static');
                $('.navbar-slide').width("100%");
                $('.navbar-collapse').hide();
            }
            else {
                $('.navbar-slide').css('position', 'fixed');
                $('.navbar-slide').width("0%");
            }
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
