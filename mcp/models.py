from djongo import models


class EventHistory(models.Model):
    eventCode = models.CharField(max_length=100)
    eventName = models.CharField(max_length=100)
    updateTime = models.DateTimeField(auto_now_add=True)
    eqpId = models.IntegerField()
    eqpCode = models.CharField(max_length=100)
    eqpName = models.CharField(max_length=100)
    eqpModuleId = models.IntegerField()
    eqpModuleName = models.CharField(max_length=100)


