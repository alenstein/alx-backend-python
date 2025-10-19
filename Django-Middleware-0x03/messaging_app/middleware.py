
from datetime import datetime
from django.http import HttpResponseForbidden
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        with open("requests.log", "a") as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour >= 21 or current_hour < 6:
            return HttpResponseForbidden("Access restricted: The chat is only available between 6 AM and 9 PM.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __call__(self, request):
        if request.method == 'POST':
            ip_address = self.get_client_ip(request)
            current_time = time.time()

            if ip_address not in self.request_counts:
                self.request_counts[ip_address] = []

            # Remove timestamps older than 60 seconds
            self.request_counts[ip_address] = [
                t for t in self.request_counts[ip_address] if current_time - t < 60
            ]

            if len(self.request_counts[ip_address]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Please try again later.")

            self.request_counts[ip_address].append(current_time)

        return self.get_response(request)

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Assuming admin-specific actions are under URLs containing 'admin'
        if '/admin/' in request.path:
            is_authorized = False
            if request.user.is_authenticated:
                # Assuming the user model has a 'role' attribute
                if hasattr(request.user, 'role') and request.user.role in ['admin', 'moderator']:
                    is_authorized = True

            if not is_authorized:
                return HttpResponseForbidden("You do not have permission to access this area.")

        return self.get_response(request)
