from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from gl_site.inventories import inventory_by_id

from gl_site.inventories.shared import InventoryForm

import gl_site.models as models
import gl_site.views

def validate_inventory_id(inventory_id):
    try:
        inventory_id = int(inventory_id)
    except ValueError:
        return False

    return inventory_id in inventory_by_id

def get_submission(user, inventory_id):
    submissions = models.Submission.objects.filter(
        user=user, inventory_id=inventory_id
    )

    if len(submissions) != 0:
        return submissions[0]
    else:
        return None

def submission_is_complete(submission):
    return submission is not None and submission.is_complete()

@login_required(redirect_field_name = None)
def take_inventory(request, inventory_id):
    if validate_inventory_id(inventory_id):
        inventory = inventory_by_id[int(inventory_id)]()
    else:
        return app.views.page_not_found(request)

    submission = get_submission(request.user, inventory_id)
    is_complete = submission_is_complete(submission)
    inventory.set_submission(submission)

    form_cls = InventoryForm
    form_kwargs = {'inventory': inventory}

    if request.method == 'POST':
        form = form_cls(request.POST, **form_kwargs)
        if form.is_valid():
            inventory.submit(request.user, form)
            is_complete = True
    else:
        form = form_cls(**form_kwargs)

    if is_complete:
        return redirect('review_inventory', inventory_id=inventory_id)

    is_final_page = (inventory.n_pages == 1 or
        (submission is not None and
        submission.current_page == inventory.n_pages - 1))

    data = {'inventory': inventory, 'form': form,
        'is_final_page': is_final_page}
    template = 'take_inventory/{}'.format(inventory.template)

    return render(request, template, data)


@login_required(redirect_field_name = None)
def review_inventory(request, inventory_id):
    if validate_inventory_id(inventory_id):
        inventory = inventory_by_id[int(inventory_id)]()
    else:
        return app.views.page_not_found(request)

    submission = get_submission(request.user, inventory_id)
    is_complete = submission_is_complete(submission)

    if not is_complete:
        return redirect('take_inventory', inventory_id=inventory_id)

    data = {'inventory': inventory}

    metrics = models.Metric.objects.filter(submission=submission)
    inventory.review_process_metrics(data, metrics)

    template = 'review_inventory/{}'.format(inventory.template)

    return render(request, template, data)
