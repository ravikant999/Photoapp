from django.contrib.auth import get_user_model

User = get_user_model()

user, created = User.objects.get_or_create(username='admin', defaults={
    'email': 'admin@example.com'
})
if created:
    user.set_password('adminpass123')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Superuser created.")
else:
    user.set_password('adminpass123')  # reset password
    user.save()
    print("Superuser password reset.")

