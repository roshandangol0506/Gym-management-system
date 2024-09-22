from django.shortcuts import render
from datetime import date

from gym_management_app.models import CustomerDue, Messages, Trainer, CustomerLeave

def trainer_detail(request):
    trainer=Trainer.objects.get(admin__username=request.user.username)

    return render(request, "staff_template/trainer_detail_template.html", {"trainer": trainer})

def trainer_home(request):
    trainer=Trainer.objects.get(admin__username=request.user.username)
    customerdue = CustomerDue.objects.filter(trainer_id=trainer) 
    message= Messages.objects.all()
    current_date = date.today()
    user_first_name = request.user.first_name 

    count = 0
    for cd in customerdue:
        if cd.trainer_id.admin.first_name == user_first_name:
            count+=1
    context = {
        "user": request.user,
        "trainer": trainer,
        "customerdue": customerdue,
        "message": message,
        "current_date": current_date,
        "matching_count": count  
    }
    return render(request, "staff_template/staff_home_template.html", {"context": context})

def customer_leave(request):
    customerleave=CustomerLeave.objects.filter(trainer_id__admin__username=request.user.username)
    current_date = date.today()
    return render(request, "staff_template/staff_customerleave_template.html", {'customerleave': customerleave, "current_date": current_date})