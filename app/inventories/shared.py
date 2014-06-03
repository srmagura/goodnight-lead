from django import forms
import app.models as models

class Inventory:

    def submit(self, user, form):
        submission = models.Submission()
        submission.inventory_id = self.inventory_id
        submission.user = user
        submission.save()
        
        for key, value in form.cleaned_data.items():
            answer = models.Answer()
            answer.submission = submission
            answer.question_id = int(key)
            answer.content = value
            answer.save()

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
        
        
