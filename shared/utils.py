import requests

def get_az_token(tenant, username, password):
  data = "grant_type=client_credentials&client_id="+username+"&client_secret="+password+"&resource=https%3A%2F%2Fmanagement.azure.com%2F"
  url = "https://login.microsoftonline.com/"+tenant+"/oauth2/token"
  response = requests.post(url, data=data)
  AccessToken = response.json()["access_token"]
  return AccessToken

def get_aks_nodes_rg(subscription, token, resourceGroup):
  url = "https://management.azure.com/subscriptions/"+subscription+"/resourceGroups/"+resourceGroup+"/providers/Microsoft.ContainerService/managedClusters?api-version=2020-06-01"
  headers = {"Authorization": "Bearer "+token, "Content-Type": "application/json"}
  response = requests.get(url, headers = headers)
  aksClusters = response.json()["value"]
  aksNodeResourceGroups = []
  for cluster in aksClusters:
    aksNodeResourceGroups.append(cluster["properties"]["nodeResourceGroup"])
  return aksNodeResourceGroups

def get_virtual_machine_scales_sets(subscription, token, resourceGroup):
  url = "https://management.azure.com/subscriptions/"+subscription+"/resourceGroups/"+resourceGroup+"/providers/Microsoft.Compute/virtualMachineScaleSets?api-version=2019-12-01"
  headers = {"Authorization": "Bearer "+token, "Content-Type": "application/json"}
  response = requests.get(url, headers = headers)
  VMScaleSets = response.json()["value"]
  VMSSNames = []
  for vmss in VMScaleSets:
    VMSSNames.append(vmss["name"])
  return VMSSNames
