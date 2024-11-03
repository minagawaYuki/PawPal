from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .forms import UpdateProfileForm
from django.db import transaction
import logging
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

@login_required
@never_cache
@require_http_methods(["GET", "POST"])
def user_profile(request):
    users = User.objects.all()
    user = request.user
    
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.username = form.cleaned_data['username']
                    user.email = form.cleaned_data['email']
                    
                    password = form.cleaned_data.get('password')
                    if password:
                        user.set_password(password)
                    
                    user.save()

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Profile updated successfully',
                        'data': {
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'username': user.username,
                            'email': user.email
                        }
                    })
                return render(request, 'userprofile/user_profile.html', {
                    'users': users,
                    'form': form,
                    'user': user,
                    'success': True,
                    'message': 'Profile updated successfully'
                })
            except Exception as e:
                logger.error(f"Error updating profile for user {user.id}: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'An unexpected error occurred. Please try again.',
                        'message': 'Profile update failed.'
                    }, status=500)
                return render(request, 'userprofile/user_profile.html', {
                    'users': users,
                    'form': form,
                    'user': user,
                    'error': 'An unexpected error occurred. Please try again.',
                    'message': 'Profile update failed.'
                })
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid form data',
                    'form_errors': form.errors
                }, status=400)
            return render(request, 'userprofile/user_profile.html', {
                'users': users,
                'form': form,
                'user': user,
                'error': 'Invalid form data'
            })
    else:
        form = UpdateProfileForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email
        })
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Form data retrieved successfully',
                'data': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'email': user.email
                }
            })
        
    return render(request, 'userprofile/user_profile.html', {
        'users': users,
        'form': form,
        'user': user
    })