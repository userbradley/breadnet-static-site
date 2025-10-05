---
title: Kubernetes secrets using Google Secret Manager
slug: kubernets-secrets-using-google-secret-manager
date: 2023-10-15T22:08:26.000Z
date_updated: 2024-03-14T15:27:21.000Z
summary: How to get Google Secret manager secrets in to GKE? Look no further. We discuss options and implementing External Secrets Operator 
---

Since my career at the current company cool enough to employ me, I've been almost exclusively working on GKE (Google's Kubernetes offering) 

One (of the many) issues I've been trying to solve in GKE is how to use Google Secrets ([Their secret manager](https://cloud.google.com/secret-manager)) **inside **GKE in a simple mean that doest require crazy add ons, and complexity. 

I've opened a Feature Request, but until then this blog post will explain what options you have, and what I did, and then a walkthrough of how to set up what I've done

- [[FR] Native support for Google Secret manager in GKE](https://issuetracker.google.com/issues/305477780)

## What is the issue to start with

We have a lot of applications that run on GKE, these span from simple things like a cron job to backup our state projects, all the way to our in house [multi-layer multi-language IDP](https://internaldeveloperplatform.org/what-is-an-internal-developer-platform/) - One of the massive issues here is most of these applications need secrets to communicate *onwards*, be it to Microsoft Auth or to third party APIs. 

How we get these secrets in, is a real pain. We used to manage these by using [Skaffold](https://skaffold.dev) to pick up local environment variables  at deploy. One issue this has, if the dev doesn't run the pre-requisite [Task command](https://taskfile.dev) then the secret gets nulled and things break. This happens maybe twice a week. 

## What is the proposed Solution

Ideally we would allow the application developers to just specify the secret in Google secret manager, and either the file on the pod to mount it to, or the environment variables it should be. 

Below details what I want from a solution

- Ability to use Service account of Pod or specific account using [Workload Identity](https://documentation.breadnet.co.uk/kubernetes/gke/configure-gke-workload-identity/)
- Generate a Kubernetes native secret
- Able to mount to pods as either env variables or File

I had a dig around on the internet and found a Medium Post which offered the below solutions.
NameCommentsDirectly Fetching SecretsSomething we used to do, but the idea of this post is to prevent thisKubernetes Secrets CSI DriveerWe tried this and goodness me it was **painfull**Using an Init containerNope. This sounds way too complicated and I dont want to have to play about with filesExternal Secrets OperatorSpoiler alertB3rg1a$Looked too complicated for what we were doing
As you can probably guess, we're going to be talking about using External Secrets Operator to get secrets in to our cluster. 

Back in August I had trialed using the CSI driver and it was painful. In order to get secrets to become Kubernetes secrets, [you had to start a pod and mount the secret to it](https://secrets-store-csi-driver.sigs.k8s.io/topics/sync-as-kubernetes-secret). This is a security issue. 

## External Secrets Operator

I decided to settle on External Secrets Operator (ESO) as it allowed us to sync secrets from GSM on a schedule we define, allows us to specify a service account that has access, and it allows name spacing resources so we can apply RBAC on them. 

Let's just set out the scene of our environment, as some parts are very important to pay attention to. 
NameOur ValueCluster Name`breadnet-cluster`Region`europe-west2`Zone`europe-west2-c`
Something we really need to make sure we pay attention is the Cluster name and Zone. This is because when using Workload Identity the ESO app makes [API calls to the tokens API, these have to match up exactly](https://github.com/external-secrets/external-secrets/blob/7b8f36b2f007306a106863b12c433edd9c8820ea/pkg/provider/gcp/secretmanager/workload_identity.go#L120-L123)

First we need to install the External Secrets Operator, You can do this with Helm, but we use Skaffold for all management operations so below is the skaffold file

    apiVersion: skaffold/v4beta6
    kind: Config
    metadata:
      name: external-secrets
    deploy:
      helm:
        releases:
          - name: external-secrets
            namespace: external-secrets
            remoteChart: external-secrets
            repo: "https://charts.external-secrets.io"
            upgradeOnChange: true
    

Once External Secrets is installed, check all is well. Ideally these should all say `1/1` under the ready column

    ➜ kubectl get pods -n external-secrets                         
    NAME                                                READY   STATUS    RESTARTS   AGE
    external-secrets-7f8fd8d64d-wfkj8                   1/1     Running   0          6d5h
    external-secrets-cert-controller-8499548dd6-ttxtf   1/1     Running   0          6d5h
    external-secrets-webhook-dbc576595-lkxxm            1/1     Running   0          6d5h
    

The next step is to create a Google Cloud Service account in the Service project for your application.

Once done, grant the service account *`roles/iam.serviceAccountTokenCreator`*on the project.

Next thing is to navigate to Secret manager, locate the secret you want the ESO to have access to, then give that service account Secret Viewer on that Secret. 

Custom resource definitions and their *imported* resources can either be [Cluster Scoped or Namespaced](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#create-a-customresourcedefinition). For our specific configuration, we will be creating a `SecretStore` opposed to a `ClusterSecretStore` which is the cluster wide one.

We wont be using `ClusterSecretStore` as this means a single service account is used cluster wide, which means this service account has way more permissions than is required [(Not good)](https://cloud.google.com/iam/docs/best-practices-service-accounts)

Before you can move ahead with creating the `SecretStore` we need to create a kubernetes service account and annotate the account with the GCP Service account. For this, follow my guide from `Service account` to `Kubernetes service account` section
[

Configure GKE workload Identity - breadNET Documentation

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/kubernetes/gke/configure-gke-workload-identity.png)
](https://documentation.breadnet.co.uk/kubernetes/gke/configure-gke-workload-identity/#service-account)
We will annotate the service account is like below:

    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: secret-accessor
      namespace: secret-store-namespace
      annotations:
        iam.gke.io/gcp-service-account: secret-accessor@secret-accessor-demo.gserviceaccount.com
    

Now create the `SecretStore`

If your secrets are in the same project as the GKE cluster, you can omit the `clusterProjectId` field (I think, I cant remember and their documentation is sparse) How ever if you have secrets in a centralized Secret Project, then you should include this field. I have included it below. 

    apiVersion: external-secrets.io/v1beta1
    kind: SecretStore
    metadata:
      name: gcp-store
      namespace: secret-store-namespace
    spec:
      provider:
        gcpsm:
          auth:
            workloadIdentity:
              clusterLocation: europe-west2-c
              clusterName: breadnet-cluster
              clusterProjectID: breadnet-gke
              serviceAccountRef:
                name: secret-accessor
          projectID: breadnet-secrets

Once this is applied, and the service account in the namespace is annotated, you can then access secrets using this store. 

    apiVersion: external-secrets.io/v1beta1
    kind: ExternalSecret
    metadata:
      name: database-credentials
    spec:
      refreshInterval: 1h             # rate SecretManager pulls GCPSM
      secretStoreRef:
        kind: SecretStore
        name: gcp-store               # name of the SecretStore (or kind specified)
      target:
        name: database-credentials    # name of the k8s Secret to be created
        creationPolicy: Owner
      data:
      - secretKey: database_username
        remoteRef:
          key: database_username      # name of the GCPSM secret key
      - secretKey: database_password
        remoteRef:
          key: database_password      # name of the GCPSM secret key

This then allows us to sync the Google cloud secret `database_username` to the field `database_username` in the secret called `database-credentials` in the current namespace. 

You're then free to use this secret as you would as a kubernetes native secret.

The below is the link to the Google Secret managet for ESO, go forth and conquer 
[

Google Cloud Secret Manager - External Secrets Operator

![](https://external-secrets.io/latest/assets/images/favicon.png)External Secrets Operator

](https://external-secrets.io/latest/provider/google-secrets-manager/)
---

If you enjoyed this blog post, please consider bookmarking this site! 

You may also be interested in my documentation site which will have more in depth examples etc: [documentation.breadnet.co.uk](documentation.breadnet.co.uk/)

As always you can contact me to discuss this post, or if you need help implementing this as your company please reachout to me and we can discuss ways to get you working cloud native!

Thanks <3 
