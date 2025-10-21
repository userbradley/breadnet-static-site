---
title: Migrating off of Bookstack
slug: migrating-off-bookstack
date: 2022-09-30T00:14:48.000Z
date_updated: 2023-11-24T14:29:47.000Z
summary: Saying good bye to BookStack 👋 (for now)
---

Organizing documentation is hard.

I'll start the post off with that.

---

Since I started my home lab back in 2018, I knew I needed a place to write down important information like the server name, where it's located and all the other stuff that goes along with that - Example below:
![](__GHOST_URL__/content/images/2022/09/image.png)
For a long time, that was bookstack. One of my favourite pieces of open source software.

For those of you who aren't familiar with BookStack:

- Self Hosted Wiki
- `wysiwyg` and `markdown` support
- Supports LDAP, AD and other integrations
- Built in PHP
- Used MariaDB as a database to store content
- Full API
- [Recently hit 10k Stars](https://www.bookstackapp.com/blog/10k-stars-and-a-look-back-at-first-sharing/)

For more information on BookStack, you can visit the site:
[

BookStack

BookStack is a simple, open-source, self-hosted, easy-to-use platform for organising and storing information.

![](https://www.bookstackapp.com/images/favicon-196x196.png)BookStack

![](https://www.bookstackapp.com)
](<https://www.bookstackapp.com>)
At the time of writing, I currently have 125 pages active:

    MariaDB [bookstack]> select count(slug) as "current pages" from pages;
    +---------------+
    | current pages |
    +---------------+
    |           125 |
    +---------------+
    1 row in set (0.001 sec)

I will add, that using BookStack has been amazing for my documentation writing skills. So much so, I have free-lanced simply being on calls with engineers, taking their *engineer* speak, and turning it into documents that the average Joe can understand.  

## I speak so highly of BookStack... Why migrate?

It's come to the point where the overhead of running BookStack is more than I need at the moment.

The way I see it is I will be making more specialized sites, and lots of them, opposed to clustering them all in to one site.

A good example of this would be the new site, as well a new undertaking I have started:
[

Welcome - breadNET Documentation

breadNET Public Documentation

![](__GHOST_URL__/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/pipeline.png)
](<https://documentation.breadnet.co.uk>)
The top one is my new home for documentation (Which I will touch on in a bit)
Where as the second on is a highly specialized site, that serves one purpose: To explain Kubernetes manifests.

## The reason for migrating

As I mentioned, I have started building more specialized sites, but never answered why.

My job's have changed so much since I started. I went from Junior network engineer to sole DevOps engineer rolling out GKE to a national retailer in less time than it takes to get a `Veterinary Medicine BVM&S` Degree (5 years) and naturally so has the type of stuff I am doing in my free time.

I've done from configuring cisco switches, to writing code to deploy a Google Kubernetes cluster with a Highly available app in 15 minutes from start to finish.

Enough chit-chat:

1. Documentation software does not need to be so complex
2. Less overhead (Does not need a database)
3. Lower barrier to entry (Just know markdown)
4. Documentation is markdown files
5. Source control (Easy roll-back)
6. No security issues

---

## Platform of choice

I don't know if I would call it a *platform* necisarrly, but I chose to go with; mkdocs, with Material Theme.
[

MkDocs

Project documentation with Markdown.

![](https://www.mkdocs.org/img/favicon.ico)MkDocsMkDocs Team

](<https://www.mkdocs.org)[>

Material for MkDocs

Write your documentation in Markdown and create a professional static site in minutes – searchable, customizable, for all devices

![](https://squidfunk.github.io/mkdocs-material/assets/favicon.png)Martin Donath

![](https://squidfunk.github.io/mkdocs-material/assets/images/social/index.png)
](<https://squidfunk.github.io/mkdocs-material/>)
The way mkocs works, is:

1. You write your site in markdown documents

![](__GHOST_URL__/content/images/2022/09/image-1.png)
2. You tell mkdocs how the site navigation should look like

    nav:
      - Home: index.md
      - KB Articles:
          - Disk management:
            - Expanding a file system: kb/disk-management/expanding-a-filesystem.md
            - Formatting drive and Auto mount: kb/disk-management/formatting-drive-automount.md
            - Mount a new drive: kb/disk-management/mount-a-new-drive.md
            - "GPT PMBR Size Mismatch will be corrected by w(rite)" : kb/disk-management/gpt-pmbr-size-mismatch-will-be-corrected-by-write.md
          - Minio:
              - OLD : kb/minio/old.md
              - Connecting to minio over s3fs: kb/minio/minio-over-s3fs.md
              - creating users and assigning policies: kb/minio/s3-policies.md
          - PHP:
              - Install PHP: kb/php/install-php.md
              - Wordpress permissions: kb/php/wordpress-permissions.md
          - Docker:
              - Installing Docker: kb/docker/installing-docker.md
              - Basics of docker: kb/docker/basics-of-docker.md
              - Installing jellyfin: kb/docker/installing-jellyfin.md
              - "Docker: Intro and notes": kb/docker/docker-intro-and-notes.md
              - Exporting and importing: kb/docker/exporting-and-importing.md
              - Docker Architecture: kb/docker/docker-architecture.md
              - Bulk retag: kb/docker/bulk-retag.md

3. You tell mkdocs what theme to use (This is comparable to a theme in wordpress, or ghost)

    theme:
      name: material

4. You build and then host it on an nginx server, or Apache.

The nice part about mkdocs is it's simple, if you can write markdown, you can build a good documentation site.

---

# Pipelines

Seeing as the site is just being built on demand, we can make a code pipeline to deploy on certain actions.

I have mine deploy on a push to `dev` branch which goes to a development site (dev-documentation.breadnet.co.uk) and then once you open a PR and merge to master, it deploys the site to production.

As you can see, there is a stark difference between Dev:
![](__GHOST_URL__/content/images/2022/09/image-2.png)Dev (dev-documentation.breadnet.co.uk)
And Production
![](__GHOST_URL__/content/images/2022/09/image-3.png)Production (documentation.breadnet.co.uk)
This is achieved in mkdocs' flexible nature to use Environment variables on build

    site_name: !ENV [env,"breadNET Documentation"]

The above sets the site name, so what you see at the top left.

What happens here is on build, mkdocs checks what the value for `env` is, and if it's `null` (so not set), it will default to `breadNET Documentation`

It's the same for the color and anything else I want to set.

---

# The Code pipeline

At the time of writing, this is how the pipeline looks
![](__GHOST_URL__/content/images/2022/09/image-4.png)

1. git clone
2. If on dev, set vars
3. If on dev, set Robots.txt
4. Build site
5. If on dev, copy to dev server
6. If on master, copy to prod server.

The nice thing is the site is built on each commit, so you can see what will be going in to production.
![](__GHOST_URL__/content/images/2022/09/image-5.png)
---

## Closing notes

I will miss BookStack. It's been one of the best pieces of software that I have used. It's opened my eyes to what open source has to offer, as well as teaching me ansible!

I don't know if I will run BookStack again -  However it's my go-to application for testing things. So at some point I will release a helm chart for BookStack as I learn helm more.

As always, a link to all the *"micro sites"* I run
[

About me - Portfolio

![](__GHOST_URL__/favicon.ico)logo

![](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style&#x3D;for-the-badge&amp;logo&#x3D;google-cloud&amp;logoColor&#x3D;white)
](<https://bradley.breadnet.co.uk)[>

Welcome - breadNET Documentation

breadNET Public Documentation

![](__GHOST_URL__/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/pipeline.png)
](<https://documentation.breadnet.co.uk>)
