---
title: Google Artifact Registry Remote Repositories
slug: google-artifact-registry-virtual
date: 2023-07-16T00:28:53.000Z
date_updated: 2023-07-16T00:28:53.000Z
summary: What is the Google Artifact Registry remote repo and how do I use it?
---

Google Cloud in April [created a blog post](https://cloud.google.com/blog/products/identity-security/take-control-your-supply-chain-artifact-registry) about a new part of the Artifact regsitry called `Remote Repositories`

In todays installment, we will look at what they are, why you'd use one, and how to integrate it with your daily workflow.

## What is Artifact Registry

Artifact Registry is the better version of Google Container Registry (gcr.io) which is a place for storing your OCI images. Artifact Registry has more features over [the now deprecated Google Container Registry](https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr)

They are, but not limited to:

- Storing Helm charts
- Storing APT packages
- Storing go and python packages
- Remote repos (this blog post covers this)
- Maven
- KubeFlow Pipelines
- Global storage or Regional
- Security Scanning of images

Unlike the old Google Container Registry, Artifact Registry has a nicer naming schema, making it easier to tell where the images are coming from

    LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG

---

## What is a remote Repository

Google defines this as `A repository that acts as a caching proxy for External public artifact repository` - which in this case, is currently only Dockehub.

In human readable terms, this special repository allows you to have cached images in your google account, that are then delivered at line speed (internal traffic) to GKE clusters, cloud run or anything else. You can also use them on your laptop

## How to create one

You are able to create a virtual Repository through the UI by navigating to the Artifact Registry and clicking `+ CREATE REPOSITORY`

Select `Remote`
![](__GHOST_URL__/content/images/2023/07/image.png)
Alternativly, if you prefer terraform

    resource "google_artifact_registry_repository" "containers" {
      location      = var.region
      repository_id = "breadnet-cache"
      description   = "breadNET Public Image cache"
      format        = "DOCKER"
      mode          = "REMOTE_REPOSITORY"
      project       = var.project
      remote_repository_config {
        description = "docker hub"
        docker_repository {
          public_repository = "DOCKER_HUB"
        }
      }
    }
    

## How to actually use it

Once you have the repository created, you will need to authenticate your local [podman (or docker)](__GHOST_URL__/docker-its-over-moving-to-podman/) to the Artifact Registry.

Click on the repository, then click `Setup Instructions` where a tab will appear with a command similar to the below

    gcloud auth configure-docker europe-west2-docker.pkg.dev

Once this is run, you are able to pull images.

### Official images

    podman pull europe-west2-docker.pkg.dev/breadnet-containers/breadnet-cache/alpine

### User created images

    podman pull europe-west2-docker.pkg.dev/breadnet-containers/breadnet-cache/squidfunk/mkdocs-material

If we have a docker file like the below, we would simply append `europe-west2-docker.pkg.dev/breadnet-containers/breadnet-cache/` to the image name, and it will use the cache

    FROM europe-west2-docker.pkg.dev/breadnet-containers/breadnet-cache/alpine:3.18.2
    
    LABEL org.opencontainers.image.title="Kubectl"
    LABEL org.opencontainers.image.description="A Docker image for Kubectl"
    LABEL org.opencontainers.image.authors="Bradley Stannard <opensource@breadnet.co.uk>"
    
    RUN apk add curl
    
    RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    
    RUN rm -rf /var/cache/apk/*
    
    
    RUN install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    
    RUN rm /kubectl
    
    ENTRYPOINT ["kubectl"]

---

As always, if you have any questions please reach out to me!
