from django.db.models.signals import post_delete
from django.dispatch import receiver
# from .tasks import delete_file


@receiver(post_delete, sender= 'bank.BankStatementFile')
def delete_file(sender, instance, **kwargs):
    """
    Delete file from storage
    """
    if instance.file:
        instance.file.delete(save=False)
