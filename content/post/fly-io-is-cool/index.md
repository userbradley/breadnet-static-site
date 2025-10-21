---
title: Fly.io is cool
slug: fly-io-is-cool
date: 2022-11-24T17:52:23.000Z
date_updated: 2022-11-24T17:52:23.000Z
summary: Looking at an easier way to host static sites? Fly.io has you covered!
---

This is not a sponsored post, but I wont say no to being sponsored in the future!

Since last month I have migrated completely off Bookstack and now 100% on mkdocs. You can read more about that below
[

Migrating from BookStack to Mkdocs

Saying good bye to BookStack 👋 (for now)

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1457694587812-e8bf29a43845?crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;fit&#x3D;max&amp;fm&#x3D;jpg&amp;ixid&#x3D;MnwxMTc3M3wwfDF8c2VhcmNofDEyfHxkb2N1bWVudHxlbnwwfHx8fDE2NjQ0NzM2OTM&amp;ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;w&#x3D;2000)
](/migrating-off-bookstack/)
The TL;DR of that is:

- Easier management
- Better caching
- More secure
- Better Uptime

Now I've added the last one in, as it's what we're going to talk about today

# The internet when I die

I am by no means a god, but when I eventually croak over and pass on, my credit cards, computers and other assorted belongings will probably be disposed of.

With this, goes all my Knowledge on Cloud, Linux and all the other assorted things I learnt in my life time.

That's a huge great waste!

I've spent many hours optimizing this site so that the Opensource community and those who are looking for things, can find it! There's nothing worse than clicking a bookmark and then it comes back with the all too familiar *This site cant be reached*
![](/content/images/2022/11/image.png)

# What's your point

The abstract point, is that running my documentation site on a server that constantly needs to be poked to work, and systematically restarting nginx because the control process exited, is a joke.
[

nginx Failed because the Control process exited - breadNET Documentation

breadNET Documentation

![](https://breadnet.co.uk/favicon.ico)logo

![](https://trace-agent.breadnet.co.uk/matomo.php?idsite&#x3D;17&amp;rec&#x3D;1)
](<https://documentation.breadnet.co.uk/kb/nginx/nginxservice-failed-because-the-control-process-exited/>)
At work I support applications that the Business rely on, so why can't I do the same thing here?

This is where Fly.io comes in...
[

Deploy app servers close to your users · Fly

![](https://fly.io/phx/ui/images/favicon/apple-touch-icon-3e4c9ce127b5cd6f5516638d4bbf1dd5.png?vsn&#x3D;d)

![](https://fly.io/phx/ui/images/livebeats-4fa2c8aa83838b17b5190c9058107baa.png?vsn&#x3D;d)
](<https://fly.io?utm_source&#x3D;breadnet_co_uk&amp;utm_campaign&#x3D;fly-io-is-coo>)

# What is fly.io

Fly pitch them selves as:

> __Purpose Built cloud__
>
> We run physical servers in cities close to your users. As close to the metal as you can get without paying shipping.

And boy do they mean it!

They run on servers (duh) but then on top of that, they run both:

- Nomad; for the containerized workloads
- [Firecracker MicroVm's](https://firecracker-microvm.github.io) for the Compute workloads you want to run

They lower the barrier to entry by using [BuildPacks](buildpacks.io/) to get your code up and running in a matter of minutes.

They allow you to have 3 free applications, in as many [regions](https://documentation.breadnet.co.uk/cloud/fly/fly-regions/) as you want!

You get given a Fly domain to use, but you can just as easily point your existing DNS to the application and call it a day!

# Why are you telling me about this

Basically; I have migrated my mkdocs site from running on my Ubuntu server in London ([actually in Slough I just found out](https://www.equinix.co.uk/data-centers/europe-colocation/united-kingdom-colocation/london-data-centers/ld5)) to being in the UK as well as Texas!

I am able to get latency in the USA down from around 2 __seconds__ for the page to paint, to around **400ms!**(This is also using Cloudflare's caching, but still)

The deployment process is a lot easier too, as we are building the site as a docker image, uploading it to their Private registry and then turning it in to a Micro VM!

Like I mentioned last time, I am using a Codefresh Pipeline to easily deploy the site
![](/content/images/2022/11/image-1.png)
So a break down of the pipeline

1. Clone the repo
2. a. Set the API Token ENV var b. Set robots.txt on dev site if branch is dev
3. Build a docker image and push it to Dockerhub
4. Build a docker image and push it to Fly.io's registry
5. Run the flyctl command line to update to the latest version of the container

All the Public images can be pulled from: [userbradley/documentation](https://hub.docker.com/r/userbradley/documentation)

I've been able to speed up the time it takes for the site to build and then become live from around 1:30 to 55s.

## Issues I had to overcome

As with anything, there's always issues.

I found that there is not a huge user base on Fly.io, so you really need to read the documentation!

One of them was how to Authenticate to their Docker registry to push my images, as they don't really tell you how to do it out of using their command line tool
[

Authenticate to Fly docker Registry - breadNET Documentation

breadNET Documentation

![](https://breadnet.co.uk/favicon.ico)logo

![](https://trace-agent.breadnet.co.uk/matomo.php?idsite&#x3D;17&amp;rec&#x3D;1)
](<https://documentation.breadnet.co.uk/cloud/fly/fly-docker-auth/>)
The other one was a known bug around scaling.
[

Fly regions and scaling - breadNET Documentation

breadNET Documentation

![](https://breadnet.co.uk/favicon.ico)logo

![](https://trace-agent.breadnet.co.uk/matomo.php?idsite&#x3D;17&amp;rec&#x3D;1)
](<https://documentation.breadnet.co.uk/cloud/fly/fly-regions/#solution_1:~:text&#x3D;config%20%3Cenv%3E.toml-,Not%20set,-You%20will%20see>)
---

# Wrapping up

If you are looking at running a static site, I highly recommend Fly.io. It took me around 40 minutes to get everything up and running, and serving traffic.

If you get stuck on anything, please reach out to me!

---

> Disclaimer, this blog post is not sponsored, but if you want to sponsor it, I wont say no!
>
> That being said, everything here is my own opinion.
