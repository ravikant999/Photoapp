from django.db import models
from django.contrib.auth.models import User


import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"

class Like(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('upload', 'user')  # prevents duplicate likes by same user

    def __str__(self):
        return f"{self.user.username} liked {self.upload.id}"

class Comment(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.upload.id}: {self.text[:20]}"
    





# Delete image file from disk when Upload is deleted
@receiver(post_delete, sender=Upload)
def delete_upload_image_file(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

# Delete old image file when it's replaced during edit
@receiver(pre_save, sender=Upload)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, nothing to delete

    try:
        old_image = Upload.objects.get(pk=instance.pk).image
    except Upload.DoesNotExist:
        return

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)

