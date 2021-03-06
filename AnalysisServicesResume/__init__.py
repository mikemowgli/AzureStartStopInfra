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
  ASServerName = os.environ["AnalysisServicesInstanceName"]

  # get the credential
  logging.info('Getting the credential...')
  AppId = os.environ["SynapseAppId"]
  SecretId = os.environ["SynapseSecretId"]

  logging.info('Getting a token...')
  azToken = utils.get_az_token(TenantId, AppId, SecretId)

  resume_analysis_services(SubscriptionId, azToken, ResourceGroupName, ASServerName)
  logging.info('Analysis Services instance resumed at %s', utc_timestamp)

def resume_analysis_services(subscription, token, resourceGroup, server):
  url = "https://management.azure.com/subscriptions/"+subscription+"/resourceGroups/"+resourceGroup+"/providers/Microsoft.AnalysisServices/servers/"+server+"/resume?api-version=2017-08-01"
  headers = {"Authorization": "Bearer "+token, "Content-Type": "application/json"}
  logging.info('Resuming Analysis Services instance %s in resource group %s', server, resourceGroup)
  requests.post(url, headers = headers, data='')
