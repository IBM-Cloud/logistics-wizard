# Deploy Logistics Wizard to Cloud Foundry Enterprise Environment (CFEE)

Step by step guide to deploy Logistic Wizard to Cloud Foundry Enterprise Environment(CFEE). The Logistic Wizard app is broken down into many microservices to function different part of the application. There are three runtimes(WebUI, ERP, and Controller) all of which deployed to CFEE while the services located in the public Cloud Foundry and been linked to the CFEE account. You may be thinking why to use CFEE at first place. 

With the IBM® Cloud Foundry Enterprise Environment (CFEE), you can instantiate multiple, isolated, enterprise-grade Cloud Foundry platforms on demand. Instances of the IBM Cloud Foundry Enterprise service run within your own account in the IBM Cloud. The environment is deployed on isolated hardware (Kubernetes clusters). You have full control over the environment, including access control, capacity management, change management, monitoring, and services.

**CFEE**

- Web UI runtime
- ERP runtime
- Controller runtime

**Non-CFEE**

- Cloudant used by the ERP
- Cloud Functions
- Cloudant used by Cloud Functions
- Weather Company Data used by Cloud Functions

The services must be created within the public Cloud Foundry(CF) and then linked to your Cloud Foundry Enterprise Environment (CFEE).

## Architecture

Logistics Wizard consists of several microservices.

![CFEE](docs/cfee.png)

## Getting Started 

1. In this instruction guide, you will explore deploying Logistic Wizard to CFEE. First, you would need a CFEE instance created. If you don't have one already, [follow these steps first](https://cloud.ibm.com/cfadmin/create).

2. The instructions below deploys to the US South region, but you can deploy to other regions available depending on your requirements.
   - (US South) public CF API endpoint: [https://api.ng.bluemix.net](https://api.ng.bluemix.net/)
   - (US South) CFEE API endpoint: https://api.<ENVIRONMENT_NAME\>.us-south.containers.appdomain.cloud
   - You can get your CFEE API endpoint from your CFEE instance dashboard.

## Set up the ERP

1. Then clone `logistics-wizard-erp` repo.
   ```bash
   git clone https://github.com/IBM-Cloud/logistics-wizard-erp
   cd logistics-wizard-erp
   ```
2. Edit the `manifest.yml` file and remove the `logistics-wizard-erp-db` service listed.

   ![Snippets](docs/snippets.png)
3. Switch the Cloud Foundry endpoint to your private CFEE instance, org and space.
   ```bash
   ibmcloud target --cf
   ```
   **Note:** For creating CFEE Org and Space, refer to https://cloud.ibm.com/docs/cloud-foundry?topic=cloud-foundry-create_orgs#create_orgs
4. Push the ERP to CFEE.
   ```bash
   ibmcloud cf push --no-start
   ```
5. Create the Cloudant NoSQLDB service for the ERP. Navigate to [IBM Cloud Dashboard](https://console.bluemix.net/dashboard/apps) > Create Resource > Search for Cloudant > name it as `logistics-wizard-erp-db`.
  ![](docs/cloudant-create.png)
6. Create the database called `logistics-wizard` by launching the Cloudant dashboard. ![](docs/database.png)
7. On the CFEE dashboard, click on the Org you created under Organizations > Spaces > Space name > Services.
1. Create a service alias for the Cloudant Service `logistics-wizard-erp-db`.
1. Bind the alias to the `logistics-wizard-erp` application. ![alias](docs/alias.png). Select `Manager` as the service access role when prompted.
8. Start the ERP microservice.
   ```bash
   ibmcloud cf start logistics-wizard-erp
   ```
9. After starting the ERP microservice, you can verify it is running.
  ![Deployed](docs/deployed.png)

## Set up the Controller Service

1. Clone the controller repo.
   ```bash
   git clone https://github.com/IBM-Cloud/logistics-wizard-controller
   cd logistics-wizard-controller
   ```
2. Push the controller microservice without starting.
   ```bash
   ibmcloud cf push --no-start
   ```
3. Make note of the Controller route in the command output (such as `logistics-wizard-controller.<environment>.us-south.containers.appdomain.cloud`).

## Set up the WebUI

1. Clone the logistics-wizard-webui repo.
   ```bash
   git clone https://github.com/IBM-Cloud/logistics-wizard-webui
   cd logistics-wizard-webui
   ```
2. Install the dependencies.
   ```bash
   npm install
   ```
3. Build the static files for the WebUI using the appropriate environment variables.
   ```bash
   export CONTROLLER_SERVICE=https://<controller-service-URL>
   npm run deploy:prod
   ```

   For example, `CONTROLLER_SERVICE=https://logistics-wizard-controller.lw-cfee-demo-cluster.us-south.containers.appdomain.cloud`
4. Deploy the WebUI to CFEE.
   ```bash
   cd dist
   ibmcloud cf push logistics-wizard
   ```

## Set up the Cloud Functions Actions

Cloud Functions is outside CFEE, so you would need to switch to the public CF to complete below section.

4. Clone the logistics-wizard-recommendation repo.
   ```bash
   git clone https://github.com/IBM-Cloud/logistics-wizard-recommendation
   cd logistics-wizard-recommendation
   ```
1. Switch to public Cloud Foundry.
   ```bash
   ibmcloud target --cf
   ```
2. Create a `Cloudant` instance.
   ```bash
   ibmcloud cf create-service cloudantNoSQLDB Standard logistics-wizard-recommendation-db
3. Create a service key, **take note of the URL values as it would be needed in a later step.**
   ```bash
   ibmcloud cf create-service-key logistics-wizard-recommendation-db for-openwhisk
   ```
1. Retrieve the Cloudant credentials
   ```bash
   ibmcloud cf service-key logistics-wizard-recommendation-db for-openwhisk
   ```
5. Copy the local env template file.
   ```bash
   cp template-local.env local.env
   ```
6. Using the URL values from the terimal output above, update the local.env file to look like the following:
7. Build your Cloud Functions actions.
   Note: node version >=6.9.1 required and npm >=3.10.8

   ```bash
   npm install
   npm run build
   ```
8. Verify your setup, Here, we perform a blocking (synchronous) invocation of `echo`, passing it "hello" as an argument.
   ```bash
   ibmcloud fn action invoke /whisk.system/utils/echo -p message hello --result
   ```

   Output should be something like `{ "message": "hello" }`.
9. Deploy your Cloud Functions actions:
   ```bash
   ./deploy.sh --install
   ```
1. Make note of the URL to call functions.

## Start the controller app

1. Log in again in your CFEE environment
   ```bash
   ibmcloud target --cf
   ```
1. Set the environment variables for the controller to connect to the ERP and to the Recommendation service. Run the below commands by providing appropriate values:

  ```bash
  ibmcloud cf set-env logistics-wizard-controller ERP_SERVICE 'https://<erp-URL>'
  ibmcloud cf set-env logistics-wizard-controller FUNCTIONS_NAMESPACE_URL <url-to-call-functions>
  ```
1. Start the controller microservice.
   ```bash
   ibmcloud cf start logistics-wizard-controller
   ```
1. Done, now access the WebUI URL in the browser and explore the app running on CFEE. ![](docs/LW-pushed.png)

## Set up Stratos Console

1. Install Stratos Console by following the install wizard, select the Kubernetes cluster option when installing.![](docs/CFEE_dashboard_view.png)

2. Open the Stratos Console to
   - view logs stream,  
   - view the health and usage,
   - view configurations, instances, routes, services, events and more. ![](docs/stratos.png)
     ![](docs/stratos2.png)
