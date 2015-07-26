/**
 * Statistics view. Document on load.
 *
 * Refer to http://api.jquery.com/jQuery.ajax/
 * for ajax documentation.
 */
$(function() {
    // Store jquery elements in more convenient varialbes
    var $form = $("#statistics_request_form");
    var $org = $form.children("#id_organization");
    var $session = $form.children("#id_session");

    // Remove all options but the empty value from the session select.
    var $options = $session.children().detach("[organization!='']");

    // Bind the organization on change to a function to dynamically
    // set the values of the session input.
    $org.change(function() {
        // Detach all but the empty value
        $session.children().detach("[organization!='']");

        // Append all sessions matching the organization
        $session.append($options.filter("[organization='" + $org.val() + "']"));
    });

    // Bind the form submit action to a custom function
    // for making an ajax post request.
    $form.submit(function(e) {
        // Prevent the default post action from occurring
        e.preventDefault();

        // Generate post data
        var get = $(this).serialize();

        // Load the post url
        var url = $(this).attr("action");

        // Make the GET request
        $.get(url, get).done(function(data) {
            gd = data;
            //  Clear the other graphs
            $("#content").empty();

            for (var key in data) {
                var inventory = data[key];

                // Create the jQuery div
                $("#content").append('<div id="' + key + '"/>');

                // Draw the plot
                var box = d3plus.viz()
                    .container(("#" + key))
                    .data(inventory)
                    .type("box")
                    .id("name")
                    .x("key")
                    .y("value")
                    .title(key)
                    .height(500)
                    .draw();
            }

        }).fail(function(xhr, status, error) {
            $("#content").html("failure: " + xhr.responseText);
        });
    });
});
var gd;
