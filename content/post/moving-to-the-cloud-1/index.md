---
title: "Moving to the cloud: Intro"
slug: moving-to-the-cloud-1
date: 2021-04-01T12:52:13.000Z
date_updated: 2021-05-05T14:17:46.000Z
summary: How did I move all my servers to the cloud? Well - Ansible, automation and CI/CD!
---

We will start this story with the facts. I am getting older, and I want to move out. As I get older, I am forced to accept more responsibilities, like paying for my own electricity.

As any selfhoster will tell you, this is what bleeds their wallets dry.

Moving to the cloud is not a decision I took lightly, there was alot of consideration put in to this. I was considering purchasing a newer server, probably a Dell r610 or something of that range and maxxing out the specs, but that pulls a fair bit of electricity, and where I plan to live, would also be in the same room as where I sleep. Fun

What cloud provider am I going with?

Well, glad you asked. I have decided to go with a french company called [OVH](https://ovh.com) as their prices are pretty hard to beat (at-least from what I have seen)

> This article was written before they burnt down their Datacentre, so I am sort of re-evaluating my decisions...

One node costs £3.60 pcm (vat inc) compared to £6 from digital ocean for a similarly specced machine. Not bad eh?

Let's do a cost break down per cloud provider, using their minimum viable product as well as correctly sizing the nodes
![Cost breakdown for Digital ocean vs OVH](/content/images/2020/07/image-1.png)
I was also considering doing something on GCP with pre-emptible vm's (They get shutdown at any time, moved around, basically abused, for a fraction of the cost)

Below is my ideal setup for moving my stuff off my host at home, to the cloud
![](/content/images/2020/07/Untitled-drawing.png)
Most of the things I run are native web applications, hence why I can slap them on a really basic vm. But, applications like Zabbix and Jellyfin are full blown applications that need COMPUTE! hence why they are on a slightly more powerful host.

Now, the issue I face here is that, I need to in effect, install 13 web apps. I don't really fancy having to do them one by one, so I plan to automate the bajeebus out of it (well, as much as possible)

A nice thing about using something like Ansible is you can see **exactly** what was done, so if something breaks, I have a rough idea of what the hell is up.

Another nice thing about ansible, is I can create a teardown playbook that dumps databases, copies config files etc to my local host, then allowing me to move cloud providers painlessly.

You can see my setup below.
It's most likely still work in progress, but you can copy parts if you so desire.

Now I am by no means an ansible expert, or a cicd engineer or what have you, but I can google and I'm pretty decent at it.
[

userbradley/breadnet-infra

Breadnet Infra setup though ansible. Contribute to userbradley/breadnet-infra development by creating an account on GitHub.

![](https://github.githubassets.com/favicons/favicon.svg)GitHubuserbradley

![](https://avatars2.githubusercontent.com/u/41597815?s&#x3D;400&amp;v&#x3D;4)
](<https://github.com/userbradley/breadnet-infra>)
This ansible playbook works methodically. Below are the steps I am striving towards:

1. Install nginx on `rev1`
2. Install Nginx and mysql on `app1` along with Analytics, Website, kanboard, status page and month server (used for reddit posts)
3. Install Nginx and mysql on `app2` along with Bookstack, Firefly, Passbolt, Nextcloud and may need to put docker in a container, this I will need to test
4. Install Zabbix, Jellyfin and Minecraft on `app3`

So far I have faced a few issues, mainly down to my own stupidity, and some down to a simple lack of knowledge of ansible.

The first being how I was calling what to install on each server, I had some funky fike structure like you see below.

The issue was you would call the file `setup.yml` which would call on the files in the folder called `setup` which would then run their respective jobs.

    .
    ├── hosts
    ├── README.md
    ├── setup
    │   ├── defaults
    │   │   └── main.yml
    │   ├── group_vars
    │   │   ├── all.yml
    │   │   ├── app1.yml
    │   │   └── app2.yml
    │   └── tasks
    │       ├── bookstack.yml
    │       ├── files
    │       │   ├── bookstack_env.j2
    │       │   ├── bookstack_nginx.j2
    │       │   ├── kanboard_config.j2
    │       │   ├── kan_nginx.j2
    │       │   ├── matomo_nginx.j2
    │       │   ├── status.env.j2
    │       │   ├── status.j2
    │       │   └── zabbix_apache2.j2
    │       ├── ghost.yml
    │       ├── - include: nginx.yml
    │       ├── jellyfin.yml
    │       ├── kanboard.yml
    │       ├── main.yml
    │       ├── matomo.yml
    │       ├── mysql.yml
    │       ├── nginx.yml
    │       ├── php7.2.yml
    │       ├── reboot.yml
    │       ├── scripts
    │       │   └── inscomp.sh
    │       ├── status.yml
    │       └── zabbix.yml
    ├── setup.yml
    ├── tasks
    │   ├── files
    │   │   ├── bookstack_env.j2
    │   │   ├── bookstack_nginx.j2
    │   │   ├── kanboard_config.j2
    │   │   ├── kan_nginx.j2
    │   │   ├── matomo_nginx.j2
    │   │   ├── status.env.j2
    │   │   ├── status.j2
    │   │   └── zabbix_apache2.j2
    │   ├── ghost.yml
    │   ├── main.yml
    │   └── scripts
    │       └── inscomp.sh
    └── test
        ├── defaults
        │   └── main.yml
        ├── hosts
        ├── roles
        │   ├── bookstack
        │   │   ├── defaults
        │   │   │   └── main.yml
        │   │   └── tasks
        │   │       └── main.yml
        │   ├── common
        │   │   └── tasks
        │   │       ├── mysql.yml
        │   │       └── php7.2.yml
        │   ├── defaults
        │   │   └── main.yml
        │   ├── jellyfin
        │   │   └── tasks
        │   │       └── main.yml
        │   ├── kanboard
        │   │   ├── defaults
        │   │   │   └── main.yml
        │   │   └── tasks
        │   │       └── main.yml
        │   ├── matomo
        │   │   ├── defaults
        │   │   │   └── main.yml
        │   │   └── tasks
        │   │       └── main.yml
        │   ├── mysql
        │   │   └── tasks
        │   │       └── main.yml
        │   ├── nginx
        │   │   ├── defaults
        │   │   │   └── main.yml
        │   │   └── tasks
        │   │       └── main.yml
        │   ├── reboot
        │   │   └── tasks
        │   │       └── main.yml
        │   ├── status
        │   │   ├── defaults
        │   │   │   └── main.yml
        │   │   └── tasks
        │   │       └── main.yml
        │   └── zabbix
        │       └── tasks
        │           └── main.yml
        └── setup.yml

Now those of you who do ansible day in day our are probably wanting to swat my house, and I'm sorry - You wont like this next part.

My solution on what tasks were to be run per server was so bad, that it actually made me consider giving up.

    ---
    - include: reboot.yml
      become: yes
      when:
         - reboot|bool

    - include: nginx.yml
      become: yes
      delegate_to: app2
      when:
         - inventory_hostname in groups['app1']
         #- inventory_hostname in groups['app2']
         - inventory_hostname == app[1]
         - inventory_hostname in groups['app1']|default([])
         - nginx|bool
      tags:
          - nginx

This was my attempt at getting it nginx to run on server `app1` - Not great.

I asked the kind people of reddit and someone pointed me in the right direction, now everything actually works for a start. So if anyone finds my page from googling 'How to run different playbooks on different servers' (not even close to what I actually needed) then check out how I have done it on github. You're welcome

My second issue I faced was that I use Nginx as I just found it so much simpler to understand. And yes, apache2 and I had a good childhood growing up, but times change
![](/content/images/2020/07/image-2.png)A meme for all you cool kids
And for some reason Apache2 was being installed when ever I ran the install php7.2 task.

Let's take a look at the task for a second (in breif)

    ---
        - name: Add PHP repository
          become: true
          apt_repository:
           repo: 'ppa:ondrej/php'
          tags: [php1]

        - name: Update repositories
          become: true
          apt:
           update_cache: yes
          tags: [php2]

        - name: Install php7.2 #Move to a global install
          become: true
          apt: name=php7.2 update_cache=yes state=latest
          tags: [php3]

        - name: Install php7.2-cli #Move to a global install
          become: true
          apt: name=php7.2-cli update_cache=yes state=latest
          tags: [php4]

Now those of you who have been dealing with linux and PHP longer than I've been alive will know exactly what the hell is going on here, something I did not.

So I went to the only place that keeps us Sysadmins employed, google.

> Does Apache2 auto install when installing PHP 7.2?

Yes - it does. See, I was installing `php7.2` which has a package dependency of... you guessed it `libapache2-mod-php7.2` which as far as I care to know, is apache2.

The way I figured this out was really painful, but I ran the playbook with `-t php1` then
`-t php2` and running `systemctl status apache2` till I saw it kick back a response.

My tip for anyone else dealing with weird issues like this? Just segment everything down, read the logs, take it a step at a time. This is the nice thing with ansible is you can see exactly what it did, and there seems to be quite a nice community over at reddit. You dont want to lean on them to spoon feed you, but use them as your last resort! (eg: after page 2 of google)
[

r/ansible

r/ansible: Automation for the People! A Subreddit dedicated to fostering communication in the Ansible Community, includes Ansible, AWX, Ansible …

![](https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png)reddit

![](https://b.thumbs.redditmedia.com/WmbHlRNHXOci-aUzBgHmKPMHRNvI2OtKF2XguHteO5A.png)
](<https://reddit.com/r/ansible>)
---

Now we have the fluff of what I'm doing out of the way, we can finally start running things!

---

Stay tuned for a part 2!

(Note from the Author: I will probably land up changing a lot of things)

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
