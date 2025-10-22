---
title: "Migrating to the cloud: The end"
slug: moving-to-the-cloud-3
date: 2023-03-31T17:25:35.000Z
date_updated: 2023-03-31T18:22:31.000Z
summary: Final blog post about moving breadNET to the cloud
feature_image: "https://images.unsplash.com/photo-1610692507254-3bc16d2527ea"
tags: ["cloud"]
---

This is the final post in my _Migrating to the cloud_ trio. Just like Orange is the new black, it can only get worse after the 3rd installment.

* [breadNET Cloud Migration](/moving-to-the-cloud-1)
* [Moving to the cloud: Infrastructure](moving-to-the-cloud-2/)

In the previous years, I wrote about migrating from servers in my parents garage to being on the cloud.

Since then, breadNET has changed a lot!

We've gone from being running 100% on premise, to 50/50, to 70/30 then back on premise and then back to the cloud. It's been quite a mish mash of moving around.

After about 3 years (almost to the date) I have 100% migrated to the cloud, and now have everything stored as code in git.

We're going to take a look at the issues I had during the migration, the data I've had to put on ice and the career changes that aided these migrations.

# First there was the IaC

Previously I migrated all my services to OVH, which was great for getting things set up and running until I was able to get a job that gave me disposable income.

I migrated as many applications as I could to Software as a service - with the most noticeable ones being:

* Jira
* Git

It was not economical for us to run a Jira instance (Requires around 4GB ram and 2 cores - Which costs more on the cloud)

I wanted everything as code, so terraform again. We previously used OVH, which under the hood is [Open Stack](https://www.openstack.org?ref=breadnet.co.uk). We can use the [Digital ocean](https://m.do.co/c/77be3c3aa96c) terraform provider to control our account

{{< bookmark "registry_terraform_io_providers_digitalocean_digitalocean_latest_docs" >}}

Since moving to [Digital Ocean](https://m.do.co/c/77be3c3aa96c), I've found my site is a lot more reliable and latency is a lot lower. Only issue I've had is it's a little more pricy.

## GitOps

This is the best thing ever, this basically means using GitHub and CI to build and deploy infrastructure.

This very nicely moves us on to the next part of the migration. Git.

I've moved all my Git based *activities*to GitHub. all in a single [Mono Repository](https://en.wikipedia.org/wiki/Monorepo) meaning that all the code related to my infrastructure is in one place.

# Accessing servers

I previously wrote about using Pritunl Zero for accessing my servers and internal applications. This method works quite well if all your applications sit on-premise and you have LDAP (as well as the paid plan for Pritunl)

Cloudflare (The people I get my DNS from) also have a feature called Zero. It's pretty much a free zero trust platform that uses the cloudflare edge to terminate your traffic, then send it back out again close to your server.

I've got this installed on all my servers, meaning I can use my native SSH client to connect, and not having to overwrite my SSH client with the one built by Pritunl.

Below is an example code snippet that goes on the server, [once you've followed the Installing cloudflared on Ubuntu page](https://documentation.breadnet.co.uk/kb/cloudflared/cloudflared-on-ubuntu-for-ssh/?mtm_campaign=breadnetsite&amp;mtm_kwd=migrating-to-cloud-the-end)

    # Server Config
    # /etc/cloudflared/config.yml
    logDirectory: /var/log/cloudflared
    tunnel: 1b70-4325-9bb5
    credentials-file: /home/<>/.cloudflared/1b70-4325-9bb51.json
    no-autoupdate: true
    ingress:
      - hostname: ssh-<server>.breadinfra.net
        service: ssh://127.0.0.1:22
      - service: http_status:404

Finally, you can then configure your laptop with the below which allows your client to connect over ssh to the server

    # Laptop Config
    # ~/.ssh/config
    host unifi
     hostname ssh-<>.breadinfra.net
     user root
     ProxyCommand /opt/homebrew/bin/cloudflared access ssh --hostname %h

# Serverless

Serverless is a weird concept. Just means that you don't manage the server, and only deploy a docker container or just your code to it.

A great example of serverless is, my documentation site. I write markdown and then it gets rendered and hosted
[

Welcome

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/index.png)
](<https://documentation.breadnet.co.uk>)
By migrating [Bookstack to Mkdocs](https://breadnet.co.uk/migrating-off-bookstack/) I have been able to save $6 a month, by hosting the site on fly.io.

Not to keep going on, but a great example of why this is great is, it costs me absolutly nothing a month. The Git is free, the CICD is free as it's a public repo

{{<bookmark "documentation_breadnet_co_uk">}}

# Firewalls

Cloudflare have Argo Tunnels`Cloudflare Tunnels`, which allows you to punch out from your device, to the Cloudflare edge opposed to port forwarding. This is great for security as you're no longer doing one of the two:

1. Port forwarding to all the Cloudflare IP ranges
2. Port forwarding `tcp/80` and `tcp/443` to the entire internet

All you have to do, if you have restrictive outbound rules, is allow `udp/7844` and `tcp/7844`

# Wrapping it up

I know this was not the best blog, but if you have noticed, the site has been migrated to a new faster server, and now uses Cloudflare Tunnels (Dog fooding)

I have plans this year to spend some more time working with Kubernetes and possibly running some applications on k3s using cloudflare tunnels.

💸

I'm sorry, I have included Digital Ocean Refferal links, it helps keep the lights on. I don't run ads on this site, or track you across the web. I only track you across the site, but as soon as you leave I have no idea what you're up to.

Thank you for your understanding on this, you're welcome to buy me a coffee instead!
