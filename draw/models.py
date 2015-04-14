from django.db import models

# Create your models here.

class student(models.Model):

    stuName = models.CharField(max_length=8, null=True)
    IDCard = models.CharField(max_length=18,primary_key=True)
    stuNum = models.IntegerField(max_length=2,null=True)
    ifDraw = models.BooleanField(max_length=1)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.stuName, self.IDCard, self.stuNum, self.ifDraw)

    class Meta:
        ordering = ['stuNum','stuName']

class numList(models.Model):
    stuNumber = models.IntegerField(max_length=2,null=False)

    def __unicode__(self):
        return self.stuNumber

class adminUser(models.Model):
    adminName = models.CharField(max_length=50, null=False)
    adminPWD = models.CharField(max_length=16, null=False)

    def __unicode__(self):
        return self.adminName