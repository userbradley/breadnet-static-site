---
title: Terraform init on codefresh with private modules
slug: terraform-init-with-modules-on-codefresh
date: 2023-02-10T23:53:59.000Z
date_updated: 2023-02-10T23:53:59.000Z
summary: How to use Terraform on Codefresh with SSH keys
---

It's no secret that I love codefresh. I find it incredibly simple to use, and it just makes sense.

One thing that does not make sense is how to easily run `terraform init` on codefresh with **private modules** stored on Github (or BitBucket)

## The issue

So the issue we have with any module, is how we access it. If your module is public, then you can use the [GitHub](https://developer.hashicorp.com/terraform/language/modules/sources#github) URL like the below

    module "consul" {
      source = "github.com/hashicorp/example"
    }

This makes the assumption that the module is public

When we have private modules, like for exmaple my DNS records one:

    module "documentation" {
      source  = "git::ssh://git@github.com/userbradley/terraform-modules-cloudflare-breadnet-<>.git"
      name    = "documentation"
      proxied = "true"
      value   = "<>"
    }

The `source` has changed to use ssh now. In order to run `terraform init` on this, we're basically doing a `git clone` ([as explained here](https://github.com/hashicorp/terraform/issues/21522#issuecomment-497963956)) on the repo's url.

---

## Some assumptions we are going to make

Annoyingly, before we get on to the solution, we need to make the below assumptions

- You have a dedicated Git/ Bitbucket account for your Codefresh account

- We are calling mine `brobot`

- You are running on a *nix based system (I am on a mac)

## Setting up SSH keys

We need to create the keys, and add them to the relevant systems that need them!

### Creating the keys

The first step is creating the SSH keys to use.

1. Open a terminal
2. Run `ssh-keygen-t ed25519` and give it a useful name like `robot`
3. Copy the keys to the clipboard
4. `cat ~/.ssh/robot.pub | pbcopy`
5. [Login to Github and add SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

### Create the secret on codefresh

Once we've got the public key uploaded to Github, we are able to add the private key to Codefresh.

Depending on your security posture, you can either add these variables at a Pipeline  level, or a Project. For ease, I recommend at Project level as it means less times you need to locate the ssh keys, and also... You can delete them from your compute.

1. Login to `g.codefresh.io`
2. Navigate to Projects
3. Click on the project you want to add the keys to
4. Click `Variables`
5. Copy the private key `cat ~/.robot | base64 | pbcopy`
6. Create a secret on codefresh called `ssh_key`
7. Paste the value in, and click encrypt

> Why are we base64 encoding it?

In order to get the file to not be formatted like garbage, we base64 the file so it keeps formatting, and means we can single line it when we put it in codefresh, as I don't think codefresh has a `--from-file=` option like kubernetes

---

## Creating the pipeline

Now that we have the SSH keys created, and the keys uploaded to both GitHub and Codefresh, now it's time to actually use them.

The tl;dr is:

- Create a step to echo the file, base64 decode it to the shared volume
- `ssh-keyscan` github and add it to shared volume
- `chmod` it
- mount shared volume

### SSH Key init step

This is the most importat step, as this is where we take the secret, and inject it in to the shared volume [(read more about that here)](https://codefresh.io/docs/docs/yaml-examples/examples/shared-volumes-between-builds/)

Below is some *okay* code that does the job

      sshSetUp:
        image: alpine/git:2.36.3
        title: Setting up SSH
        stage: init
        commands:
          - mkdir -p /codefresh/volume/ssh
          - echo $ssh_key | base64 -d > /codefresh/volume/ssh/id_rsa
          - ssh-keyscan github.com > /codefresh/volume/ssh/known_hosts
          - chmod 600 /codefresh/volume/ssh/id_rsa

A breif explination is below on what each line does

- image:

- We use an alpine based image as it's small and use the git one as it has git built in

- title: Give it a name basically
- stage: what stage this runs in the pipeline. best to use init
- commands:

- mkdir

- Creates the `/codefresh/volume/ssh` directory if it doesnt already exist

- echo `$ssh_key`
- Echos the key, base64 decodes it and then writes it to the volume

- ssh-keyscan

- scans github.com:22 for the public keys it has on record (So we dont get an error about keys not found)

- chmod

- Sets the permissions on the key file

### Consuming the keys in the init step

Now we have the keys on the shared volume, we need to consume it in the init step.

I orginally went about this by trying to copy the files from the shared volume each time, as `/root` on the steps are ephemeral

I then trued to symlink the `/codefresh/volume/ssh/id_rsa` to `/root/.ssh` when I thougt "wonder if we can mount volumes"

You can!

      TerraformInit:
        image: hashicorp/terraform:light
        title: Terraform Init
        stage: init
        working_directory: "${{clone}}/kubernetes"
        commands:
          - terraform init
        volumes:
          - ./ssh:/root/.ssh

This follows the same format, but there are 2 important details here

- working_directory

- Sets where the container is running the task. Comparible to going `cd /bradley`

- volumes

- mounting `/codefresh/volume/ssh` to `/root/.ssh` on the container

This then allows terraform to run the init step, puling the module from Github!

---

## Wrap up

I hope this page was of some use to you.

I put all the documentation I write on my new documentation site, feel free to have a look around
[

Welcome

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/index.png)
](<https://documentation.breadnet.co.uk/?mtm_campaign&#x3D;blogpost&amp;mtm_kwd&#x3D;terraform-init-codefresh>)
As always, if you struggle, you can reach out to me at `webmaster at breadnet dot co dot uk` and I will do my best to help you where I can!
