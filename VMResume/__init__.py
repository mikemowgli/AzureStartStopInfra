import datetime
import logging
import requests
import os

import azure.functions as func
from ..shared import utils


def main(resumetimer: func.TimerRequest) -> None:
  utc_timestamp = datetime.datetime.utcnow().replace(
    tzinfo=datetime.timezone.utc).isoformat()

  if resumetimer.past_due:
    logging.info('The timer is past due!')

  # getting variables
  logging.info('Getting the variables...')
  ResourceGroupName = os.environ["ResourceGroupName"]
  TenantId = os.environ["TenantId"]
  SubscriptionId = os.environ["SubscriptionId"]
  AppId = os.environ["VMOpsAppId"]
  SecretId = os.environ["VMOpsSecretId"]
  VMName = os.environ["VMName"]
  
  logging.info('Getting a token...')
  azToken = utils.get_az_token(TenantId, AppId, SecretId)

  resume_vm(SubscriptionId, azToken, ResourceGroupName, VMName)
  
  logging.info('VM %s in %s resumed at %s', VMName, ResourceGroupName, utc_timestamp)

def resume_vm(subscription, token, resourceGroup, vm):
  # resume the VM
  url = "https://management.azure.com/subscriptions/"+subscription+"/resourceGroups/"+resourceGroup+"/providers/Microsoft.Compute/virtualMachines/"+vm+"/start?api-version=2019-12-01"
  headers = {"Authorization": "Bearer "+token, "Content-Type": "application/json"}
  logging.info('Resuming Virtual Machine %s in %s', vm, resourceGroup)
  requests.post(url, headers = headers, data='')
