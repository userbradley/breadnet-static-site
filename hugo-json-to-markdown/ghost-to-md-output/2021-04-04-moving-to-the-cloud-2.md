---
title: "Moving to the cloud: Infrastructure"
slug: moving-to-the-cloud-2
date: 2021-04-04T04:26:20.000Z
date_updated: 2021-05-02T01:44:09.000Z
summary: Part 2 of moving to the cloud - Let's talk about IaC
---

Welcome back!

If you're not seen it, I suggest you have a read of:
[

breadNET Cloud Migration

How did I move all my servers to the cloud? Well - Ansible, automation and CI/CD!

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1560182413-53772f3d7134?ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;fm&#x3D;jpg&amp;crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;w&#x3D;2000&amp;fit&#x3D;max&amp;ixid&#x3D;eyJhcHBfaWQiOjExNzczfQ)
](__GHOST_URL__/cloud-migration-part-1/)
In this installment of "Something I did at 4am that really should have been done during the day" we will be looking at the infrastructure that will be powering my internal services.

I had a lot of issues during this, but let's take a look at the code first.
[

terraform / breadNET OVH

The OVH terraform for breadNET cloud servers

![](https://gitlab.breadnet.co.uk/assets/touch-icon-ipad-retina-8ebe416f5313483d9c1bc772b5bbe03ecad52a54eba443e5215a22caed2a16a2.png)GitLab

![](http://gitlab.breadnet.co.uk/assets/gitlab_logo-7ae504fe4f68fdebb3c2034e36621930cd36ea87924c11ff65dbcb8ed50dca58.png)
](<https://gitlab.breadnet.co.uk/terraform/breadnet-ovh>)
I host all my code on Gitlab, allows me more control and able to play with CI at some point.

I have decided that for this deployment that it's best to use a IaC (Infrastructure as code) approach to setting up and provisioning the instances.

Probably wondering why?

It seems like a long process at the time, but should OVH decided they want to burn down London, I can just add a variable in to the code for a different region, apply and restore from backups. Also, it allows for a single source of truth and being in git, better control of changes. Eventually I will move this to a pipeline on merge to master so I don't have to do any terraform applies my self!

Lucky for me most of my applications (Barring Jira and Jellyfin) are quite lightweight so don't require a lot of compute resources. This being said I have still built this around the ability to expand my server needs as time progresses.

---

# changes

Now, about that last comment from the previous post about changing up a lot of things...
[

[BCM-2] List apps that need to be moved - breadNET Jira

![](https://jira.breadnet.co.uk/s/q6useh/814001/75e65367690ac553d207206292c2b417/_/jira-favicon-hires.png)JIRA

![](https://jira.breadnet.co.uk/secure/projectavatar?avatarId&#x3D;10324)
](<https://jira.breadnet.co.uk/browse/BCM-2>)
Last time we looked at the services I plan to migrate, we had a lot more.

Since I wrote that post I have since moved out of my parents house, and have given them a deadline of end of Q2 to have the servers shutdown. Whilst this is quite a sad thing to do, once I am a house owner and chase all the promotions I can, I have plans to run my own local cloud. I would probably go down the Colocation route with something like Openstack as this would make moving my pre-existing infrastructure over quite easy as I am writing modules for Openstack.

That being said, I have taken a look at the services I use day to day and have come to the conclusion the only services I **need**and rely on are:

- Passbolt
- Jira
- Jellyfin
- Gitlab
- Unifi

Heres where things get fun.

Jira suggests a minimum of 8gb worth of ram for running the instances and Jellyfin can run on a pi with direct streaming. Nice.

It would seem like I will need to migrate Jira to the atlassian cloud offering, but plan on putting this off for as long as possible. I may see if I can just run a small computer at my parents for this. Still - End goal is to have it migrated.

# the why

You're probably thinking, "Why actually migrate?"
Well, running 4 pieces of equipment at my parents house when I am not paying for connections or power or space is a little unfair. I would move the server to where I live now, but we don't have a garage and nor the stable internet connection, blame Virgin Media and their [shambolic implementation  of how to handle Static IP address'](https://www.ispreview.co.uk/talk/threads/virgin-media-business-500-35-voom-13-static-ips.37005/)

Basically the way it works is the Virgin media router connects to their network, then you establish a GRE connection to  a virgin media data centre in one of the following: Birmingham/Leeds/Cambridge/Reading (according to our IP location) where traffic then flows to/from.

Now this is fine, but it adds an additional 30ms of latency on to ANYTHING, and really breaks things like Cloudflare DNS, Google DNS and anything that uses an anycast IP address as instead of connecting to the closest server geographically and per ping, we connect to stuff up in Birmingham

    traceroute to 1.1.1.1 (1.1.1.1), 64 hops max, 52 byte packets
     1  192.168.0.1 (192.168.0.1)  4.404 ms  2.788 ms  2.798 ms
     2  * * *
     3  brhm-core-2b-et-315-0.network.virginmedia.net (81.110.128.5)  19.415 ms  18.775 ms  18.458 ms
     4  * * *
     5  * * *
     6  tcma-ic-2-ae9-0.network.virginmedia.net (62.253.174.178)  20.490 ms  20.312 ms  17.615 ms
     7  162.158.32.254 (162.158.32.254)  32.277 ms  53.136 ms  38.476 ms
     8  162.158.32.9 (162.158.32.9)  31.605 ms  32.833 ms  35.764 ms
     9  one.one.one.one (1.1.1.1)  31.442 ms  31.381 ms  33.273 ms

Any way.

Let's look at the code.

I have opted to go with a minimum of 3 servers, 1 server will be a load balancer and reverse proxy, then 2 application servers.
Going this route allows me to terminate SSL on one instance, and firewall things off on one instance, then the 2 back end instances don't need to be messed with as far as installing additional software goes. It also makes backups a lot easier (we will cover this in a second)

I don't want to go in to the nitty gritty details too much as I want to do my best to do a little ["Security through obscurity"](https://danielmiessler.com/study/security-by-obscurity/) and clean opsec practices.

I am going to be identifying what the best reverse proxy is to run:

- HaProxy
- Nginx
- Varnish Proxy
This is a POS as it doesn't do SSL

So if we're being honest, the pick is between:

- HAProxy
- Nginx

For the time being, I will roll Nginx as it's something I have been using since I (about to annoy a lot of old school fold) discovered apache2 isn't cool anymore.

# actually looking at the code now

I know, I said let's look at the code like 3 times now...

I have decided to go down the Modules route for Terraform as this is something I need to learn for work.

One snag I came across was I am creating a VPC and then connecting the instances to them via a port. For each instance I need to create a port, then link it to the instance, as well as `Ext-Net` as OVH call it.

    resource "openstack_compute_instance_v2" "instance" {
      name = var.name
      flavor_name = "s1-2"
      key_pair = var.key
      image_name = "Ubuntu 18.04"
      security_groups = var.sg
      network {
        port = openstack_networking_port_v2.internet.id
      }
      network {
        port = openstack_networking_port_v2.internal.id
      }
    }

    resource "openstack_networking_port_v2" "internal" {
      name           = "${var.name}-backend"
      network_id     = var.netid
      admin_state_up = "true"

      fixed_ip {
        subnet_id  = var.subid
        ip_address = var.ip
      }
    }

    resource "openstack_networking_port_v2" "internet" {
      name           = "${var.name}-ext-net"
      network_id     = "6011fbc9-4cbf-46a4-8452-6890a340b60b"
      admin_state_up = "true"
    }

[

Files · master · terraform / modules / ovh / Instance Ports

Instance with VPC ports

![](https://gitlab.breadnet.co.uk/assets/touch-icon-ipad-retina-8ebe416f5313483d9c1bc772b5bbe03ecad52a54eba443e5215a22caed2a16a2.png)GitLab

![](http://gitlab.breadnet.co.uk/assets/gitlab_logo-7ae504fe4f68fdebb3c2034e36621930cd36ea87924c11ff65dbcb8ed50dca58.png)
](<https://gitlab.breadnet.co.uk/terraform/modules/ovh/instance-ports/-/tree/master>)
By slapping the instance creation in to a module, I dont have to create a port block each time I create an instance.

Now it looks like the below to create a new instance:

    module "lb-rp" {
      source = "git::https://gitlab.breadnet.co.uk/terraform/modules/ovh/instance-ports.git"
      ip = "172.16.18.10"
      key = openstack_compute_keypair_v2.computer.name
      name = "lon-lb-rp"
      netid = module.vpc.network_id
      sg = [
        openstack_compute_secgroup_v2.ssh.id,
        openstack_compute_secgroup_v2.icmp.id,
        openstack_compute_secgroup_v2.web.id
      ]
      subid = module.vpc.subnet_id
    }

Let's break this down as I know you care:

    module "lb-rp"{
    source = "git::https://gitlab.breadnet.co.uk/terraform/modules/ovh/instance-ports.git"
    # code goes here
    }

Defines the module
Here we are defining the module, and where it can be found. Originally I was working with the modules in file, but towards the end I plan to use these modules often, so I moved them to git.

    ip = "172.16.18.10"

This is defining the internal IP on the VPC

     key = openstack_compute_keypair_v2.computer.name

This defines what SSH key I want to use to access the instances

    name = "lon-lb-rp"

Guess what this does

    netid = module.vpc.network_id

This one is fun, this connects the instance to the port with the correct network ID for the VPC. In order to do this, in the VPC module I had to define an output.

      sg = [
        openstack_compute_secgroup_v2.ssh.id,
        openstack_compute_secgroup_v2.icmp.id,
        openstack_compute_secgroup_v2.web.id
      ]

These are the firewall rules for the instance

    subid = module.vpc.subnet_id

Much like netid, this is from the VPC module, connecting it to the VPC with the correct Subnet address.

All in all, that creates an instance, attaches it to the correct VPC and subnet, gives it an IP address, gets a public IP address, allows me to ssh, ping and also inbound 80 and 443.

Now this is done, we can take a look at something which is important after the recent events...
[

Millions of websites offline after fire at French cloud services firm

A fire at a French cloud services firm has disrupted millions of websites, knocking out government agencies’ portals, banks, shops, news websites and taking out a chunk of the .FR web space, according to internet monitors.

![](https://www.reuters.com/article/_next/static/images/favicon-196x196-052cc719f1ac872e3544e51801338b46.png)ReutersMathieu Rosemain, Raphael Satter

![](https://static.reuters.com/resources/r/?m&#x3D;02&amp;d&#x3D;20210310&amp;t&#x3D;2&amp;i&#x3D;1554440499&amp;r&#x3D;LYNXMPEH290XD&amp;w&#x3D;800)
](<https://www.reuters.com/article/us-france-ovh-fire-idUSKBN2B20NU>)
Yeah - Big Whoops.

# backups

Now I know people see the cloud as a magical place, but bro. Really? Just because it's far far away from your physical control, doesn't mean that problems still don't happen.

Meme time:
![](__GHOST_URL__/content/images/2021/04/image.png)![](__GHOST_URL__/content/images/2021/04/image-1.png)
Now we have that out of our system...

Let's have a little think about backups.

Currently I have a (lowely janky) system that works REALLY well. Let me explain:

- Backups of all servers go to backuppc (currently) running internally
- The server running backuppc has a cron job syncing the data to Wasabi
- Mail server, dbserver and reverse all backup their files to individual buckets on wasabi.
- VM's are snapshotted daily and pushed to Wasabi nightly. They are also exported to a removable harddrive for daily recovery if needed.
- All in all, there is about 2tb worth of data that is being shuffled around.

Now with us moving to the cloud, we are able to use backup services built in to OVH... But after the fire, I don't really want to have to rely on data being stored in the same data centre to be able to spin up my resources should the place flood or some strange event happen.

My plan:

- Jellyfin media is served from s3, bucket replication to RO bucket.
- At my current address, we have 300m down/20 up, I will purchase a raspberry Pi and run backuppc from it
- Backuppc on pi also has a cron job to move files to s3 bucket
- Servers push their files to s3
- Config files are all done via Ansible or Git (ci/cd)

The whole idea around this painful process is should OVH and my house decide to show the world they vape, I have __all__ the files on S3

Should OVH and the data centre in the netherlands (where s3 is) decide they don't wan't to be a data centre and instead become a warehouse, we have the files locally.

NOW - Should My house and also NL decide they <fill in some comic way of saying offline> we have the live servers, which I will snapshot and export these snapshots to my local computer. Max 30gb.

# Issues

Now the keen eyed among you who had a little scratch around Jira saw this:
[

[BCM-18] Issue log - breadNET Jira

![](https://jira.breadnet.co.uk/s/q6useh/814001/75e65367690ac553d207206292c2b417/_/jira-favicon-hires.png)JIRA

![](https://jira.breadnet.co.uk/secure/projectavatar?avatarId&#x3D;10324)
](<https://jira.breadnet.co.uk/browse/BCM-18>)
I kept a log of the bullshit strange issues I came across for your entertainment.

let's get started.
IssueDescriptionsolved?Multiple IP addressI was trying to attach internal IP address and external IP address to an instance and depeding on the order you slap them in on, one doesnt get connected.noMoving to module and IP issuesThis was sheer user error and not knowing how to then attach the Port (Which contains the IP address) to the instanceyes!Second instance failing to createThis was a stange one. I was trying to create 2 instances and use the same port as I was able to do this with the ext network. Turns out you cant actually do this so you need to create a port per instance per networkyesFirewall rules not being connectedI'm not even sure what causes this, but just doing a terraform apply agian workseh, why not?
    Error getting openstack_networking_network_v2 16ce390d-4fa1-4767-8372-f7b243f3ac89: Get "<https://network.compute.uk1.cloud.ovh.net/v2.0/networks/16ce390d-4fa1-4767-8372-f7b243f3ac89>": OpenStack connection error, retries exhausted. Aborting. Last error was: read tcp 192.168.0.11:64516->51.75.101.108:443: read: connection reset by peer

Ah this one popped up MANY times - Looks like this and it made me want to slap someone at OVH.
![](__GHOST_URL__/content/images/2021/04/image-2.png)
This is OVH being OVH. Just re-apply your terraform and you're good.

There is one more issues I need to solve, and that is getting the instances to pick up the VPC IP address, but I think I may need to do this via Ansible or Manually.

I want to avoid having to do as much as possible manually...

This leads me to on to the next post where I will be discussing the Ansible behind the services I will be running, and how I plan to move all this to a CI/CD pipeline (or something like that)

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
