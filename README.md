# Vulnerable ML Containers

## Install Trivy
local installation:

```bash
brew install trivy  # Not required, you can use the aquasec/trivy image
brew install just
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## PyTorch Docker Image
```bash
docker pull python:3.9.16
```

## Scan the Image with Trivy
```bash
trivy image python:3.9.16 -o results.json -f "json"
```

## Parse the Results
```bash
python parse_trivy.py
```