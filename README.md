# Vulnerable ML Containers

## Install Trivy
local installation:

```bash
brew install trivy
```

## PyTorch Docker Image
```bash
docker pull nvcr.io/nvidia/pytorch:23.01-py3
```

## Scan the Image with Trivy
```
trivy image nvcr.io/nvidia/pytorch:23.01-py3
```