from datetime import datetime, timedelta
from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from huey.contrib.djhuey import db_periodic_task, db_task

from .models import MosyleIntegrationModel

@db_task()
def run_integration(integration_pk):
    if MosyleIntegrationModel.objects.filter(pk=integration_pk).exists():
        print("MosyleIntegrationModel with pk '" + str(integration_pk) + "' exists")
        i = MosyleIntegrationModel.objects.get(pk=integration_pk)
        i.process()
    else:
        print("MosyleIntegrationModel with pk '" + str(integration_pk) + "' does not exist")
