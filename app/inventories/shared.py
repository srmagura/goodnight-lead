from django import forms
import app.models as models

class Inventory:

    # Default value
    n_pages = 1

    def set_submission(self, submission):
        self.submission = submission

    def submit(self, user, form):
        if self.submission is None:
            self.submission = models.Submission()
            self.submission.inventory_id = self.inventory_id
            self.submission.user = user

        if self.submission.current_page is None:
            self.submission.current_page = 0

        self.submission.current_page += 1
        if self.submission.current_page == self.n_pages:
            self.submission.current_page = None

        self.submission.save()
        self.save_answers(form)

        if self.submission.is_complete():
            if self.n_pages > 1:
                self.load_answers()

            self.save_metrics()

    def save_answers(self, form):
        self.answers = {}
        for key, value in form.cleaned_data.items():
            answer = models.Answer()
            answer.submission = self.submission
            answer.question_id = int(key)
            answer.content = value
            answer.save()
            self.answers[answer.question_id] = answer.content

    def save_metrics(self):
        self.compute_metrics()
        for key, value in self.metrics.items():
            metric = models.Metric()
            metric.submission = self.submission
            metric.key = key
            metric.value = value
            metric.save()

    def load_answers(self):
        self.answers = {}
        qs = models.Answer.objects.filter(submission=self.submission)

        for answer in qs:
            self.answers[answer.question_id] = answer.content

    # Subclasses may override, but are not required to
    def review_process_metrics(self, data, metrics):
        pass


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
