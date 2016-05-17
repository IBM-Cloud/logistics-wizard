# Logistics Wizard Overview

**WORK IN PROGRESS**

This repository serves as the central server application for the Logistics Wizard application and acts as the main controller for interaction between the system's services.

Logistics Wizard is a reimagined supply chain optimization system for the 21st century. It is comprised of a set of loosely-coupled, distributed services that take an existing ERP system and extend its functionality by leveraging various cloud services. The goal of this system is to showcase several common SaaS implementation patterns and provide them to our developer community. This demo exhibits hybrid cloud, microservices, and big data anlytics concepts that can be reused when building enterprise-level applications on Bluemix.

The following services are leveraged in the overall Logistics Wizard solution, yet are built to be extensible for other purposes:

* [logistics-wizard-erp](https://github.com/IBM-Bluemix/logistics-wizard-erp)
* [logistics-wizard-recommendation](https://github.com/IBM-Bluemix/logistics-wizard-recommendation)

![Architecture](http://g.gravizo.com/g?
  digraph G {
    node [fontname = "helvetica"]
    rankdir=RL
    user -> controller [label="1 - Makes a request"]
    recommendations -> discovery [headlabel="2 - Registers and sends heartbeat" labeldistance=12 labelangle=-16]
    erp -> discovery [label="3 - Registers and sends heartbeat"]
    controller -> discovery [taillabel="4 - Query for services" labeldistance=8 labelangle=-7]
    controller -> erp [label="5 - CRUD SCM data"]
    controller -> recommendations [label="6 - Retrieve/update recommendations" dir="back"]
    {rank=max; user}
    {rank=same; erp -> controller [style=invis]}
    {rank=same; controller -> recommendations [style=invis]}
    {rank=min; discovery}
    /* styling */
    user [shape=diamond width=1 height=1 fixedsize=true style=filled color="black" fontcolor=white label="User"]
    erp [shape=rect style=filled color="%2324B643" fontcolor=white label="ERP"]
    controller [shape=rect label="Controller API"]
    recommendations [shape=rect style=filled color="%2324B643" fontcolor=white label="Recommendations"]
    discovery [shape=circle width=1 fixedsize=true style=filled color="%234E96DB" fontcolor=white label="Service\\nRegistry"]
  }
)

## Running the app on Bluemix
<Either add a Deploy to Bluemix button or include detailed instructions on how to deploy the app(s) to Bluemix after cloning the repo. You should assume the user has little to no Bluemix experience and provide as much detail as possible in the steps.>

Coming Soon!

[Sign up for Bluemix][bluemix_signup_url] in the meantime!

<Create sub-sections to break down larger sequences of steps. General rule of thumb is that you should not have more than 9 steps in each task. Include sanity checks, or ways for the developer to confirm what they have done so far is correct, every 20 steps. Also, avoid directly referencing the Bluemix UI components so that ACE changes don't invalidate your README.>

## Run the app locally
Coming soon!

## API documentation
The API methods that this component exposes requires the discovery of dependent services, however, the API will gracefully fail when they are not available.

The API and data models are defined in [this Swagger 2.0 file](swagger.yaml). You can view this file in the [Swagger Editor](http://editor.swagger.io/#/?import=https://raw.githubusercontent.com/IBM-Bluemix/logistics-wizard/master/swagger.yaml).

## Contribute
Please check out our [Contributing Guidelines](https://github.com/IBM-Bluemix/logistics-wizard/blob/master/.github/CONTRIBUTING.md) for detailed information on how you can lend a hand to the Logistics Wizard demo implementation effort.

## Troubleshooting

The primary source of debugging information for your Bluemix app is the logs. To see them, run the following command using the Cloud Foundry CLI:

  ```
  $ cf logs logistics-wizard --recent
  ```
For more detailed information on troubleshooting your application, see the [Troubleshooting section](https://www.ng.bluemix.net/docs/troubleshoot/tr.html) in the Bluemix documentation.

## License

See [License.txt](License.txt) for license information.

[bluemix_signup_url]: http://ibm.biz/logistics-wizard-signup