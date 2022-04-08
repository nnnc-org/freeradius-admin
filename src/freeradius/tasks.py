from datetime import datetime, timedelta
from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from huey.contrib.djhuey import db_periodic_task, db_task

from .models import Device, CsvImporter, PostAuthLog

@db_task()
def process_import(import_pk):
    if CsvImporter.objects.filter(pk=import_pk).exists():
        print("CsvImporter with pk '" + str(import_pk) + "' exists")
        i = CsvImporter.objects.get(pk=import_pk)
        i.process()
    else:
        print("CsvImporter with pk '" + str(import_pk) + "' does not exist")

# Process unprocessed imports hourly
@db_periodic_task(crontab(hour='*', minute='0'))
def process_imports_schedule():
    for i in CsvImporter.objects.filter(devices=None, error_messages=None):
        process_import(i.id)

# Purge old logs daily @ midnight
@db_periodic_task(crontab(day="*", hour='0', minute='0'))
def delete_old_logs():
    PostAuthLog.objects.filter(created_at__lte=datetime.now()-timedelta(days=7)).delete()