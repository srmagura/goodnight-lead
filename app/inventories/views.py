from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.inventories import *
import app.models as models

def validate_inventory_id(inventory_id):
    try:
        inventory_id = int(inventory_id)
    except ValueError:
        return False
    
    return inventory_id in inventoryById 

@login_required(redirect_field_name = None)  
def take_inventory(request, inventory_id):
    if validate_inventory_id(inventory_id):    
        inventory = inventoryById[int(inventory_id)]()
    else:
        return page_not_found(request)
    
    submissions = models.Submission.objects.filter(
        user=request.user, inventory_id=inventory_id
    )
    already_taken = len(submissions) != 0
    
    form_cls = InventoryForm
    form_kwargs = {'inventory': inventory}
    
    if request.method == 'POST':
        form = form_cls(request.POST, **form_kwargs) 
        if form.is_valid():
            inventory.submit(request.user, form)
            
            form = None
            return redirect('review_inventory', inventory_id=inventory_id)
    else:       
        form = form_cls(**form_kwargs)
    
    show_form = not already_taken
    data = {'inventory': inventory, 'form': form,
        'already_taken': already_taken,
        'show_form': show_form}
    template = 'take_inventory/{}'.format(inventory.template)
  
    return render(request, template, data)
    
@login_required(redirect_field_name = None)
def review_inventory(request, inventory_id):
    if validate_inventory_id(inventory_id):    
        inventory = inventoryById[int(inventory_id)]()
    else:
        return page_not_found(request)
        
    submissions = models.Submission.objects.filter(
        user=request.user, inventory_id=inventory_id
    )
    metrics = models.Metric.objects.filter(submission=submissions)
    
    data = {'inventory': inventory, 'metrics': metrics}
    template = 'review_inventory/{}'.format(inventory.template)
    
    return render(request, template, data)
