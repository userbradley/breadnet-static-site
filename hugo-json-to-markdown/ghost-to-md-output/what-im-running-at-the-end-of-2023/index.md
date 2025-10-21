---
title: What I'm running at the end of 2023
slug: what-im-running-at-the-end-of-2023
date: 2023-12-27T02:10:59.000Z
date_updated: 2023-12-27T02:10:59.000Z
summary: A quick recap on what I'm running at the end of 2023, and a look to the future of the self hosting lab
---

I'm going to try and do a yearly blog post detailing what I'm running at the end of each year.

This year had some pretty interesting additions to the breadNET stack as well as some changes

- Kubernetes
- Bringing Matomo back home
- More Zero Trust
- DNS fully migrated to cloudflare
- Shutdown a web server
- Using Azure AD for authentication
- Using GCP for cloud offerings

---

I am going to start this post off by managing your expectations, below is what we will cover

- What services I'm running
- What services I plan to run
- What's the hardware
- Why am I relying on the cloud more (and what services)
- What this year cost me
- What's the plan for next year

## What services I'm running

I've really cut down quite a lot of services from a while ago where I was running like 10 services across multiple VM's on my Dell server.

Now I've kept it lean with just a few important services. This covers things up in the cloud as well as on prem
Service nameDescriptionLocationPassboltPassword manager*cloud*pritunl ZeroPassbolt's security*cloud*GhostThis site, a blog*cloud*Snipe-ITIT asset managerOn prem (k8s)GatusStatus page with yaml configk8sPiholeDo you even self host bro?k8smatomoSelf hosted analyticsk8smkdocs site[Personal Documentation site](https://documentation.breadnet.co.uk/?utm_source=main_blog&amp;utm_medium=blog_post&amp;utm_campaign=self_hosting_2023) for all things I need to documentfly.io

### What services I plan to run

Ideally I'd like to get the below up and running in 2024

- Arr Stack: [For downloading Linux ISO's](https://peoplemaking.games/@gamesbymanuel/110667316416843436)
- Jellyfin: Stream the ISO's to TV's
- Grocy (again): Kitchen inventory system (Much to my partners displeasure)
- Some form of web archive system: So when I link to something in my articles, it will never Dead link
- Home inventory Softare: Ability to know what I own and then claim on insurance (adult stuff I know)
- Book Inventory: So I can see how little I read
- Hound: CodeSearch to search across multiple repos across multiple git hosting companies
- Link Shorter: I would like to build my own (with my coding buddy chatGPT) that is K8's native and uses a custom resource definition I will learn
- Monica: Personal CRM system allowing me to be a better friend
- [2fauth](https://docs.2fauth.app): Allows you to manage 2FA codes in a web browser. Only supports sqlite (boo) but does support proxy username headers (woo)

> My beef with sqlite is it's not really a database is it? It's a glorified text file, and it just breaks with nfs3, which means I need to figure out how to get nfsv4 working, and also I can't scale the containers well. If you don't like my take on this, [you can send me an angry email](mailto:breadmaster69@breadnet.co.uk?subject=Sqlite%20does%20suck%20you're%20right&amp;body=Hi%20Bradley%2C%0D%0A%0D%0AI%20was%20going%20to%20write%20you%20an%20email%20full%20of%20abuse%20about%20how%20sqlite%20is%20actually%20amazing%2C%20but%20then%20I%20realized%20you're%20right.%0D%0A%0D%0AI%20just%20wanted%20to%20let%20you%20know%20how%20right%20you%20were%0D%0A%0D%0ALots%20of%20love.)

#### Options for the * inventory

- HomeBox: [I dont want to use SQlite](https://github.com/hay-kot/homebox)
- [Shelf](https://www.shelf.nu): Looks promising, need to see if it has an android app for my scanner, also means I have to self host Supabase

### Whats the hardware

For compute I have 3 Dell SFF PC's that run the K3s cluster
NameRamCPUStoragek3s-01`8gb``Intel(R) Core(TM) i3-6100T CPU @ 3.20GHz`500 SSDk3s-02`8gb``Intel(R) Core(TM) i3-6100T CPU @ 3.20GHz`120 SSDk3s-03`8gb``Intel(R) Core(TM) i5-6500T CPU @ 2.50GHz`120 SSD
If you're wondering why there's a mismatch of CPU, It's because reading is not a strong suit of mine when it comes to Ebay

For what I call Persistence (Eg: Databases, Storing files etc) I have another Dell SFF PC, with 8GB of ram and an `Intel(R) Core(TM) i5-6500T CPU @ 2.50GHz` Processor. This also has around 120GB of storage on an SSD.

### Why are you relying on the cloud

For some things I have to rely on the cloud. Let me explain

At the moment, all my DNS is managed on Cloudflare, who have a very nice simple to use Zero Trust system, which then very nicely integrates with Azure AD (I refuse to call it Entra) - I use Office 365 for my emails as [I migrated off Postfix and Dovecot](__GHOST_URL__/leaving-selfhosted-mail/?utm_source=main_blog&amp;utm_medium=blog_post&amp;utm_campaign=self_hosting_2023) quite some time ago

As far as cloud dependency goes, I'm not using too much

Digital ocean still hosts my Web server (This site), and Passbolt server (Until I migrate this to my home) and GCP is being used for it's Artifact Registry storage as I [store helm charts as OCI objects](https://documentation.breadnet.co.uk/kubernetes/helm/push-chart-to-ar/?utm_source=main_blog&amp;utm_medium=blog_post&amp;utm_campaign=self_hosting_2023) which is then consumed by flux

If you're interested about running k3s at home, then:
[

Kubernetes at home

Ever wondered what it’s like running kubernetes at home? This post tries to answer that

![](__GHOST_URL__/content/images/size/w256h256/2020/06/favicon.png)breadNETBradley Stannard

![](__GHOST_URL__/content/images/2023/11/cluster-top-1.jpg)
](__GHOST_URL__/kubernetes-at-home/?utm_source&#x3D;main_blog&amp;utm_medium&#x3D;blog_post&amp;utm_campaign&#x3D;self_hosting_2023)
The end end end (yes I meant to type that 3 times) goal would be to colocate a server somewhere in the UK, and run all my services off that opposed to at home where it's susceptible to power cuts and terrible UK non symmetrical internet.

## What this year cost me

This year was a year of investment so the upfront costs (capex) are higher than the Operational Costs (opex)

All costs are in GBP (Great Brexit Pounds), and table assumes one year cost
Item nameCostCost TypeRunning totalDigital ocean 3 droplets for 11 months171.56Operational171.56Digital ocean 2 droplets for 1 month13.40Operational184.96Domain renewal14.79Operational199.75Wasabi Cloud Storage52.86Operational252.61Google Cloud0.12Operational252.73New SFF PC's277.98Capital Expenditure530.71New router83.00Capital Expenditure613.71Electricity97Operational710.71Office 365 Account47.52Operational758.23
All in all, this years home labbing cost me £758.23 ($964, €874.01) which could have bought me [3.45 Litres of blood](https://www.nhsbt.nhs.uk/news/change-to-nhsbt-pricing-of-products-in-201718-and-introduction-of-universal-screening-for-hepatitis-e/#:~:text=(from%20%C2%A3120%20to%20%C2%A3124.46%20per%20unit)) or [141 ham subways](https://subway-menu.net/subway-prices-uk#:~:text=%C2%A32.99-,%C2%A35.39,-Italian%20B.M)

🤑

If you'd like to have £1000, start with £2000 and get a home lab

### What's the plan for next year

Without sounding like I use AI to write this (I didn't, which is why it reads so badly), 2024 will be a good year for the home lab.

I plan to migrate another server off of Digital ocean which will save me £67.92 a year (Current price of a droplet at 6 usd +20% tax converted to brexit pounds)

This £70 will probably get eaten up by my partner in the form of food, if I'm being honest.

As always a home lab is meant to be fun and a space to play, but my home lab has turned more in to a home production lab, where we still have the gung-ho of a lab, but with more on the line.

As the lab expands and I move up the country in search of cheaper rent, I plan to custom build a rack for the computers, and get a UPS so they can remain up when I inevitably trip over a power cable, or the power goes out.

Here's to 2023, and the future

_bradley
