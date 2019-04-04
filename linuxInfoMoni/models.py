from django.db import models

# Create your models here.

class serverInfo(models.Model):
    serverName=models.CharField(max_length=16)
    ip=models.GenericIPAddressField(protocol='ipv4')
    port=models.IntegerField()
    uname=models.CharField(max_length=16)
    pwd=models.CharField(max_length=16)
    resultPath=models.CharField(max_length=32)
    isTraced=models.CharField(max_length=1,null=True)

class trace_info(models.Model):
    trace_name=models.CharField(max_length=32)
    data=models.CharField(max_length=12)
    server_id=models.ForeignKey('serverInfo',to_field='id',on_delete='PROTECT')


class trace_detail(models.Model):
    time=models.CharField(max_length=8)
    usr_cpu=models.CharField(max_length=12)
    sys_cpu=models.CharField(max_length=12)
    total_cpu=models.CharField(max_length=12)
    recvList=models.CharField(max_length=12)
    sendList=models.CharField(max_length=12)
    total_dk=models.CharField(max_length=12)
    mem_used=models.CharField(max_length=12)
    mem_free=models.CharField(max_length=12)
    mem_cache=models.CharField(max_length=12)
    trace_id=models.ForeignKey('trace_info',to_field='id',on_delete=models.CASCADE)