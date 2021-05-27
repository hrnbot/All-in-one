""" This File will take care of Authentication """
from django.contrib.auth.models import User

class AuthBackend(object):
    """ Authenticate using an email address """

    def authenticate(self, username=None, password=None):
        """
        Authenticate UserName and Password
        :param username: username
        :type username: str
        :param password: SHA256
        :type password: str
        :return: User Model
        :rtype: object
        """
        kwargs = {"email": username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

