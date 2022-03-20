from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from huey.contrib.djhuey import db_periodic_task, db_task

from .models import Device, CsvImporter

@db_task()
def process_import(import_pk):
    if CsvImporter.objects.filter(pk=import_pk).exists():
        print("CsvImporter with pk '" + str(import_pk) + "' exists")
        i = CsvImporter.objects.get(pk=import_pk)
        i.process()
    else:
        print("CsvImporter with pk '" + str(import_pk) + "' does not exist")