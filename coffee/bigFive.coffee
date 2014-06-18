window.bigFiveReviewInit = ->
    $(window).resize(bigFiveReviewInit)

    scaleWidth = $('.scale').width()
    lineDivWidth = $('.marker .line div').width()

    for marker in $('.marker')
        marker = $(marker)
        value = marker.find('.value').text()
        factor = .5 + (value - 8) / 12
        left = factor*scaleWidth - lineDivWidth

        marker.css('left', left)
