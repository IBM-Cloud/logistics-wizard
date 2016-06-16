# Logistics Wizard Overview

[![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard.svg?branch=master)](https://travis-ci.org/IBM-Bluemix/logistics-wizard) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard/badge.svg?branch=master)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard?branch=master)

**WORK IN PROGRESS**

This repository serves as the central server application for the Logistics Wizard application and acts as the main controller for interaction between the system's services.

Logistics Wizard is a reimagined supply chain optimization system for the 21st century. It is comprised of a set of loosely-coupled, distributed services that take an existing ERP system and extend its functionality by leveraging various cloud services. The goal of this system is to showcase several common SaaS implementation patterns and provide them to our developer community. This demo exhibits hybrid cloud, microservices, and big data anlytics concepts that can be reused when building enterprise-level applications on Bluemix.

[![Create Toolchain](./.bluemix/create_toolchain_button.png)](https://new-console.ng.bluemix.net/devops/setup/deploy/?repository=https%3A//github.com//IBM-Bluemix/logistics-wizard.git)

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/IBM-Bluemix/logistics-wizard.git)

The following services are leveraged in the overall Logistics Wizard solution, yet are built to be extensible for other purposes:

* [logistics-wizard-erp][erp_github_url]
* [logistics-wizard-recommendation][recommendation_github_url]

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

1. If you do not already have a Bluemix account, [sign up here][bluemix_signup_url]

2. Download and install the [Cloud Foundry CLI][cloud_foundry_url] tool

3. Clone the app and its submodules to your local environment from your terminal using the following command:

	```bash
	$ git clone --recursive https://github.com/IBM-Bluemix/logistics-wizard.git
	```

4. `cd` into this newly created directory

5. Open the `manifest.yml` file and change the `host` value to something unique.

  The host you choose will determinate the subdomain of your application's URL:  `<host>.mybluemix.net`

6. Connect to Bluemix in the command line tool and follow the prompts to log in.

	```bash
	$ cf api https://api.ng.bluemix.net
	$ cf login
	```
7. Push the app to Bluemix.

	```bash
	$ cf push
	```

And voila! You now have your very own instance of Logistics Wizard running on Bluemix.

## Run the app locally

1. If you have not already, [download Python 2.7][download_python_url] and install it on your local machine.

2. Clone the app to your local environment from your terminal using the following command:

  ```bash 
  $ git clone --recursive https://github.com/IBM-Bluemix/logistics-wizard.git
  ```

3. `cd` into this newly created directory

4. In order to create an isolated development environment, we will be using Python's [virtualenv][virtualenv_url] tool. If you do not have it installed already, run

  ```bash
  $ pip install virtualenv
  ```
  
  Then create a virtual environment called `venv` by running

  ```bash
  $ virtualenv venv
  ```

5. Activate this new environment with

  ```bash
  $ source .env
  ```
  
6. Install module requirements

  ```bash
  $ pip install -r requirements.dev.txt
  ```

7. Finally, start the app

  ```bash
  $ python bin/start_web.py
  ```

## Running Unit Tests

There are series of unit tests located in the [`server/tests`](server/tests) folder. The tests are composed using the Python [unittest framework][unittest_docs_url]. To run the tests, execute the following commands:

  ```bash
  $ python server/tests/test_demos_service.py
  $ python server/tests/test_users_service.py
  ```

The tests will print a dot for each succefully completed unit test. If a test fails for any reason, it will immediately exit and print the reason for its failure. For example, here is the output of a successfully complete [`test_demos_service.py`](server/tests/test_demos_service.py) test:

  ```bash
  (venv) MyMac:logistics-wizard Jake_Peyser$ python server/	tests/test_des_service.py 
  .......
  ----------------------------------------------------------------------
  Ran 7 tests in 30.597s
  
  OK
  ```

The unit tests are currently hitting the production version of the [logistics-wizard-erp][erp_github_url] application. In the future these tests will be able to be run in isolation.

## API documentation
The API methods that this component exposes requires the discovery of dependent services, however, the API will gracefully fail when they are not available.

The API and data models are defined in [this Swagger 2.0 file](swagger.yaml). You can view this file in the [Swagger Editor](http://editor.swagger.io/#/?import=https://raw.githubusercontent.com/IBM-Bluemix/logistics-wizard/master/swagger.yaml).

Use the Postman collection to help you get started with the controller API:  
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b39a8c0ce27371fbd972)

## Contribute
Please check out our [Contributing Guidelines](.github/CONTRIBUTING.md) for detailed information on how you can lend a hand to the Logistics Wizard demo implementation effort.

## Troubleshooting

The primary source of debugging information for your Bluemix app is the logs. To see them, run the following command using the Cloud Foundry CLI:

  ```
  $ cf logs logistics-wizard --recent
  ```
For more detailed information on troubleshooting your application, see the [Troubleshooting section](https://www.ng.bluemix.net/docs/troubleshoot/tr.html) in the Bluemix documentation.

## License

See [License.txt](License.txt) for license information.

<!--Links-->
[erp_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-erp
[recommendation_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-recommendation
[bluemix_signup_url]: http://ibm.biz/logistics-wizard-signup
[cloud_foundry_url]: https://github.com/cloudfoundry/cli
[download_python_url]: https://www.python.org/downloads/
[virtualenv_url]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[unittest_docs_url]: https://docs.python.org/3/library/unittest.html