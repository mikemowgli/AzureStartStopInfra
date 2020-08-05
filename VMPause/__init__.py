import datetime
import logging
import requests
import os

import azure.functions as func
from ..shared import utils


def main(pausetimer: func.TimerRequest) -> None:
  utc_timestamp = datetime.datetime.utcnow().replace(
    tzinfo=datetime.timezone.utc).isoformat()

  if pausetimer.past_due:
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

  pause_vm(SubscriptionId, azToken, ResourceGroupName, VMName)
  
  logging.info('VM %s in %s paused at %s', VMName, ResourceGroupName, utc_timestamp)

def pause_vm(subscription, token, resourceGroup, vm):
  # pause the VM
  url = "https://management.azure.com/subscriptions/"+subscription+"/resourceGroups/"+resourceGroup+"/providers/Microsoft.Compute/virtualMachines/"+vm+"/poweroff?api-version=2019-12-01"
  headers = {"Authorization": "Bearer "+token, "Content-Type": "application/json"}
  logging.info('Pausing Virtual Machine %s in %s', vm, resourceGroup)
  requests.post(url, headers = headers, data='')
