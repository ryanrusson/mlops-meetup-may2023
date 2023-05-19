# pull and scan the base python image
demo:
    docker pull python:3.9.16
    trivy image python:3.9.16 --severity CRITICAL,HIGH,MEDIUM -o .cache/results.json -f "json"
    python parse_trivy.py

# scan only for fixable vulnerabilites
demo-fixable:
    docker pull python:3.9.16
    trivy image --severity CRITICAL,HIGH,MEDIUM --ignore-unfixed python:3.9.16 -o .cache/results.json -f "json"
    python parse_trivy.py

# attempt to remediate "fixable" OS vulns
demo-os-fix:
    docker build -t python:osfix -f ./Dockerfile.os --load .
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/code/mlops-meetup-may2023/.cache/:/root/.cache/ aquasec/trivy:0.41.0 image --severity CRITICAL,HIGH,MEDIUM --ignore-unfixed python:osfix -o /root/.cache/results.json -f "json"
    python parse_trivy.py

# attempt to remediate "fixable" library vulns
demo-lib-fix:
    docker build -t python:libfix -f ./Dockerfile.lib --load .
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/code/mlops-meetup-may2023/.cache/:/root/.cache/ aquasec/trivy:0.41.0 image --severity CRITICAL,HIGH,MEDIUM --ignore-unfixed python:libfix -o /root/.cache/results.json -f "json"
    python parse_trivy.py
