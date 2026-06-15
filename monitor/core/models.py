from django.db import models

# Create your models here.
class TestStore(models.Model):
    name = models.CharField(max_length=100)
    
class TestEnviroments(models.Model):
    test_store_id = models.ForeignKey(TestStore, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class TestValues(models.Model):
    test_enviroments_id = models.ForeignKey(TestEnviroments, on_delete=models.CASCADE)
    env_tp = models.FloatField(blank=True)
    suc_tp = models.FloatField(blank=True)
    eva_tp = models.FloatField(blank=True)
    deg_tp = models.FloatField(blank=True)
    def_status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['test_enviroments_id_id', 'date'],
                name='idx_envid_date'
            )
        ]
