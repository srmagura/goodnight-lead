# Used to create columns of equal height within bootstrap 3 rows, since
# there is no convenient native way to do so.
#
# Currently only used for registration and account settings pages. Probably
# needs to be generalized if it's going to be used in other places.

$(document).ready( ->
    equalizeHeights(true)
)

# Go through all of the elements that have class 'equal-height' and find
# the maximum height. Then set all of the elements to this maximum height.
equalizeHeights = (initial=false) ->
    elements = $('.equal-height')
    maxHeight = 0

    for el in elements
        el = $(el)
        if el.height() > maxHeight
            maxHeight = el.height()

    if initial or $size == "full"
        elements.height(maxHeight);
    else
        elements.height('auto');

# Override the default resize function
# FIXME What if we want to have two resize functions at once?
window.sizeChange = equalizeHeights
