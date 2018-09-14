# Deploy Logistics Wizard to Cloud Foundry Enterprise Environment (CFEE)

These are instructions to deploy Logistic Wizard to Cloud Foundry Enterprise Environment. The application is broken down into a number of microservices. The core runtimes(WebUI, ERP, and Controller) are deployed to CFEE and the services to public Cloud Foundry. 

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

The instructions below deploys to the US South region, but you can deploy to other regions available depending on your requirements. 

- (US South) public CF API endpoint: [https://api.ng.bluemix.net](https://api.ng.bluemix.net/) 

- (US South) CFEE API endpoint:   https://api.<ENVIRONMENT_NAME\>-cluster.us-south.containers.appdomain.cloud

  You can get your CFEE API endpoint from the IBM Cloud [CFEE dashboard](https://console.bluemix.net/dashboard/cloudfoundry?filter=cf_environments). ![CFEE dashboard](docs/cfee_dashboard.png)

## Set up the ERP

1. In your terminal, point to public CF API endpoint and login targeting your org and space.

   ```bash
   [sudo] cf api https://api.ng.bluemix.net 
   cf login
   ```

2. Create the Cloudant database for the ERP.

   ```
   cf create-service cloudantNoSQLDB Lite logistics-wizard-erp-db
   ```

3. Create the database called `logistics-wizard` in the Cloudant dashboard. ![](docs/database.png)

4. Then clone `logistics-wizard-erp` repo.

   ```bash
   git clone https://github.com/IBM-Cloud/logistics-wizard-erp
   cd logistics-wizard-erp
   ```

5. Edit the [manifest.yml](ToDo: add url) and remove the `logistics-wizard-erp-db` service listed.

   ![Snippets](docs/snippets.png)

6. Switch to CFEE API endpoint and target your CFEE Org and Space.

   ```bash
   cf api <CFEE_API ENDPOINT>
   cf login
   ```
   **Note:** For creating CFEE Org and Space, refer https://console.bluemix.net/docs/cloud-foundry/orgs-spaces.html#create_orgs

7. Push the ERP to CFEE.

   ```bash
   cf push --no-start
   ```

8. On the CFEE dashboard, click on the Org you created under Organizations > Spaces > Space name > Services and then Create a service alias for the Cloudant Service `logistics-wizard-erp-db` and then bind it to the `logistics-wizard-erp` application. ![alias](docs/alias.png)

9. Start the ERP microservice.

   ```bash
   cf start logistics-wizard-erp
   ```

10. After starting the ERP microservice, you can verify it is running.

   ![Deployed](docs/deployed.png)

## Set up the Controller Service

1. Clone the controller repo.

   ```bash
   git clone https://github.com/IBM-Cloud/logistics-wizard-controller
   cd logistics-wizard-controller
   ```

2. Push the controller microservice without starting.

   ```bash
   cf push --no-start
   ```

3. Set the environment variables for the controller to connect to the ERP.

   ```
   cf set-env logistics-wizard-controller ERP_SERVICE 'https://<erp-url>'
   cf set-env logistics-wizard-controller OPENWHISK_AUTH <openwhisk-auth>
   cf set-env logistics-wizard-controller OPENWHISK_PACKAGE lwr
   ```

   You can get the `OPENWHISK_AUTH` from the [IBM Cloud console](https://console.bluemix.net/openwhisk/learn/api-key). 

4. Start the controller microservice.

   ```bash
   cf start logistics-wizard-controller
   ```

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
   export CONTROLLER_SERVICE=<controller-service-URL> 
   npm run deploy:prod
   ```

    For example, `CONTROLLER_SERVICE=https://logistics-wizard-controller.lw-cfee-demo-cluster.us-south.containers.appdomain.cloud/`

4. Deploy the WebUI to CFEE.

   ```bash
   cd dist
   cf push logistics-wizard
   ```

## Set up the Cloud Functions Actions

Cloud Functions is outside CFEE, so you would need to switch to the public CF to complete below section.

1. Switch to public Cloud Foundry.

   ```bash
   cf api https://api.ng.bluemix.net 
   cf login
   ```

2. Create the two services, `Cloudant` and  `Weather Company Data` service.

   ```bash
   cf create-service weatherinsights Base-v2 logistics-wizard-weatherinsights
   cf create-service cloudantNoSQLDB Lite logistics-wizard-recommendation-db
   ```
   **Note**: Weatherinsights is a 

3. Create service keys for two services created, **take note of the URL values as it would be needed in step 6.**

   ```bash
   cf create-service-key logistics-wizard-weatherinsights for-openwhisk
   cf create-service-key logistics-wizard-recommendation-db for-openwhisk
   cf service-key logistics-wizard-weatherinsights for-openwhisk
   cf service-key logistics-wizard-recommendation-db for-openwhisk
   ```

4. Clone the logistics-wizard-recommendation repo.

   ```bash
   git clone https://github.com/IBM-Cloud/logistics-wizard-recommendation
   cd logistics-wizard-recommendation
   ```

5. Copy the local env template file. 

   ```bash
   cp template-local.env local.env
   ```

6. Using the URL values from the terimal output above, update the local.env file to look like the following:

   ```bash
   PACKAGE_NAME=lwr
   CONTROLLER_SERVICE=<controller-service-URL>
   WEATHER_SERVICE=<logistics-wizard-weatherinsights-URL>
   CLOUDANT_URL=<logistics-wizard-recommendation-db-URL>
   CLOUDANT_DATABASE=recommendations
   ```

7. Build your Cloud Functions actions. 

   Note: node version >=4.2.0 required and npm >=3.0.0 

   ```bash
   npm install
   npm run build
   ```

8. Deploy your Cloud Functions actions:

   ```bash
   ./deploy.sh --install
   ```

9. Done, now access the WebUI URL in the browser and explore the app running on CFEE. ![](docs/LW-pushed.png)



## Set up Stratos Console

1. Install Stratos Console by following the install wizard, select the Kubernetes cluster option when installing.![](docs/CFEE_dashboard_view.png)

2. Open the Stratos Console to 

   - view logs stream,  

   - view the health and usage, 

   - view configurations, instances, routes, services, events and more. ![](docs/stratos.png) 

     ![](docs/stratos2.png)
