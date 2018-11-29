# Enable container-to-container communication

This guide complements the [Logistics Wizard](https://github.com/IBM-Cloud/logistics-wizard) demonstration application.

Logistics Wizard's ERP microservice is designed to communicate with two endpoints: a system of record and the Controller microservice. Since it does not facilitate any public requests from users, you can enable container-to-container communication. This ensures that only the Controller can communicate with the ERP service and also that any traffic to the ERP service will be confined to Cloud Foundry's private overlay network.

## Steps

1. Ensure that the Logistics Wizard application is deployed. The most straightforward method is using the [Toolchain](https://github.com/IBM-Cloud/logistics-wizard-toolchain). This will result in all micro and supporting services deployed in IBM Cloud.

2. Access the **logistics-wizard-erp** app from the [Dashboard](https://console.bluemix.net/dashboard/apps).

3. Confirm the app is live by using the **Visit App URL** link. It should return the following.

   ```javascript
    {"started":"2018-11-27T15:41:23.927Z","uptime":156.335}
   ```

4. Also confirm the Web UI is live (it will indirectly use the Controller). Follow the same process to **Visit App URL** for the **logistics-wizard-webui** app. Click on any truck icon; the **Current Weather** information will display.

5. From the command line, login to IBM Cloud and target the organization and space where Logistics Wizard is deployed.

    ```sh
    ibmcloud login
    ibmcloud target --cf
    ```

6. Export the application names using the `ibmcloud cf apps` command to make working with subsequent steps easier.

  ```sh
    export CONTROLLER_NAME=$(ibmcloud cf apps | grep logistics-wizard-toolchain-.*controller | awk '{ print $1 '})
    export ERP_NAME=$(ibmcloud cf apps | grep logistics-wizard-toolchain-.*erp | awk '{ print $1 '})
  ```

7. List the existing routes. Then remove the public route to the ERP service and confirm it is no longer present in the **apps** column.

    ```sh
    ibmcloud cf routes
    ibmcloud cf unmap-route $ERP_NAME mybluemix.net --hostname $ERP_NAME
    ibmcloud cf routes
    ```

8. Try refreshing and accessing the Logistics Wizard application in your browser. It will fail to load because the Controller can no longer contact the ERP service.

9. Create a policy to allow the Controller microservice to contact the ERP microservice.

    ```sh
    ibmcloud cf add-network-policy $CONTROLLER_NAME --destination-app $ERP_NAME --port 8080 --protocol tcp
    ```

10. The ERP microservice is now configured to accept connections from the Controller. But since you removed the public route, you'll need to tell the Controller how to contact the ERP service. The container-to-container method uses the overlay IP address of the ERP service. For now, the easiest way to obtain the IP address is to SSH into the container and retrieve it from the `CF_INSTANCE_INTERNAL_IP` environment variable. Once you have it, copy it to the clipboard and `exit` the SSH session.

    ```sh
    ibmcloud cf ssh $ERP_NAME
    env | grep CF_INSTANCE_INTERNAL_IP
    exit
    ```

11. Next, export the IP address and update the Controller's configuration.

    ```sh
    export CF_INSTANCE_INTERNAL_IP=<the-IP-address-from-SSH>
    ibmcloud cf set-env $CONTROLLER_NAME ERP_SERVICE http://$CF_INSTANCE_INTERNAL_IP:8080
    ibmcloud cf restart $CONTROLLER_NAME
    ```

12. After the Controller has successfully started, refresh the Logistics Wizard web application. It should now display the map again with truck and location information. This indicates that the Controller can once again communicate with the ERP service using container-to-container networking.

## Notes

While the Controller is now communicating container-to-container with the ERP service, it will fail if you restart the ERP service. This is because the ERP service will receive a new IP address upon restart. Perform step 10-11 again. This highlights the need for service discovery and will be covered in a future update.

## Additional Material

* [Cloud Foundry Understanding Container-to-Container Networking](https://docs.cloudfoundry.org/concepts/understand-cf-networking.html)
* [Cloud Foundry C2C Sample](https://github.com/cloudfoundry/cf-networking-examples/blob/master/docs/c2c-no-service-discovery.md)