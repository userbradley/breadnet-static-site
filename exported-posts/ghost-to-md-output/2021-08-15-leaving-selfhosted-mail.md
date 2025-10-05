---
title: Why I chose to migrate my mail server
slug: leaving-selfhosted-mail
date_published: 2021-08-15T01:19:18.000Z
date_updated: 2021-08-15T01:19:18.000Z
tags: mail, cloud, dns, servers, security, #Import 2023-03-30 20:40
excerpt: Is it worth self hosting email?
---

Well, once again, this isn't something I expected to be writing about but here we are!

So if you've read any of my posts, you'd know that I self hosted my own mail server. At the time of writing, that server had been online for 2 years. I first installed it in 2018, and it's done well! 

Now, the main question here is why I've decided to migrate it, and where to?

---

So let's look at the pros vs cons of self hosting your own mail server:

1. First and foremost, it teaches you **so much **about how email deliverability works, and how temperamental it is. 
2. Increased privacy, the emails reside on **your **server that you control. No one else has access to the server (If you've set it up correctly) 
3. As many accounts as you want for the price of the server per month
This is nice to have, you can give friends and family email accounts and the milboxes can be as big as you want
4. Faster release tracks - Seeing as you're self hosting the server, you can upgrade and install new software when ever you want
5. Flexing rights, being able to tell people "Yeah, I host my own email server" 

There are more, but this is all I can think of at the moment

---

Now lets look at the cons

1. Reliability - If your server goes down, your emails aren't accessable
2. If your server goes down, you cant access emails
3. You are the only support staff for your email domain
4. **the amount of hackers and spammers**
5. Hard to secure **properly **(it can be done, but it's a never ending road of "what if I enable this"
6. Sender score - How will gmail office 365 etc inbox your mail (spoiler: spam)
7. Updates sometimes break things
8. You're responsible for **good **backups 

Once again, there are many more, but these are the main ones I can think of

---

As someone who hosted their mail server for **2 **years, I think I have enough experience here to say it was fun, but the novelty wears off after about 6 months. Let me detail some of the issues I had:

1. IP address was blacklisted, provider wouldn't change IP address
2. Provider had to be convinced to open port 25 etc
3. Certificates that auto-renew, you need to restart postfix 
4. Stopping and starting your mail server each time you make a change to the config
5. Log files aren't always useful and sometimes lead you down a rabbit hole
6. Lots of things to customize (and then break)
7. Server reboots would cause bounces in mail
8. Sender reputation was hard to get right
9. Inboxing was a **nightmare **on both google and microsoft
(If someone from ms or google is reading this, fight me, 1v1 me in club penguin)
10. Emails would have weird formatting, attachments wouldn't display correctly. 

Now I know from this article, it looks like I've spent most of the time taking a dump on hosting your own mail server, and whilst that is true, I highly reccomend it. If you or your team are responsible for emails, be it spam filtering or office 365 - You should run your own mail server.

Running your own mail server is great, albeit a little annoying and you need to be on top of things like backups etc, the learning is great!

In my opinion the best place to run your own mail server is for **internal only use**, so this could be you testing zabbix integrations, or just having an internal mail system for your IOT, or your team to shoot the shit at work and play.

## Cost

I was running my email on Digital Ocean for 2 years at $6 a month, which at the time of writing this (aug152021) it's around £4.33 a month for a server where as Office exchange online plan 1, is £3.60 

2 years running cost of Self hosting: 103.92
2 years running cost of M$ hosting: 86.4

Savings by M$ hosting it: 17.52

Whilst the 17.52 doesn't really seem like a big number, when we look at the hours it took to get working, we're looking at around about 80 hours over the 2 years, and considering I charge $17 per hour for contracting, that's $1360 worth of charges

vs

2 hours setup on Office 365: $34

---

Closing notes:

Despite the higher cost and time taken to self host, I highly recommend it, most blogs will tell you don't do it, but I really think this should be every sysadmin's weekend project! It's fun and something usable!

As always, you can [contract me](https://www.upwork.com/freelancers/~01c61ee9802b94133e) if you want help or [contact me](mailto:website@breadnet.co.uk)
