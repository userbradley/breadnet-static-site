---
title: Dependabot for terraform and terraform modules
slug: dependabot-for-terraform-and-terraform-modules
date: 2023-07-16T01:00:31.000Z
date_updated: 2023-07-16T01:00:31.000Z
summary: Looking at using Dependabot to manage your terraform modules and providers? I've got you covered
feature_image: https://images.unsplash.com/photo-1637002722490-5f8ceed9774c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDM1fHxyb2JvdHxlbnwwfHx8fDE2ODk0Njc1MTh8MA&ixlib=rb-4.0.3&q=80&w=1000
---

I recently stumbled across [Dependabot](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/) and was curious if it can be used to keep Terraform up to date. Turns out you can, but there are some small catches that you should be aware of.

In todays installment, we look at what it is, why you'd use it, and how to set it up.

## What is Dependabot

Dependabot is a tool from GitHub that allows automatic updates and patching of code in repositories. This is especially useful as once you get over about 3 terraform dependencies, you start having the issue where Providers become out dated, and modules fall behind on patches to issues.

By enabling Dependabot, you basically get a colleage for free who's sole job is finding out dated terraform packages (modules, providers), creating a pull request to update them and managing rebasing.

## Why would I use it for terraform

As mentioned, once you get past about 3 providers across a codebase (and in my case, over 30k lines of terraform) keeping things up to date becomes a real hassle.

Dependabot will search for the releases of Modules and Providers frequently and update them. Even Private modules.

## What are the limitations

For some reason, when configuring the terraform dependabot config, you will need to create a new *line item* per directory which contains a `provider.tf` file, or in the case of modules, the directory.

## How to set it up

Lets assume for the time being the below is our file layout

    monorepo
    ├── .github
    │   └── dependabot.yml
    ├── artifact-registry
    │   └── provider.tf
    ├── dns
    │   └── provider.tf
    └── gke
        ├── dev
        │   └── provider.tf
        ├── prod
        │   └── provider.tf
        └── test
            └── provider.tf

Once you've enabled Dependabot [(follow these instructions)](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates#enabling-dependabot-version-updates) create a file called `.github/dependabot.yml` and inset the below

    version: 2

    updates:
    # Terraform - One entry per thing we want to scan as per https://github.com/dependabot/dependabot-core/issues/649
      - package-ecosystem: "terraform" # DNS
        directory: "/dns"
        schedule:
          interval: "daily"
      - package-ecosystem: "terraform" # GKE Dev
        directory: "/gke/dev"
        schedule:
          interval: "weekly"
      - package-ecosystem: "terraform" # GKE Prod
        directory: "/gke/prod"
        schedule:
          interval: "weekly"
      - package-ecosystem: "terraform" # GKE Test
        directory: "/gke/test"
        schedule:
          interval: "weekly"
      - package-ecosystem: "terraform" # Artifact Registry
        directory: "/artifact-registry"
        schedule:
          interval: "weekly"

What does each part mean?
NameWhat it does`package-ecosystem`What package ecosystem to scan from [Supported Packages](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates#supported-repositories-and-ecosystems)`directory`Where this code it should scan lives`schedule`How often to scan, based on [`schedule.interval`](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#scheduleinterval)
Once you've created the file, go to your repo and click on `Insights`
![](__GHOST_URL__/content/images/2023/07/image-1.png)
Then click on `Dependency graph`
![](__GHOST_URL__/content/images/2023/07/image-2.png)
Then click on Dependabot and you should see a healthy scan
![](__GHOST_URL__/content/images/2023/07/image-3.png)

## How to add access to Private Modules

When creating private modules in a Private Git Repository, you will need to give Dependabot access to these.

To do so, navigate to your Org's home page, and click on `Settings` and then `Code security and analysis`
![](__GHOST_URL__/content/images/2023/07/image-4.png)
Once here, you will need to scroll down to the section that reads `Grant Dependabot access to private repositories`

Here search for the name of all the repos that contain modules. Once added, Dependabot will check if they have releases, and if so, will update them

## How to ignore certain modules

This is out of scope for this post, but see the below documentation for an example and walkthrough
[

Ignore terraform module version dependabot - breadNET Documentation

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/kb/dependabot/ignore-terraform-module-version-dependabot.png)
](<https://documentation.breadnet.co.uk/kb/dependabot/ignore-terraform-module-version-dependabot/>)
