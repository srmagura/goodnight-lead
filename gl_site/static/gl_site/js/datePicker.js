/**
 * Configure a jQuery date picker existing on a page.
 * The date picker has the dependencies:
 * //code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css"
 * //code.jquery.com/ui/1.11.4/jquery-ui.js
 * //code.jquery.com/jquery.js
 */
$(document).ready(function() {
    $(function() {
        $('.date-picker').datepicker({
            clickInput:true,
            changeYear:true,
            yearRange:"c-30:c+30"
        });
    });
});
