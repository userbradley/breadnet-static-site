---
title: "Resolving the 'sts:GetCallerIdentity' error"
slug: wasabi-x-terraform
date: 2022-03-03T20:17:24.000Z
date_updated: 2022-03-03T20:17:24.000Z
summary: Using Wasabi Hot Cloud Storage as a back end for Terraform
---

I'll be honest, other than the 90 day delete policy (which annoys me to no end) wasabi is **dank****af**.

Didn't expect me to start a blog post with that, did you? (Looking at you wasabi employees 👀)

## The problem at hand

I'm in the middle of a digital transformation, which means re-defining how I do things.

One of those is how I deal with terraform state.

Those of you who don't *terraform on the regular,*let me explain the issue.

Terraform keeps track of what it's created, and what needs to be created or deleted next using a file called `terraform.tfstate` - which for the most part is a `json` file, see below.
![](__GHOST_URL__/content/images/2022/03/image-8.png)
Now, when we're scaling our infra over multiple repos, modules etc, and having more people work on them, we get to this stage where we need a better solution on storing (and also versioning) state files.

Terraform has a few solutions you can use, see below
[

Backend Overview - Configuration Language | Terraform by HashiCorp

A backend defines where Terraform stores its state. Learn about how backends work.

![](https://www.terraform.io/favicon.ico)Terraform by HashiCorp

![](https://www.terraform.io/img/og-image.png)
](<https://www.terraform.io/language/settings/backends>)
I've decided to use s3 over others as:

1. GCS is expensive
2. AWS S3 is expensive
3. I already use Wasabi
4. Terraform cloud is cool, but annoys me for some reason.
5. The moose on my desk told me to ([See this post to learn more](__GHOST_URL__/how-i-got-to-where-i-am-now/))

## What we can use wasabi for

So as it stands, wasabi is AWS S3 compliant - But it's not AWS.

Without sounding like [Corey Quinn](https://twitter.com/QuinnyPig) here, this is a stupid naming conventions.

Effectively what it means is you can use the AWS cli to connect to the endpoint that Wasabi offer, or use any other S3 cli to connect. It has the same IAM rules and stuff attached.

If I was to re-do it I would make S3 the standard, then each provider just has their offering.

I digress.

We are going to use wasabi to store our precious `terraform.tfstate` file, with versioning enabled on the bucket.

This is important as without versioning it's hard to see what has changed for the environment, as well as later down the line using stuff like Open Policy Agent to enforce certain policies against the infrastructure.

## The error I had

![](__GHOST_URL__/content/images/2022/03/image-7.png)
    Error: error configuring S3 Backend: error validating provider credentials: error calling sts:GetCallerIdentity: InvalidClientTokenId: The security token included in the request is invalid.
           status code: 403, request id:

What does this error mean?

I'll be honest, I have no clue. I was following the guide that Wasabi put out, [here](https://wasabi-support.zendesk.com/hc/en-us/articles/360003362071-How-do-I-use-Terraform-with-Wasabi-) - but it just would not work.

Here's what I had:

    terraform {

        backend "s3" {
        access_key = "<WASABI-ACCESS-KEY>"
        secret_key = "<WASABI-SECRECT-KEY>"
        endpoint = "https://s3.uk-1.wasabisys.com"
        region = "us-east-1"
        bucket = "bradleys-terraform-state"
        key = "ovh/terraform.tfstate"
      }
    }

It just would not work. No one else on the internet seems to have fixed this.

### Except me :)

Here's what the file was missing - Call it the secret sauce:

    skip_credentials_validation = true

So our block should look something like this

      backend "s3" {
        endpoint = "https://s3.uk-1.wasabisys.com"
        region = "eu-west-1"
        bucket = "bradleys-terraform-state"
        key = "ovh/terraform.tfstate"
        skip_credentials_validation = true
      }

This seems to have done it!

---

In my next post, we will be looking in to how to set up Wasabi to be a backend for Terraform, as well as the IAM policy required!

---

## A meme

![Man on a beach, sand falling between their fingers with the word &quot;terraform&quot; on the top centre, and &quot;state bucket&quot; at the bottom centre](__GHOST_URL__/content/images/2022/03/a40a1329fd5e6b07239fb0c82be4ecb8.jpeg)Meme
