from django.db import models

# Create your models here.
class TestStore(models.Model):
    name = models.CharField(max_length=100)
    
class TestEnviroments(models.Model):
    test_store_id = models.ForeignKey(TestStore, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class TestValues(models.Model):
    test_enviroments_id = models.ForeignKey(TestEnviroments, on_delete=models.CASCADE)
    env_tp = models.CharField()
    suc_tp = models.CharField()
    eva_tp = models.CharField()
    deg_tp = models.CharField()
    def_status = models.BooleanField()
    date = models.DateTimeField(auto_now=True)
