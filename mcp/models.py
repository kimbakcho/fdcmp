from djongo import models


class FdcDataGroup(models.Model):
    _id = models.ObjectIdField()
    eqpId = models.IntegerField()
    eqpCode = models.CharField(max_length=255)
    eqpName = models.CharField(max_length=255)
    eqpModuleId = models.IntegerField()
    eqpModuleName = models.CharField(max_length=255)
    context = models.JSONField(default={})
    groupType = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    betweenTimeSec = models.IntegerField()
    etc = models.JSONField(default={})


class EventHistory(models.Model):
    _id = models.ObjectIdField()
    eventCode = models.CharField(max_length=255)
    eventName = models.CharField(max_length=255)
    updateTime = models.DateTimeField()
    eqpId = models.IntegerField()
    eqpCode = models.CharField(max_length=255)
    eqpName = models.CharField(max_length=255)
    eqpModuleId = models.IntegerField()
    eqpModuleName = models.CharField(max_length=255)
    value = models.JSONField(default={})
    context = models.JSONField(default={})
    fdcDataGroup = models.GenericObjectIdField()

class AlarmHistory(models.Model):
    _id = models.ObjectIdField()
    alarmCode = models.CharField(max_length=255)
    alarmName = models.CharField(max_length=255)
    updateTime = models.DateTimeField()
    eqpId = models.IntegerField()
    eqpCode = models.CharField(max_length=255)
    eqpName = models.CharField(max_length=255)
    eqpModuleId = models.IntegerField()
    eqpModuleName = models.CharField(max_length=255)
    value = models.JSONField(default={})
    context = models.JSONField(default={})
    fdcDataGroup = models.GenericObjectIdField()


class TraceData(models.Model):
    _id = models.ObjectIdField()
    traceGroupCode = models.CharField(max_length=255)
    traceGroupName = models.CharField(max_length=255)
    value = models.JSONField(default={})
    eqpId = models.IntegerField()
    eqpCode = models.CharField(max_length=255)
    eqpName = models.CharField(max_length=255)
    eqpModuleId = models.IntegerField()
    updateTime = models.DateTimeField()
    context = models.JSONField(default={})
    fdcDataGroup = models.GenericObjectIdField()
