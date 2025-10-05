---
title: Terraform state chicken and egg problem
slug: terraform-state-chicken-and-egg-problem
date_published: 2023-10-04T15:40:00.000Z
date_updated: 2023-10-04T15:49:50.000Z
tags: terraform, google cloud, aws
excerpt: Terraform is full of chicken and egg problems, let's solve the state one
---

Since the dawn of time people have been dealing with Chicken and egg problems in terraform.

> I need to create a resource, which is depended on by another resource, but the first resource depends on the last one

 Imagine a circle. 

One of the main issues I've come across when you start a new engagement with a client or a company where they don't use terraform is: How do I create state buckets

The solution can be as simple or as advanced as you want it to be. Let's explore some solutions:

I prefer to create a state bucket, then use CI to create more state buckets in terraform. 

- Command to create the first state bucket
- Terraform in the repo

---

## Command to create the first state bucket

Most cloud providers allow you to use their CLI, Google has  `gcloud` and Amazon has `aws` respectively to interact with the cloud provider.

This solution relies on you running a command. By doing this you get no state to check the bucket against, but the command is set and forget.

AWS:

    REGION="us-east-1"
    aws s3api create-bucket \
    	--region "${REGION}" \
    	--bucket "companyname-terraformstate-state" \
    
    aws dynamodb create-table \
    	--region "${REGION}" \
    	--table-name companyname_terraformstate_state \
    	--attribute-definitions AttributeName=LockID,AttributeType=S \
    	--key-schema AttributeName=LockID,KeyType=HASH \
    	--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
       

GCP

    gsutil mb -c nearline gs://compantname-terraformstate-state

In GCP, state locking is done through the bucket opposed to needing a dynamoDB table. 

You can then point your terraform repo/ directory for managing new state buckets to this bucket. 

## Terraform in the repo

This is the option I chose to go for, as it shows the bucket was created and you've got state for that bucket so you can look and see how the bucket was configured. A nice touch of this is that you can then scan it with things like `tfsec` and `checkov`

Because I am a GCP engineer, this will be a GCP example but I am sure chatGPT will be able to convert the below in to your cloud provider of choice 

    resource "google_storage_bucket" "bucket" {
      location                    = "europe-west2"
      name                        = "companyname-terraformstate-state
      project                     = "companyname-terraform-state"
      public_access_prevention    = "enforced"
      storage_class               = "STANDARD"
      uniform_bucket_level_access = true
      force_destroy               = false
      versioning {
        enabled = true
      }
    
      lifecycle_rule {
        action {
          type = "Delete"
        }
        condition {
          num_newer_versions = 100
          with_state         = "ARCHIVED"
        }
      }
    
      lifecycle_rule {
        action {
          type = "Delete"
        }
        condition {
          days_since_noncurrent_time = 100
          with_state                 = "ANY"
        }
      }
    
    }

You will then run the below commands

    terraform plan
    terraform apply
    git add terraform.tfstate
    git add .
    git commit -m 'Configuring state bucket for other state'
    git push

You're now free to use this bucket for holding the central state for terraform to provision other state

---

If you need help with configuring terraform state, reach out and we can work together on a solution! 
