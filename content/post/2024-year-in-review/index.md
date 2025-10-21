---
title: 2024 Year in review
slug: 2024-year-in-review
date: 2024-12-31T20:35:00.000Z
date_updated: 2025-01-02T20:37:50.000Z
summary: 2024, great fun. Broke kubernetes many times, changed careers and big plans for 2025
feature_image: https://images.unsplash.com/1/work-station-straight-on-view.jpg
author: "Bradley Stannard"
---

As 2024 has already come to an end, I thought I should probably write a post as I've not made one in over a year... I thought no better way to round it out with what I've been up to

## Let's start with my personal life

I've moved house to a nice apartment along the river Kennet, with amazing views of the Town. It's a recently built 2 bed apartment so I now have an office, opposed to my desk being *literally* in the middle of the Dining Room/Kitchen/Living room/ Hallway... Fun of a one bed apartment.

I've changed *careers*. I have spent several years of my career as a DevOps/ Cloud engineer and after a few events at work, I thought perhaps I am better suited to security, as it works quite well with my ADHD. That is to say, pushing boundaries, trying to break things and then writing detailed documents on how this happened.

Since writing the [last blog post in 2023](/what-im-running-at-the-end-of-2023/) I've been learning to ride a motorbike too, I started on a Yamaha YZF-R 125, and then in around June I purchased a BMW G310GS, and on my birthday I took it down to Cornwall for a day trip. I've also been on a day trip to [Barry Island](https://en.wikipedia.org/wiki/Barry_Island) which is where Gavin and Stacey was filmed, where I had a great chat with some local bikers who found it hilarious I rode from [Berkshire to Barry](https://www.google.com/maps/dir/Berkshire/Barry+Island,+Barry/@51.6366402,-2.8929707,188791m/data=!3m2!1e3!4b1!4m16!4m15!1m5!1m1!1s0x48769bd8c5af65a3:0xf3d97f73063f8d6d!2m2!1d-1.1853677!2d51.4669939!1m5!1m1!1s0x486e05e4fc7a9865:0xc61cb81f44727466!2m2!1d-3.2688889!2d51.3930556!2m1!1b1!3e0?entry=ttu&amp;g_ep=EgoyMDI0MTIxMS4wIKXMDSoJLDEwMjExMjMzSAFQAw%3D%3D) on the backroads and then went home.

I am hoping to fly out to the united states of 'murica to see a friend and, hopefully, build out a datacenter in a shed.

## Now on to the technology

This year I had the simple plan to move a few things from the cloud, back to on premise.

I used to run the below applications on a few [Digital Ocean Droplets](https://m.do.co/c/77be3c3aa96c), but I've since moved them back

- Monica
- Mealie
- Passbolt
- Grocy
- Snipe IT
- Matomo
- Cloudflared
- Gatus

I've moved them to my home cluster, which I have since moved from K3S to Talos, which I will be writing a blog post about later

![](/content/images/2025/01/F9F8C433-641C-41B7-A04B-DB5A9CBBAD8A_1_102.jpeg)

The above is my 3 node k3s cluster running on ubuntu, plus an additional node running mariadb and NFS exports for Persistent volumes.

Plan is to add 3 more nodes to my *lab* and run a specific OS for Storage, as well as a node with an SSD for Databases. You would be surprised to know, it's more Dell 3040 SFF's

![](/content/images/2025/01/03951064-8924-438D-8268-ED1BD99ED590_1_201_a.jpeg)

The reason I went for the Dell 3040's is, they're cheap, decent CPU's, can take around 16gb of max ram, and the largest SSD you can possibly find. This means you can really get some chooch out of them.

The cluster should eventually be 3 nodes, and one control plane node with scheduling disabled. This means the control plane node can just crack on with working out what's going on in the cluster, and not wasting CPU and Ram on random apps I'm running.

Back in my old apartment, I was running the ISP's default router, which provided great reads like ["Update DNS on EE Router"](https://documentation.breadnet.co.uk/kb/networking/ee-update-dns/) and ["Show Broadband password on EE router"](https://documentation.breadnet.co.uk/kb/networking/show-broadband-password-ee/). For my birthday I decided to *splash the cash,*all £400ish and got a Unifi router, POE Switch, Unifi Access point and a Switch Lite

![](/content/images/2025/01/image.png)

I am so thankful to be off EE internet, and on to *literally* anything else, in this case, Hyperoptic. I'm on, I think, a 150/150 (symmetrical) package which is quite decent as most ISP's in the UK offer pretty decent download speed, then abysmal upload speed. Take EE, offering 150/30. If someone can explain to me, how this is fair then I am all ears

![](/content/images/2025/01/image-1.png)

Now I am on a decent internet package, I am able to host a lot more public services on my connection, as well as actually backup things like photos, documents and files to S3 and it wont take all night.

### Plan to move more on-prem

Currently, there are a few services I still have on [Digital ocean](https://m.do.co/c/77be3c3aa96c) that I plan to migrate

| Service      | 	Plan                                |
|--------------|--------------------------------------|
| Auth Service | Cloudflare Zero                      |
| Ghost Blog   | Kubernetes Ghost blog or Static site |
| Passbolt	    | On prem passbolt                     |

Something I have on fly.io is my [Documentation Site](https://documentation.breadnet.co.uk), which with my plan for my new cluster is to move my Documentation site to my cluster. The idea is that I will run a OCI registry, as well as GitHub actions runner on the cluster to run all my internal CI jobs

---

I'm going to close this post out as I am rambling too much, and leaking too much fun about my new cluster.

I plan to try and post more this year on the blog, as most of my material goes to my [Documentation](https://documentation.breadnet.co.uk) site
