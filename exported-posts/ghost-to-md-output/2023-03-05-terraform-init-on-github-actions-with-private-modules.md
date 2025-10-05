---
title: Terraform init on GitHub actions with private modules
slug: terraform-init-on-github-actions-with-private-modules
date_published: 2023-03-05T22:17:52.000Z
date_updated: 2023-04-19T20:53:46.000Z
tags: GitHub actions, terraform, cicd, #Import 2023-03-30 20:40
excerpt: How to use Terraform on GitHub Actions with SSH keys
---

Last month I wrote a blog post about how to run `terraform init` on codefresh. Sadly Codefresh are changing their pricing which makes it alot more expenive per developer. For this reason, we're migrating our pipelines at work to GitHub actions.
[

Pricing & Plans | Codefresh

Sign up for Codefresh today and get a 14-day trial of our Enterprise plan. Flexible pricing plans for every project and budget.

![](https://codefresh.io/wp-content/uploads/2022/07/cropped-favicon_codefresh_2_512x512-192x192.png)Codefresh

![](https://codefresh.io/wp-content/uploads/2023/03/Open_Graph_Homepage.jpg)
](https://codefresh.io/pricing/)
tl;dr: It's going from $34 pcm for 10 devs on a small runner to ~$50+ per dev per month. 

---

# The issue we have

At work, all our terraform modules are store in Git Hub. Also, all our modules use `git::ssh://` as the method of pulling them.
[

Module Sources | Terraform | HashiCorp Developer

The source argument tells Terraform where to find child modules’s configurations in locations like GitHub, the Terraform Registry, Bitbucket, Git, Mercurial, S3, and GCS.

![](https://developer.hashicorp.com/icon.svg)Module Sources | Terraform | HashiCorp Developer

![](https://developer.hashicorp.com/og-image/terraform.jpg)
](https://developer.hashicorp.com/terraform/language/modules/sources#generic-git-repository)
I've tried to follow blog posts like the below, which did not work.

When I say this, I mean I could not for the life of me get it work, regardless of what [permissions](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs) I gave the pipeline.
[

Github Actions with a private Terraform module

Terraform makes it easy to manage infrastructure at scale; you might want to share code between modules, and that’s where it becomes tricky. In this post, I try to give some clues on how to use terraform across private Github repos.

![](https://maelvls.dev/favicon-32x32.png)maelvls dev blogMaël Valais

![](https://maelvls.dev/gh-actions-with-tf-private-repo/cover-gh-actions-with-tf-private-repo.png)
](https://maelvls.dev/gh-actions-with-tf-private-repo/)
I was still getting the issue

    Cloning into 'terraform-module-google-dns'...
    remote: Repository not found.
    fatal: repository 'https://github.com/<>/terraform-module-google-dns.git/' not found
    

Despite the repo **very much being there**

# Solution

The solution was pretty much the same as the [Codefresh](__GHOST_URL__/terraform-init-with-modules-on-codefresh/) solution: Install SSH Keys on the pipeline, so when terraform runs [git clone ](https://github.com/hashicorp/terraform/issues/21522#issuecomment-497963956)on the module, it has the keys.

## Create the keys

You need to create specific keys for the modules. I recommend creating ones called `githubactions-terraform`

    ssh-keygen -t ed25519

When it asks what you want to name it, supply the full path to your `.ssh` directory, and append `githubactions-terraform`

Now we have the keys created, we can upload them to the GitHub repo that the pipeline needs to pull them from

## Adding the keys to the relevant GitHub repos

Navigate to your repo of choice, in this example I will use my Codefresh IP module

Click on `Settings`
![](__GHOST_URL__/content/images/2023/03/image.png)
Then click on `Deploy Keys` down the left hand side
![](__GHOST_URL__/content/images/2023/03/image-1.png)
Open your terminal and copy the public key to the clipboard

    cat githubactions-terraform.pub | pbcopy

Click `Add Deploy Key` and paste it in
![](__GHOST_URL__/content/images/2023/03/image-2.png)
Next step is to add the **private** SSH keys to the repo with the GitHub actions enaled

## SSH Keys on the actions repo

Open Terminal and copy the private keys to clipboard

    cat githubacionts-terraform | pbcopy

Navigate to the repo with the actions in, click settings, then click `Security > Actions`
![](__GHOST_URL__/content/images/2023/03/image-3.png)
Click `New repository secret`
![](__GHOST_URL__/content/images/2023/03/image-4.png)
Give it a name, for example I am calling this `SSH_KEY_GITHUB_ACTIONS`

Paste the Private SSH key in.

Read the below page if you are worried about secrets being leaked
[

Encrypted secrets - GitHub Docs

Encrypted secrets allow you to store sensitive information in your organization, repository, or repository environments.

![](https://docs.github.com/assets/cb-803/images/site/favicon.svg)GitHub Docs

![](https://github.githubassets.com/images/modules/open_graph/github-logo.png)
](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
## The GitHub actions part

So, we have the SSH keys setup, now we need to actually use them!

I have created the below GitHub actions that:

- Installs terraform on the runner
- Adds the SSH keys
- Runs `terraform init`

    name: DNS
    
    on:
      push:
        branches:
          - main
    
    jobs:
      terraform:
        runs-on: ubuntu-latest
    
        steps:
          - name: Checkout code
            uses: actions/checkout@v3
    
          - name: Install Terraform
            uses: hashicorp/setup-terraform@v2
            with:
              terraform_version: 1.3.9
    
          - name: Terraform Init
            working-directory: ${{ env.DIR }}
            run: |
              eval `ssh-agent -s`
              ssh-add - <<< '${{ secrets.SSH_KEY_GITHUB_ACTIONS }}'
              terraform init

You are then free to continue with what ever other terraform steps you need to do in your pipeline.
