from allianceauth.services.hooks import get_extension_logger

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .manager import WikiJSManager
from allianceauth.services.forms import ServicePasswordForm
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

logger = get_extension_logger(__name__)

ACCESS_PERM = 'wikijs.access_wikijs'

@login_required
@permission_required(ACCESS_PERM)
def deactivate_wikijs(request):
    result = WikiJSManager().deactivate_user(request.user)
    if result:
        logger.info("Deactivated Wiki.JS %s" % request.user)
        messages.success(request, _('Deactivated Wiki.JS'))
    else:
        logger.error("Failed to deactivate Wiki.JS for user %s" % request.user)
        messages.error(request, _('An error occurred while processing your Wiki.JS account.'))

    return redirect("services:services")


@login_required
@permission_required(ACCESS_PERM)
def activate_wikijs(request):
    
    credentials = WikiJSManager().activate_user(request.user)

    if credentials:
        logger.info("Activated Wiki.JS %s" % request.user)
        messages.success(request, _('Activated Wiki.JS'))
    else:
        logger.error("Failed to Activate Wiki.JS for user %s" % request.user)
        messages.error(request, _('An error occurred while processing your Wiki.JS account.'))
        return redirect("services:services")

    return render(request, 'services/service_credentials.html',
                context={'credentials': {"password":credentials}, 'service': 'Wiki.JS'})

@login_required
@permission_required(ACCESS_PERM)
def set_password(request):
    logger.debug("set_wikijs_password called by user %s" % request.user)
    if request.method == 'POST':
        logger.debug("Received POST request with form.")
        form = ServicePasswordForm(request.POST)
        logger.debug("Form is valid: %s" % form.is_valid())
        character = request.user.profile.main_character
        if form.is_valid() and WikiJSManager.user_has_account(request.user) and character is not None:
            password = form.cleaned_data['password']
            logger.debug("Form contains password of length %s" % len(password))
            try:
                result = WikiJSManager()._update_password(request.user.wikijs.uid, password)
                if result:
                    logger.info("Successfully set Wiki.JS password for user %s" % request.user)
                    messages.success(request, _('Set Wiki.JS password.'))
                else:
                    logger.error("Failed to install custom Wiki.JS password for user %s" % request.user)
                    messages.error(request, _('An error occurred while processing your Wiki.JS account.'))
                    return redirect("services:services")
            except Exception as e:
                logger.error("Failed to install custom Wiki.JS password for user %s" % request.user, exc_info=1)
                messages.error(request, _('An error occurred while processing your Wiki.JS account.'))
            return redirect("services:services")

    else:
        logger.debug("Request is not type POST - providing empty form.")
        form = ServicePasswordForm()

    logger.debug("Rendering form for user %s" % request.user)
    context = {'form': form, 'service': 'Wiki.JS'}
    return render(request, 'services/service_password.html', context=context)


@login_required
@permission_required(ACCESS_PERM)
def reset_password(request):
    password = get_random_string(15)
    result = WikiJSManager()._update_password(request.user.wikijs.uid, password)
    if result:
        logger.info("Successfully set Wiki.JS password for user %s" % request.user)
        messages.success(request, _('Set Wiki.JS password.'))
    else:
        logger.error("Failed to install custom Wiki.JS password for user %s" % request.user)
        messages.error(request, _('An error occurred while processing your Wiki.JS account.'))
        return redirect("services:services")

    return render(request, 'services/service_credentials.html',
                context={'credentials': {"password":password}, 'service': 'Wiki.JS'})

