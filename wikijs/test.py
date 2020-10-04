from unittest import mock

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from allianceauth.tests.auth_utils import AuthUtils

from .auth_hooks import WikiJSService
from .models import WikiJs

MODULE_PATH = 'wikijs'
DEFAULT_AUTH_GROUP = 'Member'


def add_permissions():
    permission = Permission.objects.get(codename='access_wikijs')
    members = Group.objects.get_or_create(name=DEFAULT_AUTH_GROUP)[0]
    AuthUtils.add_permissions_to_groups([permission], [members])


class WikiJSHooksTestCase(TestCase):
    def setUp(self):
        self.member = 'member_user'
        member = AuthUtils.create_member(self.member)
        WikiJs.objects.create(user=member, uid=3)
        self.none_user = 'none_user'
        none_user = AuthUtils.create_user(self.none_user)
        self.service = WikiJSService
        self.del_user = 'del_user'
        del_user = AuthUtils.create_user(self.del_user)
        add_permissions()

    def test_has_account(self):
        service = self.service()
        member = User.objects.get(username=self.member)
        none_user = User.objects.get(username=self.none_user)
        self.assertTrue(service.user_has_account(member))
        self.assertFalse(service.user_has_account(none_user))

    def test_service_enabled(self):
        service = self.service()
        member = User.objects.get(username=self.member)
        none_user = User.objects.get(username=self.none_user)

        self.assertTrue(service.service_active_for_user(member))
        self.assertFalse(service.service_active_for_user(none_user))

    def test_delete_user_with_no_wiki(self):  #this deosnt fail properly on sqlite investigate more tests on mysql/psql
        none_user = User.objects.get(username=self.del_user).delete()

    @mock.patch(MODULE_PATH + '.manager.WikiJSManager._update_user')
    def test_update_user(self, disable):
        disable.execute.return_value = True
        service = self.service()
        # Test member is not deleted
        member = User.objects.get(username=self.member)
        self.assertTrue(service.update_groups(member))
        self.assertTrue(disable.called)

    @mock.patch(MODULE_PATH + '.manager.WikiJSManager._update_user')
    def test_update_non_user(self, disable):
        disable.execute.return_value = True
        service = self.service()
        # Test member is not deleted
        member = User.objects.get(username=self.none_user)
        self.assertFalse(service.update_groups(member))
        self.assertFalse(disable.called)

    @mock.patch(MODULE_PATH + '.manager.WikiJSManager._update_user')
    def test_update_all_users(self, disable):
        disable.execute.return_value = True
        service = self.service()
        # Test member is not deleted
        service.update_all_groups()
        self.assertEqual(disable.call_count, 1)

    @mock.patch(MODULE_PATH + '.manager.WikiJSManager.client')
    def test_validate_user(self, disable):
        disable.execute.return_value = '{"data": {"users": {"deactivate": {"responseResult": {"succeeded": true}}}}}'
        service = self.service()
        # Test member is not deleted
        member = User.objects.get(username=self.member)
        service.validate_user(member)
        self.assertTrue(member.wikijs)

        # Test none user is deleted
        none_user = User.objects.get(username=self.none_user)
        WikiJs.objects.create(user=none_user, uid=4)
        service.validate_user(none_user)
        with self.assertRaises(ObjectDoesNotExist):
            none_wikijs = User.objects.get(username=self.none_user).wikijs

    @mock.patch(MODULE_PATH + '.manager.WikiJSManager.client')
    def test_delete_user(self, disable):
        disable.execute.return_value = '{"data": {"users": {"deactivate": {"responseResult": {"succeeded": true}}}}}'
        member = User.objects.get(username=self.member)
        service = self.service()
        result = service.delete_user(member)

        self.assertTrue(result)
        with self.assertRaises(ObjectDoesNotExist):
            wikijs_user = User.objects.get(username=self.member).wikijs

    def test_render_services_ctrl(self):
        service = self.service()
        member = User.objects.get(username=self.member)
        request = RequestFactory().get('/services/')
        request.user = member

        response = service.render_services_ctrl(request)
        self.assertTemplateUsed(service.service_ctrl_template)
        self.assertIn('href="%s"' % settings.WIKIJS_URL, response)
