from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from urllib.parse import quote

from gym_management_app.models import CustomUser, Customer, Trainer, CustomerDue, Event, EventParticipation, Messages
from gym_management_app.forms import AddTrainerForm, EditTrainerForm, AddCustomerForm, EditCustomerForm, AddGymFeesForm, EditGymFeesForm, AddEventForm, EditEventForm, AddParticipationForm, AddCustomerLeaveForm

def admin_home(request):
    trainers=Trainer.objects.all()
    customers=Customer.objects.all()

    count_trainer=0
    for trainer in trainers:
        count_trainer+=1

    count_customer=0
    for customer in customers:
        count_customer+=1

    context = {
        "trainer": trainers,
        "customer": customers,
        "count_trainer": count_trainer,
        "count_customer": count_customer,  
    }
    return render(request, "hod_template/home_content.html", {"context": context})

def add_trainer(request):
    form=AddTrainerForm()
    return render(request, "hod_template/add_staff_template.html", {"form": form})

def save_add_trainer(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddTrainerForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            gender=form.cleaned_data["gender"]
            price=form.cleaned_data["price"]
            phoneno=form.cleaned_data["phoneno"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                user.trainer.address=address
                user.trainer.gender=gender
                user.trainer.price=price
                user.trainer.phoneno=phoneno
                user.trainer.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Trainer")
                return HttpResponseRedirect("/add_trainer")
            except:
                messages.error(request,"Failed to add Trainer")
                return HttpResponseRedirect("/add_trainer")
        else:
            messages.error(request,"Invalid form data")
            return HttpResponseRedirect("/add_trainer")
        
def manage_trainer(request):
    query = request.GET.get('search')
    
    if query:
        trainers = Trainer.objects.filter(
            Q(admin__first_name__icontains=query) | 
            Q(admin__last_name__icontains=query)
        ).order_by('admin__first_name', 'admin__last_name')
    else:
        trainers = Trainer.objects.all().order_by('admin__first_name', 'admin__last_name')
    
    return render(request, "hod_template/manage_staff_template.html", {"Trainer": trainers})


def edit_trainer(request, trainer_id):
    request.session['trainer_id']= trainer_id
    trainer=Trainer.objects.get(admin=trainer_id)
    form=EditTrainerForm()
    form.fields['email'].initial=trainer.admin.email
    form.fields['first_name'].initial = trainer.admin.first_name
    form.fields['last_name'].initial = trainer.admin.last_name
    form.fields['username'].initial = trainer.admin.username
    form.fields['address'].initial = trainer.address
    form.fields['phoneno'].initial = trainer.phoneno
    form.fields['price'].initial = trainer.price
    form.fields['gender'].initial = trainer.gender

    return render(request, "hod_template/edit_staff_template.html", {"form": form, "id": trainer_id, "username": trainer.admin.username})


def save_edit_trainer(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        trainer_id=request.session.get("trainer_id")
        if trainer_id==None:
            return HttpResponseRedirect("/manage_trainer")
        
        form=EditTrainerForm(request.POST, request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            address=form.cleaned_data["address"]
            gender=form.cleaned_data["gender"]
            price=form.cleaned_data["price"]
            phoneno=form.cleaned_data["phoneno"]

            if request.FILES.get('profile_pic', False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None

            try:
                user=CustomUser.objects.get(id=trainer_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                trainer=Trainer.objects.get(admin=trainer_id)
                trainer.address=address
                trainer.phoneno=phoneno
                trainer.gender=gender
                trainer.price=price
                if profile_pic_url!=None:
                    trainer.profile_pic=profile_pic_url
                trainer.save()
                del request.session['trainer_id']
                messages.success(request,"Successfully Edited Trainer")
                return HttpResponseRedirect(reverse("edit_trainer",kwargs={"trainer_id":trainer_id}))
            except:
                messages.error(request,"Failed to Edit Trainer")
                return HttpResponseRedirect(reverse("edit_trainer",kwargs={"trainer_id":trainer_id}))
        else:
            form=EditTrainerForm(request.POST)
            trainer=Trainer.objects.get(admin=trainer_id)
            return render(request,"hod_template/edit_staff_template.html",{"form":form,"id":trainer_id,"username":trainer.admin.username})


def delete_trainer(request, trainer_id):
    try:
        trainer = Trainer.objects.get(admin_id=trainer_id)
        print(trainer.admin.username)
        
        customer_due = CustomerDue.objects.filter(trainer_id=trainer)

        if customer_due.exists():
            messages.error(request, "Trainer cannot be deleted as they are associated with customer dues.")
            return redirect('/manage_trainer')
        
        trainer.delete()

        customuser = get_object_or_404(CustomUser, username=trainer.admin.username)
        customuser.delete()

        messages.success(request, "Trainer successfully deleted.")
    except Trainer.DoesNotExist:
        messages.error(request, "Trainer does not exist.")
    except Exception as e:
        messages.error(request, f"Failed to delete Trainer: {e}")

    return redirect('/manage_trainer')
 


def add_customer(request):
    form=AddCustomerForm()
    return render(request, "hod_template/add_student_template.html", {"form": form})

def save_add_customer(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddCustomerForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            phoneno=form.cleaned_data["phoneno"]
            gender=form.cleaned_data["gender"]
            height=form.cleaned_data["height"]
            weight=form.cleaned_data["weight"]
            age=form.cleaned_data["age"]
            bicepsize=form.cleaned_data["bicepsize"]
            chestsize=form.cleaned_data["chestsize"]
            legsize=form.cleaned_data["legsize"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.customer.address=address
                user.customer.phoneno=phoneno
                user.customer.gender=gender
                user.customer.height=height
                user.customer.weight=weight
                user.customer.age=age
                user.customer.profile_pic=profile_pic_url
                user.customer.bicepsize=bicepsize
                user.customer.chestsize=chestsize
                user.customer.legsize=legsize
                user.save()
                messages.success(request,"Successfully Added Gym Member")
                return HttpResponseRedirect("/add_customer")
            except:
                messages.error(request,"Failed to add Gym Member")
                return HttpResponseRedirect("/add_customer")
        else:
            messages.error(request,"Invalid Form Data")
            return HttpResponseRedirect("/add_customer")
        
def manage_customer(request):
    query = request.GET.get('search')
    order = request.GET.get('order')

    customer = Customer.objects.all()

    if query:
        customer = customer.filter(
            Q(admin__first_name__icontains=query) | 
            Q(admin__last_name__icontains=query)
        )

    if order:
        if order == "join-date":
            customer = customer.order_by('admin__date_joined')
        elif order == "name":
            customer = customer.order_by('admin__first_name', 'admin__last_name')
        elif order == "height":
            customer = customer.order_by('-height')
        elif order == "weight":
            customer = customer.order_by('-weight')
        elif order == "age":
            customer = customer.order_by('-age')
        elif order == "chest-size":
            customer = customer.order_by('-chestsize')
    else:
        customer = customer.order_by('admin__first_name', 'admin__last_name')
    
    return render(request, "hod_template/manage_student_template.html", {'customer': customer})

def edit_customer(request, customer_id):
    request.session['customer_id']= customer_id
    customer=Customer.objects.get(admin=customer_id)
    form=EditCustomerForm()
    form.fields['email'].initial=customer.admin.email
    form.fields['first_name'].initial = customer.admin.first_name
    form.fields['last_name'].initial = customer.admin.last_name
    form.fields['username'].initial = customer.admin.username
    form.fields['address'].initial = customer.address
    form.fields['phoneno'].initial = customer.phoneno
    form.fields['gender'].initial = customer.gender
    form.fields['height'].initial = customer.height
    form.fields['weight'].initial = customer.weight
    form.fields['age'].initial = customer.age
    form.fields['bicepsize'].initial = customer.bicepsize
    form.fields['chestsize'].initial = customer.chestsize
    form.fields['legsize'].initial = customer.legsize

    return render(request, "hod_template/edit_student_template.html", {"form": form, "id": customer_id, "username": customer.admin.username})


def save_edit_customer(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        customer_id=request.session.get("customer_id")
        if customer_id==None:
            return HttpResponseRedirect("/manage_customer")
        
        form= EditCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            email=form.cleaned_data["email"]
            username=form.cleaned_data["username"]
            address=form.cleaned_data["address"]
            phoneno=form.cleaned_data["phoneno"]
            gender=form.cleaned_data["gender"]
            height=form.cleaned_data["height"]
            weight=form.cleaned_data["weight"]
            age=form.cleaned_data["age"]
            bicepsize=form.cleaned_data["bicepsize"]
            chestsize=form.cleaned_data["chestsize"]
            legsize=form.cleaned_data["legsize"]

            if request.FILES.get('profile_pic', False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None

            try:
                user=CustomUser.objects.get(id=customer_id)
                user.first_name=first_name
                user.last_name=last_name
                user.email=email
                user.username=username
                user.save()

                customer=Customer.objects.get(admin=customer_id)
                customer.address=address
                customer.phoneno=phoneno
                customer.gender=gender
                customer.height=height
                customer.weight=weight
                customer.age=age
                customer.bicepsize=bicepsize
                customer.chestsize=chestsize
                customer.legsize=legsize
                if profile_pic_url!=None:
                    customer.profile_pic=profile_pic_url
                customer.save()
                del request.session['customer_id']
                messages.success(request,"Successfully Edited Gym Memeber")
                return HttpResponseRedirect(reverse("edit_customer",kwargs={"customer_id":customer_id}))
            except:
                messages.error(request,"Failed to Edit Gym Member")
                return HttpResponseRedirect(reverse("edit_customer",kwargs={"customer_id":customer_id}))
        else:
            form=EditCustomerForm(request.POST)
            customer=Trainer.objects.get(admin=customer_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":customer_id,"username":customer.admin.username})

def delete_customer(request, customer_id):
    customer=Customer.objects.get(admin_id=customer_id)
    print(customer.admin.username)
    try:
        customer_due = CustomerDue.objects.filter(customer_id=customer)
        customer_due.delete()

        customer = get_object_or_404(Customer, admin_id=customer_id)
        customer.delete()

        customuser=get_object_or_404(CustomUser, username=customer.admin.username)
        customuser.delete()

        messages.success(request, "Gym Member successfully deleted.")
    except Exception as e:
        messages.error(request, "Failed to delete Gym Member: {e}")

    return redirect('/manage_customer') 


def add_gymfees(request):
    form=AddGymFeesForm()
    return render(request, "hod_template/add_gymfees_template.html", {"form": form})

def save_add_gymfees(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddGymFeesForm(request.POST)
        if form.is_valid():
            trainer = form.cleaned_data["trainer"]
            customer = form.cleaned_data["customer"]
            session_start_date = request.POST.get("session_start_date")
            amount = request.POST.get("amount")
            session_end_date = request.POST.get("session_end_date")

            try:
                trainer_id = Trainer.objects.get(id=trainer)
                customer_id = Customer.objects.get(id=customer)

                customerdue, created = CustomerDue.objects.update_or_create(
                    customer_id=customer_id,
                    defaults={
                        "trainer_id": trainer_id,
                        "session_start_date": session_start_date,
                        "amount": amount,
                        "session_end_date": session_end_date
                    }
                )

                if created:
                    messages.success(request, "Successfully Added Gym Fees")
                else:
                    messages.success(request, "Successfully Updated Gym Fees")

                return HttpResponseRedirect("/add_gymfees")
            except Exception as e:
                messages.error(request, f"Failed to Add Gym Fees: {e}")
                return HttpResponseRedirect("/add_gymfees")



def manage_gymfees(request):
    query = request.GET.get('search')
    order=request.GET.get('order')
    
    customerdue = CustomerDue.objects.all()
    if query:
        customerdue = CustomerDue.objects.filter(
            Q(customer_id__admin__first_name__icontains=query) | 
            Q(customer_id__admin__last_name__icontains=query) |
            Q(trainer_id__admin__first_name__icontains=query) |
            Q(trainer_id__admin__last_name__icontains=query)
        ).order_by('customer_id__admin__first_name', 'customer_id__admin__last_name', 'trainer_id__admin__first_name', 'trainer_id__admin__last_name')
    elif order:
        if order == "days-left":
            customerdue = customerdue.order_by('session_end_date')
        elif order == "name":
            customerdue = customerdue.order_by('customer_id__admin__first_name', 'customer_id__admin__last_name')
        elif order == "amount":
            customerdue = customerdue.order_by('-amount')
        elif order == "updated-at":
            customerdue = customerdue.order_by('-updated_at')
    else:
        customerdue=CustomerDue.objects.all().order_by('session_end_date')
    return render(request, "hod_template/manage_gymfees_template.html",{'customerdue':customerdue})

def edit_gymfees(request, customerdue_id):
    request.session['customerdue_id']= customerdue_id
    customerdue=CustomerDue.objects.get(id=customerdue_id)
    form=EditGymFeesForm()
    form.fields['trainer'].initial=customerdue.trainer_id.id
    form.fields['customer'].initial = customerdue.customer_id.id
    form.fields['session_start_date'].initial = customerdue.session_start_date
    form.fields['session_end_date'].initial = customerdue.session_end_date
    form.fields['amount'].initial = customerdue.amount
    return render(request, "hod_template/edit_gymfees_template.html", {"form": form, "id": customerdue_id, "username": customerdue.customer_id.admin.first_name})


def save_edit_gymfees(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        customerdue_id=request.session.get("customerdue_id")
        if customerdue_id==None:
            return HttpResponseRedirect("/manage_gymfees")
        
        form=EditGymFeesForm(request.POST)
        if form.is_valid():
            trainer=form.cleaned_data["trainer"]
            customer=form.cleaned_data["customer"]
            session_start_date=form.cleaned_data["session_start_date"]
            amount=form.cleaned_data["amount"]
            session_end_date=form.cleaned_data["session_end_date"]

            try:
                customerdue=CustomerDue.objects.get(id=customerdue_id)
                trainer_id=Trainer.objects.get(id=trainer)
                customer_id=Customer.objects.get(id=customer)
                customerdue.trainer_id=trainer_id
                customerdue.customer_id=customer_id
                customerdue.session_start_date=session_start_date
                customerdue.amount=amount
                customerdue.session_end_date=session_end_date
                customerdue.save()
                del request.session['customerdue_id']
                messages.success(request,"Successfully Edited Gym Fees")
                return HttpResponseRedirect(reverse("edit_gymfees",kwargs={"customerdue_id":customerdue_id}))
            except:
                messages.error(request,"Failed to Edit Gym Fees")
                return HttpResponseRedirect(reverse("edit_gymfees",kwargs={"customerdue_id":customerdue_id}))
            

def delete_gymfees(request, customerdue_id):
    try:
        customerdue = get_object_or_404(CustomerDue, id=customerdue_id)
        customerdue.delete()
        messages.success(request, "Gym Fees successfully deleted.")
    except Exception as e:
        messages.error(request, f"Failed to delete Gym Fees: {e}")

    return redirect('/manage_gymfees')

def send_gymfees(request, customerdue_id):
    try:
        customerdue = CustomerDue.objects.get(id=customerdue_id)

        customer_email = customerdue.customer_id.admin.email
        
        subject = quote("Reminder for Payment in Evengreen Gym Fitness")
        body = quote(f"Dear {customerdue.customer_id.admin.first_name} {customerdue.customer_id.admin.last_name},\n\nThis mail is a gentle reminder for your pending payment in Evergreen Gym Fitness. The final due date for your payment was {customerdue.session_end_date}. Kindly make the payment as soon as possible.\n\nBest regards,\nEvergreen Gym Fitness")

        context = {
            "emails_string": customer_email,
            "subject": subject,
            "body": body,
            "name": customer_email,
        }  
        return render(request, "hod_template/send_email_template.html", context)
    except CustomerDue.DoesNotExist:
        messages.error(request, "Failed to find the Customer Due.")
        return redirect("/manage_customerdue")
    except Exception as e:
        print(str(e))
        messages.error(request, "Failed to send email.")
        return redirect("/manage_customerdue")


def add_event(request):
    form=AddEventForm()
    return render(request, "hod_template/add_event_template.html", {"form": form})

def save_add_event(request):
    if request.method!= "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddEventForm(request.POST)
        if form.is_valid():
            eventname = form.cleaned_data["eventname"]
            eventdate = form.cleaned_data["eventdate"]
            eventdesc = form.cleaned_data["eventdesc"]
            amount = form.cleaned_data["amount"]
            try:
                Event.objects.create(event_name=eventname, event_date=eventdate, event_description=eventdesc, amount=amount,)
                messages.success(request, "Successfully Added Event")
                return HttpResponseRedirect("/add_event")
            
            except:
                messages.error(request, "Failed to Add Event")
                return HttpResponseRedirect("/add_event")
        else:
            messages.error(request,"Invalid Form Data")
            return HttpResponseRedirect("/add_event")
        
def manage_event(request):
    event=Event.objects.all()
    return render(request,"hod_template/manage_event_template.html",{"event":event})
        
def edit_event(request, event_id):
    request.session['event_id']= event_id
    event=Event.objects.get(id=event_id)
    form=EditEventForm()
    form.fields['eventname'].initial = event.event_name
    form.fields['eventdesc'].initial = event.event_description
    form.fields['eventdate'].initial = event.event_date
    form.fields['amount'].initial = event.amount

    return render(request, "hod_template/edit_event_template.html", {"form": form, "id": event_id, "name": event.event_name})


def save_edit_event(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        event_id=request.session.get("event_id")
        if event_id==None:
            return HttpResponseRedirect("/manage_event")
        
        form=EditEventForm(request.POST)
        if form.is_valid():
            eventname = form.cleaned_data["eventname"]
            eventdate = form.cleaned_data["eventdate"]
            eventdesc = form.cleaned_data["eventdesc"]
            amount = form.cleaned_data["amount"]

            try:
                event=Event.objects.get(id=event_id)
                event.event_name=eventname
                event.event_description=eventdesc
                event.event_date=eventdate
                event.amount=amount
                event.save()

                del request.session['event_id']
                messages.success(request,"Successfully Edited Event")
                return HttpResponseRedirect(reverse("edit_event",kwargs={"event_id":event_id}))
            except:
                messages.error(request,"Failed to Edit Event")
                return HttpResponseRedirect(reverse("edit_event",kwargs={"event_id":event_id}))
        else:
            form=EditEventForm(request.POST)
            event=Event.objects.get(id=event_id)
            return render(request,"hod_template/edit_event_template.html",{"form":form,"id":event_id,"name":event.event_name})


def delete_event(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.success(request, "Event successfully deleted.")
    except Exception as e:
        messages.error(request, f"Failed to delete Event: {e}")

    return redirect('/manage_event')

def send_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        customers = Customer.objects.all()
        trainers = Trainer.objects.all()

        customer_emails = [customer.admin.email for customer in customers]
        trainer_emails = [trainer.admin.email for trainer in trainers]
        
        all_emails = customer_emails + trainer_emails
        emails_string = ",".join(all_emails)  

        subject = quote(event.event_name)
        body = quote(f"Dear All,\n\nWe are excited to inform you about the upcoming event: {event.event_name} on {event.event_date}.\n\nBest regards,\nEvergreen Gym Fitness")

        context = {
            "emails_string": emails_string,
            "subject": subject,
            "body": body,
            "name": "everyone", 
        }

        return render(request, "hod_template/send_email_template.html", context)
    except Event.DoesNotExist:
        messages.error(request, "Failed to find the event.")
        return redirect("/manage_event")
    except Exception as e:
        print(str(e))
        messages.error(request, "Failed to send email.")
        return redirect("/manage_event")

def add_participation(request):
    form = AddParticipationForm()
    events = Event.objects.all()
    event_data = [{"id": event.id, "amount": event.amount} for event in events]
    
    return render(request, "hod_template/add_participation_template.html", {
        "form": form,
        "event_data": event_data,
    })

def save_add_participation(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddParticipationForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data["event"]
            participators = form.cleaned_data["participator"]
            amount = request.POST.get("amount")
            print(amount)

            try:
                event_id = Event.objects.get(id=event)
                
                for participator in participators:
                    if participator.startswith("trainer_"):
                        _, first_name, last_name = participator.split("_")
                        # Fetch trainer
                        trainer_instance = Trainer.objects.get(
                            admin__first_name=first_name,
                            admin__last_name=last_name
                        )
                        EventParticipation.objects.create(
                            event_id=event_id,
                            participator=trainer_instance.admin.first_name+" "+trainer_instance.admin.last_name,  
                            amount=amount
                        )
                    elif participator.startswith("customer_"):
                        _, first_name, last_name = participator.split("_")
                        customer_instance = Customer.objects.get(
                            admin__first_name=first_name,
                            admin__last_name=last_name
                        )
                        EventParticipation.objects.create(
                            event_id=event_id,
                            participator=customer_instance.admin.first_name+" "+customer_instance.admin.last_name, 
                            amount=amount
                        )

                messages.success(request, "Successfully Added Participation")
                return HttpResponseRedirect("/add_participation")
            except Exception as e:
                print(e)  
                messages.error(request, "Failed to Add Participation")
                return HttpResponseRedirect("/add_participation")
        else:
            messages.error(request, "Invalid Form Data")
            return HttpResponseRedirect("/add_participation")

        

def manage_participation(request):
    eventparticipation = EventParticipation.objects.all()
    return render(request, "hod_template/manage_participation_template.html",{'eventparticipation':eventparticipation})


def delete_eventparticipators(request, event_id):
    try:
        EventParticipation.objects.filter(event_id=event_id).delete()
        messages.success(request, f"All participators for Event have been successfully deleted.")
    except EventParticipation.DoesNotExist:
        messages.error(request, f"No participators found for this Event.")
    return redirect("/manage_participation")  


def save_add_message(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        description = request.POST.get("description")
        end_date = request.POST.get("end_date")

        try:
            # Check if any message already exists
            message = Messages.objects.first()

            if message:
                # Update the existing message
                message.description = description
                message.end_date = end_date
                message.save()
                messages.success(request, "Successfully Updated Message")
            else:
                # Create a new message if none exists
                Messages.objects.create(
                    description=description,
                    end_date=end_date
                )
                messages.success(request, "Successfully Added Message")

            return HttpResponseRedirect("/message")

        except Exception as e:
            # Handle any errors
            print(e)  # For debugging
            messages.error(request, "Failed to Add or Update Message")
            return HttpResponseRedirect("/message")

         