$size = ""; //Current size of the window
$prev_size = ""; //Previous size of the window

$xsBreakpoint = 768; //Breakpoint between mobile and full in px
$mdBreakpoint = 992; //Breakpoint between tablet and full

$animationTime = 300; //Time taken to animate extensions
$extendedWidth = 150; //The width of the extended navbar

$(window).load(
    function() {
        $('.popover-toggle').popover({
            trigger: 'click',
            template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>',
        });

        //Get the initial window size - breakpoint at 768px (bootstrap xs breakpoint)
        $windowWidth = $(window).width();
        $size = ($windowWidth <= $xsBreakpoint) ? "mobile" : (($windowWidth < $mdBreakpoint) ? "tablet" : "full");

        $prev_size = $size;

        //Toggle the initial collapse (for mobile devices or small browser windows)
        toggleCollapse();

        //Set the initial state for the navbar positioning
        if($size == "mobile") {
            $('.navbar-slide').css('position', 'fixed');
        }
        else {
            $('.navbar-slide').css('position', 'static');
        }


        //Set the behavior for .navbar-toggle
        $('.navbar-toggle').click(function() {
            //If the nav is collapsed, show the correct menu and
            //slide the nav out
            if($('.navbar-slide').width() == 0) {
                $($(this).data('target')).show();
                $('.navbar-slide').animate({width: $extendedWidth}, $animationTime);
            }
            //If the nav is not collapsed and the toggle for the
            //currently shown menu is pressed, hide the navbar-slider
            //and then hide the menus
            else if($($(this).data('target')).css('display') == "block") {
                $('.navbar-slide').animate({width: "0"}, $animationTime, function(){
                        $('.navbar-collapse').hide();
                });
            }
            //If the nav is not collapsed, and the toggle for the other menu
            //is pressed, hide the current menu and display the other
            else {
                $($(this).data('target')).slideDown($animationTime);
                $('.navbar-collapse').not($(this).data('target')).slideUp($animationTime);
            }
        });
    }
);

//If a computer user is resizing their browser window
$(window).resize(
    function(){
        //Get the current size
        $windowWidth = $(window).width();
        $size = ($windowWidth <= $xsBreakpoint) ? "mobile" : (($windowWidth < $mdBreakpoint) ? "tablet" : "full");
        //If the size has changed
        if($size != $prev_size) {
            //The size has changed
            sizeChange();

            //Make sure the .navbar-slide has the appropriate width
            if($size == "mobile") {
                $('.navbar-slide').css('position', 'fixed');
                $('.navbar-slide').width("0%");
            }
            else {
                $('.navbar-slide').css('position', 'static');
                $('.navbar-slide').width("100%");
                $('.navbar-collapse').hide(); //Hide the collapses
            }
        }

        //Store previous size
        $prev_size = $size;
    }
);

//What to do when the size changes
sizeChange = function() {
    toggleCollapse();
}

//Expand if size is full, collapse if size is mobile
toggleCollapse = function() {
    //Collapse the collapse for mobile
    if($size == "mobile") {
        $(".collapse-xs").removeClass("in");

        //Make sure the chevron points the correct direction.
        $span = $(document).find(".visible-xs-icon");

        if($span.hasClass("glyphicon-chevron-down")) {
            $span.removeClass("glyphicon-chevron-down");
            $span.addClass("glyphicon-chevron-up");
        }
    }
    //Expand the collapse to make sure it is always visible
    else {
        $(".collapse-xs").height("auto");
        $(".collapse-xs").addClass("in");
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
