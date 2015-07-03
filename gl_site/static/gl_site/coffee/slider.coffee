window.initSliders = ->
    $(window).resize(initSliders)

    sliders = $('.slider')
    sliderWidth = sliders.width()
    lineDivWidth = sliders.find('.marker .line div').width()

    for slider in sliders
        slider = $(slider)

        min = Number(slider.find('.min').text())
        max = Number(slider.find('.max').text())
        mid = (min + max) / 2

        for marker in slider.find('.marker')
            marker = $(marker)
            value = marker.find('.value').text()
            factor = .5 + (value - mid) / (max - min)
            left = factor*sliderWidth - lineDivWidth

            marker.css('left', left)
