from django.db import models

# Create your models here.
class AdminUser(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=300, blank=True, null=True)
    Totalfunding = models.IntegerField(blank=True, null=True)
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name

class Startup(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    totalbid = models.IntegerField(blank=True, null=True)
    current = models.BooleanField(blank=True, null=True)
    done = models.BooleanField(blank=True, null=True, default=False)
    showprogress = models.BooleanField(blank=True, null=True, default=False)
    showinvestor = models.BooleanField(blank=True, null=True, default=False)
    isfunded = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name

class Funding(models.Model):
    investor_name = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    startup_name = models.ForeignKey(Startup, on_delete=models.CASCADE)
    funding = models.IntegerField(blank=True, null=True)
    finalsubmit = models.BooleanField(blank=True, null=True, default=False)

    # def __str__(self):
    #     return self.investor_name