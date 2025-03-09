# from django.shortcuts import redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import user_passes_test

# def group_required(*group_names):
#     """Requires user membership in at least one of the groups passed in."""
#     def in_groups(u):
#         if u.is_authenticated:
#             if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
#                 return True
#         return False

#     return user_passes_test(in_groups, login_url='login')

# def group_required_with_message(*group_names, message="No tienes permiso para acceder a esta página."):
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#             if request.user.is_authenticated:
#                 if bool(request.user.groups.filter(name__in=group_names)) | request.user.is_superuser:
#                     return view_func(request, *args, **kwargs)
#             messages.error(request, message)
#             return redirect('home')  # Redirige a la página de inicio o a donde desees
#         return wrapper
#     return decorator