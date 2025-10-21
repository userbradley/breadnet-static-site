---
title: Mount a GCS bucket to nginx
slug: gcs-web-server-using-gcsfuse
date: 2023-03-05T22:32:00.000Z
date_updated: 2023-07-01T17:14:43.000Z
summary: Mount a GCS Bucket to a pod in kubernetes
tags: ["Kubernetes"]
---

Recently I had to solve a problem where we needed to serve a web page from GCS.

You've probably come here from googling something like:

- How to mount a GCS bucket to a docker container
- How to mount a GCS bucket to a pod
- How to serve a gcs bucket in nginx

I know the Hard core Google cloud engineers among us are screaming

> [Why dont you use a load balancer with a GCS bucket as a backend?](https://cloud.google.com/load-balancing/docs/https/ext-load-balancer-backend-buckets)

This is why: You cant attach Cloud IAP to it.
[

Google Issue Tracker

![](https://www.gstatic.com/buganizer/img/v0/favicon.ico)

](<https://issuetracker.google.com/issues/114133245>)

## The Solution

We have a number of GKE clusters I manage, so the easiest solution was below:

- Mount buckets as file mounts in linux
- whack nginx in front of it
- create a load balancer and enable IAP

## GitHub examples

I put together a repo for you, that has terraform and Kubernetes manifests in to get you up and running
[

GitHub - userbradley/gcs-web-server: Container that allows you to mount a GCS Bucket and serve it via nginx

Container that allows you to mount a GCS Bucket and serve it via nginx - GitHub - userbradley/gcs-web-server: Container that allows you to mount a GCS Bucket and serve it via nginx

![](https://github.githubassets.com/favicons/favicon.svg)GitHubuserbradley

![](https://opengraph.githubassets.com/549a2784b6270b8fcf62f865f6b6d01de2dfb93915f7d575c5f89e0d6e5440d4/userbradley/gcs-web-server)
](<https://github.com/userbradley/gcs-web-server>)
The idea behind this is that you are equipped with all the tools needed in a docker container to run the web server.

All you have to do is put the `html` files you want to serve, in the GCS bucket anywhere, and then the container will serve them.

If you have any issues with this, please don't hesitate to get in contact with me, or open an issue on GitHub
