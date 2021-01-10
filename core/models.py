from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class WebsiteUser(models.Model):
    user_id = models.CharField(null=True,blank=True,max_length=150,unique=True)
    user_name = models.CharField(null=True,blank=True,max_length=150)
    user_last_name = models.CharField(null=True,blank=True,max_length=150)
    user_address = models.CharField(null=True,blank=True,max_length=1000)
    user_phone = models.CharField(null=True,blank=True,max_length=1000)
    user_birthday  = models.CharField(null=True,blank=True, max_length=50)
    salary = models.CharField(null=True,blank=True, max_length=50)

    user_status = models.CharField(null=True,blank=True,max_length=150,choices=(('G',"Good"),('NG',"Not Good")))

    user_type  = models.CharField(null=True,blank=True, choices=(('A',"ADMIN"),('D',"DOCTOR") ,('P',"PATIENT")),max_length=400)
    user_password = models.CharField(null=True,blank=True,max_length=150)
    
    added = models.DateTimeField(auto_now=True)
    

   
            
    def __str__(self):
        return u'{0}'.format(self.user_id)

class Test(models.Model):
    """Model definition for Test."""
    test_id = models.CharField(null=True,blank=True,max_length=150,unique=True)
    test_number = models.CharField(null=True,blank=True,max_length=150,unique=True)
    patient = models.ForeignKey(WebsiteUser,null=True,blank=True, on_delete=models.CASCADE,related_name="tests")
    test_date = models.DateTimeField(null=True,blank=True)
    test_type  = models.CharField(null=True,blank=True, max_length=50 , choices=(('B',"BLOOD"),('C',"CORONA")))
    added = models.DateTimeField(auto_now=True)


    class Meta:
        """Meta definition for Test."""

        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    def __str__(self):
        """Unicode representation of Test."""
        return u'{0}'.format(self.test_id)


class Drug(models.Model):
    """Model definition for Drug."""

    drug_name  = models.CharField(null=True,blank=True, max_length=50,unique=True)
    added = models.DateTimeField(auto_now=True)


    class Meta:
        """Meta definition for Drug."""

        verbose_name = 'Drug'
        verbose_name_plural = 'Drugs'

    def __str__(self):
        """Unicode representation of Drug."""
        return u'{0}'.format(self.drug_name)

class Order(models.Model):
    """Model definition for Order."""

    order_id = models.CharField(null=True,blank=True, max_length=50,unique=True)
    order_name  = models.CharField(null=True,blank=True, max_length=50)
    order_description  = models.CharField(null=True,blank=True, max_length=5000)
    order_amount  = models.CharField(null=True,blank=True, max_length=50)
    order_quantity  = models.CharField(null=True,blank=True, max_length=50)
    order_price  = models.CharField(null=True,blank=True, max_length=50)

    added = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return u'{0}'.format(self.order_id)


class WorkSchedule(models.Model):
    """Model definition for WorkSchedule."""

    doctor = models.ForeignKey(WebsiteUser,null=True,blank=True, on_delete=models.CASCADE)
    start = models.DateTimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
    end = models.DateTimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
    added = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for WorkSchedule."""

        verbose_name = 'WorkSchedule'
        verbose_name_plural = 'WorkSchedules'

    def __str__(self):
        """Unicode representation of WorkSchedule."""
        return u'{0}'.format(self.doctor.user_id)

class Mail(models.Model):
    """Model definition for Mail."""
    sender = models.ForeignKey(WebsiteUser,null=True,blank=True, on_delete=models.CASCADE)
    reciever = models.ForeignKey(WebsiteUser,null=True,blank=True, on_delete=models.CASCADE,related_name="recieved_mails")
    message = models.CharField(null=True,blank=True, max_length=50000)
    added = models.DateTimeField(auto_now=True)

    

    class Meta:
        """Meta definition for Mail."""

        verbose_name = 'Mail'
        verbose_name_plural = 'Mails'

    def __str__(self):
        """Unicode representation of Mail."""
        pass

