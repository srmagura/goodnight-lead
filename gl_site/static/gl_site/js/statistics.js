/**
 * Statistics view. Document on load.
 *
 * Refer to http://api.jquery.com/jQuery.ajax/
 * for ajax documentation.
 */

VIA = "VIA"
BAR = "bar"
BOX = "box"

function getPlotType(inventoryName) {
    return (inventoryName === VIA) ? BAR : BOX;
}

$(function() {
    // Graph height
    var graph_height = 600;

    // Drawn plots
    var graphs = {};

    // Users in sample
    var users_in_sample = {};

    // Store jquery elements in more convenient varialbes
    var $form = $("#statistics_request_form"),
        $org = $("#id_organization"),
        $session = $("#id_session"),
        $downloads_session = $("#id_downloads_session"),
        $downloads_organization = $("#id_downloads_organization"),
        $options,

        $graphColumn = $("#graph-column"),
        $graphs = $("#graphs"),
        $graphContainers,

        $messages = $("#statistics-messages"),

        $inventorySelect = $("#inventory-selection"),
        $analysis = $("#analysis"),
        $tables = $();

    // Other variables
    var MIN = 0,
        MAX = 1,
        MEAN = 2,
        STANDARD_DEVIATION = 3,
        PRECISION = 2,
        ANALYSIS_PRIFIX = "#analysis-",
        MIN_DATA_POINTS_FOR_PLOT = 6,
        DATA_ERROR = "There are not enough data points to render a box plot";

    // Hide the graphs and analysis
    $graphColumn.hide();
    $analysis.hide();

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
        $downloads_organization.val($(this).val());
        $downloads_session.val(null);
    });

    // Bind session on change to dynamically set the corresponding
    // downloads input.
    $session.change(function() {
        $downloads_session.val($(this).val())
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
        // Get the selected inventory
        var selected = $inventorySelect.val();

        // Set users in sample
        $(".sample-users").html(users_in_sample[selected]);

        // Empty the graphs, add the correct one, and draw
        $graphs.empty();
        $graphs.append($graphContainers.filter("#" + selected));
        graphs[selected].draw();

        // Empty the tables
        $analysis.empty();

        // Add the correct one if it exists, otherwise hide
        var $table = $tables.filter(ANALYSIS_PRIFIX + selected);

        if ($table.length) {
            $analysis.append($table);
            $analysis.show();
        } else {
            $analysis.hide();
        }

        if (getPlotType(selected) === BOX) {
            $('.boxplot-popover').show()
        } else {
            $('.boxplot-popover').hide()
        }
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
            $tables = $();

            // Process all available inventories
            for (var key in data) {
                var inventory = data[key].inventory,
                    inventory_name = inventory.replace(/ /g, "-"),
                    inventory_data = data[key].data,
                    inventory_analysis = data[key].analysis;

                // Set the count of users in sample
                users_in_sample[inventory_name] = data[key].count;

                // If there is an inventory analysis, build the table for it
                if (inventory_analysis) {
                    var $table = $(
                        '<table id="analysis-' + inventory_name +
                        '" class="table table-hover table-collapsed"></table>'
                    );
                    $table.append(
                        $("<caption>Additional statistics for " +
                            inventory + "</caption>"),
                        $("<thead></thead>").append(
                            $("<th>Metric</th>"),
                            $("<th>Min</th>"),
                            $("<th>Max</th>"),
                            $("<th>Mean</th>"),
                            $("<th>Standard Deviation</th>")
                        )
                    );

                    var $body = $("<tbody></tbody>");

                    for (var i in inventory_analysis) {
                        analysis = inventory_analysis[i];
                        $body.append(
                            $("<tr></tr>").append(
                                $("<td>" + analysis[MIN].metric +
                                    "</td>"),
                                $("<td>" + analysis[MIN].value.toFixed(
                                        PRECISION) +
                                    "</td>"),
                                $("<td>" + analysis[MAX].value.toFixed(
                                        PRECISION) +
                                    "</td>"),
                                $("<td>" + analysis[MEAN].value.toFixed(
                                        PRECISION) +
                                    "</td>"),
                                $("<td>" + analysis[STANDARD_DEVIATION]
                                    .value.toFixed(PRECISION) +
                                    "</td>")
                            )
                        );
                    }

                    // Add to the list of tables
                    $table.append($body);
                    $tables = $tables.add($table);
                }

                var type = getPlotType(inventory_name)

                // Append the select option and graph div for the inventory
                $inventorySelect.append(
                    $("<option></option>")
                    .val(inventory_name)
                    .html(inventory)
                );
                $graphs.append(
                    $('<div></div>').attr("id", inventory_name)
                );

                // Generate the plot
                graphs[inventory_name] = d3plus.viz()
                    .container(("#" + inventory_name))
                    .data(inventory_data)
                    .type(type)
                    .x("key")
                    .y("value")
                    .height(graph_height)
                    .width($graphs.width());

                // Set the color for bar graphs like VIA
                if (type == BAR) {
                    graphs[inventory_name].id(["name", "key"])
                        .color("name")
                        .text({
                            "name": "name",
                            "key": "key"
                        })
                        .tooltip({
                            "Strength": "key"
                        })
                        .y({
                            "label": "Total number of people with this signature strength"
                        });
                } else {
                    graphs[inventory_name].id("name").text("mute");

                    if (inventory_data.length < MIN_DATA_POINTS_FOR_PLOT) {
                        graphs[inventory_name].error(DATA_ERROR);
                    }
                }
            }

            // Detach the rendered graphs.
            $graphContainers = $graphs.children().detach();

            // Fire the change event manually
            $inventorySelect.change();

        }).fail(function(xhr, status, error) {
            // Hide the graph column and parse for messages
            $graphColumn.hide();
            $analysis.hide();

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

    $form.submit()
});
