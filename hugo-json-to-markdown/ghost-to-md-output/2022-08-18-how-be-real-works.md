---
title: How BeReal works
slug: how-be-real-works
date: 2022-08-18T10:00:00.000Z
date_updated: 2022-08-25T00:33:47.000Z
summary: Today we take a deep dive on how the BeReal app works, behind the Scenes
---

And no, this not a *how to,* on how to use the app. But a deep dive on the infrastructure behind BeReal, and the engineering decisions that were taken.

---

Firstly, what is BeReal?

BeReal is an app designed by a French Developer called [Alexis Barreyat](https://fr.linkedin.com/in/alexisbarreyat), which aims to break down the highly edited social media that we have come to know and hate.

You get a notification once a day, like the below, where you are urged to whip out your phone, and snap a pic.
![The BeReal notification: An iOS notificaiton bubble with the words &quot;Time to be real&quot; surrounded by two warning symbols. Below the  warning is the words &quot;2 min left to capture a BeReal and see what your friends are up to !&quot;](__GHOST_URL__/content/images/2022/08/image.png)BeReal Notification
The application makes use of both the front facing and back facing camera to give *real view* in to what you're up to.

See the example below:
![](__GHOST_URL__/content/images/2022/08/BeReal_example.png)BeReal, where I was on the roof of a building
Enough about the app, let's take a look at how it works, under the hood.

---

## The Legal stuff

I want to make this very clear, this does not go against the terms of service, as nothing malicious was intended, I did not send requests to the application, merely peeked in to the network traffic the application was sending.

Below is the part of the ToS' that could apply to this post, how ever for legal reasons, I must specify that there was no tampering as this is network traffic one can see when running an SSL proxy on their network.

> Tamper or attempt to tamper with the proper working of the Application, interfere with access to the Application or circumvent any measures we may use to block or restrict access to the Services;

Everything I say below is purely speculative, I do not work for, nor ever have worked for the BeReal Company/ Corporation.

For any legal issues, please contact legal@

---

## The cloud Provider

From what I can see, BeReal makes extensive use of the below cloud providers

### DataDog

DataDog is being used for in-app metrics, as well as logging and something called RUM (Real user monitoring) - Which looks in to how the application is used by the user

### OneSignal

One**S**ignal is being used for the the push notifications that users all over the world receive. I'm not sure about how Time Zones work, so don't ask me.

### Amplitude

I'm still not 100% sure on this one, but from their [website](https://amplitude.com) - They seem to be a user journey tracking tool, so how you signed up, and also surfacing better metrics.

### Google Cloud

BeReal makes **heavy** use of the google cloud **global architecture**.
A good example of this is they use serverless where ever possible, as well as managed services.

---

## The API's

The application is pretty bare bones, but the way it makes the API calls is... interesting.

> This blog post has taken over 2 months to write, and since starting they have implemented Certificate Pinning, preventing the Network wide proxy from intercepting the app traffic.

BeReal uses a GCS bucket called `storage.bere.al` running on GCS. This bucket is behind a Global Load balancer on Google cloud.

We can try and run a gsutil ls gs://storage.bere.al but will get an IAM error

    ➜ gsutil ls gs://storage.bere.al/Photos/

    AccessDeniedException: 403 <>k does not have storage.objects.list access to the Google Cloud Storage bucket.

So it seems the DevOps team are on top of the Bucket IAM permissions.

When a user takes a photo, (this is after the notification goes off), BeReal app sends a Post to `/**sendCaptureInProgressPush**`which from what I can tell, publishes a message on Pubsub:

    {
        "data": {
            "photoURL": "Photos/<me>/profile/<me>-1655905537-profile-picture.jpg",
            "topic": "<me>",
            "userName": "<me>"
        }
    }

And the response being

    {
        "result":"projects/alexisbarreyatbereal/messages/7517087177659076139"
    }

This let's BeReal know that there will be an upload for the user.

When the user has finally taken the photo, it calls to `content/post` API, and sends the below:

    {
        "backCamera": {
            "bucket": "storage.bere.al",
            "height": 2000,
            "path": "Photos/<me>/bereal/7c44d6e8-086b-4a18-b8b4d3785f58cda8-1660122851.jpg",
            "width": 1500
        },
        "frontCamera": {
            "bucket": "storage.bere.al",
            "height": 2000,
            "path": "Photos/<me>/bereal/7c44d6e8-086b-4a18-b8b4d3785f58cda8-1660122851-secondary.jpg",
            "width": 1500
        },
        "isLate": true,
        "isPublic": false,
        "location": {
            "latitude": <>>,
            "longitude": <>>
        },
        "retakeCounter": 4,
        "takenAt": "2022-08-10T09:14:11Z"
    }

Something of note here, is the way that BeReal stores images in a way that I can't just crawl all the Images, and download them all.

Something of concern here is the Precise location of a post, down to a 1M accuracy.

    "location": {
            "latitude": <>>,
            "longitude": <>>
     },

You're wondering what we can do with this data?

We can scrape it for all our friends, and plot it out in Grafana or Tableau and work out where they spend a lot of time, as well as predict places of work, partners houses etc.

[Someone else who reverse engineered the app did something similar](https://shomil.me/bereal/#:~:text=Now%20one%20might,people%E2%80%99s%20homes%3F%20Workplaces%3F)

### Let's break down the Image URL

    Photos/<me>/bereal/7c44d6e8-086b-4a18-b8b4-d3785f58cda8-1660122851.jpg

Image URL
`Photos` - This is the subdirectory in the Bucket that the images are stored in (This is down to how GCS and Load balancers interact with each other)

`<me>` - This is going to be the Users Unique ID, AlphaNumeric string

`bereal` - Not too sure why this is in here, I assume this may have something to do with where videos are also stored?

`7c44d6e8-086b-4a18-b8b4-d3785f58cda8` - I'm not too sure about this, I would *assume* that it's going to be a unique ID for that day and user to upload the image with

`1660122851` - Linux Epoch time the image was finalized
![](__GHOST_URL__/content/images/2022/08/image-1.png)

### Perhaps, the most interesting API

One of the API's that stuck out the most was the `cloudfunctions` one

    https://us-central1-alexisbarreyat-bereal.cloudfunctions.net

This is an application that runs on Google App Engine (GAE) which does some cool things:

- Convert Id's to Names
- Convert Phone numbers to users
- Publishes a message to Pub/Sub
- [Deprecated] Suggest friends you may know

Now this is useful especially from a data exfiltration standpoint as you are able to convert a butt load of Phone numbers to Users, and do some Osint.

## Public Feeds

The public feeds works a different way compared to your actual friends feeds.

1. You navigate to the feeds page
2. It loads the feeds page
3. It makes subsequent calls to the [`https://us-central1-alexisbarreyat-bereal.cloudfunctions.net/getUserNames`](https://us-central1-alexisbarreyat-bereal.cloudfunctions.net/getUserNames) API to convert `uid`'s to Usernames
4. Loads the images from the storage bucket

---

## Closing Notes

There are alot more API endpoints I have not found yet, as well as don't want to mention from fear of lawyers coming at me.

But I have made a list of API endpoints, as well as responses etc available on my Github.
[

GitHub - userbradley/BeReal: How does BeReal work (Under the hood)

How does BeReal work (Under the hood). Contribute to userbradley/BeReal development by creating an account on GitHub.

![](https://github.githubassets.com/favicons/favicon.svg)GitHubuserbradley

![](https://opengraph.githubassets.com/008e444a696cd7cde3b7e5b5219f89fafbcd509bee2c1277c4172ed25bc277d3/userbradley/BeReal)
](<https://github.com/userbradley/beReal>)
BeReal seems to be cool application, and their intentions are good, but I am somewhat suspicious of what they do with the data, as I mean, they have daily coordinates of where you are and can build patterns around it.

---

## About the Author

Bradley is the DevOps engineer for the biggest Pet care company in the UK, specializing in GCP as well as finding solutions for all problems.

His blog posts go from How to's to Infrastructure deep dives as well as reverse engineering.
