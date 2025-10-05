---
title: Free stuff to start your business with
slug: free-stuff-to-start-your-business-with
date_published: 2022-12-29T23:13:11.000Z
date_updated: 2022-12-29T23:13:11.000Z
tags: free, business, docker, codefresh, cicd, google cloud, #Import 2023-03-30 20:40
excerpt: A useful list of free products to get your business off the ground, and spend as little as you can on infrastructure
---

No, this isn't me trying to shill you an online course on how to start your business.

In fact, I am doing the opposite here! I am writing a little list of the free technology (and some slightly paid) that I use to run my tech stack.

This is somewhat of an extension of my previous blog post 
[

What’s behind breadNET

Let’s take a peak behind the scenes at breadNET and see what it takes to keep this well(ish) oiled machine chugging

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1616551569669-b60598758c4f?crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;fit&#x3D;max&amp;fm&#x3D;jpg&amp;ixid&#x3D;MnwxMTc3M3wwfDF8c2VhcmNofDZ8fHRlYXIlMjBkb3dufGVufDB8fHx8MTYxODAyNDM2NQ&amp;ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;w&#x3D;2000)
](__GHOST_URL__/what-it-takes-to-run-breadnet/)
Where I talked about what it takes to run breadNET, how much it costs etc. 

I've since been able to cut my costs down a fair bit, and as the country I reside in is in the middle of a [governmental failure ](https://www.huffingtonpost.co.uk/entry/brexit-cost-uk-government-revealed_uk_63a2d473e4b0a13a950ba3b5)as well as a [Cost of living crisis](https://en.wikipedia.org/wiki/2021%E2%80%93present_United_Kingdom_cost_of_living_crisis). 

Politics aside, lets look at the tech I have found

It's broken down in to 2 parts:

- Pretty much free
- Somewhat expensive

*Pretty much free* is services that cost under $15 a year totally, provided you are happy with their free services. 

*Somewhat expensive* is the services that have a monthly billing cycle, and can get pretty expensive if not done well. 

As the list goes down, it moves from hosting your domain, to code, cicd, storing artifacts and finally hosting a website. 

---

## Pretty much free

### Cloudflare

Cloudflare is a CDN, DNS service and recently a domain registrar. 

As with all of these services, you *can *pay, but I have been using it for YEARS with no worries. 

The nice thing about Cloudflare is if you buy your domain through them, they deal with the DNS for you automatically.

If you didn't purchase it through them you can transfer it to them, and you will see a huge reduction in cost.

My domain used to cost £13 a year, and now has gone to $9 a year. 
[

Cloudflare Registrar | New Domain Registration

Cloudflare Registrar securely registers your domain names. We offer domain names at cost, with no fees or markups. Register new domains or transfer existing domains to Cloudflare Registrar.

![](https://www.cloudflare.com/favicon.ico)Cloudflare

![](https://www.cloudflare.com/static/149f58294a9d0b11de8c0ae35f9590b4/facebook-link-image.png)
](https://www.cloudflare.com/en-gb/products/registrar/)
Cloudflare charge you what they get charged, [their business model isn't selling domains](https://seekingalpha.com/article/4437171-cloudflare-is-much-more-scalable-than-you-think), it's building a CDN network and everything around it.

Below is a list of services they offer

- Domain Registration
- DNS management 
- Zero Trust
- CDN

---

### [Github](github.com)

At a high level, GitHub is a website and cloud-based service that helps developers store and manage their code, as well as track and control changes to their code.

Github is pretty much free, unless you're an absolute code machine and want to flex on your friends, there is no need to hand over payment.

You can create unlimited repositories, have access to 2000 CI/CD minutes a month (that's like an entire day of the job running btw) 

Below is a list of services they offer:

- Unlimited public/private repositories
- Automatic security and version updates
- 500MB of Packages storage
- Creating Organizations and then, unlimited repos

[

Pricing · Plans for every developer

Whether you’re starting an open source project or choosing new tools for your team, we’ve got you covered.

![](https://github.githubassets.com/favicons/favicon.svg)GitHub

![](https://github.githubassets.com/images/modules/site/social-cards/pricing.png)
](https://github.com/pricing)
---

### [Codefresh](codefresh.io/)

Codefresh is my chosen CI/CD provider because it's simple to use, each step is simply a docker image, and it's fast. 

Codefresh's free tier is very generous and allows *1000 cloud credits *(what ever that means) 

It allows you to pretty much make as many pipelines as you wish, with as many  steps as you want.

I use it for building docker images, running terraform and deploying documentation sites... and hopefully in the future this site will be built too.

Below is a list of services they offer:

- CI/CD Pipelines
- Private Helm store
- Private Docker repo
- Full stack testing (they call this composition) 

[

Codefresh | The #1 Argo and GitOps CI/CD Solution

Codefresh is the #1 software delivery platform that brings the best of Argo and GitOps into a single cohesive, scalable, and secure platform.

![](https://codefresh.io/wp-content/uploads/2022/07/cropped-favicon_codefresh_2_512x512-192x192.png)Codefresh

![](https://codefresh.io/wp-content/uploads/2022/08/Open_Graph_Homepage.png)
](https://codefresh.io)
---

### Docker Hub

Moving on from Codefresh, where we build the images, we now need a place to store them.

Docker Hub is pretty much the go to for the average Joe who doesn't have a corporate credit card and unlimited money to use the likes of Google artifact registry. 

Just to clear it up, Docker is the software that uses OCI compliant images, and Docker Inc is the company that made it. 

Docker Hub is where we can store the images we build either Locally, or on Codefresh. 

Docker hub allows 2 free `Private` registries (no one can see them unless invited to) and then unlimited public images ([Example](https://hub.docker.com/r/userbradley/documentation))

Below is a list of services they offer:

- Docker image storage

---

### Fly.io

I recently posted about this company on it's own. 

Fly is awesome if you ask me. They take docker images, host them on either Nomad or turn them in to a *Micro-vm *using [Firecracker](https://firecracker-microvm.github.io).

For free you can run 3 *applications *anywhere in the world. 

I make heavy use of this, like I mentioned previously I plan to re-write this site to be hosted on fly, further reducing my costs.

I host my documentation site on Fly and have had 0 down time since
[

Welcome

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/index.png)
](https://documentation.breadnet.co.uk)
Below is a list of services they offer:

- Hosted Docker ([Requires some fiddling](https://documentation.breadnet.co.uk/cloud/fly/fly-docker-auth/?mtm_campaign=free-stuff-to-start-your-business-with))
- Hosted Applications
- SQL Hosting
- 3 free applications or
- 2 free applications and a builder
- Free URL
- Free SSL Certificates

[

Deploy app servers close to your users · Fly

![](https://fly.io/phx/ui/images/favicon/apple-touch-icon-3e4c9ce127b5cd6f5516638d4bbf1dd5.png?vsn&#x3D;d)

![](https://fly.io/phx/ui/images/livebeats-4fa2c8aa83838b17b5190c9058107baa.png?vsn&#x3D;d)
](https://fly.io)
---

## Somewhat expensive

This section focuses on platforms that you have to pay to use.

Note, that Digital Ocean is a referral link. You get $200 in credit over 60 days, I get a little kickback once you spend $25. You are welcome to not use it, but it helps me bring this content to you <3 

### [Digital Ocean](https://m.do.co/c/77be3c3aa96c)

[Digital ocean](https://m.do.co/c/77be3c3aa96c) is one of the *smaller *cloud providers, they have a different target audience then the next mentioned Google cloud. 

I've been using [Digital Ocean](https://m.do.co/c/77be3c3aa96c) for around 4 years now, and never had any issues. 

They offer everything from Kubernetes to S3 *compliant *storage. 

You can *purchase *a *droplet *from them starting at $4 a month, which is more than enough to run a static site on.
[

Droplet Pricing | DigitalOcean

Helping millions of developers easily build, test, manage, and scale applications of any size – faster than ever before.

![](https://www.digitalocean.com/_next/static/media/android-chrome-512x512.5f2e6221.png)DigitalOcean

![](https://www.digitalocean.com/_next/static/media/social-share-default.e8530e9e.jpeg)
](https://www.digitalocean.com/pricing/droplets)
Below is a list of services they offer:

- [Apps](https://m.do.co/c/77be3c3aa96c)
- [Droplets](https://m.do.co/c/77be3c3aa96c)
- [Functions](https://m.do.co/c/77be3c3aa96c)
- [Kubernetes](https://m.do.co/c/77be3c3aa96c)
- [Volumes](https://m.do.co/c/77be3c3aa96c)
- [Managed Databases](https://m.do.co/c/77be3c3aa96c)
- [Container Registry](https://m.do.co/c/77be3c3aa96c)
- [Compute images](https://m.do.co/c/77be3c3aa96c)
- [VPC](https://m.do.co/c/77be3c3aa96c)

### Google Cloud

I know you're reading this thinking... "[Eh google isn't free](https://www.youtube.com/watch?v=N6lYcXjd4pg)"  and you're *technically *not wrong.

Google actually has a very generous Free tier 
[

Free cloud features and trial offer | Google Cloud Free Program

Discover the free cloud features that come with the Google Cloud trial offer and more information on how to upgrade your account.

![](https://www.gstatic.com/devrel-devsite/prod/vdbc400b97a86c8815ab6ee057e8dc91626aee8cf89b10f7d89037e5a33539f53/cloud/images/favicons/onecloud/super_cloud.png)Google Cloud

![](https://cloud.google.com/_static/cloud/images/social-icon-google-cloud-1200-630.png)
](https://cloud.google.com/free/docs/free-cloud-features)
This has offerings like free compute instances, Big query (analytics) 

If you're planning to use Google clouds free tier, I have some recommendations for you:

- 
Decice what your business is and what it's compute needs are

- 
Try and use Cloud native systems

- This is basically Docker, use docker

- 
Look in to running everything on Serverless

- Cloud Run
- Cloud Functions

- 
Try avoid compute as much as you can

- 
Look at using other services like [Firebase](https://firebase.google.com) for Mobile applications

Also, shameless self plug, but I am a Google certified cloud architect, so like, hit me up if you need some help!
