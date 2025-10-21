---
title: Introduction to home-labbing
slug: homelab
date: 2020-06-12T17:27:33.000Z
date_updated: 2021-05-02T01:47:26.000Z
summary: A quick intro on a home lab and the minimum to set one up
---

Hello, welcome. Settle down as we're about to take a dive in to the topic of Homelabs, selfhosting and how to break in to Linux administration.

A little about me: I am by no means a professional writer or programmer. I do however use linux as part of my day to day job and as my daily driver.

---

The objective here is to look at:

- The server
- Building the server
- Building infrastructure
- Building a VM
- Hosting something
- Monitoring
- Backups (Most important part)

Now you know what to expect from this, let's start.

Basic hardware I suggest:

An 8 port gigabit switch
Computer that can run all the time
15/5 connection (stable internet is nice to have)

As long as you have a computer that you can run a virtual machine in, it's a lab. Don't worry about what others think. It's your lab, for you.

---

## The server

Depending on what purpose your lab servers, this will be the most important part of your lab. I suggest a budget of around £1500 ($1878.34) for everything.

### Where to get parts from

Depending on what you're looking for, you can build a server from off the shelf parts, the same parts you would use to build a computer. Just ensure that those parts are rated for 24/7/365 operation.

I chose to purchase pre-built rackmount servers. Depending on your country you can use [Labgopher](https://labgopher.com/) if not, I found that Ebay was the best place to locate servers. Labgopher just makes it easier for you to compare server. Once again, this is dependant on your location but there can be government auctions near by where they can be selling hardware.

Don't expect to find a second hand server that has been released in the last 3 years unless you live next to a financial datacentre as they regularly swap servers out.

### What do I suggest?

This is a difficult question to answer but you want to buy something that will last you around 5-6 years. I personally like the Dell r710/ r720 line for servers as alot of people run these in their homelabs. My self included. Another solid choice are Supermicro but personally I find their modeling confusing, but I do plan on my next server being a supermicro.

Storage: Starting out, I suggest 2TB. It sounds alot, but VM's take up space, all the stuff you put on there will start to add up.

memory: Depending on your use case, you will want at minimum 16gb of ram, but if you're just running docker (containers) you can get away with less

CPU: This is a per use case, I just used the CPU's that came with my server. ([e5520](https://ark.intel.com/content/www/us/en/ark/products/40200/intel-xeon-processor-e5520-8m-cache-2-26-ghz-5-86-gt-s-intel-qpi.html))

---

## Building a server

Now that we have all the parts (or the whole pre-built server) we need to look at what to install.

## Operating system

This is really back to what you plan on using your lab for. I highly suggest you use a form of virtualisation as it allows for the most servers to be installed on one piece of hardware. You want to get the most dense deployment as you're the poor sod who needs to pay for power. I will admit I am very biased, but I will do my best to be diplomatic and explain the best options as of 2020.

### XCP-NG: Turnkey Open Source Hypervisor

Based on XenServer, XCP-ng is the result of massive cooperation between individuals and companies, to deliver a product without limits. No restrictions on features and every bit available on GitHub!

### Proxmox

Proxmox VE is a complete open-source platform for enterprise virtualization. With the built-in web interface you can easily manage VMs and containers, software-defined storage and networking, high-availability clustering, and multiple out-of-the-box tools on a single solution.

### Hyper-v

This is the virtulization program from Microsoft. I've used it at work before but didn't enjoy the way it's managed and I don't like the fact that everything is closed source.

[https://xcp-ng.org](https://xcp-ng.org)

[proxmox.com/en/](https://proxmox.com/en/)
[

Introduction to Hyper-V on Windows 10

Introduction to Hyper-V, virtualization, and related technologies.

Microsoft Docsscooley

![](https://docs.microsoft.com/en-us/media/logos/logo-ms-social.png)
](<https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/about/>)
My personal favourite is XPC-NG as it scales so well across both home labs, data centres and cluster based computing. The control interface runs as a vm and can be used to manage thousands of servers, from one place. This is what I run in my lab across 2 servers.

---

Now that we have everything in boxes, we can start to build out.

Depending on what your lab will do for you, I suggest having a separate router for everything. You can virtulise it, but I prefer to run mine as hardware. I chose to go with a dell r210ii which runs Pfsense. This allows for fine grain control on what the servers can see, who can get in and any VPN's I want to connect, can be done through the firewall/ router opposed to having to connect each vm.

Putting everything together is quite simple, you'll need a couple of ethernet cables, a few kettle lead powerr cables, a monitor, keyboard (no mouse, we don't do that in the linux world) and a USB stick to boot the os of your choice off of.

Instead of filling up this page with how to install the 3 OS' I mentioned, here are 3 good videos:
[

XCP NG Xenserver 7.4 Install Tutorial. From bare metal to loaded VM using XenCenter

Amazon Affiliate Store ➡️ <https://www.amazon.com/shop/lawrencesystemspcpickup> Gear we used on Kit (affiliate Links) ➡️ <https://kit.co/lawrencesystems> Try ITP...

![](https://www.youtube.com/yts/img/favicon_144-vfliLAfaB.png)YouTube

![](https://i.ytimg.com/vi/bG5enpij0e8/maxresdefault.jpg)
](<https://www.youtube.com/watch?v&#x3D;bG5enpij0e8)[>

Virtualize Everything! - Proxmox Install Tutorial

Want to know how to setup Proxmox so you can start virtualizing servers? This tutorial is for you. But first... What am I drinking??? Tutorials mean cocktail...

![](https://www.youtube.com/yts/img/favicon_144-vfliLAfaB.png)YouTube

![](https://i.ytimg.com/vi/azORbxrItOo/maxresdefault.jpg)
](<https://www.youtube.com/watch?v&#x3D;azORbxrItOo)[>

Windows Server 2016 - Install Hyper-V Server, Virtual Switch, VMs (How to Step by Step Tutorial)

Installing HyperV from nothing to Virtual Switch to VMs step by step tutorial on Windows Server 2016 or Windows 10

![](https://s.ytimg.com/yts/img/favicon_144-vfliLAfaB.png)YouTube

![](https://i.ytimg.com/vi/wGZrhKhj0Fk/hqdefault.jpg)
](<https://www.youtube.com/watch?v&#x3D;wGZrhKhj0Fk>)
Now that you've got the OS installed, you'll probably want to configure a router of choice.

 I highly suggest using the `172.16.0.0/16` range of IP address' as it gives you quite alot of flexibility as well as easily being able to distinguish ranges. You're able to put say DNS servers on `172.16.53.0/24` and then web servers on `172.16.80.0/24` and then your bastion server can be on `172.16.22.0/24`... you get the idea.

Most people will say the crux of a homelab is being able to spin up servers at will, and not have to build a server each time with hardware, get a disk, you know the pain. Seeing as we installed a virtualisation operating system, it allows us to chop the host server up in to small blocks if you will where we're able to present it to a virtual machine to use. You can give a server 1 cpu that is actually 20 cores combined or 20 cores on 1 cpu. Virtualisation allows you to have fine grain control over everything.

### Gues OS

This is really dependant on what your lab is for. If you are learning windows server, you will run windows server. If you are trying to get in to the IT world, I suggest start with Linux and work back to windows as once you figure out the syntax of command line, you become a lot more powerful at managing windows.

---

## Monitoring

This plays a big role in working out what is wrong. having good monitoring software can really speed up locating performance issues, building dank graphs and give you a high level overview on what's going on.

2 tools that I use are Zabbix and Cockpit projec

[Zabbix](https://www.zabbix.com): (Post coming soon)

Cockpit:
[

Cockpit Project — Cockpit Project

Cockpit makes it easy to administer your GNU/Linux servers via a web browser.

![](https://cockpit-project.org/images/favicon.png)

![](https://cockpit-project.org/FIXME)
](<https://cockpit-project.org)(Their> website doesn't like it here, hence the missing image)

## Backups

These are probably the most important part of a lab as 90% of the time, your time fucking things upbreaking things learning through breaking. It's crucial to have backups at least once a week at a minimum.

You can custom roll your own script backing everything up to a wasabi bucket, a flash drive or if you want to be fancy and have some extra cash, replicate it off site.

You can also use something like Veeam (which is awesome) or BackupPC

[http://backuppc.sourceforge.net](http://backuppc.sourceforge.net)
[

Free Backup Solution - Veeam Backup & Replication Community Edition

Veeam® ONE™, part of Veeam Availability Suite™, provides comprehensive monitoring and analytics for your backup, virtual and physical environments. With support for Veeam Backup & Replication™ and Veeam Agents, as well as VMware vSphere, Microsoft Hyper-V and Nutanix AHV, Veeam ONE delivers deep, in…

![](https://www.veeam.com/content/dam/veeam/global/favicon_228x228px.png)Veeam SoftwareBersayder Mejia Networking TechnicianITSC

![](https://www.veeam.com/content/dam/veeam/global/og-images/1600x800_vas_v10.png?ck&#x3D;1581061105410)
](<https://www.veeam.com/virtual-machine-backup-solution-free.html)Veeam> community is free
---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
