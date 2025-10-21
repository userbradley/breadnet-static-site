---
title: Installing your_spotify
slug: your-spotify-2020
date: 2020-06-05T17:40:39.000Z
date_updated: 2022-10-23T16:18:56.000Z
summary: Your_spotify is a web application running on docker showing you stats about your account in the past 24 hours as well as current.
---

This page is now outdated.
[

Installing your_spotify

Your_spotify is a web application running on docker showing you stats about your account in the past 24 hours as well as current.

![](https://breadnet.co.uk/favicon.png)breadNETBradley Stannard

![](https://images.unsplash.com/photo-1532354058425-ba7ccc7e4a24?ixlib&#x3D;rb-1.2.1&amp;q&#x3D;80&amp;fm&#x3D;jpg&amp;crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;w&#x3D;2000&amp;fit&#x3D;max&amp;ixid&#x3D;eyJhcHBfaWQiOjExNzczfQ)
](/your-spotify-2020)
---

I came across this beautiful project by someone called Timothee Boussus or better known as [Yooooomi](https://github.com/Yooooomi/your_spotify) on Github. This project displays stats about your spotify account like recently played, most listened to artists in near real time.
[

Yooooomi/your_spotify

Self hosted Spotify tracking dashboard. Contribute to Yooooomi/your_spotify development by creating an account on GitHub.

![](https://github.githubassets.com/favicons/favicon.svg)GitHubYooooomi

![](https://avatars1.githubusercontent.com/u/17204739?s&#x3D;400&amp;v&#x3D;4)
](<https://github.com/Yooooomi/your_spotify)[>

r/selfhosted - YourSpotify

84 votes and 36 comments so far on Reddit

![](https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png)reddit

![](https://external-preview.redd.it/pWsf1-4nzsxAO9oN7whpPEyHEF3xY0NI_ggA3sakpdo.jpg?auto&#x3D;webp&amp;s&#x3D;c5c9eb469e5369a2096718fbd20b8b2d9dd0b27c)
](<https://www.reddit.com/r/selfhosted/comments/fjjw0j/yourspotify/)![Pages>](/content/images/2020/06/68747470733a2f2f692e696d6775722e636f6d2f77624f687030462e706e67.png)
You will need to have some knowledge of docker. I have a quick write up [here](https://bookstack.breadnet.co.uk/books/kb-articles/page/docker-intro-and-notes) on how to install it on Linux.

Once your docker is up and running, we will need to gitclone this to our computer. I prefer to keep all my github projects in one folder. Where you put it is up to you.

    stannardb@bread-d1:~/github$ git clone git@github.com:Yooooomi/your_spotify.git

Once that's downloaded, we can go to [developer.spotify.com](https://developer.spotify.com/dashboard/applications) and create a new application.

Login and click 'Create an app'
![](/content/images/2020/06/image-2.png)
Name your app as you like. I called mine 'Docker' because #originality Answer the questions and make up something on what it does. I just wrote docker again. Sign away your first born and family name.
![](/content/images/2020/06/image-3.png)
Keep this page open as we will need it again.

I had some issues with the config file so you can use mine below. It's based off the original except I have had to change the name of the mongo container.

Save this file as docker-compose.yml

    version: "3"

    services:
      app:
        image: yooooomi/your_spotify_server
        container_name: express-mongo
        restart: always
        ports:
          - "8080:8080"
        links:
          - mongo
        depends_on:
          - mongo
        environment:
          - API_ENDPOINT=http://localhost:8080 # This MUST be included as a valid URL in the spotify dashboard
          - CLIENT_ENDPOINT=http://localhost:3000
          - SPOTIFY_PUBLIC=__your_spotify_client_id__
          - SPOTIFY_SECRET=__your_spotify_secret__
          - CORS=http://localhost:3000,http://localhost:3001
          #- CORS=all
          #- MONGO_ENDPOINT=mongodb://mongo:27017/your_spotify
      mongo:
        container_name: mongo_spotify
        image: mongo
        volumes:
          - ./your_spotify_db:/data/db

      web:
        image: yooooomi/your_spotify_client
        container_name: web
        restart: always
        ports:
          - "3000:3000"
        environment:
          - API_ENDPOINT=http://localhost:8080

On the spotify webpage, replace the **`your_spotify_client_id`**with the public key and then the same thing for the secret. Obviously using the secret.

Next go back to spotify and click edit.
![](/content/images/2020/06/image-4.png)
In here scroll down till you find redirect links:
![](/content/images/2020/06/image-5.png)
I had some issues the first time so I slapped both these in there. If you're hosting this on a publically accessable server, you will put the address such as:

`https://spotify.breadnet.co.uk/oauth/spotify/callback`

just append `/oauth/spotify/callback` to the end of the address to access this.

Now we can start actually using the application. In the same folder as your `docker-compose.yml` file run `docker-compose up` and it should whirr away. it took mine around 5 minutes the first time.

Depending on where this is being hosted, you can go to `http://localhost:3000` or where ever you've got it. If you're going to have this publicly hosted, use a reverse proxy like nginx or traefik

Once running, click register and make a username and password up:
![](/content/images/2020/06/image-6.png)
then login. Once loggedin you'll be presented asking to connect to spotify. Click and login.

Give it around 20 minutes for good measure and you *should* start to see stats being generated.

If you're having issues, check the [[g](https://github.com/Yooooomi/your_spotify/issues?q=is%3Aissue+)ithub](<https://github.com/Yooooomi/your_spotify/issues?q=is%3Aissue+>) issues or the reddit post from the top!

> A quick update. if you see that you cant login to the app, check all the docker containers are running. I found that after rebooting one of the containers had not started up and thus I was unable to login

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
