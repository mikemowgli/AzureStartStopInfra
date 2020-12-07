# Azure Infra Scheduled Pause/Resume using Azure Functions

This is a small project to schedule pausing and resuming of an various Azure resources with Azure Functions. It currently handles
* Pause and resume of a Synapse Pool (given its name, server name, and resource group)
* Pause and resume of an Analysis Services instance (given its name and resource group)
* Start and stop of AKS cluster (will act on all VM scale sets associated with all AKS clusters in a given resource group)
* Start and stop of a VM (given its name and resource group)

# Functions

* SynapsePause
* SynapseResume
* AnalysisServicesPause
* AnalysisServicesResume
* AKSPause
* AKSResume
* VMPause
* VMResume

# Variables

* ResourceGroupName: the resource group of the Synapse pool, the AKS clusters and the VM
* TenantId: the Azure Tenant ID
* SubscriptionId: the subscription ID of the resource group
* DatabaseServerName: The name of the server where the Synapse pool lives
* DatabaseName: The name of the Synapse pool
* SynapseAppId: The Application ID of the Service Principal that triggers the Synapse (and Analysis Services) pause/resume actions
* SynapseSecretId: The Secret ID of the Service Principal
* VMOpsAppId: The Application ID of the Service Principal that stops/starts the VM and AKS clusters
* VMOpsSecretId: The Secret ID of the Service Principal
* SynapsePauseTime: The cron formatted schedule to pause the Synapse pool, in UTC. Example: `0 35 14 * * *` (everyday at 14:35:00 UTC)
* SynapseResumeTime: The cron formatted schedule to resume the Synapse pool, in UTC.
* AKSPauseTime: The cron formatted schedule to stop the AKS clusters
* AKSResumeTime: The cron formatted schedule to start the AKS clusters
* VMPauseTime: The cron formatted schedule to stop the VM
* VMResumeTime: The cron formatted schedule to start the VM
* AnalysisServicesPauseTime: the cron formatted schedule to pause the Analysis Services instance, in UTC.
* AnalysisServicesResumeTime: the cron formatted schedule to resume the Analysis Services instance, in UTC.
* AnalysisServiceInstanceName: the name of the Analysis Services instance

# zipping

To automate the deployment of these Azure Functions (with Terraform or Azure RM templates), the Function apps are expected in a zip file. The zip command used is:
```
zip -r ../AzureStartStopInfra.zip . -x \.gitignore \local.settings.json .git/\* azure-functions-core-tools/\* releases/\* venv/\*
```
To exclude specific functions depending on the target environments, such examples could be used:
```
# in UAT
zip -r ../AzureStartStopInfraUAT.zip . -x \.gitignore \local.settings.json .git/\* azure-functions-core-tools/\* releases/\* venv/\*
# in PROD
zip -r ../AzureStartStopInfraPROD.zip . -x \.gitignore \local.settings.json .git/\* azure-functions-core-tools/\* releases/\* venv/\* AKSPause/\* AKSResume/\*
```

# Useful commands
* To list the available templates: `func templates list`
* To initialize a new Function app: `func init SynapseAutoPause --python`
* To create a new Function: `func new --name SynapsePause --template "Timer Trigger"`
* To populate the local.settings.json with the Storage Account connectoin string: `func azure functionapp fetch-app-settings <name_of_Functions_App_Service>`
* To run locally: `func start`
* To publish to the Functions App Service: `func azure functionapp publish <name_of_Functions_App_Service>`

# Tips

* The Storage Account needs to be of type GP v1 and must not be firewalled
* The Azure documentation recommends using the app settings `"ENABLE_ORYX_BUILD": "true"` and `"SCM_DO_BUILD_DURING_DEPLOYMENT": "true"` to enable remote build for Linux App Services. However these settings [are not effective when running from a package](https://docs.microsoft.com/en-us/azure/azure-functions/run-functions-from-deployment-package#integration-with-zip-deployment) (`WEBSITE_RUN_FROM_PACKAGE = <uri_to_zip_file>`) which is the option used when publishing the Functions with Terraform.
* As a consequence, when running from a package, Azure Functions won't perform any build, and as such, won't honor the `requirements.txt`, and won't pull any dependency. It is then a *must* that the zip file includes the necessary Python modules.
* How to include the Python modules? The Python modules are expected in `.python-packages`. However, when developing the Functions locally, this folder is not populated, since the modules are kept in your venv. And when publishing your Functions to Azure, the remote build kicks in, so that the build process happens in the cloud and the local `.python-packages` folder remains empty. One needs to force a local build to populate this directory with the expected dependencies: `func azure functionapp publish <name_of_Functions_App_Service> --build local`. Only then could the zip archive be created.
* When running the Functions from a package, Azure cannot notice any change in the remote zip file, and won't update the Functions automatically. It is the responsibility of the user [to perform the trigger syncs](https://docs.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies#trigger-syncing).
