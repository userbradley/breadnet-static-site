---
title: HTML 5 Speed test server
slug: html-5-speed-test-server
date_published: 2020-06-09T17:56:43.000Z
date_updated: 2021-05-02T01:48:11.000Z
tags: How To, #Import 2023-03-30 20:40
excerpt: How to install a HTML5 based speedtest server for your network, family and friends!
---

Originally this was posted on my [old](https://www.old.breadnet.co.uk) website but seeing as several people still come to my site for this, I will add it here

Firstly you will need to SSH to the server you are running. If you are unsure how to do this, there are lots of good videos on youtube. If you're still struggling, hit the Contact button at the top and get in touch! 

Install apache2 and php 

    sudo apt-get install apache2 php -y

Once that is done, enable apache2 to start on boot. This may vary but on most modern systems you can use 

    sudo systemctl enable apache2
    

In your current directory, git clone the repository to your server

    git clone https://github.com/adolfintel/speedtest.git

Copy all the files from here in to `/var/www/html` with 

    cp speedtest/* /var/www/html

Once that is done, go to the `/var/www/html` folder with `cd /var/www/html`

In here, delete the index.html

`sudo rm index.html`

Now depending on what page you like, I chose the one called 'Example-pretty' as it sounded nice, you just need to change it's name to index.html/

I suggest copying it

    touch index.html
    cp example-pretty.html index.html

Once done, restart apache2 for good measures

    sudo systemctl restart apache2

Go to the IP address or host name of your server, and you should be presented with the page!

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
