---
title: Docker it's over, moving to podman
slug: docker-its-over-moving-to-podman
date: 2023-04-19T23:58:13.000Z
date_updated: 2023-08-18T16:22:01.000Z
summary: Docker, we're breaking up! Tips on moving to podman
feature_image: https://images.unsplash.com/photo-1633967920376-33b2d94f091f?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D
---

Docker is cool, don't get me wrong. They pretty much brought containerization to the masses. 

So why the breakup letter? What pushed you over the edge

1. [2017: Licensing changes ](https://boxboat.com/2018/12/07/docker-ce-vs-docker-ee/)
2. [Docker hub pricing changes](https://www.docker.com/pricing/october-2022-pricing-change-faq/)
3. [Malware hosted on docker](https://www.bleepingcomputer.com/news/security/docker-hub-repositories-hide-over-1-650-malicious-containers/)
4. [Price changes 2022](https://www.docker.com/pricing/october-2022-pricing-change-faq/#:~:text=On%20October%2027%2C%202022%2C%20Docker,)%2C%20per%20user%20per%20month)
5. [Docker Desktop pricing](https://www.infoworld.com/article/3630393/docker-desktop-is-no-longer-free-for-enterprise-users.html)
6. [Rate limit](https://docs.docker.com/docker-hub/download-rate-limit)
7. [Docker free teams being sunsetted (and then saying sorry for bad comms, and then actually saying sorry and no longer doing it)](https://www.docker.com/blog/no-longer-sunsetting-the-free-team-plan/)

Sure, most of these above points are about money, but the docker desktop and docker hub ones annoyed me the most

💡

I will get on to installing podman and how to use it later on in this blog
we just need to talk a bit about docker and podman.

Specifically, on mac [(which has 32% market share on devs)](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-operating-system) you can only install docker using the desktop CLI. If you then use it for work, you need to pay.

Of course I am still yet to see Docker Inc take a company to court for not paying for licenses. 

## So why podman? Why switch?

The real reason I switched was because I broke my docker install so much, that it was easier to switch to a new container runtime *thing* on my computer, than it was to try fix it.

Having a search about, I came across a blog from Michael Friedrich
[

Docker Desktop alternatives on macOS: podman, nerdctl, Rancher Desktop

Docker changed its subscription model including Docker Desktop, thus generatingmore demand for alternatives. In this blog post, we look into podman, nerdctl,and Rancher Desktop as Docker Desktop alternatives on macOS. The Docker Desktop subscription changes[https://www.docker.com/blog/updating-…

![](https://dnsmichi.at/favicon.ico)dnsmichi.atMichael Friedrich

![](https://dnsmichi.at/content/images/2022/03/AC6BA369-E613-464F-AEB7-CCA674DC61BE.jpeg)
](https://dnsmichi.at/2022/03/15/docker-desktop-alternatives-macos-podman-nerdctl-rancher-desktop/?utm_source&#x3D;breadnet-co-uk&amp;utm_medium&#x3D;Docker-its-over-moving-to-podman)
One of his suggestions was podman, so I turned away from the spike I was working on (Configuring Hound) and put all the time in to getting podman working on my laptop

# The install process

📬

I am going to assume that you don't need me to explain what podman is and what docker is, if you are reading this post 

For context, I am using an M1 mac - Which requires some additional configuration.

    brew install podman
    podman machine init
    podman machine start

That's pretty much it.

Podman will *hijack* your docker config file, so stuff like authentication to google cloud artifact registry and custom registries are **just going to work**

Something to note is that if you plan to run containers with local volumes, you will need to change your init command to the below

    podman machine init --now --cpus=4 --memory=2046 -v $HOME:$HOME

# I miss things about docker

This is normal, for the past 10 years you've been typing `docker` and `docker-compose`

Firstly we will take care of `docker-compose` as podman has it's own compose tool.
[

GitHub - containers/podman-compose: a script to run docker-compose.yml using podman

a script to run docker-compose.yml using podman. Contribute to containers/podman-compose development by creating an account on GitHub.

![](https://github.com/fluidicon.png)GitHubcontainers

![](https://opengraph.githubassets.com/feddadaf0941e1f1c56e0d8857ead38a124850f7d0dd0f6668371a29e3c8c76a/containers/podman-compose)
](https://github.com/containers/podman-compose)
It's called... `podman-compose`

    brew install podman-compose

### Aliasing stuff

edit your `~/.zshrc` or `~/.bashrc` file and add the below in

    alias "docker"="podman"
    alias "docker-compose"="podman-compose"
    

Then update your source 

    source ~/.zshrc

Any time you invoke `docker` or `docker-compose` it will just be podman sitting back there running for you!

### Podman Desktop

    brew install podman-desktop

![](__GHOST_URL__/content/images/2023/04/image.png)
# What is it actually like to live with?

I have been using podman since the 27th of march, and I have to say I am impressed.

At work, I am the only person using podman, so support is non existant. This also raises a very important factor of adopting podman

> If my team uses docker, can I change with no affect to my productivity

The answer: Sort of

### The good

- It works with google artifact registry using my docker `config.json` file right off the bat
- Docker pulls default to `docker.io/library` so you don't have to change pulling images
- Pulling images from other registries is as you expect, un-changed.

### The not so good

- Configuration is annoying
- Takes a few extra seconds to spin up a container
- Resources are limited by the VM that runs the containers, so lots of running containers = some are slow
- Skaffold does not work

I am going to elaborate on the bad ones, as this is going to be your deciding factor on if you move or not

#### Configuration is annoying

Because of the VM that podman runs containers in, you have to SSH in to the machine, and make the changes in nano or vi/vim. This gets quite annoying after about 3 minutes. 

#### Takes a few extra seconds to spin up a container 

I have not been able to do a side by side comparison (my docker is borked) but running something like the below, just ***feels*** slower. 

    podman run -it alpine /bin/sh

#### Resources are limited by the vm

This is self explanatory. It's actually the same on docker, if you have a look on the docker Desktop app, it's there. The only reason I raise it here is because we're manually setting it, so we see it
![](__GHOST_URL__/content/images/2023/04/image-1.png)
#### Skaffold does not work

Skaffold is this super slick tool that allows you to automate so much
[

Skaffold

Easy and Repeatable Container & Kubernetes Development

![](https://skaffold.dev/favicons/android-192x192.png)SkaffoldWarren Strange, Engineering Director, ForgeRock

![](https://skaffold.dev/featured-background.jpeg)
](https://skaffold.dev)
The issue I have is that it does not work for building docker images, as it requires either the docker daemon or the docker cli

There is an open issue about this, but I think it works, providing you follow the most recent comment from my self
[

Feature Request - Support for podman builder · Issue #8430 · GoogleContainerTools/skaffold

It would be great to have podman in the builders list. I have also tried using podman-docker to fake docker commands to use podman in vain (as expected). ❯ skaffold build Generating tags... - azure…

![](https://github.com/fluidicon.png)GitHubGoogleContainerTools

![https://github.com/GoogleContainerTools/skaffold/issues/8430](https://opengraph.githubassets.com/281d390ecbfd29e95c5012d81a0d1e791974ea590843d0674c4500f7aebde57a/GoogleContainerTools/skaffold/issues/8430)
](https://github.com/GoogleContainerTools/skaffold/issues/8430)
# Wrapping up

- I like podman
- My manager is not sold on it
- Saves the company some [dosh](https://www.urbandictionary.com/define.php?term=dosh)

I plan to use podman as much as I can. I can run everything we have at work through podman and it's fine. If I have issues and need to run more complex stuff, I have a local k3s cluster I can use.
