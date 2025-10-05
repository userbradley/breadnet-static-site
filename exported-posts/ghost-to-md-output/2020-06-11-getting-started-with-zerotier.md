---
title: Getting started with Zerotier
slug: getting-started-with-zerotier
date_published: 2020-06-11T20:54:45.000Z
date_updated: 2021-05-02T01:47:35.000Z
tags: How To, #Import 2023-03-30 20:40
excerpt: Let's look at how we can use zerotier to bridge the gaps between us and a remote server to connect using private IP's and not mess about with firewalls
---

Zerotier is something I struggle to sumarise. The best way I can explain it is a mesh VPN that requires no setup on routers or port forwarding. It overlays a 'lan' if you will that you can connect servers to from anywhere. If possible it will pass traffic from host to host, but if that is not doable, it will bounce it past their servers.

Zerotier promise encryption, so I guess there's quite a bit of trust. They are Opensource so you can look in to their code if you like

> All traffic is automatically end-to-end encrypted using keys only you control. Access to virtual networks is controlled by certificates.

[

ZeroTier, Inc.

Directly Connecting the World’s Devices with Universal Software Defined Networking - ZeroTier, Inc.

![](https://github.githubassets.com/favicons/favicon.svg)GitHub

![](https://avatars2.githubusercontent.com/u/4173285?s&#x3D;280&amp;v&#x3D;4)
](https://github.com/zerotier)Zerotier Github
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

If you want your friends to be able to join your locally hosted game server, or view an internal webpage and you don't [fancy setting up a reverse proxy](__GHOST_URL__/nginx-reverse/) then you can get them to join your zerotier network. 

It works the same way a lan does, except it spans over great distances and can be used (I don't suggest it) as a VPN

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
