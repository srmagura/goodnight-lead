# Import forms for Question
from django import forms

# Import models for saving inventory results
# to the database
import gl_site.models as models

# Inventory represents an inventory taken by a user.
# Handles submission of an inventory to save as part
# of the database using the django model framework.
class Inventory:
    # Class values
    n_pages = 1

    # Init Inventory. Set default fields used by
    # sublcasses to remove linter warnings.
    def __init__(self):
        # Fields which get set elsewhere
        self.submission = None
        self.inventory_id = None
        self.answers = None
        self.metrics = None

    # Sets the current submission
    def set_submission(self, submission):
        self.submission = submission

    # Submits the inventory and handles saving
    # to the database.
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

    # Handles the saving of each individual answer
    # to the database.
    def save_answers(self, form):
        self.answers = {}
        for key, value in form.cleaned_data.items():
            answer = models.Answer()
            answer.submission = self.submission
            answer.question_id = int(key)
            answer.content = value
            answer.save()
            self.answers[answer.question_id] = answer.content

    # Computes the metrics for the inventory and then
    # saves it to the database.
    def save_metrics(self):
        self.compute_metrics()
        for key, value in self.metrics.items():
            metric = models.Metric()
            metric.submission = self.submission
            metric.key = key
            metric.value = value
            metric.save()

    # Load the answers corresponding to the submission
    def load_answers(self):
        self.answers = {}
        qs = models.Answer.objects.filter(submission=self.submission)

        for answer in qs:
            self.answers[answer.question_id] = answer.content

    # Subclasses may override, but are not required to
    def review_process_metrics(self, data, metrics):
        pass

    # Overridden by subclasses. Used to compute metrics.
    def compute_metrics(self):
        pass

# An Inventory question.
class Question:
    def __init__(self, qid, text):
        self.question_id = qid
        self.text = text

# Question sublcass that has a range of numbers
# as answer choices. Contains its own answer
# form field.
class NumberQuestion(Question):
    # Fields set by subclasses
    minimum = None
    maximum = None
    choice_labels = None

    # Return the form answer field for the question.
    def get_field(self):
        choices = zip(range(self.minimum, self.maximum+1),
            self.choice_labels)
        label = '{}. {}'.format(self.question_id, self.text)

        return forms.ChoiceField(widget=forms.RadioSelect,
            label=label,
            choices=choices)

# Form for an inventory that is built out of each of the
# fields for each of the questions contained within the
# inventory.
class InventoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        inventory = kwargs.pop('inventory')
        super(InventoryForm, self).__init__(*args, **kwargs)

        for question in inventory.questions:
            self.fields[str(question.question_id)] = question.get_field()
