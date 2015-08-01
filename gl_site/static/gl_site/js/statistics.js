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
    var graphs = {};

    // Store jquery elements in more convenient varialbes
    var $form = $("#statistics_request_form");
    var $org = $("#id_organization");
    var $session = $("#id_session");
    var $options;
    var $graphColumn = $("#graph-column");
    var $graphs = $("#graphs");
    var $graphContainers;
    var $messages = $("#statistics-messages");
    var $inventorySelect = $("#inventory-selection");

    // Hide the graphs
    $graphColumn.hide();

    // If there is more than one organization, remove
    // all options but the empty value from the session select.
    if ($org.children().length > 1) {
        $options = $session.children().detach("[organization!='']");
    }
    // Disable organization select if there is only one choice
    else {
        $org.prop("disabled", true);
    }

    // Bind the organization on change to a function to dynamically
    // set the values of the session input.
    $org.change(function() {
        // Detach all but the empty value
        $session.children().detach("[organization!='']");

        // Append all sessions matching the organization
        $session.append($options.filter("[organization='" + $org.val() + "']"));

        // Set the downloads fields.
        $('#id_downloads_organization').val($(this).val());
        $('#id_downloads_session').val(null);
    });

    // Bind session on change to dynamically set the corresponding
    // downloads input.
    $session.change(function() {
        $('#id_downloads_session').val($(this).val())
    });

    // Bind the window resize event to a funciton for
    // redrawing the graphs
    $(window).resize(function() {
        var width = $graphs.width();

        for (var key in graphs) {
            graphs[key].width(width).draw();
        }
    });

    // Inventory selection change
    // Attach the selected graph.
    $inventorySelect.change(function() {
        var selected = $inventorySelect.val();
        $graphs.empty();
        $graphs.append($graphContainers.filter("#" + selected));
        graphs[selected].draw();
    });

    // Bind the form submit action to a custom function
    // for making an ajax post request.
    $form.submit(function(e) {
        // Prevent the default post action from occurring
        e.preventDefault();

        // Clear old messages
        $messages.empty();

        // Generate post data
        var get = $(this).serialize();

        // Load the post url
        var url = $(this).attr("action");

        // Make the GET request
        $.get(url, get).done(function(data) {
            // Show the graphs column and empty the previous data choices
            $graphColumn.show();
            $inventorySelect.empty();
            $graphs.empty();

            // Process all available inventories
            for (var key in data) {
                var inventory = data[key].inventory;
                var inventory_data = data[key].data;

                var type = (inventory == "Via") ? "bar" : "box";

                // Append the select option and graph div for the inventory
                $inventorySelect.append(
                    $("<option></option>")
                    .val(inventory)
                    .html(inventory)
                );
                $graphs.append(
                    $('<div></div>').attr("id", inventory)
                );

                // Generate the plot
                graphs[inventory] = d3plus.viz()
                    .container(("#" + inventory))
                    .data(inventory_data)
                    .type(type)
                    .id("name")
                    .x("key")
                    .y("value")
                    .height(graph_height)
                    .width($graphs.width())
            }

            // Detach the rendered graphs.
            $graphContainers = $graphs.children().detach();

            // Fire the change event manually
            $inventorySelect.change();

        }).fail(function(xhr, status, error) {
            // Hide the graph column and parse for messages
            $graphColumn.hide();
            messages = JSON.parse(xhr.responseText);

            // Process each message
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
                $messages.append($messageDiv);
            }
        });
    });
});
