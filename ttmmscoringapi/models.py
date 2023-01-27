from django.db import models
# Create your models here.
#creating model for ttmm

def upload_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "acco-%s-%s-.%s" % (instance.name, instance.id, ext)
    return '/'.join(['esummit23/', filename])


def upload_ppt(instance, filename):
    ext = filename.split('.')[-1]
    filename = "acco-%s-%s-.%s" % (instance.name, instance.id, ext)
    return '/'.join(['esummit23/', filename])


class AdminUser(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=300, blank=True, null=True)
    Totalfunding = models.IntegerField(blank=True, null=True)
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


choices =(
    ('0','beforebidding'),
    ('1','bidding'),
    ('2','afterbidding'),
)


class Startup(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    image2 = models.FileField( upload_to=upload_image, blank=True)
    ppt = models.FileField( upload_to=upload_ppt, blank=True)
    totalbid = models.IntegerField(blank=True, null=True)
    bid_overview = models.TextField(blank=True, null=True,max_length=512)
    current = models.BooleanField(blank=True, null=True, default=False)
    isfunded = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name

class PortalControl(models.Model):
    control_name= models.CharField(null=True, blank=True,max_length=30)
    transaction_type = models.CharField(max_length=20, choices=choices, blank=True, null=True)
    current_startup = models.ForeignKey(Startup, on_delete=models.CASCADE , null=True,blank=True)
    # bidding_start = models.BooleanField(default=False)

    def __str__(self):
        return self.control_name

class Funding(models.Model):
    investor_name = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    startup_name = models.ForeignKey(Startup, on_delete=models.CASCADE)
    funding = models.IntegerField(blank=True, null=True)
    finalsubmit = models.BooleanField(blank=True, null=True, default=False)


class Funding2(models.Model):
    investor_name = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    startup_name = models.ForeignKey(Startup, on_delete=models.CASCADE)
    funding = models.IntegerField(blank=True, null=True)
    finalsubmit = models.BooleanField(blank=True, null=True, default=False)

class Question(models.Model):
    question_text = models.CharField(max_length = 200)
 
    def __str__(self):
        return self.question_text
 
 
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
 
    def __str__(self):
        return self.choice_text