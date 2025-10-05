---
title: Showcasing your knowledge
slug: showcasing-your-knowledge
date_published: 2021-12-14T01:01:31.000Z
date_updated: 2022-01-24T13:03:29.000Z
tags: cicd, codefresh, terraform, google cloud, mkdocs, markdown, automation, cli, cloudflare, cool stuff, docker, git, Getting Started, How To, ssh, #Import 2023-03-30 20:40
excerpt: Scratching your head isn't the best way to show recruiters what you know... Portfolios are
---

Being in IT is... *fun*

As with any job, you naturally move around and, if you're in IT, the second you open Linkedin to recruiters, 10,000 recruiters will blow your inbox up trying to get you. And boy, do they harass you! Wow.

See, I've had my fare share of interviews, and I know what I want (cough slack cough jira), and don't want - Windows. 

So in order to speed up the process of recruiters talking to me, and also to have a place to showcase my work, I decided it was a cool idea to make a `readme.md` file almost, detailing what I do, past work and past projects.

Enter: [bradley.breadnet.co.uk](__GHOST_URL__/showcasing-your-knowledge/bradley.breadnet.co.uk)

Now this site looks pretty simple, and really, it is. But the magic is how it's come to exist.

(recruiters get out your bingo sheet)

---

## Mkdocs

Mkdocs is the platform on which the site is built, this is a project based documentation platform that renders `md` files in to a static site. 
![](__GHOST_URL__/content/images/2021/12/image-3.png)
I decided to go with this over something like Hugo was simple: I find Hugo overly complicated for what it is, and there is a lack of flexibility if you don't know a reasonable amount of WebDev, then it's just lost
![](__GHOST_URL__/content/images/2021/12/image-4.png)
It's SUPER simple to develop with, you just write a config file and then boom bow, run `mkdocs serve` and you can see the live site

## Git

Seeing as all the files are `.md`, it only makes sense to store this all in Github. 

Now here's the catch. What we've done is build a Codefresh Pipeline ([Same things used for terraform](__GHOST_URL__/dns-terraform-cloudflare/)) that on a commit, builds the site and then deploys it. 

## Docker

Now we have the pipeline running, we mentioned that it 'Builds the site' - This is managed as a docker container. This has to be the most simple docker contaier in the world...

    FROM nginx:alpine
    COPY site/ /usr/share/nginx/html

That's it! 

This docker container is then pushed to [gcr.io](https://cloud.google.com/container-registry/) for a later stage!

We also use docker for building the site, as there is a mkdocs docker container. If you're new to the world of cicd, most things need to run as a container in order to be used on a cicd pipeline!

## Terraform

This is the 'later stage'
To be able to host this site as cheaply as possible, I've selected to run on [google cloud run](https://cloud.google.com/container-registry/), which is a super pain free means to running simple containers in production, and scale automatically.

Terraform uses the git commit ID as the container ID, and variables for what to deploy. This is actually pulled from the Codefresh Pipeline

## CICD

Here's the coolest part I think!

The pipeline looks like below
![](__GHOST_URL__/content/images/2021/12/image-5.png)
Mkdocs build, docker build and deploy are the coolest parts.

mkdocs build connects to the local volume codefresh presnets, builds the static files to a directory, then the docker build pulls these files over, build the container and automatically pushes to GCR! 

Finally the deploy steps are as you'd expect. The first one deploys to terraform, then the second one copies the files to my webserver where you've probably visited at some point! 

---

## The coolest part?

Everything is managed as code.

This includes but not limited to:

- GCP API Enablement
- GCP Service account creation
- DNS Config
- Site
- Docker Containers
- Pipeline setup

---

Closing notes:

The best way that I've seen to present your knowledge to recruiters as well as companies etc, is a site! I've got more comments about my site and my portfolio than my CV, as you're boxed in to this one page paradox where you're expected to **only **fill out a page, and miss things!

A good example of this, is the skills matrix on the home page, this shows anyone what I know, and how well!
![](__GHOST_URL__/content/images/2021/12/image-6.png)
This is also a really good project to learn cloudrun, terraform and CICD - And the best part is you have an actual end product that you can use, and present to people! If you want to have a crack at it, you can find a "Homework" assignment at the link below
[

GitHub - bysd-project/portfolio-assignment

Contribute to bysd-project/portfolio-assignment development by creating an account on GitHub.

![](https://github.githubassets.com/favicons/favicon.svg)GitHubsd-project

![](https://opengraph.githubassets.com/8f004369117ca694b11fe0ba282659c57304c8e7c266273442ee7a8d6acf4f9a/bysd-project/portfolio-assignment)
](https://github.com/bysd-project/portfolio-assignment)
---

So I've added the ability to subscribe to my site... I know no one will, but I thought I would try and let yall enjoy it? It will just be a link to the latest post! 
