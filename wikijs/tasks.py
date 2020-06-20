import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from allianceauth.notifications import notify
from celery import shared_task
from allianceauth.services.tasks import QueueOnce
import requests

from .manager import WikiJSManager
from .models import WikiJs

logger = logging.getLogger(__name__)

class WikiJSTasks:
    @staticmethod
    @shared_task(bind=True, name='wikijs.update_member', base=QueueOnce)
    def update_member(self, user_id):
        u = User.objects.get(id=user_id)
        try:
            u.wikijs
        except ObjectDoesNotExist:
            return "User has no Wiki.JS account"
        else:
            return f"Updated Wiki.JS for {u.username}, Result:{WikiJSManager().update_user(u)}"
    
    @staticmethod
    @shared_task(bind=True, name='wikijs.update_all_members', base=QueueOnce)
    def update_all_members(self):
        for u in WikiJs.objects.all():
            WikiJSTasks.update_member.delay(u.pk)
