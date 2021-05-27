"""Here you can define Models"""
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save the new User
        :parameter email: email address of the user
        :type email: str
        :parameter password: password of the user
        :type password: str
        :parameter extra_fields: extra fields of user model
        :type extra_fields: dict
        """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create super user
        :parameter email: email address of the user
        :type email: str
        :parameter password: password of the user
        :type password: str
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model to save user information
    :parameter id: Auto increment id with primary key
    :type id: int
    :parameter first_name: first name of the user
    :type first_name: str
    :parameter last_name: last_name of the user
    :type last_name: str
    :parameter email: email address of user
    :type email: str
    :parameter ip_address: ip address of the user
    :type ip_address: str
    :parameter created_at: entry created date time
    :type created: django.utils.timezone
    """
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(unique=True, default=None)
    created_at = models.DateTimeField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        return super(User, self).save(*args, **kwargs)


class Document(models.Model):
    """
    Document model to save user information of Pdf Data.
    :parameter id: Auto increment id with primary key
    :type id: int
    :parameter file_id: uuid4 for unique public key
    :type file_id: str
    :parameter document_uploaded: Save Uploaded document file
    :type document_uploaded: FileObject
    :parameter uploaded_at: Date and time of upload
    :type uploaded_at: DateTime
    :parameter document_analyzed: Save analyzed File
    :type document_analyzed: FileObject
    :parameter name: File Name
    :type name: str
    """
    id = models.AutoField(primary_key=True)
    file_id = models.UUIDField(default=uuid.uuid4, editable=False)
    document_uploaded = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    document_analyzed = models.FileField(upload_to='document_analyzed/')
    name = models.CharField(default="unknown", max_length=200)

    def __str__(self):
        return self.document_analyzed.name

    def save_uploaded_doc(self, document_uploaded, document_analyzed=None, *args, **kwargs):
        """
        Save Uploaded Documents
        :param document_uploaded: File of Uploaded Document
        :type document_uploaded: FileObject
        :param document_analyzed: File Analyzed
        :type document_analyzed: FileObject
        """
        self.uploaded_at = timezone.now()
        self.document_uploaded = document_uploaded
        # Save analyzed object if it is in argument
        if document_analyzed is not None:
            self.document_analyzed = document_analyzed
        else:
            self.name = self.document_uploaded.name
        return super(Document, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """
        Delete Saved File Object
        """
        try:
            self.document_analyzed.delete()
        except:
            pass
        self.document_uploaded.delete()
        return super(Document, self).delete()
