/**
 * Statistics view. Document on load.
 *
 * Refer to http://api.jquery.com/jQuery.ajax/
 * for ajax documentation.
 */
$(function() {
    // Graph height
    var graph_height = 600;
    // Drawn plots
    var graphs = [];

    // Store jquery elements in more convenient varialbes
    var $form = $("#statistics_request_form");
    var $org = $("#id_organization");
    var $session = $("#id_session");

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

    // Bind the window resize event to a funciton for
    // redrawing the graphs
    $(window).resize(function() {
        var width = $("#graphs").width();

        for (var key in graphs) {
            graphs[key].width(width).draw();
        }
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
            //  Clear the other graphs
            $("#graphs").empty();

            for (var key in data) {
                var inventory = data[key].inventory;
                var inventory_data = data[key].data;

                // Create the jQuery div
                $("#graphs").append('<div id="' + inventory + '"/>');

                var type = (inventory == "Via") ? "bar" : "box";

                // Draw the plot
                graphs.push(
                    d3plus.viz()
                    .container(("#" + inventory))
                    .data(inventory_data)
                    .type(type)
                    .id("name")
                    .x("key")
                    .y("value")
                    .title(inventory)
                    .height(graph_height)
                    .draw()
                );
            }

        }).fail(function(xhr, status, error) {
            messages = JSON.parse(xhr.responseText);

            for (var i in messages) {
                // Append the error message to the page
                $messageDiv = $("<div></div>").attr(
                    "class",
                    "alert alert-danger alert-dismissable"
                );
                $dismiss = $("<button></button>").attr(
                        "class", "close"
                    ).attr(
                        "data-dismiss", "alert"
                    ).attr(
                        "aria-hidden", "true"
                    )
                    .html("&times;");
                $messageDiv.html(messages[i]).append($dismiss);
                $("#statistics-messages").append($messageDiv);
            }
        });
    });
});
