# Logistics Wizard Overview

[![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard.svg?branch=master)](https://travis-ci.org/IBM-Bluemix/logistics-wizard) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard/badge.svg?branch=master)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard?branch=master)

**WORK IN PROGRESS**

This repository serves as the central server application for the Logistics Wizard application and acts as the main controller for interaction between the system's services.

Logistics Wizard is a reimagined supply chain optimization system for the 21st century. It is comprised of a set of loosely-coupled, distributed services that take an existing ERP system and extend its functionality by leveraging various cloud services. The goal of this system is to showcase several common SaaS implementation patterns and provide them to our developer community. This demo exhibits hybrid cloud, microservices, and big data anlytics concepts that can be reused when building enterprise-level applications on Bluemix.

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/IBM-Bluemix/logistics-wizard.git)

The following services are leveraged in the overall Logistics Wizard solution, yet are built to be extensible for other purposes:

* [logistics-wizard-erp][erp_github_url]
* [logistics-wizard-recommendation][recommendation_github_url]

To deploy the full system all at once, check out the [Logistics Wizard Toolchain][toolchain_github_url]

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

To get values for your local environment variables in `.env.local`, check out the [Setting up email](#setting-up-email) section.

## Testing

### Unit Tests
There are series of unit tests located in the [`server/tests`](server/tests) folder. The tests are composed using the Python [unittest framework][unittest_docs_url]. To run the tests, execute the following commands:

  ```bash
  $ python server/tests/test_demos_service.py
  $ python server/tests/test_users_service.py
  $ python server/tests/test_shipments_service.py
  $ python server/tests/test_distribution_centers_service.py
  $ python server/tests/test_retailers_service.py
  $ python server/tests/test_products_service.py
  $ python server/tests/test_messaging_service.py
  ```

The tests will print a dot for each successfully completed unit test. If a test fails for any reason, it will immediately exit and print the reason for its failure. For example, here is the output of a successfully complete [`test_demos_service.py`](server/tests/test_demos_service.py) test:

  ```bash
  (venv) MyMac:logistics-wizard Jake_Peyser$ python server/	tests/test_des_service.py 
  .......
  ----------------------------------------------------------------------
  Ran 7 tests in 30.597s
  
  OK
  ```

### Travis CI
One popular option for continuous integration is [Travis CI][travis_url]. We have provided a `.travis.yml` file in this repository for convenience. In order to set it up for your repository, take the following actions:

1. Go to your [Travis CI Profile][travis_profile_url]

2. Check the box next to your logistics-wizard GitHub repository and then click the settings cog

3. Create the following environment variables
	- `LOGISTICS_WIZARD_ENV` - TEST
	- `SMTP_SERVER` - smpt.gmail.com
	- `SMTP_SERVER_PORT` - 587
	- `SMTP_USER_NAME`
	- `SMTP_PASSWORD`

	To get values for the `SMTP_USER_NAME` and `SMTP_PASSWORD` variables, check out the [Setting up email](#setting-up-email) section.

Thats it! Now your future pushes to GitHub will be built and tested by Travis CI.

### Code Coverage Tests
If you have you would like to perform code coverage tests as well, you can use [coveralls][coveralls_url] to perform this task. If you are using [Travis CI][travis_url] as your CI tool, simply replace `python` in your test commands with `coverage run` and then run `coveralls` as follows:

  ```bash
  $ coverage run server/tests/test_demos_service.py
  $ coverage run server/tests/test_users_service.py
  $ coverage run server/tests/test_shipments_service.py
  $ coverage run server/tests/test_distribution_centers_service.py
  $ coverage run server/tests/test_retailers_service.py
  $ coverage run server/tests/test_products_service.py
  $ coverage run server/tests/test_messaging_service.py
  $ coveralls
  ```

To determine how to run coveralls using another CI tool or for more in-depth instructions, check out the [coveralls usage documentation][coveralls_usage_url].

**Note**: The unit tests are currently hitting the production version of the [logistics-wizard-erp][erp_github_url] application. In the future these tests will be able to be run in isolation.

## Setting up email
In order to send welcome emails, we need to configure the app to use an SMTP server. For simplicity's sake, we will use the free SMTP server that Gmail provides. This section will walk you through how to do this:

1. [Create a new Gmail account][gmail_signup_url] to serve as the `FROM` address for your application's emails

2. Turn on [Gmail access for less secure apps][google_less_secure_setting_url] so that your app will be able to send emails on your behalf

3. Go to the _Forwarding/IMAP_ tab in your [Gmail settings][gmail_settings_url] and make sure IMAP is enabled. This ensures emails are properly copied into your sent folder.

4. Lastly, your Gmail username and password must be copied to the service you are using for deployment. Here are some common options:
	- **CF CLI**: Update the environment variables in your `manifest.yml` file or in your app dashboard's *Runtime* --> *Environment Variables* section after deployment.
	- **DevOps Services Toolchain**: Configure the environment properties for the `TEST` stage in the `logistics-wizard` delivery pipeline.
	- **Travis CI**: Go to the *Settings* tab for your repo and update the environment variables there.
	- **`.env.local`**: If you would like to test this functionality while developing locally, copy the values into this file.

Your app should now be capable of sending welcome emails to any end users that include their email address during signup.

**Note**: Be aware that Google restricts the number of messages sent per day to 99 emails. The restriction is automatically removed within 24 hours after the limit was reached.

## API documentation
The API methods that this component exposes requires the discovery of dependent services, however, the API will gracefully fail when they are not available.

The API and data models are defined in [this Swagger 2.0 file](swagger.yaml). You can view this file in the [Swagger Editor](http://editor.swagger.io/#/?import=https://raw.githubusercontent.com/IBM-Bluemix/logistics-wizard/master/swagger.yaml).

Use the Postman collection to help you get started with the controller API:  
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b39a8c0ce27371fbd972#?env%5BLW_Prod%5D=W3sia2V5IjoiZXJwX2hvc3QiLCJ2YWx1ZSI6Imh0dHA6Ly9sb2dpc3RpY3Mtd2l6YXJkLWVycC5teWJsdWVtaXgubmV0LyIsInR5cGUiOiJ0ZXh0IiwiZW5hYmxlZCI6dHJ1ZSwiaG92ZXJlZCI6ZmFsc2V9LHsia2V5IjoiY29udHJvbGxlcl9ob3N0IiwidmFsdWUiOiJodHRwczovL2xvZ2lzdGljcy13aXphcmQubXlibHVlbWl4Lm5ldCIsInR5cGUiOiJ0ZXh0IiwiZW5hYmxlZCI6dHJ1ZSwiaG92ZXJlZCI6ZmFsc2V9XQ==)

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
[toolchain_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-toolchain
[bluemix_signup_url]: http://ibm.biz/logistics-wizard-signup
[cloud_foundry_url]: https://github.com/cloudfoundry/cli
[download_python_url]: https://www.python.org/downloads/
[virtualenv_url]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[unittest_docs_url]: https://docs.python.org/3/library/unittest.html
[travis_url]: https://travis-ci.org/
[travis_profile_url]: https://travis-ci.org/profile/
[coveralls_url]: https://coveralls.io/
[coveralls_usage_url]: https://pypi.python.org/pypi/coveralls#usage-travis-ci
[gmail_signup_url]: https://accounts.google.com/signup
[gmail_settings_url]: https://mail.google.com/mail/u/1/#settings/fwdandpop
[google_less_secure_setting_url]: https://www.google.com/settings/security/lesssecureapps