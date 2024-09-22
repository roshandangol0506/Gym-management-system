from django.shortcuts import render
from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from gym_management_app.models import CustomerDue, Customer, Event, Messages,  CustomerLeave, Trainer
from gym_management_app.forms import AddCustomerLeaveForm

def customer_home(request):
    customer=Customer.objects.filter(admin__username=request.user.username)
    customerdue = CustomerDue.objects.filter(customer_id__admin__username=request.user.username)
    current_date = date.today()
    event= Event.objects.all()
    message= Messages.objects.all()

    form=AddCustomerLeaveForm()

    context = {
        "due": customerdue, 
        "customer": customer,
        "event": event,
        "message": message, 
        "current_date": current_date,
        "form": form
    }
        
    return render(request, "student_template/student_home_template.html", context)

def customer_detail(request):
    customer=Customer.objects.filter(admin__username=request.user.username)

    return render(request, "student_template/student_detail_template.html", {"customer": customer})


def save_add_customerleave(request):
    if request.method == 'POST':
        form = AddCustomerLeaveForm(request.POST)
        if form.is_valid():
            start_date= form.cleaned_data["start_date"]
            end_date= form.cleaned_data["end_date"]
            description= form.cleaned_data["description"]
            trainer=request.POST.get('trainer')
            try:
                trainer_id=Trainer.objects.get(admin__username=trainer)
                customer_id=Customer.objects.get(admin__username=request.user.username)

                CustomerLeave.objects.create(customer_id=customer_id, trainer_id=trainer_id, start_date=start_date, end_date=end_date, description=description)
                messages.success(request, "Successfully Added Event")
                return HttpResponseRedirect("/add_event")
            
            except:
                messages.error(request, "Failed to Add Event")
                return HttpResponseRedirect("/add_event")
        else:
            messages.error(request,"Invalid form data")
            return HttpResponseRedirect("/customer_detail")