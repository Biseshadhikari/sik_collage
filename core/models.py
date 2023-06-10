from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from django.template.defaultfilters import slugify
import uuid
from django.conf import settings


class Collage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500,default=' ')
    image = models.ImageField(upload_to='img',default= ' ')
    # qr_code = models.ImageField(upload_to='qr_codes',blank= True)
    qr_code = models.ImageField(upload_to='qr_codes',blank= True)
    slug = models.SlugField(max_length=200,default = ' ')



    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        self.slug = f"{slugify(self.name)}-{str(uuid.uuid4())}"
        site = f"{settings.SITE_URL}forms/{self.slug}"
        

        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4)
        qr.add_data(site)
        qr.make(fit=True)
        img = qr.make_image(fill_color ="black",back_color = "white")
        fname = f'qr_code-{self.name}+.png'
        buffer = BytesIO()
        img.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        super().save(*args, **kwargs)   

class CollageForm(models.Model):
    collage = models.ForeignKey(Collage,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length= 200)
    address = models.CharField(max_length=500)
    gpa = models.CharField(max_length=50)  
    faculty = models.CharField(max_length=300)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}-{self.collage}"