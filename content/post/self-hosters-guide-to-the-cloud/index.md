---
title: Self hosters guide to the cloud
slug: self-hosters-guide-to-the-cloud
date: 2021-04-26T23:00:00.000Z
date_updated: 2021-05-05T14:10:57.000Z
summary: Think 'the hitchhiker's guide to the galaxy' but for the cloud, and for those of us who self host
---

- services to offer
- how it's different
- ways to manage it
- best practices
- how to make the most of it
- companies I suggest

I'll be honest with eneryone here, I never thought I would ever write something like this.

The time has come, I am moving my servers to the cloud.

I still am a selfhoster as I rely on my own knowledge and experience to operate all my services and ensure that they are online for the people who have come to rely on them.

The reason I am moving to the cloud is since moving out of my parents, I need to decom all my on premise infrastructure as the network connection isn't the best and also it's at my parent house.

Let's take a look in to the reasons you would want to move your lab to the cloud (If you plan on still labbing), how to set it up and then how to maintain it.

---

A lot of cloud providers will have different plans and offerings. Let's focus real quick on the terminology they use, as some of it is literal bullshit

IaaS : Infrastructure as a service:
 This would be renting the servers, network (yeah you can do that), storage etc from the  provider

PaaS : Platform as a service:
 This is delivering a platform to the user, so the developer just runs their code on their       service and don't have to manage the infrastrucute. I'm not sure what their underlying       tech is, but I'm probably going to go with K8

SaaS : Software as a service:
 This would be using something like Google drive, SAP etc. You use the software as a       service

DBaaS : Database as a service
 If you run a lot of applications that need a database, I suggest you use your cloud providers database offering as it's got backups usually and runs as a cluster with HA.

You will want to look at each cloud providers offerings. One thing to note is that you can actually land up causing cloud lock in.

<Place holder till I write about that>
![](/content/images/2021/04/image-7.png)I will be writing a blog post shortly about that
You can avoid vendor lock in (which in this case is a cloud provider) by ensuring you have a planned exist strategy, as well as ensuring that you have 100% ownership of your data.

If you are developing an application, use docker! You can run docker on basically anything [(well, almost)](https://stackoverflow.com/questions/53527277/is-it-possible-to-run-containers-on-android-devices) you then can bang it in to K8 (which every cool cloud provider will have)

Finally once you've picked your cloud provider you then have the whole setting 'it' up.
'it' being what ever you're hosting at home.

The common misconception I've seen with people and the cloud is that:
![](/content/images/2021/04/image-8.png)
no. Just no. Stop. I can understand that thought process if you were new to computers, but you guys running a datacetnre in your mom's living room, no.

Let me introduce you to a little friend called 'Firewalls'

At an absolute minimum, your cloud provider will have a form of managed firewall service where you can click and point.

My favourite way of this, which GCP does quite well is:

You create the firewall rules first. So we will create one allowing http/s access to our instances, and then we say we want to add it to any instance that has the tag of `web` assigned under the network section:
![](/content/images/2021/04/image-9.png)
then under our instance we get this:
![](/content/images/2021/04/image-10.png)
Point in case, if you are still worried about people getting to your servers, then you can make a career out of that as a cyber security expert. Start studying my friend!

Now we have that out the way, we will talk about how to actually deploy.

Running on the cloud has some perks. You get access to things like API's where you can tell the cloud:

    Dear sir,

    I write to you to request one server with a gigabyte of ram, 1TB data and 2vcpu

    Signed,

    Bradley

(Side note, if you want to see how to actually do it: --> [Here](https://gitlab.breadnet.co.uk/terraform/modules/ovh/instance-ports/-/blob/074ac784d6c9533a7de7c4c4de32ecaa0c6f72f7/main.tf) <– )

and it will give you a server.

Now you're probably wondering why I mention this? Why cant I just do things normally? Ah well! You can manage everything as code now. You can use something like Terraform and Codefresh with Git to manage your infrastructure.

If you're using Terraform, I strongly suggest you learn to create modules so you can have a quick and standardised way to create instances and stuff. Feel free to checkout my modules I have created for OVH/ Openstack:
[

ovh

GitLab Enterprise Edition

![](https://gitlab.breadnet.co.uk/assets/touch-icon-ipad-retina-8ebe416f5313483d9c1bc772b5bbe03ecad52a54eba443e5215a22caed2a16a2.png)GitLab

![](https://gitlab.breadnet.co.uk/assets/gitlab_logo-7ae504fe4f68fdebb3c2034e36621930cd36ea87924c11ff65dbcb8ed50dca58.png)
](<https://gitlab.breadnet.co.uk/terraform/modules/ovh>)
The use case for this is repeatability and simplicity. If I want to deploy another instance to my stack, I simply create another module request in `main.tf` and then it's done.

A nice example of this is my DNS records are all managed from Cloudflare, through terraform. Once I push to master on gitlab, Codefresh picks up the changes and deploys them.

At work we are Codefresh partners, but I use them personally as they are actually really good. (Just a little disclaimer)

From here, now that your infrastrucute is created, you need to provision your instances.

I suggest using something like an Ansible playbook or bash scripts (if push comes to shove)

If you're going to be working on Digital ocean, I suggest learning [Packer](https://www.packer.io) for image creation from a playbook/ script.

---

Lastly there is backups and migrations.

A lot of things that people forget with running on the cloud is backups as it's out of their sight and mind.

The recent fire that was [experienced by OVH speaks to this](https://www.reuters.com/article/us-france-ovh-fire-idUSKBN2B20NU) - Just because it's in the cloud, doesn't mean that it's not still your responsibility to maintain it.

For this, I recommend daily snapshots of the instance, as well as file based backups to something like S3. I personally recommend something like Wasabi storage as they are pretty cheap.

Daily snapshots are managed by your cloud provider, but you can also use something like backuppc running on a pi at home with a 2tb drive (This is what I do to follow the 3-2-1 rule)

For example from my mail server to Wasabi is over a 200g connection so daily file backups are easy.

Oh that's something I forgot to mention about the cloud is the bandwidth. You will really enjoy this alot.

### Companies I suggest

[Digital ocean for hosting](https://m.do.co/c/77be3c3aa96c)

OVH for hosting

Gitlab for code and Cicd

Codefresh for hosted CiCd

Cloudflare for DNS

Ubuntu as an OS provider

[Zerotier for Mesh overlay](zerotier.com)

### How to make the most of the cloud?

Having since moved to my own place, I don't have the luxury of running my own servers so I have had to throw everything on the cloud.

The nice thing here is that if you need a resource for say, 30 minutes, you only pay for 30 minutes.

I sometimes use a throw away instance (created and destroyed via terraform) for downloading large files quickly. I will download it to the instance, work on it there and push it back, utilising the bandwidth available.

OVH and most cloud providers don't block ports 6881-6889 6969 so if you're hosting linux ISO's for the community to download faster, god for you! <3

Finally, you have the platform to help and inspire people, host a website with Ghost/ wordpress/ CMS of your choice!

Safe hosting and don't open anything other than tcp:80/443 to the web!

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
