---
title: Terraform with OVH
slug: terraform-ovh-openstack
date: 2020-12-26T16:38:30.000Z
date_updated: 2021-05-02T01:45:40.000Z
summary: Having issues terraforming OVH and Openstack? Well, I think I solved it for you.
---

OVH is a french cloud provider that has ([According to w3techs](https://w3techs.com/technologies/details/ho-ovhsas)) 3.2% of the web hosting market. Whist this does seem small, remember the market is around [$56.7 billion](https://www.grandviewresearch.com/industry-analysis/web-hosting-services-market#:~:text=The%20global%20web%20hosting%20services,Virtual%20Private%20Server%20(VPS).). So that's a decent piece of the cake.

Moving on.

I am working on a project that I will most likely abandon at some point called cTorrent
[

userbradley/cTorrent

Automatic torrenting though OVH. Contribute to userbradley/cTorrent development by creating an account on GitHub.

![](https://github.githubassets.com/favicons/favicon.svg)GitHubuserbradley

![](https://avatars2.githubusercontent.com/u/41597815?s&#x3D;400&amp;v&#x3D;4)
](<https://github.com/userbradley/cTorrent>)
[Which you can track the progress on Jira](https://jira.breadnet.co.uk/projects/CTOR/issues/CTOR-15?filter=allissues)

Any way.

In this project, I need to create instances on OVH, firewall rules and volumes. I could manually go to the website and do this, but I want to be able to exert as minimal effort as possible and have the biggest reward possible.

So we use something called Terraform.
Below is an accurate representation of how using terraform will speed up your life
![](/content/images/2020/12/image.png)me using terraform to create infrastructure
So what is the issue here?

I found that no matter how much I tried, I could not get authentication to work. Usually you would set up the provider like below. Set the authentication scheme, so here we use an API key.

    provider "digitalocean" {
      token = var.do_token
    }

provider.tf
    variable "do_token" {
      type = string
      description = "API key to communicate to Digital Ocean with"
    }

vars.tf
    do_token = "loluthought58ead42e01f1a62d6f422004e69cd5ba775af3b09"

terraform.tfvars
Or with google:

    provider "google" {
      version = "3.5.0"
      credentials = file("terraform-c8b2b88693d4.json")

      project = "absolute-access-271419"
      region  = "us-central1"
      zone    = "us-central1-c"
    }

Here we set the provider as usual, then the credential file, as well as other fluff like where we want things to pop up in, and what compute zone.

With OVH it's different - Let me explain.

OVH uses a technology stack called Openstack, which you can read more about [here](https://www.openstack.org). Openstack has many API endpoints we can interface with. But the part that caused confusion is the providers.

You can connect to OVH using their OVH provider on terraform, but for the life of me, I was unable to get authentication working. You were required to create an API key through [some backdoor looking website.](https://api.ovh.com/createToken/index.cgi?GET=/*&amp;POST=/*&amp;PUT=/*&amp;DELETE=/*)Any way, below is what they expect your provider setup to look like:

    provider "ovh" {
      endpoint           = "ovh-eu"
      application_key    = "yyyyyy"
      application_secret = "xxxxxxxxxxxxxx"
      consumer_key       = "zzzzzzzzzzzzzz"
    }

Now I would like to say, I am by no means an idiot, but this made me feel like an idiot. I just could not get it working.

Besides that, this provider did not actually support creating compute instances. Odd.

This is the point at which I had to use my brain and get creative - You remember how I said OVH uses Openstack? Well they make their Openstack endpoints public.

We will be connecting to something called [Horizon](https://docs.openstack.org/horizon/latest/), which is the dashboard project for Openstack.
![](/content/images/2020/12/image-1.png)Horizon for OVH
Now to get in to Horizon, we need to create a user.

Login to [OVH public cloud management portal](/terraform-ovh-openstack/www.ovh.com/manager/public-cloud/) with your account credentials.

Once here go to the far left, scroll down to `Users & Roles` and create a new user.
![](/content/images/2020/12/image-2.png)
Pick `Administrator` and then copy the username, and the password to a text file so you can come back to them for the next step.

Login to Horizon
[https://horizon.cloud.ovh.net/auth/login/?next=/](https://horizon.cloud.ovh.net/auth/login/?next=/)

Paste the username and the password in to their respective fields. Once logged in, go to the top right then click `OpenStack RC File v3`
![](/content/images/2020/12/image-3.png)
This will download a file which just has numbers and prepended by `.sh`

If you're lazy, you can edit this file and hard code the password in to it. To do so:

Open the file in an editor. On linux just use nano.

Where it says `export OS_PASSWORD=$OS_PASSWORD_INPUT` change it so that `$OS_PASSWORD_INPUT` is your password.

like below:

    export OS_AUTH_URL=https://auth.cloud.ovh.net/v3
    # With the addition of Keystone we have standardized on the term **project**
    # as the entity that owns the resources.
    export OS_PROJECT_ID=thisisaplaceholder
    export OS_PROJECT_NAME="bunchofnumbersgohere"
    export OS_USER_DOMAIN_NAME="Default"
    if [ -z "$OS_USER_DOMAIN_NAME" ]; then unset OS_USER_DOMAIN_NAME; fi
    export OS_PROJECT_DOMAIN_ID="default"
    if [ -z "$OS_PROJECT_DOMAIN_ID" ]; then unset OS_PROJECT_DOMAIN_ID; fi
    # unset v2.0 items in case set
    unset OS_TENANT_ID
    unset OS_TENANT_NAME
    # In addition to the owning entity (tenant), OpenStack stores the entity
    # performing the action as the **user**.
    export OS_USERNAME="user-sike"
    # With Keystone you pass the keystone password.
    echo "Please enter your OpenStack Password for project $OS_PROJECT_NAME as user $OS_USERNAME: "
    read -sr OS_PASSWORD_INPUT
    export OS_PASSWORD=whaddyatalkinabout
    # If your configuration has multiple regions, we set that information here.
    # OS_REGION_NAME is optional and only valid in certain environments.
    export OS_REGION_NAME="UK1"
    # Don't leave a blank variable, unset it if it was empty
    if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi
    export OS_INTERFACE=public
    export OS_IDENTITY_API_VERSION=3

The reason I've done this is because it sets environment variables for the username, region, password and some other fluff.

Once this is done, we need to change our provider from OVH, to Openstack.

[https://registry.terraform.io/providers/terraform-provider-openstack/openstack/latest/docs](https://registry.terraform.io/providers/terraform-provider-openstack/openstack/latest/docs)

Luckily, their documentation is beautiful so not hard to understand.

We need to set the provider like:

    provider "openstack" {
      auth_url = "https://auth.cloud.ovh.net/v3"
      alias = "ovh"
    }

Let's just create SSH keys to test this -  Format the files as below.

    provider "openstack" {
      auth_url = "https://auth.cloud.ovh.net/v3"
      alias = "ovh"
    }

provider.tf
    pub_file_location = "/path/to/your/home/directory/.ssh/id_rsa.pub"

terraform.tfvars
    variable "pub_file_location" {
      type = string
    }

variables.tf
    resource "openstack_compute_keypair_v2" "key" {
      name       = "SSH"
      public_key = file(var.pub_file_location)
    }

ssh.tf
Now we can open the terminal, navigate to the folder and then run `terraform init`

Now run `terraform plan`

Here's where I had the issue that prompted me to write this.

    ➜ terraform plan
    Refreshing Terraform state in-memory prior to plan...
    The refreshed state will be used to calculate this plan, but will not be
    persisted to local or remote state storage.


    Error: One of 'auth_url' or 'cloud' must be specified

      on <empty> line 0:
      (source code not available)

We have the `auth_url` set tho? This stumped me for a while.
![](/content/images/2020/12/image-4.png)
In the current directory you working in, run

    source /path/to/sh/file/we/downloaded/erlier/<name>.sh

Depending on if you did my cheeky hack, you can press enter, or if not paste the password from earlier.

Now run Terraform plan and you should see it creating the SSH key.

From here you're able to play around. Feel free to check out my Terraform code that I have written at like 3 am, so excuse the formatting. Still learning :)

Any questions please feel free to reach out to me on linkedin, or find my email address somewhere.

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
