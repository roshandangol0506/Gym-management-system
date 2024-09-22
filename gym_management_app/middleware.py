from django.shortcuts import redirect
from django.urls import reverse

class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths based on user_type
        admin_paths = ['/admin_home', '/save_add_trainer', '/add_trainer', '/manage_trainer', '/edit_trainer/<str:trainer_id>', '/save_edit_trainer', '/delete_trainer<str:trainer_id>', '/save_add_customer', '/add_customer', '/manage_customer', '/edit_customer<str:customer_id>', '/save_edit_customer', '/delete_customer/<str:customer_id>' '/save_add_gymfees', '/add_gymfees', '/manage_gymfees', '/edit_gymfees/<str:customerdue_id>', '/save_edit_gymfees', '/delete_gymfees/<str:customerdue_id>']  # Add other admin-specific URLs
        trainer_paths = ['/trainer_home', ...]  # Add other trainer-specific URLs
        customer_paths = ['/customer_home', ...]  # Add other customer-specific URLs

        # Allow access to login page without checking user_type
        excluded_paths = [reverse('ShowLoginPage'), reverse('do_login')]

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Restrict access to admin pages
            if request.user.user_type == '1' and request.path not in admin_paths + excluded_paths:
                return redirect(reverse('ShowLoginPage'))
            # Restrict access to trainer pages
            elif request.user.user_type == '2' and request.path not in trainer_paths + excluded_paths:
                return redirect(reverse('ShowLoginPage'))
            # Restrict access to customer pages
            elif request.user.user_type == '3' and request.path not in customer_paths + excluded_paths:
                return redirect(reverse('ShowLoginPage'))
        else:
            # If user is not authenticated and tries to access a protected page, redirect to login
            if request.path not in excluded_paths:
                return redirect(reverse('ShowLoginPage'))

        # Proceed with the request
        return self.get_response(request)