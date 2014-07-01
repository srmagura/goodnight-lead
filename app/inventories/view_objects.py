from django.template.loader import render_to_string

class SliderMarker:

    def __init__(self, css_id, label, value):
        self.css_id = css_id
        self.label = label
        self.value = value
    
class Slider:

    def __init__(self, min_value, max_value, markers):
        self.min_value = min_value
        self.max_value = max_value
        self.markers = markers
 
    def render(self):
        data = {
            'min_value': self.min_value,
            'max_value': self.max_value,
            'markers': self.markers
        }
        
        return render_to_string('slider.html', data)
