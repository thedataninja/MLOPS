# Named Entity Recognition — Model Serving & MLOps

A practical example of packaging a named entity recognition (NER) system for service-based inference.

## Architecture

The repository combines an application API, TensorFlow Serving, containerization, and Kubernetes deployment manifests.

| Component | Purpose |
| --- | --- |
| `intent_entity_detection/views.py` | Flask endpoint that invokes the model and returns JSON predictions |
| `Dockerfile` | Container packaging |
| `kubernetes/deployment.yaml` | Kubernetes deployment configuration |
| `kubernetes/service.yaml` | Kubernetes service configuration |
| `supervisord.conf` | Supervises TensorFlow Serving and Flask processes |
| `run.py` | Application entry point |

## What this demonstrates

- Exposing an NLP model through a service API.
- Separating model serving from request handling.
- Packaging inference services for container-based deployment.
- Defining Kubernetes deployment and service resources.

## Getting started

Review the Dockerfile and Kubernetes manifests for environment-specific settings before running. Configure the model artifacts, container image, ports, and infrastructure for your environment. This repository is a reference implementation; production readiness, reproducible deployment, and benchmark results have not been independently verified.

## Related experience

This repository reflects my interest in production NLP and ML infrastructure. For professional background, see [LinkedIn](https://www.linkedin.com/in/lakhaniashish/).
