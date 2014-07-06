from django.template.loader import render_to_string

class SliderMarker:

    def __init__(self, css_id, label, value):
        self.css_id = css_id
        self.label = label
        
        if type(value) is float:
            self.value = round(value, 2)
        else:
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
        
class SliderContainer:

    def __init__(self, labels, slider):
        self.labels = labels
        self.slider = slider
        
    def render(self):
        data = {
            'labels': self.labels,
            'slider': self.slider
        }
        
        return render_to_string('slider_container.html', data)
