# Logistics Wizard Overview

Logistics Wizard is a reimagined supply chain optimization system for the 21st century. It is comprised of a set of loosely-coupled, distributed services that take an existing ERP system and extend its functionality by leveraging various cloud services. The goal of this system is to showcase several common SaaS implementation patterns and provide them to our developer community. This demo exhibits hybrid cloud, microservices, and big data analytics concepts that can be reused when building enterprise-level applications on Bluemix.

The following projects are leveraged in the overall Logistics Wizard solution, yet are built to be extensible for other purposes:

* [logistics-wizard-webui][webui_github_url]
* [logistics-wizard-controller][controller_github_url]
* [logistics-wizard-erp][erp_github_url]
* [logistics-wizard-recommendation][recommendation_github_url]

## Code Status

| :point_down: Repositories ... Branches :point_right: | master | dev |
| --- | :--- | :--- |
| [logistics-wizard-webui][webui_github_url] | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-webui.svg?branch=master)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-webui) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-webui/badge.svg?branch=master)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-webui?branch=master) | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-webui.svg?branch=dev)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-webui) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-webui/badge.svg?branch=dev)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-webui?branch=dev)|
| [logistics-wizard-controller][controller_github_url] | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-controller.svg?branch=master)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-controller) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-controller/badge.svg?branch=master)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-controller?branch=master) | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-controller.svg?branch=dev)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-controller) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-controller/badge.svg?branch=dev)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-controller?branch=dev) |
| [logistics-wizard-erp][erp_github_url] | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-erp.svg?branch=master)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-erp) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-erp/badge.svg?branch=master)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-erp?branch=master) | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-erp.svg?branch=dev)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-erp) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-erp/badge.svg?branch=dev)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-erp?branch=dev)|
| [logistics-wizard-recommendation][recommendation_github_url] | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-recommendation.svg?branch=master)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-recommendation) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-recommendation/badge.svg?branch=master)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-recommendation?branch=master) | [![Build Status](https://travis-ci.org/IBM-Bluemix/logistics-wizard-recommendation.svg?branch=dev)](https://travis-ci.org/IBM-Bluemix/logistics-wizard-recommendation) [![Coverage Status](https://coveralls.io/repos/github/IBM-Bluemix/logistics-wizard-recommendation/badge.svg?branch=dev)](https://coveralls.io/github/IBM-Bluemix/logistics-wizard-recommendation?branch=dev)|

## Deploy

To deploy the full system all at once, check out the [Logistics Wizard Toolchain][toolchain_github_url]

## Architecture

![Architecture Diagram](architecture.png)

![Architecture](http://g.gravizo.com/g?
  digraph G {
    node [fontname = "helvetica"]
    rankdir=RL
    user -> controller [label="Makes a request"]
    controller -> erp [label="CRUD SCM data"]
    controller -> recommendations [label="Retrieve/update recommendations" dir="back"]
    {rank=max; user}
    {rank=same; erp -> controller [style=invis]}
    {rank=same; controller -> recommendations [style=invis]}
    user [shape=diamond width=1 height=1 fixedsize=true style=filled color="black" fontcolor=white label="User"]
    erp [shape=rect style=filled color="%2324B643" fontcolor=white label="ERP"]
    controller [shape=rect label="Controller API"]
    recommendations [shape=rect style=filled color="%2324B643" fontcolor=white label="Recommendations"]
  }
)

Visit the [wiki](https://github.com/IBM-Bluemix/logistics-wizard/wiki) for a detailed breakdown of the Logistics Wizard demo architecture and deployment strategy.

## Related Blog Posts, Videos, etc

- [Build a smarter supply chain with LoopBack](https://developer.ibm.com/bluemix/2016/07/11/building-smarter-supply-chain-developer-journey-loopback/)

- [Master continuous integration and delivery with the IBM Devops Toolchain](https://developer.ibm.com/bluemix/2016/08/09/master-continuous-integration-delivery-ibm-devops-toolchain/)

## Project Milestones

The GitHub milestones for this project and its children are managed by editing the [repository config](repository-config.json) file. The syntax is described in [this project](https://github.com/Jimdo/github-sync-labels-milestones). Modify the file and commit. Travis will take care of creating/updating the milestones.

## Contribute
Please check out our [Contributing Guidelines](.github/CONTRIBUTING.md) for detailed information on how you can lend a hand to the Logistics Wizard demo implementation effort.

## License

See [License.txt](License.txt) for license information.

<!--Links-->
[webui_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-webui
[controller_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-controller
[erp_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-erp
[recommendation_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-recommendation
[toolchain_github_url]: https://github.com/IBM-Bluemix/logistics-wizard-toolchain
