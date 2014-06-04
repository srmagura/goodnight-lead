from django import forms
import app.models as models

class Inventory:

    def submit(self, user, form):
        self.submission = models.Submission()
        self.submission.inventory_id = self.inventory_id
        self.submission.user = user
        self.submission.save()
        
        self.answers = {}
        for key, value in form.cleaned_data.items():
            answer = models.Answer()
            answer.submission = self.submission
            answer.question_id = int(key)
            answer.content = value
            answer.save()
            self.answers[answer.question_id] = answer.content
            
        self.compute_metrics()
        for key, value in self.metrics.items():
            metric = models.Metric()
            metric.submission = self.submission
            metric.key = key
            metric.value = value
            metric.save()

class Question:

    def __init__(self, qid, text):
        self.question_id = qid
        self.text = text

class NumberQuestion(Question):
    
    def get_field(self):
        choices = zip(range(self.minimum, self.maximum+1), 
            self.choice_labels)
        label = '{}. {}'.format(self.question_id, self.text)  
            
        return forms.ChoiceField(widget=forms.RadioSelect, 
            label=label,
            choices=choices)
    
class InventoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        inventory = kwargs.pop('inventory')
        super(InventoryForm, self).__init__(*args, **kwargs)

        for question in inventory.questions:
           self.fields[str(question.question_id)] = question.get_field()
        
        
