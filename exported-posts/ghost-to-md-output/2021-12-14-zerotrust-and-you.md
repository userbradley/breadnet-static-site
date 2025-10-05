---
title: ZeroTrust and you
slug: zerotrust-and-you
date_published: 2021-12-14T00:34:52.000Z
date_updated: 2021-12-14T01:43:09.000Z
tags: security, proxy, ssh, #Import 2023-03-30 20:40
excerpt: What is zerotrust, and how does one trust.. zero?
---

## Firstly what is zero trust

So from what I can tell, zero trust is a process of trusting nothing, not even the network you're on! It's designed to help with the "Digital transition to the cloud", which especially with the big 'rona around, this is good!

We're seeing more business' adopting a zero trust model as employees are working from home, and Corporate IT teams are scrambling to enable workers to access internal servers and applications. 

[According to Okta](https://www.okta.com/sites/default/files/2021-07/WPR-2021-ZeroTrust-070821.pdf), zero trust has increased as a priority for 78% of business!   

### The TLDR;

Zero trust is exposing internal services behind a login page that has secure communication to the backend, or using hardware keys on computers. Be this using SSO or federated systems like LDAP behind the proxy, we call this zero trust. 

## Options on the market

As with anything, there are several options that one can use. 

- Duo Beyond
- Perimeter81
- Forcepoint Dynamic Security Solutions
- Prove
- Google BeyondCorp
- Microsoft 365 Azure
- Okta Identity Cloud
- Palo Alto Networks
- Proofpoint Meta
- Unisys Stealth
- Cloudflare Teams access
- Pritunl Zero
- Teleport

Each one had it's fare share of good as well as bad things about it.

I needed my solution to:

- Allow SSH Bastion
- Allow web connections
- 2FA
- Central user management
- Simple to use
- Run on minimal hardware (s1-2 on OVH)

## Option I went with

Based on my above requirements, I've decided to go with [Pritunl Zero](https://zero.pritunl.com)

It allows SSH, Web, 2FA on both web interfaces and the admin UI, Users are managed via the webUI, and stored in MongoDB and it's pretty simple to use!

## Implementation

All my code for this can be located on the below github repo:
[

GitHub - userbradley/zerotrust-public

Contribute to userbradley/zerotrust-public development by creating an account on GitHub.

![](https://github.githubassets.com/favicons/favicon.svg)GitHubuserbradley

![](https://opengraph.githubassets.com/2308e21c024e7a78416d8c208b1ab6c624b50f62905581ef7298b47a62472324/userbradley/zerotrust-public)
](https://github.com/userbradley/zerotrust-public)
For getting started on using terraform with OVH, follow [This guide ](__GHOST_URL__/terraform-ovh-openstack/)

Once setup with terraform, set the `me` variables in `terraform.tfvars` if on a mac, or edit the file path under `ssh.tf` to the full path of your SSH key. 

Once that's up, you need to SSH in to the server, copy the `install.sh` file and run it! 

Finally get the password with `sudo pritunl-zero default-password`

If you plan on running an SSH bastion, you need to install Docker, which can be found [here](https://docs.docker.com/get-docker/)

Full setup can be found below:
[

Getting Started SSH

Install and configure Pritunl Zero SSH certificates with two-factor authentication

![](https://files.readme.io/gkjYhYaZQkyKjQTOFpIn_favicon.ico)Pritunl

![](https://files.readme.io/306844c-ssh0.png)
](https://docs.pritunl.com/docs/pritunl-zero)
## Issues I've had

So there have been a few teething issues I've had!

1. Installing the bastion service doesn't detail installing docker, the logs reflect this: 

![](__GHOST_URL__/content/images/2021/12/image.png)
As soon as Docker was installed:
![](__GHOST_URL__/content/images/2021/12/image-1.png)
2. SSH not working after certificate has expired

So the specific error you'd get here is: 

    check_host_cert: certificate signature algorithm ssh-rsa: signature algorithm not supported
    Received disconnect from <ip> port 9800:2: Too many authentication failures
    Disconnected from <ip> port 9800
    kex_exchange_identification: Connection closed by remote host

The simple way to solve this is run `pritunl-ssh` and allow the new key on the web interface
![](__GHOST_URL__/content/images/2021/12/image-2.png)
3. Config files are confusing!
 So this was more on me than anything, and I'm hoping that by me showing you how to write one, as well as where the username comes from etc

Example config file:

    Host 198.244.155.107
        ProxyJump bastion@<bastionaddress>:9800
    
     host reverse1-lon
     hostname reverse1.lon.eu.breadnet.co.uk
     user root
     ProxyJump bastion@<bastionaddress>:9800

- 
Lines `1-2`

- Connects to the host 198...
- Username is your logged in user
- Uses the ssh key defined when you setup the local pritunl-ssh

- 
Rest of the file

- Using a simple name
- Logs in as root
- Jumps via the bastion
- Same SSH key as the above

---

Closing notes:

So this was a really short one, but I really wanted to share this as there's sub-minimal documentation around this topic and specifically around pritunl-zero.

If you have any issues or confused with anything please feel free to reach out to me! 

---

So I've added the ability to subscribe to my site... I know no one will, but I thought I would try and let yall enjoy it? It will just be a link to the latest post! 
