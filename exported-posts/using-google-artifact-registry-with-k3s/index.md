---
title: Using Google Artifact Registry with k3s
slug: using-google-artifact-registry-with-k3s
date: 2023-03-15T00:01:12.000Z
date_updated: 2023-03-30T22:01:44.000Z
summary: Authenticate K3S to Google Artifact Registry
tags: ["Kubernetes"]
---

It's been a while since we've done a post about truly self hosted stuff. This is in part due to me being a DevOps engineer.

That aside, today I aim to solve the problem of how to authenticate a k3s cluster to Google Artifact Registry

## Why we need to do this

Google has a really good Container registry, called [Artifact Registry](https://cloud.google.com/artifact-registry). I am hosting all of my images on the container registry as it allows better IAM control, as well as being easier to authenticate to when using GKE.

Why bother mentioning GKE? Well I spend about 90% of my day working on GKE, so it makes sense that I would use a Google Cloud service for this.

## What is the actual issue

Unless your GAR (Google Artifact Registry) repo is public, then you have to authenticate to it.

If we try and pull an image on our k3s cluster without authentication we get the below error

     ErrImagePull: rpc error: code = Unknown desc = failed to pull and unpack image "europe-west2-docker.pkg.dev/breadnet-container-store/redacted/documentation-dev:0.0.1": failed to resolve reference "europe-west2-docker.pkg.dev/breadnet-container-store/redacted/documentation-dev:0.0.1": failed to authorize: failed to fetch anonymous token: unexpected status: 403 Forbidden

This is basically saying, you've not told me who you are, I am not letting you in.

In order to resolve this, we need to authenticate k3s to Google Cloud.

## How to fix this

I wont go in to detail on the GCP cloud side, as if you've come across this I assume you know how to do the below but:

1. Create a Service account
2. Export the Service account keys to your computer as a json file (hold on to this, we need it later!)
3. Add that service account to the Google Artifact Registry using `Artifact Registry Reader`

### Formatting the Service account file correctly

In order to provision the *custom* registry in k3s, we need to authenticate to it.

The json file needs to be *stacked* or converted to a single line.

This can be done by going to the end of each line, and deleting the new line. Example is below

    {
      "type": "service_account",
      "project_id": "redacted",
      "private_key_id": "redacted",
      "private_key": "-----BEGIN PRIVATE KEY-----\nredacted\n-----END         PRIVATE KEY-----\n",
      "client_email": "k3s-container-puller@redacted.iam.gserviceaccount.com",
      "client_id": "redacted",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/k3s-container-puller%40redacted.iam.gserviceaccount.com"
    }

Becomes

    { "type": "service_account", "project_id": "redacted",  "private_key_id": "redacted",  "private_key": "-----BEGIN PRIVATE KEY-----\nredacted\n-----END PRIVATE KEY-----\n",  "client_email": "k3s-container-puller@redacted.iam.gserviceaccount.com",  "client_id": "redacted",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/k3s-container-puller%40redacted.iam.gserviceaccount.com"}

Ignore the formatting, if you copied and pasted this, it would be on one line
We are then able to creat the `registries.yaml` file

    # registries.yaml
    mirrors:
      europe-west2-docker.pkg.dev:
        endpoint:
          - "https://europe-west2-docker.pkg.dev"
    configs:
      europe-west2-docker.pkg.dev:
        auth:
          username: _json_key
          password: '{ "type": "service_account", "project_id": "redacted",  "private_key_id": "redacted",  "private_key": "-----BEGIN PRIVATE KEY-----\nredacted\n-----END PRIVATE KEY-----\n",  "client_email": "k3s-container-puller@redacted.iam.gserviceaccount.com",  "client_id": "redacted",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/k3s-container-puller%40redacted.iam.gserviceaccount.com"}'

> Note!
> Ensure that you surround the value for `password` with `'` or it will brea

Name this `registries.yaml`

Copy this file to **all workers** (and servers if pods can be scheduled on them)

Put the file in `/etc/rancher/k3s`

You will then need to restart `k3s`

    systemctl restart k3s

# Further reading

This blog post was made off of a documentation page I wrote
[

K3s private registry using Google Artifact Registry - breadNET Documentation

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/kubernetes/k3s/k3s-private-registry-using-google-artifact-registry.png)
](<https://documentation.breadnet.co.uk/kubernetes/k3s/k3s-private-registry-using-google-artifact-registry/?mtm_campaign&#x3D;breadnet&amp;mtm_kwd&#x3D;private-reg>)
