import json
from allianceauth.services.hooks import get_extension_logger
import re
from hashlib import md5

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from graphqlclient import GraphQLClient

from allianceauth.services.hooks import NameFormatter

from .models import WikiJs
from .queries import (
    _activate_user_mutation,
    _create_group_mutation,
    _create_user_mutation,
    _deactivate_user_mutation,
    _find_user_query,
    _get_group_list_query,
    _update_user_mutation,
    _user_password_mutation,
    _user_single_query,
)

logger = get_extension_logger(__name__)

GROUP_CACHE_MAX_AGE = getattr(settings, 'WIKIJS_GROUP_CACHE_MAX_AGE', 2 * 60 * 60)  # default 2 hours

class WikiJSManager:
    _client = None
    def __init__(self):
        try:
            self.client
        except Exception as e:
            print(e)

    @property
    def client(self):
        if not self._client:
            self._client = GraphQLClient("{}/graphql".format(settings.WIKIJS_URL))
            self._client.inject_token("Bearer {}".format(settings.WIKIJS_API_KEY))
        return self._client

    ### Groups! ****************************************************************************************************

    def _get_groups(self):
        data = json.loads(self.client.execute(_get_group_list_query)).get("data",{}).get("groups",{}).get("list",[])
        return data

    def _create_group(self, name):
        data = json.loads(self.client.execute(_create_group_mutation, variables={"group_name":name}))
        try:
            if not data["data"]["groups"]["create"]["responseResult"]['succeeded']:
                logger.error("WikiJs unable to create group. {}".format(data["data"]["groups"]["create"]["responseResult"]["message"]))
                return None
        except:
            logger.error("API returned invalid response when creating group {}".format(data), exc_info=1)
        return data.get("data",{}).get("groups").get("create").get("group")


    def __group_name_to_id(self, name):
        name = WikiJSManager._sanitize_groupname(name)

        def get_or_create_group():
            groups = self._get_groups()
            if groups is not None:
                for g in groups:
                    if g['name'].lower() == name.lower():
                        return g['id']
            return self._create_group(name)['id']

        return cache.get_or_set(WikiJSManager._generate_cache_group_name_key(name), get_or_create_group,
                                GROUP_CACHE_MAX_AGE)

    def __group_id_to_name(self, g_id):
        def get_group_name():
            groups = self._get_groups()
            for g in groups:
                if g['id'] == g_id:
                    return g['name']
            raise KeyError("Group ID %s not found on Wiki.JS" % g_id)

        return cache.get_or_set(WikiJSManager._generate_cache_group_id_key(g_id), get_group_name,
                                GROUP_CACHE_MAX_AGE)
    
    def __generate_group_list(self, names):
        group_list = []
        for name in names:
            group_list.append(self.__group_name_to_id(name))
        return group_list
    
    ### Users *****************************************************************************************************
    def __find_user(self, email):
        data = json.loads(self.client.execute(_find_user_query, variables={"char_email":email}))
        users = data.get("data",{}).get("users",{}).get("search",[])
        if users is None:
            return False
        for user in users:
            if user.get("email", "").lower() == email.lower():
                return user.get("id")
        return False

    def __create_user(self, user, password=False):
        from .auth_hooks import WikiJSService

        name = NameFormatter(WikiJSService(), user).format_name()

        if not password:
            password = get_random_string(15)

        groups = [WikiJSManager._sanitize_groupname(user.profile.state.name)]
        for g in user.groups.all():
            groups.append(WikiJSManager._sanitize_groupname(str(g)))
        
        group_list = self.__generate_group_list(groups)
        data = json.loads(self.client.execute(_create_user_mutation, 
                            variables={
                                "group_list":group_list,
                                "email":user.email,
                                "name":name,
                                "pass":password}))
        if data["data"]["users"]["create"]["responseResult"]["succeeded"]:
            uid = self.__find_user(user.email)
            if uid:
                WikiJs.objects.update_or_create(user=user, uid=uid)
                return True
        else:
            logger.error("WikiJs unable to Create User. {}".format(data["data"]["users"]["create"]["responseResult"]["message"]))
        return False

    def __deactivate_user(self, uid):
        data = json.loads(self.client.execute(_deactivate_user_mutation, variables={"uid":uid}))
        result = data["data"]["users"]["deactivate"]["responseResult"]["succeeded"]
        if not result:
            logger.error("WikiJs unable to deactivate User. {}".format(data["data"]["users"]["deactivate"]["responseResult"]["message"]))
        else:
            WikiJs.objects.filter(uid=uid).delete()
        return result

    def __activate_user(self, uid):
        data = json.loads(self.client.execute(_activate_user_mutation, variables={"uid":uid}))
        result = data["data"]["users"]["activate"]["responseResult"]["succeeded"]
        if not result:
            logger.error("WikiJs unable to activate User. {}".format(data["data"]["users"]["activate"]["responseResult"]["message"]))
        return result

    def _update_password(self, uid, password):
        data = json.loads(self.client.execute(_user_password_mutation, 
                            variables={
                                "uid":uid,
                                "password":password
                                }))
        result = data["data"]["users"]["update"]["responseResult"]["succeeded"]
        if not result:
            logger.error("WikiJs unable to update password for User. {}".format(data["data"]["users"]["update"]["responseResult"]["message"]))
        return result

    def _update_user(self, user):
        from .auth_hooks import WikiJSService

        groups = [WikiJSManager._sanitize_groupname(user.profile.state.name)]
        for g in user.groups.all():
            groups.append(WikiJSManager._sanitize_groupname(str(g)))
        group_list = self.__generate_group_list(groups)
        name = NameFormatter(WikiJSService(), user).format_name()

        data = json.loads(self.client.execute(_update_user_mutation, 
                            variables={
                                "uid":user.wikijs.uid,
                                "name":name,
                                "group_list":group_list
                                }))
        result = data["data"]["users"]["update"]["responseResult"]["succeeded"]
        if not result:
            logger.error("WikiJs unable to update User. {}".format(data["data"]["users"]["update"]["responseResult"]["message"]))
        return result


    #Statics ******************************************************************************************************
    @staticmethod
    def _generate_cache_group_name_key(name):
        return 'WIKIJS_GROUP_NAME__%s' % md5(name.encode('utf-8')).hexdigest()

    @staticmethod
    def _generate_cache_group_id_key(g_id):
        return 'WIKIJS_GROUP_ID__%s' % g_id

    @staticmethod
    def _sanitize_name(name):
        name = name.replace(' ', '_')
        name = name.replace("'", '')
        name = name.lstrip(' _')
        name = name[:20]
        name = name.rstrip(' _')
        return name

    @staticmethod
    def _sanitize_groupname(name):
        name = re.sub('[^\w]', '', name)
        name = WikiJSManager._sanitize_name(name)
        if len(name) < 3:
            name = "Group " + name
        return name

    @staticmethod
    def user_has_account(user):
        try:
            user.wikijs
        except ObjectDoesNotExist:
            return False
        else:
            return True

    ### Methods **************************************************************************************************
    def update_user(self, user):
        return self._update_user(user)


    def activate_user(self, user):
        #search
        try:
            uid = self.__find_user(user.email)
            #create
            if not uid:
                logger.info("Creating new user for {}".format(user.username))
                uid = self.__create_user(user)
            else:
                logger.info("reactivating disabled account for {}".format(user.username))
                self.__activate_user(uid)
                WikiJs.objects.update_or_create(user=user, uid=uid)
                self.update_user(user)

            #password
            password = get_random_string(15)
            self._update_password(uid, password)

            #return
            return password
        except Exception as e:
            logger.error(e,exc_info=1)
            return False

    def deactivate_user(self, user):

        try:
            result = self.__deactivate_user(user.wikijs.uid)
        except AttributeError: #no wikijs model
            return True

        if result:
            try:
                user.wikijs.delete()
            except:
                pass
        return result 
