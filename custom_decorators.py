from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from shopRX.core.constant_data.choices import *
from django.shortcuts import render
from rest_framework import status as http_status
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from functools import wraps

class IsPhysicianMixin(AccessMixin):

    login_url           = settings.PHYSICIAN_LOGOUT_REDIRECT_URL
    redirect_field_name = None

    def test_user_type(self, request, *args, **kwargs):
        return request.user.is_physician

    def dispatch(self, request, *args, **kwargs):
        template_403_error = "errors/403.html"
        if not self.test_user_type(request, *args, **kwargs):
            if request.is_ajax():
                return JsonResponse({"error": ""}, status=http_status.HTTP_403_FORBIDDEN)
            context = {"prev_url" : request.META.get('HTTP_REFERER')}
            return render(request, template_403_error, context, status=http_status.HTTP_403_FORBIDDEN)
        return super(IsPhysicianMixin, self).dispatch(request, *args, **kwargs)        

class IsPharmacyMixin(AccessMixin):

    login_url           = settings.PHARMACY_LOGOUT_REDIRECT_URL
    redirect_field_name = None

    def test_user_type(self, request, *args, **kwargs):
        return request.user.is_pharmacy


    def dispatch(self, request, *args, **kwargs):
        template_403_error = "errors/403.html"
        if not self.test_user_type(request, *args, **kwargs):
            if request.is_ajax():
                return JsonResponse({"error": ""}, status=http_status.HTTP_403_FORBIDDEN)
            context = {"prev_url" : request.META.get('HTTP_REFERER')}
            return render(request, template_403_error, context, status=http_status.HTTP_403_FORBIDDEN)
        return super(IsPharmacyMixin, self).dispatch(request, *args, **kwargs)      

class IsAdminMixin(AccessMixin):

    LOGIN_URL           = settings.LOGIN_URL
    redirect_field_name = None

    def test_user_type(self, request, *args, **kwargs):
        return request.user.is_admin_org

    def dispatch(self, request, *args, **kwargs):
        template_403_error = "errors/403.html"
        if not self.test_user_type(request, *args, **kwargs):
            if request.is_ajax():
                return JsonResponse({"error": ""}, status=http_status.HTTP_403_FORBIDDEN)
            context = {"prev_url" : request.META.get('HTTP_REFERER')}
            return render(request, template_403_error, context, status=http_status.HTTP_403_FORBIDDEN)
        return super(IsAdminMixin, self).dispatch(request, *args, **kwargs)      

class PermissionsRequiredMixin(AccessMixin):

    LOGIN_URL           = settings.LOGIN_URL
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        template_403_error = "errors/403.html"
        permissions_required    = self.permissions_required
        test_any_perm           = self.test_any_perm
        if test_any_perm:
            user_has_perm = any(map(lambda perm: request.user.has_perm(perm.value), permissions_required))
        else:
            user_has_perm = all(map(lambda perm: request.user.has_perm(perm.value), permissions_required))
        if not user_has_perm:
            context = {"prev_url" : request.META.get('HTTP_REFERER'), "error": "Permission denied."}
            if request.is_ajax():
                return JsonResponse(context, status=http_status.HTTP_403_FORBIDDEN)
            return render(request, template_403_error, context, status=http_status.HTTP_403_FORBIDDEN)
        return super(PermissionsRequiredMixin, self).dispatch(request, *args, **kwargs)    

def permissions_required(**parms):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            template_403_error  = "errors/403.html"
            permissions         = parms.get("permissions")
            test_any_perm       = parms.get("test_any_perm")
            if test_any_perm:
                user_has_perm = any(map(lambda perm: request.user.has_perm(perm.value), permissions))
            else:
                user_has_perm = all(map(lambda perm: request.user.has_perm(perm.value), permissions))
            if not user_has_perm:
                context = {"prev_url" : request.META.get('HTTP_REFERER'), "error": "Permission denied."}
                if request.is_ajax():
                    return JsonResponse(context, status=http_status.HTTP_403_FORBIDDEN)
                return render(request, template_403_error, context, status=http_status.HTTP_403_FORBIDDEN)
            return function(request, *args, **kwargs)
        return wrapper
    return decorator
