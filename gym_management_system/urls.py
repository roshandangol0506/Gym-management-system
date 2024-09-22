from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from gym_management_app import views, HodViews, TrainerViews, CustomerViews

from gym_management_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', views.showDemoPage),
    path('', views.ShowLoginPage, name="ShowLoginPage"),

    path('logout_user', views.Logout_user,name="logout"),
    path('doLogin', views.do_Login, name="do_login"),

    path("admin_home", HodViews.admin_home, name="admin_home"),
    path("trainer_home", TrainerViews.trainer_home, name="trainer_home"),
    path("trainer_detail", TrainerViews.trainer_detail, name="trainer_detail"),

    path("customer_home", CustomerViews.customer_home, name="customer_home"),
    path("customer_detail", CustomerViews.customer_detail, name="customer_detail"),
    path("save_add_customerleave", CustomerViews.save_add_customerleave, name="save_add_customerleave"),
    path("customer_leave", TrainerViews.customer_leave, name="customer_leave"),

    path("add_trainer", HodViews.add_trainer, name="add_trainer"),
    path("save_add_trainer", HodViews.save_add_trainer, name="save_add_trainer"),
    path("manage_trainer", HodViews.manage_trainer, name="manage_trainer"),
    path('edit_trainer/<str:trainer_id>',HodViews.edit_trainer,name="edit_trainer"),
    path("save_edit_trainer", HodViews.save_edit_trainer, name="save_edit_trainer"),

    path('delete_trainer/<str:trainer_id>',HodViews.delete_trainer,name="delete_trainer"),

    path("add_customer", HodViews.add_customer, name="add_customer"),
    path("save_add_customer", HodViews.save_add_customer, name="save_add_customer"),
    path("manage_customer", HodViews.manage_customer, name="manage_customer"),
    path("edit_customer/<str:customer_id>", HodViews.edit_customer, name="edit_customer"),
    path("save_edit_customer", HodViews.save_edit_customer, name="save_edit_customer"),

    path("delete_customer/<str:customer_id>", HodViews.delete_customer, name="delete_customer"),

    path("add_gymfees", HodViews.add_gymfees, name="add_gymfees"),
    path("save_add_gymfees", HodViews.save_add_gymfees, name="save_add_gymfees"),
    path("manage_gymfees", HodViews.manage_gymfees, name="manage_gymfees"),
    path("edit_gymfees/<str:customerdue_id>", HodViews.edit_gymfees, name="edit_gymfees"),
    path("save_edit_gymfees", HodViews.save_edit_gymfees, name="save_edit_gymfees"),

    path('delete_gymfees/<int:customerdue_id>/', HodViews.delete_gymfees, name='delete_gymfees'),
    path('send_gymfees/<int:customerdue_id>/', HodViews.send_gymfees, name='send_gymfees_email'),

    path("add_event", HodViews.add_event, name="add_event"),
    path("save_add_event", HodViews.save_add_event, name="save_add_event"),
    path("manage_event", HodViews.manage_event, name="manage_event"),
    path("edit_event/<str:event_id>", HodViews.edit_event, name="edit_event"),
    path("save_edit_event", HodViews.save_edit_event, name="save_edit_event"),

    path('delete_event/<int:event_id>/', HodViews.delete_event, name='delete_event'),
    path('send_event/<int:event_id>/', HodViews.send_event, name='send_event_email'),

    path("add_participation", HodViews.add_participation, name="add_participation"),
    path("save_add_participation", HodViews.save_add_participation, name="save_add_participation"),
    path("manage_participation", HodViews.manage_participation, name="manage_participation"),

    path('delete_eventparticipators/<int:event_id>/', HodViews.delete_eventparticipators, name='delete_eventparticipators'),

    path("save_add_message", HodViews.save_add_message, name="save_add_message"),
    path("message", HodViews.admin_home, name="message"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)