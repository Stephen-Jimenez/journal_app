from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
   def registration_validator(self, postData):
        errors = {}
        NAME_REGEX = re.compile(r'[a-zA-Z]')
        if not NAME_REGEX.match(postData['first_name']):
            errors['first_name_re'] = 'First name can only include letters'
        if len(postData['first_name']) == 0:
            errors['first_name'] = 'First name is required'
        if len(postData['first_name']) < 2:
            errors['first_name_len'] = 'First name must include at least 2 characters'
        if not NAME_REGEX.match(postData['last_name']):
            errors['last_name_re'] = 'Last name can only include letters'
        if len(postData['last_name']) == 0:
            errors['last_name'] = 'Last name is required'
        if len(postData['last_name']) < 2:
            errors['last_name_len'] = 'Last name must include at least 2 characters'
        if len(postData['email']) == 0:
            errors['email'] = 'Email address is required'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):        
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['email_unique'] = 'Email is already registered'
        if len(postData['password']) == 0:
            errors['password'] = 'Password is required'
        if len(postData['password']) < 8:
            errors['password_len'] = 'Password must include at least 8 characters'
        if postData['password'] != postData['password_confirm']:
            errors['password_match'] = 'Password and password confirm do not match'
        return errors
   def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email = postData['email'])
        if len(postData['email']) == 0:
            errors['email_check'] = 'Email is required'
        if not existing_user:
            errors['email_reg'] = 'Email is not registered'
            return errors
        if len(postData['password']) == 0:
            errors['password'] = 'Password is required'
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password_check'] = 'Email and password do not match'
        return errors
   def edit_validator(self, postData):
       errors = {}
       NAME_REGEX = re.compile(r'[a-zA-Z]')
       if not NAME_REGEX.match(postData['first_name']):
            errors['first_name_re'] = 'First name can only include letters'
       if len(postData['first_name']) == 0:
            errors['first_name'] = 'First name is required'
       if len(postData['first_name']) < 2:
            errors['first_name_len'] = 'First name must include at least 2 characters'
       if not NAME_REGEX.match(postData['last_name']):
            errors['last_name_re'] = 'Last name can only include letters'
       if len(postData['last_name']) == 0:
            errors['last_name'] = 'Last name is required'
       if len(postData['last_name']) < 2:
            errors['last_name_len'] = 'Last name must include at least 2 characters'
       EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
       if not EMAIL_REGEX.match(postData['email']):        
            errors['email'] = "Invalid email address!"
       if len(postData['email']) == 0:
            errors['email'] = 'Email address is required'
       return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Entry(models.Model):
    entry_text = models.TextField()
    title = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(User, related_name="entries", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)