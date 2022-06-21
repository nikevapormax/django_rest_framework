from django.db import models
from user.models import User as UserModel


class Product(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    thumbnail = models.FileField("썸네일", upload_to="product/", null=True)
    desc = models.TextField("설명")
    created_at = models.DateTimeField("등록일자", auto_now_add=True)
    exposure_start = models.DateField("노출시작일")
    exposure_end = models.DateField("노출종료일")
    
    def __str__(self):
        return f'{self.title} | {self.desc}'
    
    