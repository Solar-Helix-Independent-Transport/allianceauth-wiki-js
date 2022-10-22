import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from allianceauth import hooks
from allianceauth.services.hooks import ServicesHook

from wikijs.app_settings import WIKIJS_AADISCORDBOT_INTEGRATION

from .manager import WikiJSManager
from .models import WikiJs
from .tasks import WikiJSTasks
from .urls import urlpatterns

logger = logging.getLogger(__name__)


class WikiJSService(ServicesHook):
    def __init__(self):
        ServicesHook.__init__(self)
        self.urlpatterns = urlpatterns
        self.name = 'Wiki JS'
        self.service_url = settings.WIKIJS_URL
        self.access_perm = 'wikijs.access_wikijs'
        self.name_format = '{character_name}'

    @property
    def title(self):
        return self.name

    def delete_user(self, user):
        logger.debug(f'Deleting user {user} {self.name} account')
        return WikiJSManager().deactivate_user(user)

    def validate_user(self, user):
        logger.debug(f'Validating user {user} {self.name} account')
        if self.user_has_account(user) and not self.service_active_for_user(user):
            WikiJSManager().deactivate_user(user)

    def update_groups(self, user):
        logger.debug(f'Updating {self.name} groups for {user}')
        if self.user_has_account(user):
            return WikiJSTasks.update_member.delay(user.pk)
        return False

    def update_all_groups(self):
        logger.debug('Update all %s groups called' % self.name)
        for u in WikiJs.objects.all():
            self.validate_user(u.user)
            WikiJSTasks.update_member.delay(u.user_id)

    def service_active_for_user(self, user):
        return user.has_perm(self.access_perm)

    def render_services_ctrl(self, request):
        urls = self.Urls()
        urls.auth_activate = 'wikijs:activate'
        urls.auth_deactivate = 'wikijs:deactivate'
        urls.auth_reset_password = 'wikijs:reset_password'
        urls.auth_set_password = 'wikijs:set_password'
        return render_to_string(self.service_ctrl_template, {
            'service_name': self.title,
            'urls': urls,
            'service_url': self.service_url,
            'username': request.user.email if self.user_has_account(request.user) else ''
        }, request=request)

    def user_has_account(self, user):
        try:
            user.wikijs
        except ObjectDoesNotExist:
            return False
        else:
            return True


@hooks.register('services_hook')
def register_service():
    return WikiJSService()


@hooks.register('discord_cogs_hook')
def register_cogs():
    if WIKIJS_AADISCORDBOT_INTEGRATION is True:
        return ["wikijs.cogs.wikijs"]
    else:
        return [""]
