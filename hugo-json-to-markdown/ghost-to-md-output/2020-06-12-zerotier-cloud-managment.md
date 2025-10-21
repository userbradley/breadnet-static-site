---
title: How to manage remote servers using Zerotier
slug: zerotier-cloud-managment
date: 2020-06-12T18:07:38.000Z
date_updated: 2021-05-02T01:47:06.000Z
---

(it's hard to find photos for an article like this)

Currently, I use zerotier to manage cloud servers in Amsterdam, the UK as well as in the USA. Despite the huge distance there is surprisingly mininal latency. In this article, we will look in to how to use it to manage remote servers via ssh, what firewall rules you should setup to prevent people from trying to login.

prereqs: Zerotier and ssh knowledge
[

Getting started with Zerotier

Let’s look at how we can use zerotier to bridge the gaps between us and a remote server to connect using private IP’s and not mess about with firewalls

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1512699126689-b59fb4e97c92?ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;fm&#x3D;jpg&amp;crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;w&#x3D;2000&amp;fit&#x3D;max&amp;ixid&#x3D;eyJhcHBfaWQiOjExNzczfQ)
](__GHOST_URL__/getting-started-with-zerotier/)[

A beginners guide to SSH

Sweet, you just got a linux server running on <insert cloud provider > but nowyou need to actually do something on it. You tried to use the web console but now you need to paste something in... Itdoesn’t work? Shit. Luckilly SSH was designed to allow for Secure SHell accessto a server. (Hence S…

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1586772002345-339f8042a777?ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;fm&#x3D;jpg&amp;crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;w&#x3D;2000&amp;fit&#x3D;max&amp;ixid&#x3D;eyJhcHBfaWQiOjExNzczfQ)
](__GHOST_URL__/a-beginners-guide-to-ssh/)
Once you've got your head around connecting a machine to zerotier, as well as how to setup seure ssh, we can look more towards the firewall rules. How ever, instead of telling you to go read something I will explain some basics here just to make life easier.

Firstly start with getting zerotier setup if you haven't already:

You will need to create an account and install it on both machines.

Create an account at [my.zerotier.com/](https://my.zerotier.com/)

Once your account is creates, click `Networks` at the top and then `+ Create a Network`

You will see one appear under the `Your Networks` section
![](__GHOST_URL__/content/images/2020/06/image-14.png)
Click the ID of the network and pick the network range you want. You NEED it to not be used anywhere else!

> A note to my homies who hage CGnat, make sure that you check their range before you pick one, as well as your own internal range

![](__GHOST_URL__/content/images/2020/06/image-15.png)
Once that is done, you will need to install Zerotier on the machines you want to connect to each other.

If you trust SSL on linux:

    curl -s https://install.zerotier.com | sudo bash

Else, Zerotier have good instructions [here](https://www.zerotier.com/download/)

Now we need to add the server's to the network!

    sudo zerotier-cli join <network ID>

If it returns with `200` it's happy days. Wait a few minutes and you should see the first server show up in the management page. Add a name to it so you know what's what.

Rinse and repeat for all the other devices.

Now that Zerotier is configured, you can optionally enable SSH Keybased authentication. For cloud servers and servers that will be managed by many people, you're going to want to set this up. I wont write how to do this, as I'm hoping you took the time to read the SSH article at the top.

Seeing as this machine is hopefully a new one, and you're just about to get started managing it, you're going to want to enable ufw.

    sudo ufw enable

Now that it's enabled, we will need to add in our IP address range of either zerotier, or just one machines zerotier IP address to the ufw rule for allowing ssh

    sudo ufw allow from <zerotier>/<subnet> to any port 22

or if you want, just an IP address

    sudo ufw allow from <ip> to any port 22

The rule I go with which allows me broad access is to allow all ports from the zerotier ip range. This allows me to manage databases', websites and ssh.

    sudo ufw allow from <zerotier>/<range>

The open the ports for services you may be running. HTTP(S) are below for example

    sudo ufw allow http
    sudo ufw allow https

By defaul UFW is set to deny all incoming connections till you explicitly allow ports to be open

Now we can apply the rules

    sudo ufw enable
    sudo ufw reload

If you want to see the rules, just type

    sudo ufw status numbered

and then to delete a rule it's just pick the number from the previous command and

    sudo ufw delete <numner>

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
