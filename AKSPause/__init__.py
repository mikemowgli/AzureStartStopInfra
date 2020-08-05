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
  
  logging.info('Getting a token...')
  azToken = utils.get_az_token(TenantId, AppId, SecretId)

  logging.info('Getting AKS Node Resource Group name(s) for AKS cluster(s) in %s', ResourceGroupName)
  aksManagedResourceGroups = utils.get_aks_nodes_rg(SubscriptionId, azToken, ResourceGroupName)

  for nodeRg in aksManagedResourceGroups:
    logging.info('Getting Virtual Machine Scale Sets in AKS Node Resource Group %s', nodeRg)
    aksVMScalesSets = utils.get_virtual_machine_scales_sets(SubscriptionId, azToken, nodeRg)

    for vmss in aksVMScalesSets:
      logging.info('Pausing Virtual MAchine Scale Set %s in AKS Node Resource Group %s', vmss, nodeRg)
      pause_vmss(SubscriptionId, azToken, nodeRg)
  
  logging.info('AKS cluster(s) in %s paused at %s', ResourceGroupName, utc_timestamp)

def pause_vmss(subscription, token, resourceGroup, virtualMachineScaleSet):
  # pause the VM scale set
  url = "https://management.azure.com/subscriptions/"+subscription+"/resourceGroups/"+resourceGroup+"/providers/Microsoft.Compute/virtualMachineScaleSets/"+virtualMachineScaleSet+"/poweroff?api-version=2019-12-01"
  headers = {"Authorization": "Bearer "+token, "Content-Type": "application/json"}
  logging.info('Pausing Virtual Machine Scale Set %s in %s', virtualMachineScaleSet, resourceGroup)
  requests.post(url, headers = headers, data='')
