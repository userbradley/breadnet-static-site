---
title: What's behind breadNET
slug: what-it-takes-to-run-breadnet
date: 2021-04-10T03:15:01.000Z
date_updated: 2023-03-26T14:42:13.000Z
summary: Let's take a peak behind the scenes at breadNET and see what it takes to keep this well(ish) oiled machine chugging
---

Ever since I read "[The architecture behind a one man SaaS](https://anthonynsimon.com/blog/one-man-saas-architecture/?utm_source=breadnet.co.uk)" and "[Tools and services I use to run my SaaS](https://jake.nyc/words/tools-and-services-i-use-to-run-my-saas/)" I thought it would be cool to write about what powers breadNET and how I have things setup!

### Let's start

We will first take a look at what  breadNET is, as the about breadNET page is pretty bad and is pending a re-write.

breadNET (Yes, it's typed like that) started as my home lab project and business venture where I would host FOSS software like Kanboard, Bookstack, Jellyfin, passbolt etc. Basically the stuff I use day to day. Sadly this never took and another company came in and took this opportunity, gap in the market if you will, and did a pretty good job of it. Kudos!

> You can still by all means contact me to have me host these things for you for the cost of the server! Contact me via email or linkedin or what ever and we can work something out!

From there I decided just to change the site to a blog as for my job (just like everyone who works in IT) I spend a lot of time on google, and wanted to give back to the communities who rely on resources for help with things.

Enough chit-chat, let's dive in!

---

We will break this down in to a few categories:

- Hosted solutions
- Config management
- Servers and Software
- Backups
- Logging/ Monitoring
- Applications
- Cost
- Workflows

---

## Hosted Solutions

There are things that are just not best to host your self when you're looking for the best uptime avalible.

**[Coudflare](https://cloudflare.com)** : DNS and DDOS protection

[**Digitalocean**](https://m.do.co/c/77be3c3aa96c) : VPS hosting for mail server and web server (Highly recommend)

**[OVH](https://ovh.com)** : Internal app hosting

**[Codefresh](https://codefresh.io/)** : Ci/Cd pipelines

[**Terraform** cloud](https://app.terraform.io/) : Remote state for Terraform

**[Wasabi](https://wasabi.com)** : S3 compliant backups for cheap (but **very** reliable)

**[Namecheap](https://namecheap.com)** : Really good pricing for domains and my GO TO for anything domain related (Except DNS)

## Config Management

This is the bane of my existence. In my ideal world anything I do I should be able to delete it and have it up and running again on Monday. (Let's be honest, this is more around me messing something up lol)

> "Even if you lose all one day, you can build all over again if you retain your calm!" - Thuan Pham, former CTO of Uber.

[**Terraform**](/p/d7793028-b3c3-4e8d-9f01-1bee7fb2d34f/terraform.io/) :  This is what I use for creating cloud deployments, all the way from a load balancer to a database as a service, terraform can do it

[**Ansible**](https://www.ansible.com) : This is what I use for provisioning my servers and getting them up to operating standards. Also use it on a cron job to keep all my servers up to date.

[**Gitlab**](https://gitlab.breadnet.co.uk/explore/) : This is where all my code lives. I don;t know why I use this over github, but I like it :)

## Servers and software

This little section is about the servers and software that power this place

**Ubuntu** : The choice OS for any server I deploy. This is what I grew up with, and this is what I know very well.

**nginx** : Once again, this is what I grew up with and know well. This powers EVERY web server I have ever deployed. Unless it's apache then that wast me!

**mariadb** : This is my go to database engine for any database that I require. If an application allows me to use mariadb, you bet I will use it!

**rclone** : This is an important piece of software I use for synching data between many different services, s3, drive, gcs etc...

**intelliJ** : This is the most beautiful IDE I have ever used, strongly recommend

**direnv** : Allows setting environment variables per directory, great for terraform and projects that need env variables

## Backups

This is the most important part of any business or lab. Without backups, nothing is really important.
![](/content/images/2021/04/image-3.png)
I follow the 3-2-1 rule, and I suggest you do!
The off site backups are designed to be used if something was to [burn down](https://www.reuters.com/article/us-france-ovh-fire-idUSKBN2B20NU)or the [backup generators not actually doing what they're meant to](https://www.datacenterknowledge.com/archives/2012/07/03/multiple-generator-failures-caused-amazon-outage) or [routers just going "nah bro"](https://www.zdnet.com/article/it-wasnt-just-you-why-google-suffered-widespread-outages/) - Okay, I'm done shitting on the cloud proving why you should have many backups!

[**backuppc**](<http://backuppc.sourceforge.net) : I know, the site looks bad and the UI is old, but boy does this software haul ass. Highly reccomend

**S3** : See Wasabi from Above

[**Raspberry pi and a harddrive and a solid connection**](https://www.youtube.com/watch?v=fC7oUOUEEi4): This serves as the UK backup location

## Monitoring/ Logging

This is one of those things that are often overlooked, but when shit hits the fan things go wrong, being able to look at a graph and point to a spike and go "yeah that's fucked broken" really helps, especially if you're able to then dial down in to each service and see what's happening.

[**Zabbix**](/what-it-takes-to-run-breadnet/zabbix.com) : Providing agent metrics, mtr, snmp and everything I can jam in to it, in one place as well as alerting

[**Datadog**](https://www.datadoghq.com) : Monitoring for cloud environments, little pricey but free tier is DECENT

[**libreNMS**](https://www.librenms.org) : as I move all resources to the cloud, this will be decommissioned, but really good for network monitoring where Zabbix just wont cut it.

**Elastic stack** : Coming soon! (I think?)

## Applications

This is the stuff I use day to day, and will happily host for you if you pay me to do it.

- Ghost

- This is what runs my beautiful site

- Bookstack

- KB and how to articles

- Gitlab

- Source code and config managemnt lives here

- Jira

- Project managment software and a good attempt to organize my life

- Jellyfin

- Media server for all my legally sourced movies

- Grocy

- Manages my food

- firefly-iii

- Manages and makes me feel bad for spending money

- Passbolt

- Password manager

- Matomo

- Provides website analytics

- AWX

- Ansible tower for server stuff and updates

## Cost

I've never done an exact break down but a rough estimate would look like
ItemCountCostOccurrenceTotal MonthlyTotal YearlyDigital Ocean Droplet2$5Monthly$10$120OVH Instance3£2.99Monthly£10.76£129Wasabi Storageidk($6 to 12) let's say $9Monthly~$9$108
So all in all, it costs me around about £295 at the time of writing this
*(April the 10th at 3:33am like an idiot, my (new) girlfriend will be here in like 8 hours and this is what I decide to do... let's see how long she can survive seeing someone who works in IT and takes their hobbies very very seriously)*

Now the reason I don't know about Wasabi is due to it being how much I use and delete per month. They don't charge upload and download so I can do that as much as I want, more so for storage and if you delete 1TB tomorrow, you pay for that TB for 3 months. Eh, sucks but i'm yet to find a better offering that is so simple.

## Workflows

This is a strange one to write about as I am constantly learning new technology and moving things around, but let's look at an example that we're currently working on!

Moving my sheeeet to the cloud!

(shameless self plug below)
[

breadNET Cloud Migration

How did I move all my servers to the cloud? Well - Ansible, automation and CI/CD!

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1560182413-53772f3d7134?ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;fm&#x3D;jpg&amp;crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;w&#x3D;2000&amp;fit&#x3D;max&amp;ixid&#x3D;eyJhcHBfaWQiOjExNzczfQ)
](**GHOST_URL**/cloud-migration-part-1/)[

Moving to the cloud: Infrastructure

Part 2 of moving to the cloud - Let’s talk about IaC

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1555066931-4365d14bab8c?crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;fit&#x3D;max&amp;fm&#x3D;jpg&amp;ixid&#x3D;MnwxMTc3M3wwfDF8c2VhcmNofDEzfHxjb2RlfGVufDB8fHx8MTYxNzUwMzcyMA&amp;ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;w&#x3D;2000)
](**GHOST_URL**/moving-to-the-cloud-2/)
I have decided that I want to be able to simply deploy DNS records with minimal pain and agg, and to do this it would be best to do it though Terraform and then if I hadn't over complicated it enough, decided to automate the process of actually deploying it!

For this I have used Terraform, Gitlab and Codefresh
![](/content/images/2021/04/breaddns.png)
Below is an example of the codefresh.yml

    version: '1.0'
    stages:
      - checkout
      - prepare
      - deploy
    steps:
      main_clone:
        title: Cloning main repository...
        stage: checkout
        type: git-clone
        repo: '<bang your repo url here>'
        revision: master
        git: gitlab
      SetupAuth:
        image: alpine:3.9
        title: Configuring Auth
        stage: prepare
        commands:
          - export TF_VAR_cloudflare_email=$CLOUDFLARE_EMAIL
          - export TF_VAR_cloudflare_api_key=$CLOUDFLARE_API_KEY
      DeployWithTerraform:
        image: hashicorp/terraform:light
        title: Deploying Terraform plan
        stage: deploy
        commands:
          - terraform init -backend-config="token="$token""
          - terraform apply -auto-approve

<https://gitlab.breadnet.co.uk/cicd/terraform/-/blob/master/codefresh.yml>
Second workflow would be creating infrastructure for a deployment
![](/content/images/2021/04/Terraform-deployments.png)
This way I ensure that terraform is uniform, and where the module already exists, I don't have to fart around with some strange issues.

Future plans are to fully opensource all code I write and move any secrets to environment vars so modules can be used anywhere!

My end goal here is to have everything under git control and cicd so I just describe something as code and then boom, it appears 3 minutes later.  

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
