---
title: How I manage my DNS
slug: dns-terraform-cloudflare
date: 2021-05-24T19:57:00.000Z
date_updated: 2021-05-24T20:00:10.000Z
summary: What's the best way to over engineer DNS record management? CI/CD - let me tell you
---

Managing DNS can be a complicated thing for a large company, many departments changing things.

Let's be honest here, at some point someone somewhere asked a web developer to update a DNS record and then landed up wiping out an mx record (I made this up, [but it turns out someone did it](https://www.reddit.com/r/msp/comments/4j9spm/why_the_hell_do_web_designers_take_control_of_dns/))

I chose to complicate my DNS as much as possible by moving the name servers from the registrar, to cloud flare, then importing the records in to Terraform, then moving things like IP address' of servers to variables, then got bored and moved everything over to cnames, then got bored again and moved to modules. - I know :)

---

> this post is a little confusing to follow, so if you get lost or it's just too confusing, please reach out!

## The why?

Back in 2020 I set my self a goal, get everything that it takes to manage breadNET in to a git repo. This spanned all the way from creating servers in the cloud to server config and app install scripts to DNS.

Here's where it gets interesting. I hadn't heard about terraform before April 2020 so I was trying to go about it in some strange way by using a bash script I was working on, and then pull from the cloudflare API blah blah blah. Simple story - would not have worked.

I want everything in git so should my server fall off the face of the earth, all it takes is running the playbook/ `terraform apply`, restore the databse backups and files and we're good to go!

## Dribble about my DNS

So like most people who host things at loss ([see how much](__GHOST_URL__/what-it-takes-to-run-breadnet/)) using free services is a must.

- Domain

- Namecheap

- DNS Hosting

- Cloudflare

- Git Hosting

- Selfhosted GIT server

- Pipeline

- Codefresh

## The How

Buckle up, this gets way too complicated for what it really is!
![](__GHOST_URL__/content/images/2021/05/4waycycle-02.png)The "pipeline"
I manage my DNS through Cloudflare, using terraform which gets applied on a push to master via a service called Codefresh.

Let's start at the DNS level.

I chose to use Cloudflare for DNS as they provide a proxy level to your services so I am able to serve more people with less resources! They also have DDOS protection which I laughed at, but I've come under a few DDOS attacks. Not sure why but hey-ho!

My records are set out in a way that all records that end with `.breadnet.co.uk` are cnames! Even the main domain is a cname.

These cnames point to a second domain which follows a simple layout

`<server purpose>.breadinfra.net` so the reverse proxy server is `reverse.breadinfra.net`

This means that my nslookups now look like this:

    stannardb@bread-l1:~$ nslookup
    > unifi.breadnet.co.uk
    Server:  127.0.0.53
    Address: 127.0.0.53#53

    Non-authoritative answer:
    unifi.breadnet.co.uk canonical name = unifi.breadinfra.net.
    Name: unifi.breadinfra.net
    Address: 51.77.109.126
    >

I chose to do it this way as it allows me to only have to update the server record is I decide to move it. It originally came from when I was managing DNS through the UI. I have something like 75 records pointing to a few servers

Here comes the terraform!

Due to this abstraction I manage it through terraform using modules. Below is what a module looks like

    #main.tf
    resource "cloudflare_record" "a" {
      zone_id = "<redacted>"
      name    = var.name
      type    = "A"
      ttl     = "1"
      proxied = var.proxied
      value   = var.value
    }

    #outputs.tf
    output "id" {
      value = cloudflare_record.a.id
    }

    output "name" {
      value = cloudflare_record.a.name
    }

    output "hostname" {
      value = cloudflare_record.a.hostname
    }

    #provider.tf
    terraform {
      required_providers {
        cloudflare = {
          source = "cloudflare/cloudflare"
          version = "~> 2.0"
        }
      }
    }

    #variables.tf
    variable "name" {
      type = string
    }
    variable "value" {
      type = string
    }
    variable "proxied" {
      type = string
    }

These modules allow me to repeat as little as possible when creating a new record.

If I want to create an A record, it looks like:

    module "hosted_on" {
      source = "git::ssh://git@<redacted>a.git"
      name = "hosted.on"
      proxied = "false"
      value = var.<redacted>

This then creates a record which cloudflare sees as:

    # module.hosted_on.cloudflare_record.a:
    resource "cloudflare_record" "a" {
        created_on  = "2021-04-22T20:49:44.673066Z"
        data        = {}
        hostname    = "hosted.on.breadinfra.net"
        id          = "<redacted>"
        metadata    = {
            "auto_added"             = "false"
            "managed_by_apps"        = "false"
            "managed_by_argo_tunnel" = "false"
            "source"                 = "primary"
        }
        modified_on = "2021-04-22T20:49:44.673066Z"
        name        = "hosted.on"
        proxiable   = true
        proxied     = false
        ttl         = 1
        type        = "A"
        value       = "<redacted>"
        zone_id     = "<redacted>"
    }

Then when I create a cname it looks like

    module "bookstack" {
      source = "git::ssh://git@<redacted>/cname.git"
      name = "bookstack"
      proxied = "true"
      value = module.reverse.hostname
    }

Here we are passing the output of the module that created the A record for the reverse server (notice it's the hostname) - then we create it's fqdn, which will be `bookstack.breadnet.co.uk` and set it to proxy through cloudflare's network

    > bookstack.breadnet.co.uk
    Server:  127.0.0.53
    Address: 127.0.0.53#53

    Non-authoritative answer:
    Name: bookstack.breadnet.co.uk
    Address: 104.21.43.73
    Name: bookstack.breadnet.co.uk
    Address: 172.67.222.140
    Name: bookstack.breadnet.co.uk
    Address: 2606:4700:3036::ac43:de8c
    Name: bookstack.breadnet.co.uk
    Address: 2606:4700:3037::6815:2b49
    >

Once I've got all the records created, I then push it to my private git server where codefresh picks it up and runs a pipeline on it

This is what it looks like from the UI
![](__GHOST_URL__/content/images/2021/05/image.png)
There are 3 steps. Each step caused me hours of lost sleep just because

- This was my first time using codefresh
- I don't know how to write the `codefresh.yml` file
- I didn't know how to auth to my git server
- I didn't know how to auth to Terraform cloud for remote state

Before we continue, let me show you the file:

    version: '1.0'
    stages:
      - checkout
      - prepare
      - deploy
    steps:
      main_clone:
        title: Git clone
        image: alpine/git:latest
        stage: checkout
        commands:
          - mkdir -p ~/.ssh
          - echo "${SSH_KEY}" | base64 -d > ~/.ssh/id_rsa
          - chmod 600 ~/.ssh/id_rsa
          - echo "${gitlab_known_host}" > ~/.ssh/known_hosts
          - rm -rvf *dns*
          - git clone git@<redacted>/dns.git
          - mv dns/* .
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
          - mkdir -p ~/.ssh
          - echo "${SSH_KEY}" | base64 -d > ~/.ssh/id_rsa
          - chmod 600 ~/.ssh/id_rsa
          - echo "${gitlab_known_host}" > ~/.ssh/known_hosts
          - terraform init -backend-config="token="$token""
          - terraform apply -auto-approve

Let's break it down

It's broken in to 3 steps:

- checkout
- Prepare
- Deploy

The checkout step was where I had the most issues, I had to git clone from my private git server behind a firewall.

I had to open the firewall to codefresh's IP range and then configure SSH keys.

I did the SSH keys by setting a secret in codefresh, generating a random SSH key on my laptop, echoing the private key to base64 ( `cat ./ssh/<key> | base64` ) and then putting that base64 encoded private key in to codefresh. It's important that you set it as a secret and then delete that private key from your laptop.

In your git platform, create a user and add that user to your repo, and then add the public key to their account.

I do a `rm` because codefresh has persistence between running and it was causing issues with not updating the files. I would rather pull each time and waste 3 seconds than cause terraform state drift.

The `config auth` stage just sets the cloudlfare API key as an environment variable so I'm not storing it in the terraform code.

Finally there is the deploy phase.

I use terraform cloud to manage my remote state file, this just helps as if I was to run this on my computer, I can just run when ever needed as long as I don't delete the file, I'm all good!

Where as running in an ephemeral environment, you want the persistence to be outside the platform.

You need to authenticate with a token to the terraform cloud which is usually stored under `$HOME/.terraform.d/credentials.tfrc.json` and looks like

    {
      "credentials": {
        "app.terraform.io": {
          "token": "<redacted ya cheeky bugger>"
        }
      }

so I had the idea to try and pass it to the command as `--backend-config` and low and behold, it worked!

Codefresh then runs the full thing, auto approves this apply and puts it in to action.

From committing the code to the records being created takes about 50 seconds, which allows me to do other things, like finish the nginx config file, or queue up the command to get an LE certificate.

If any part of this doesn't make sense, please reach out to me!

---

Illustrations by [Kirsty Lawrie](__GHOST_URL__/dns-terraform-cloudflare/kirstylawrie.com/)

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
