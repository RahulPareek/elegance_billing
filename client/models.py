from django.db import models


class Client(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200)
    mobile_no = models.CharField(max_length=10, null = True, blank = True)
    email_id = models.EmailField(null = True, blank = True)

    def __str__(self):
        return self.name


