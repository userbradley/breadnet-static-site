---
title: What I'm running
slug: what-im-running
date_published: 2020-06-05T17:35:25.000Z
date_updated: 2023-11-24T14:20:12.000Z
tags: servers, #Import 2023-03-30 20:40
excerpt: Finally, the question you never had about my stuff has been answered
---

All my servers are currently (and always will be)  running Linux. My choice is mainly Ubuntu LTS how ever there are 2 Debian VM's running.

I have got my backups of VM's done over XOA which copies the full image of the VM to an external hard drive.

For file based backups as well as database backups, I have writted my own scripts to back up servers to a Wasabi bucket. This is done for, you guessed it, Databases as well a media servers as it doest not make sense to backup 300gb vm easch week when nothing changes

Server: Dell R710

Use: Hypervisor

OS: [XCP-NG](https://www.google.com/url?q=https%3A%2F%2Fxcp-ng.org&amp;sa=D&amp;sntz=1&amp;usg=AFQjCNHpemVlzMiyZtgC6GhF_G6v1rq7rQ) (centos basically)

VM's:

1: Firefly-iii
2: Grafana
3: phpipam
4: invoiceninja
5: JellyFin
6: Librenms
7: Nextcloud
8: Database server
9: Unifi
10: Xen Orchestra
11: Zabbix
12: Bookstack
13: postfix and dovecot with dkim
14: Leantime Project managment
15: Status page
16: Bind dns
17: Nginx Reverse proxy
18: Kanboard

I have a few sites that are publicly accessible:

- [Status page](https://status.breadnet.co.uk/?pk_campaign=BreadnetMain&amp;pk_kwd=https%3A%2F%2Fbreadnet.co.uk%2Fwhat-im-running%2F)
- [Bookstack](https://documentation.breadnet.co.uk/?pk_campaign=BreadnetMain&amp;pk_kwd=https%3A%2F%2Fbreadnet.co.uk%2Fwhat-im-running%2F) (update 2023: Migrated to mkdocs)
- [email server](https://www.youtube.com/watch?v=dQw4w9WgXcQ&amp;pk_campaign=BreadnetMain&amp;pk_kwd=mailServer)

All the names link to their respective project. They are all FOSS and run on linux

Second server (Bottom one)

Server: R710

OS: [Ubuntu 18.04 LTS](http://www.google.com/url?q=http%3A%2F%2Freleases.ubuntu.com%2F18.04%2F&amp;sa=D&amp;sntz=1&amp;usg=AFQjCNH3s1iSgARCKCp3uTjMvN2c83Vb2w)

Use: In house Min.io server

Screenshot of XOA

> I just want to add that I know the photos are broken - it's in my to do list

![](https://lh5.googleusercontent.com/XAPS6nULuTmhGaHC7RuES25PCLfOIBRjd_7HtRANUJrkLR9LL6Xce8dJNxqVw1mNCsvzENRDl5tAUUxpTfCqZcAjlp1pNBJlZQsHr0_bkbEN0W4LjI0=w1280)![](https://lh3.googleusercontent.com/Il4pC2DJSA9x560nvPcXFdmzXnkcjR4lnlY6i4BQqxZwjoI_8L4OBh3EkWXvvbozRaaMi3ec6FEBmb_7CWT0346fqzpAZnfkIVqJCVd_QkwchOBqSg=w1280)
Xcp-ng host
![](https://lh4.googleusercontent.com/YnxjBvCN5qrTW4zEESgGvZPeknWCqR8BPj0vfSqVOrbI24z_gDqM6FSR2qazD1I3M7_JfZnV6SU48GS0JAwetY_yYA72znBqQK8gzJKsm5znOknbzQ=w1280)
Firefly login screen
![](https://lh6.googleusercontent.com/ABp5kC-WPMbIEHlOTpKoZDm-rggMis3UsRxsWoF-xxSQYEIl7EFIcxSAjl2voS0KBHYiaPeP1MDo_yss5Ow0A4XLp0Q3kVXeIMzo2mcqOIWuVjWCoxw=w1280)
Jellyfin Home screen
![](https://lh4.googleusercontent.com/ZnJS5SPIUaDYldCQ46tLZfgFCtNQKdTsI_0UABLKQupUYKFF7eipix4MK10vUYuCcRSmmBMGQ1p7ImIuzS8hriG3lWq_1Dhr5y2-5mTUH7sL4CsUgg=w1280)
Unifi dashboard
![](https://lh5.googleusercontent.com/u3ViM-3nkpKF0aLW6S-NgvMs3UoByTS88I8AYlb_MCRi0dxLYvX8oybZLYg2mL-osOdHsOx6EMJ7UipqSP8YaE4x2cYQDJjdCyBpJ-bfHuGWjj8qMg=w1280)
Nextcloud - Login page
![](https://lh6.googleusercontent.com/ghCKGzhrPTG_CmB9GrudtEaGVgmEYTOiMXJaQdu2DIZVnqFQMe90aRJqXgNoLaT12esEgVJLuqhX01IM4WnLThTneiGxvHBgPbAFCHSQrH8ccXPIWGA=w1280)
Database server - Phpmyadmin
![](https://lh5.googleusercontent.com/zD9KmDxsB4yxD7tSAvWfGgXnYyQrYL65r1Ip3xEUvun0Gpyh6A0x31bD4ymqvgW-YJLi6yQ44qxbMV38qNX11_03KpmSFhLmjVXC6I324hiradkaunc=w1280)![](https://lh3.googleusercontent.com/V9imIVZxj2wcSTac6d2nrDxEkUP6bNE4JH0OJllYCE1rRrHZRGe_SNZvQEKJE1G3nLg9fSykSi_CcOJECRmP3kTz0unUqysZsm-G7DNgM-P53yDWyQg=w1280)
Leantime
This is the server I use to manage my projects and a built in kanboard.
![](https://lh4.googleusercontent.com/2pGT3PFBVXCzogsS68HJgHQo4DbFLgBVN36mISdDJ1JC6BzrkxrRZA8Z6COz_0M-_WkvH5TZhMDLMJSVAhXpycJNwo5670Hlo9WeFG7UGErnkVOx3w=w1280)
Digital ocean, this is where I have my public facing servers
![](https://lh5.googleusercontent.com/bEHuIzfp3uNsUmwMJPYrIqEW1wWUmldZcyOu0DriywL07-L3Vahif7QJARQIgyarFzhTxYw_wpEdtgYTpCq2yb2rsB-ZJvs7BaiCl9d0dmIpukCZwCYV=w1280)
