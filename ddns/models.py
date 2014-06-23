from django.db import models

def pdns(type):
    type.pdns = True
    return type

@pdns
class Record(models.Model):
    domain_id = models.IntegerField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    content = models.CharField(max_length=65535)
    ttl = models.IntegerField()
    prio = models.IntegerField()
    change_date = models.IntegerField()
    ordername = models.CharField(max_length=255)
    auth = models.BooleanField()

    class Meta(object):
        db_table = 'records'
