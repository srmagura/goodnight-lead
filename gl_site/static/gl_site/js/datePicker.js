/**
 * Configure a jQuery date picker existing on a page.
 * The date picker has the dependencies:
 * //code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css"
 * //code.jquery.com/ui/1.11.4/jquery-ui.js
 * //code.jquery.com/jquery.js
 *
 * It also relies on the bootstrap glyphicon set.
 */
$(document).ready(function() {
    $(function() {
        // Initialize
        $('.date-picker').datepicker({
                clickInput: true,
                changeYear: true,
                yearRange: "c-30:c+30",
                showOn: "both",
            })
            // Set the datepicker css classes
            .attr(
                'class', 'date-picker-input-group form-control'
            );

        // Set the button text to a span with correct calendar icon
        $('.ui-datepicker-trigger').html(
            '<span class="glyphicon glyphicon-calendar"></span>'
        );
        // Set the button css class
        $('.ui-datepicker-trigger').attr(
            'class',
            'ui-datepicker-trigger btn btn-default'
        );

        // Wrap the button inside of the bootstrap input group btn class
        $('.ui-datepicker-trigger').wrap(
            '<div class="date-picker-input-group input-group-btn"></div>'
        );

        // Wrap the input and button in an input group
        $('.date-picker-input-group').wrapAll(
            '<div class="input-group"></div>'
        );
    });
});
