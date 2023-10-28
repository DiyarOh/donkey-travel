from django.http import HttpResponseRedirect
from django.urls import reverse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # If the user is authenticated, prevent them from accessing login and register
            if request.path_info.startswith('/login') or request.path_info.startswith('/register'):
                return HttpResponseRedirect(reverse('index'))  # Redirect to another page

        if not request.user.is_authenticated and not request.path_info.startswith('/admin') and not request.path_info.startswith('/login') and not request.path_info.startswith('/register'):
            return HttpResponseRedirect(reverse('login'))
        
        response = self.get_response(request)
        return response