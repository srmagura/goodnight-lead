"""
Objects used for displaying inventory results to the user. All of the
classes in this module map fairly directly to HTML.
"""

from django.template.loader import render_to_string

class Slider:
    """
    A numberline with defined minimum and maximum values. SliderMarkers are
    used to show a datapoint on the numberline.
    """

    def __init__(self, min_value, max_value, markers):
        """
        min_value -- minimum value for the numberline (float or int)
        max_value -- minimum value for the numberline (float or int)
        markers -- iterable containing SliderMarkers to display on the
        slider
        """
        self.min_value = min_value
        self.max_value = max_value
        self.markers = markers

    def render(self):
        """
        Return a string containing the HTML for this slider.
        """
        data = {
            'min_value': self.min_value,
            'max_value': self.max_value,
            'markers': self.markers
        }

        return render_to_string('slider.html', data)

class SliderMarker:
    """
    A marker on a slider. Basically a small colored box with a small piece
    of text lies at a certain position along the slider.
    """

    def __init__(self, css_id, label, value):
        self.css_id = css_id
        self.label = label

        if type(value) is float:
            self.value = round(value, 2)
        else:
            self.value = value


class SliderContainer:
    """
    A container for the Slider object that places labels at the left and
    right ends of the slider.
    """

    def __init__(self, labels, slider):
        self.labels = labels
        self.slider = slider
        self.sublabels = ('', '')

    def render(self):
        data = {
            'labels': self.labels,
            'sublabels': self.sublabels,
            'slider': self.slider,
        }

        return render_to_string('slider_container.html', data)
