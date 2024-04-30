from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_placeholder_user(sender, **kwargs):
	User = get_user_model()
	if not User.objects.filter(username='Guest').exists():
		User.objects.create(username='Guest', email='guest@guest.fr')
	if not User.objects.filter(username='IA').exists():
		User.objects.create(username='IA', email='ia@ia.fr', avatar='ForbiddenDeletion/AI_Cat.png')
