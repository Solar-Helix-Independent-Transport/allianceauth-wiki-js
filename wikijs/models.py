from django.contrib.auth.models import User
from django.db import models


class WikiJs(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE,
                                related_name='wikijs')

    uid = models.BigIntegerField()

    def __str__(self):
        return "WikiJS User - {}".format(self.user.username)

    class Meta:
        permissions = (
            ("access_wikijs", u"Can access the WikiJS service"),
        )
