---
marp: true
paginate: true
theme: default
style: | 
    img[alt~="meme"] {
        display: block;
        margin: 0 auto;
        border-radius: 0%;
        box-shadow: 5px 5px 10px;
    }
    img[alt~="center"] {
        display: block;
        margin: 0 auto;
        box-shadow: 5px 5px 10px;
    }
---

# What Do You Mean My ML Container is Vulnerable?

Ryan Russon
MLOps and AI Utah
May 2023

---

# "You've been working hard on training a great model"



![meme](imgs/just-need-to-deploy.gif)

---

## "Success!"

![meme](imgs/deployed-greatest-model.jpg)

---

## "and then Cyber comes along..."

![meme](imgs/remember-that-model.jpg)

---

## "...and lets you know about some critical vulnerabilities"

![meme](imgs/that-would-be-great.jpg)

---

## "You then might feel like this..."

![meme](imgs/not-my-model.jpg)


---

# Our Journey 👟

* Brief history of the containerization of applications
* The lexicon
* Why containerization in ML?
* The dreaded "CVE"
* Tools and practices for maintaining ML images

---

# The Rise of Containerized Applications

* **2006:** *Process Containers* was launched by Google for limiting, accounting and isolating resource usage
* **2008:** LinuX Containers (LXC) was the first, complete implementation of Linux container manager
* **2013:** Docker debuts to the public at PyCon 2013 in Santa Clara
* **2016:** The imporatance of container security is revealed
* **2017:** Mature container tools, `containerd` and `rkt` adopted by CNCF, and K8s grows up
* **2018:** App development via containerization becomes the "Gold Standard"


source: https://blog.aquasec.com/a-brief-history-of-containers-from-1970s-chroot-to-docker-2016

---

# Remember This?

> *"Eric Riddoch provided one of the best introductions to using Docker containers for Data Science"*

![bg right:50% 100%](imgs/docker-for-data-scientists.png)

---

# Docker Images and Containers: Overview
* **Image:** The binary used as a ***blueprint*** for a specific runtime
* **Container:** The result when an ***image*** is deployed to an environment
* **Orchestrator:** A tool that allows the ***coordination, scheduling and communication*** of deployed containers (e.g. Kubernetes, ECS, Docker Swarm)

---

![bg left:30% 90%](imgs/kubeflow-new-notebook.png)

# Containerization in ML

* Exploratory Data Analysis ➡️ *Jupyter Notebook*
* Model Training ➡️ *PyTorch GPU acceleration*
* Batch Serving ➡️ *Running inference on a schedule*
* Real-time Inference ➡️ *Endpoint on the cloud*

---

![bg right:50% 70%](imgs/docker-pytorch.png)

# Popular ML Images
* `python`
* `pytorch/pytorch`
* `tensorflow/tensorflow`
* `jupyter/scipy-notebook`


---

# CVE?! What is this?

> "CVE, short for **Common Vulnerabilities and Exposures**, is a list of *publicly disclosed* computer security flaws" - *redhat.com*

---

# Vulnerability Scanning Tools

* Trivy
* AWS ECR
* GCP Container and Artifact Registry
* Docker Scout
* Grype

---

# Let's Scan Some Stuff!

Starting with a local scan using `trivy`
```
$ docker pull python:3.9.16
$ trivy image python:3.9.16 --severity CRITICAL,HIGH,MEDIUM -o results.json -f "json"
$ python parse_trivy.py
```

---

# Trivy Results 😱

```
VULN TYPE    SEVERITY      COUNT
-----------  ----------  -------
LIBRARY      MEDIUM            1
OS           CRITICAL         19
OS           HIGH            235
OS           MEDIUM          241
```

---

# Trivy Results (Only Fixable) 😑

```
VULN TYPE    SEVERITY      COUNT
-----------  ----------  -------
LIBRARY      MEDIUM            1
OS           HIGH              5
OS           MEDIUM            2
```

---

# Let's Fix the OS Vulns

> In theory, a simple OS upgrade should fix these

```docker
FROM python:3.9.16

RUN apt-get update
RUN apt-get dist-upgrade -y
```

---

# Survey Says...

```
VULN TYPE    SEVERITY      COUNT
-----------  ----------  -------
LIBRARY      MEDIUM            1
```

---

# What About the Library Vulns?

**CVE-2022-40897** 
```json
"Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-2022-40897",
          "PkgName": "setuptools",
          "PkgPath": "usr/local/lib/python3.9/site-packages/setuptools-58.1.0.dist-info/METADATA",
          "InstalledVersion": "58.1.0",
          "FixedVersion": "65.5.1",
          ...
        }
```

---

# What About the Library Vulns?

```docker
FROM python:3.9.16

RUN apt-get update
RUN apt-get dist-upgrade -y

RUN python -m pip install --upgrade setuptools
```

---

# "Oh yeah!" 🥳

```bash
VULN TYPE    SEVERITY    COUNT
-----------  ----------  -------
```

---


# AWS ECR Scanner 🤔

![center](imgs/ecr-image-scan.png)

---

# AWS ECR Scanner 😟

![center](imgs/ecr-python-scan-cve.png)

---

# Docker Hub Scanner
![w:640 center](imgs/docker-hub-scan-results.png)

---

# What Gives? 🤷

> *"Why do the results of these different scanning systems differ in their results?*

---

# Security Scanners Aren't Created Equally...

![w:800 center](imgs/Malicious%20Compliance.png)

> *From: "Malicious Compliance" https://www.youtube.com/watch?v=9weGi0csBZM*

---

# Where To From Here? 🏔️

* Standardize what scans your organize requires and risk tolerance 
* Set up CI pipelines to scan image builds for vulns
* Practice network security
    * *"Who can get to my container?"*
* Don't run containers as `root`
* What's the remediation process?

---

# Standardize What Scans and Severity

* All scanners aren't the same, the organziation should align
* Risk tolerance: *"Do we allow medium"* vulns? 
* When do scans happen? 

---

# Scan Inside CI Pipelines

![w:640 center](imgs/trivy-action.png)

---

# Network Security

---

# No `root` Access! ⚠️

---

# Remediation Process 🎯

* This is by far the toughest, but most important
* Some vulns are remediated by simple OS updates (e.g. `apt-get update`)
* Others require specific packages to be upgraded (e.g. `log4j`)
* This *can* break your entire environment! ...😏 malicious compliance?
