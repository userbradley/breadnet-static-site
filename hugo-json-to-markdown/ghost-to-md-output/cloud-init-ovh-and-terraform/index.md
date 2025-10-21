---
title: Cloud-init, OVH and terraform
slug: cloud-init-ovh-and-terraform
date: 2022-03-02T23:24:15.000Z
date_updated: 2022-03-02T23:24:15.000Z
summary: I'll be honest, this one was a struggle but we did it!
---

Yup, it's that time of the year again when I talk about some issues I've had and couldn't find a solution on google so I wrote about it.

## What is the problem?

If you're never used OVH and terraform, you'll know that standing up the instance using terraform is quite easy. But adding a second network adapter and getting that to get DHCP... No.

I've previously written about using cloud-init, see below, on local infrastructure.
[

Cloud-init that works

Want to speed up the deployment of Linux servers on your Xen based server? Well I finally figured it out!

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;fm&#x3D;jpg&amp;crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;w&#x3D;2000&amp;fit&#x3D;max&amp;ixid&#x3D;eyJhcHBfaWQiOjExNzczfQ)
](__GHOST_URL__/cloud-init-that-works/)
But the difference here, is that the documentation is even worse!

I'm talking, like 3 different places saying something different.

If you're not here to read the entire blog, scroll to the bottom where I have the solution to getting cloud init to work on OVH

## Let's start

So seeing as we're using terraform, our first call of action is to look at their documentation for cloud init, which uses a field called `user_data`
[

Provision Infrastructure with Cloud-Init | Terraform - HashiCorp Learn

Deploy preconfigured infrastructure with Terraform using the Cloud-Init tool.

![](https://learn.hashicorp.com/img/favicons/favicon-192x192.png)HashiCorp Learn

![](https://www.datocms-assets.com/2885/1622161215-learn-card-2x.jpg)
](<https://learn.hashicorp.com/tutorials/terraform/cloud-init>)
The part that annoys me here, is they make you use a provider called `template_file` which is actually deprecated...

    data "template_file" "user_data" {
      template = file("../scripts/add-ssh-web-app.yaml")
    }

so if you get an error like below, you're welcome

`Provider registry.terraform.io/hashicorp/template v2.2.0 does not have a package available for your current platform, darwin_arm64.`
![](__GHOST_URL__/content/images/2022/03/image-1.png)
I tried to run terraform in a docker container forcing amd64 (as I am on an M1 mac) - No luck :(

The resolution for this one was to use a new provider, called `cloudinit_config` which looks a little something like this

    data "cloudinit_config" "user_data" {
      gzip = false
      base64_encode = false
      part {
        content_type = "text/x-shellscript"
        content = "baz"
        filename = file("./cloudinit.cfg")
      }
    }

But for the life of me, could not get this working. I was passing it to the instance rendered.

I'd had enough and thought, well fuck this noise we can probably pass the file straight in... Surely?

      user_data = file("./cloudinit.cfg")

This should work?

So I've tried it with the classic `hello world` and it seemed to work.
![](__GHOST_URL__/content/images/2022/03/image-2.png)
Below is what `./cloudinit.cfg` looks like, if you're wondering

    #cloud-config

    runcmd:
     - 'echo ============ Hello World ================'

---

## Now on to the actual issue at hand - Network Interfaces

Because I am lazy I wont be doing a nifty `for` loop, just going with a basic file that the instance calls.

Below is that file:

    #cloud-config
    runcmd:
      - 'echo ============ Hello World ================'
    network:
      ethernets:
        ens3:
          dhcp4: true
        ens4:
          dhcp4: true
      version: 2

I've saved this file as `netplan.cfg` and kept the hello world, as this outputs to logs so hopefully, we can see if it actually applies or no!
![](__GHOST_URL__/content/images/2022/03/image-3.png)
It ran hello world, but the network interface `ens4` isnt enabled and getting DHCP

:(

We can re-load our cloud init, whist logged in using

    cloud-init -d init

Here's the error:
![](__GHOST_URL__/content/images/2022/03/image-4.png)
Looks like we need to fix the file

    #cloud-config
    write_files:
     - path: /etc/cloud/cloud.cfg.d/99-custom-networking.cfg
            permissions: '0644'
            content: |
            network: {config: disabled}

     - path: /etc/netplan/my-new-config.yaml
       permissions: '0644'
       content: |
              network:
                  version: 2
                  ethernets:
                      ens3:
                          dhcp4: true
                      ens4:
                          dhcp4: true
    runcmd:
            - rm /etc/netplan/50-cloud-init.yaml
            - netplan generate
            - netplan apply
            - echo "=== hello === "

Becomes

    #cloud-config
    write_files:
      - encoding: b64
        content: bmV0d29yazoge2NvbmZpZzogZGlzYWJsZWR9Cg==
        owner: root:root
        path: /etc/cloud/cloud.cfg.d/99-custom-networking.cfg
        permissions: '0644'

      - encoding: b64
        content: bmV0d29yazoKICBldGhlcm5ldHM6CiAgICBlbnMzOgogICAgICBkaGNwNDogdHJ1ZQogICAgZW5zNDoKICAgICAgZGhjcDQ6IHRydWUKICB2ZXJzaW9uOiAyCg==
        owner: root:root
        path: /etc/netplan/my-new-config.yaml
        permissions: '0644'


    runcmd:
            - rm /etc/netplan/50-cloud-init.yaml
            - netplan generate
            - netplan apply
            - echo "=== hello === "
    final_message: "The system is finally up, after $UPTIME seconds"

And would you look at that, it worked!
![](__GHOST_URL__/content/images/2022/03/image-5.png)![](__GHOST_URL__/content/images/2022/03/image-6.png)

## The solution

1. Base 64 encode both the new netplan file, and the disable auto-gen config file
2. Use the above file
3. Pull the file in under `user_data`

`netplan.yml`

    #cloud-config
    write_files:
      - encoding: b64
        content: bmV0d29yazoge2NvbmZpZzogZGlzYWJsZWR9Cg==
        owner: root:root
        path: /etc/cloud/cloud.cfg.d/99-custom-networking.cfg
        permissions: '0644'

      - encoding: b64
        content: bmV0d29yazoKICBldGhlcm5ldHM6CiAgICBlbnMzOgogICAgICBkaGNwNDogdHJ1ZQogICAgZW5zNDoKICAgICAgZGhjcDQ6IHRydWUKICB2ZXJzaW9uOiAyCg==
        owner: root:root
        path: /etc/netplan/my-new-config.yaml
        permissions: '0644'


    runcmd:
            - rm /etc/netplan/50-cloud-init.yaml
            - netplan generate
            - netplan apply
            - echo "=== hello === "
    final_message: "The system is finally up, after $UPTIME seconds"

`instance.tf`

    resource "openstack_compute_instance_v2" "zero-access" {
      name = "zero-access"
      flavor_name = "s1-2"
      key_pair = openstack_compute_keypair_v2.key.name
      image_name = "Ubuntu 18.04"
      security_groups = [ "default" ]
      user_data = file("./netplan.yml")
      network {
        name = "Ext-Net"
      }
      network {
        name = openstack_networking_network_v2.vpc.name

      }

---

This post is more of a brain dump than anything, hoping to help those with the issue I had:

## multiple interfaces on ovh not getting dhcp

## how to use cloud-init on ovh with terraform

## how to use cloud-init with openstace
