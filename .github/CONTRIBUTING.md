# Contributing to Logistics Wizard

A preliminary thank you for contributing to our demo! :tada:

The following is a set of guidelines for contributing to the Logistics Wizard application and related services. This document is meant to detail the guidelines for contributing to our effort. These are not hard and fast rules, but should be considered before spending time on an Issue or Pull Request.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Where can I contribute?](#where-can-i-contribute)
- [How can I contribute?](#how-can-i-contribute)
  - [Filing a Bug Report](#filing-a-bug-report)
    - [Template for Bug Reports](#template-for-bug-reports)
  - [Requesting an Enhancement](#requesting-an-enhancement)
    - [Template for Enhancement Requests](#template-for-enhancement-requests)
  - [Making a Pull Request](#making-a-pull-request)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Where can I contribute?

Before diving in, consider that the Logistics Wizard codebase is more than just this repository. The demo is comprised of mutliple, loosely-coupled services, each reusable in its own right. Check out [the list of services in our wiki](https://github.com/IBM-Bluemix/logistics-wizard/wiki/Services) and carefully consider which one is of interest to you and how you would go about improving it.

## How can I contribute?

There are so many ways to lend a hand I would run out of fingers counting them on my two hands. This section will walk you through the ways in which you can contribute.

First thing's first, download and install [ZenHub for GitHub](https://www.zenhub.io/). This is the tool we use for managing our GitHub Issues and moving them along the pipeline, from Backlog to Closed. It really is a great tool and we recommend using it in any of your projects. Plus, it is free for public repos!

We use four different scopes for managing project work: bugs, enhancements, stories, and epics. Now that you've got the tools, there are three main ways that you can contribute by filing a bug report, a request for enhancement, or making updates and creating a pull request (our favorite). They are each outlined in more detail below.

### Filing a Bug Report

The easiest way to lend a hand is to let us know when you've found a bug in the demo! Here are the steps you should take once you've found a bug and would like to file a report:

1. [Check the existing Issues](https://github.com/IBM-Bluemix/logistics-wizard/issues) and make sure that the bug you've found has not already been reported
2. Create a new issue and make sure to include the following:
	- Clear and descriptive title
	- Steps to reproduce the problem
	- Expected behavior
	- Actual behavior
3. Apply the proper labels, using the [Labels wiki page](https://github.com/IBM-Bluemix/logistics-wizard/wiki/Labels) as a reference

That's it! We will do our best to fix the bug as soon as humanly possible and keep you informed on its progress.

#### Template for Bug Reports

```
[Short description of problem here]

**Reproduction Steps:**

1. [First Step]
2. [Second Step]
3. [Other Steps...]

**Expected behavior:**

[Describe expected behavior here]

**Observed behavior:**

[Describe observed behavior here]

**Screenshots and GIFs**

![Screenshots and GIFs which follow reproduction steps to demonstrate the problem](url)

**Release version:** [Enter Logistics Wizard version here]
**OS and version:** [Enter OS name and version here]
**Browser and version:** [Enter browser name and version here]
```

### Requesting an Enhancement

If you like the app and want to suggest an improvement without doing the leg work, that's alright. Just follow the steps below to file a request for enhancement:

1. [Check the existing Issues](https://github.com/IBM-Bluemix/logistics-wizard/issues) and make sure that the enhancement you are requesting has not already been made.
2. Create a new issue which describes your enhancement request in detail
3. Apply the proper labels, using the [Labels wiki page](https://github.com/IBM-Bluemix/logistics-wizard/wiki/Labels) as a reference

The Logistics Wizard delivery team will review your RFE and turn turn it into a story or epic, depending on the scope we determine. There is no guarantee that we will take on the RFE, but we will do our best

#### Template for Enhancement Requests

```
[Short description of enhacement]

**Steps which explain the enhancement**

1. [First Step]
2. [Second Step]
3. [Other Steps...]

**Current and suggested behavior**

[Describe current and suggested behavior here]

**Screenshots and GIFs**

![Screenshots and GIFs which demonstrate the steps or part of Logistics Wizard that the enhancement suggestion is related to](url)

```

### Making a Pull Request

If you see an issue you would like to tackle yourself, we certainly welcome code contributions. Here are the steps we suggest taking in order to have the best chance of your PR being accepted:

1. Make sure the issue is not already being worked on. You can ensure this by checking if the issue has been moved to the `To Do` pipeline and beyond.
2. Comment on the issue to let the delivery team know you are addressing it.
3. Fork the repo from the `dev` branch and make your code changes.
4. Create a pull request on `dev`, making sure to include the following:
	- reference to the issue(s) your PR addresses
	- screenshots and animated GIFs whenever possible

We will accept and merge your PR as soon as we can! Feel free to give us a little @ nudge if you see it taking a little while.
