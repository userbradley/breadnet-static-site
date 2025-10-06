---
title: Kubernetes at home
slug: kubernetes-at-home
date: 2023-11-21T17:42:44.000Z
date_updated: 2023-11-21T17:49:37.000Z
summary: Ever wondered what it's like running kubernetes at home? This post tries to answer that
feature_image: https://breadnet.co.uk/content/images/size/w1000/2023/11/cluster-top-1.jpg
---

I first started learning Kubernetes in 2021, as a Junior Systems Administrator in my bedroom in Cambridge. I'll be honest, I didn't really understand it much. What's a pod? Why cant I just deploy a container? 

Over the years, 2 of them to be exact, I have learning Kubernetes piece by peace, not really following a specific course, so if you're looking for course recommendations, I have none. 

I've spent most of my Career operating and using GKE, a Kubernetes *flavour* if you will, from Google. GKE is designed to run on Google cloud, and [sort of](https://issuetracker.google.com/issues/305477780) integrates with most of the GCP API's 

Enough about my work, you're here to see my Cluster at home.

---

When I lived at my parents (Oh the good old days) I had a 48U rack with multiple dell servers. Due to the housing crisis affecting the UK, I cant afford to buy a house, let alone rent a place that isn't classified as a *[shoe box](https://www.redbrick.sg/blog/shoebox-apartments-is-it-worth-the-investment/#:~:text=Shoebox%20apartments%2C%20also%20known%20as%20%E2%80%98compact%20units%E2%80%99%20are%20typically%20defined%20as%20an%20apartment%20of%20500%20square%20feet%20or%20less%20and%20designed%20for%20a%20single%20occupant) - *As such, some design considerations had to be made.

## Design Considerations

- Needs to not be a server chassis
- Needs to be *light* on power ([Energy Crisis](https://www.ons.gov.uk/economy/inflationandpriceindices/articles/costoflivinginsights/energy))
- Needs to be somewhat cheap ([Cost of living Crisis](https://en.wikipedia.org/wiki/2021%E2%80%93present_United_Kingdom_cost-of-living_crisis))
- Needs to be small (read: Shoebox apartment)

All in all, I decided the best way to build the cluster was to use a mix of things I owned, and then buy things I did not.

- 4 Dell 3040 SFF pc's with a minimum of 8gb ram and 128gb SSD (Purchased)
- Ubiquiti EdgeSwitch 8 XP (Owned already)
- Juniper SRX-300 (Purchased)
- Load of ethernet cables (Made them my self)

I am currently learning the Juniper CLI with the end goal of replacing my ISP's router with the Juniper and having vlans etc. 

## Kubernetes flavor of choice

There are lots of distributions of kubernetes you can run, to list a few:

- Anthos 
- Raw Kubernetes
- Rancher Kubernetes Engine
- K3s
- Microk8s

I decided that running full blown vanilla Kubernetes required too many moving parts, so I settled on K3s

> K3s is packaged as a single <70MB binary that reduces the dependencies and steps needed to install, run and auto-update a production Kubernetes cluster

Due to it being so small, it makes installing the cluster **super simple** and not very network intensive

I wont go in to the install process here, but below are some useful links that I suggest following 

- [https://docs.k3s.io/quick-start](https://docs.k3s.io/quick-start)
- [https://www.youtube.com/watch?v=UoOcLXfa8EU](https://www.youtube.com/watch?v=UoOcLXfa8EU)

You can get away with a single node, but if you plan to run this in *production* (ctx: production at home) then I recommend 3 nodes. 

This is the design for the network at a high level. 
![](__GHOST_URL__/content/images/2023/11/cluster.png)
## Design Specifics

My cluster is made up of 3 nodes, and a `persistence` server.

### nodes

I have one `Control plane` node, which is `k3s-01`, this runs `etcd`, `control-plane` and `master`

Each node runs `Ubuntu 22.04.3 LTS`, and because I am an idiot and didnt read the listing on Ebay, the nodes are a mix of i3 and i5 processors, but I honestly have not noticed a difference. 

    ➜ kubectl get nodes              
    NAME     STATUS   ROLES                       AGE     VERSION
    k3s-01   Ready    control-plane,etcd,master   23d     v1.27.6+k3s1
    k3s-02   Ready    <none>                      23d     v1.27.6+k3s1
    k3s-03   Ready    <none>                      5d21h   v1.27.7+k3s2
    

### Networking

I have carved out the below IP ranges for the Cluster

 These IP ranges are used for when the cluster exposes an IP address via either `type: LoadBalancer` or `type: Service`. Something to note is I dont use `type: NodePort` as this is just a pain. 
IP rangeUse`172.16.2.0/28`Node IP address`172.16.0.0/25`Services
## What I'm running

So with Kubernetes, there's a few ways to manage applications.

You can use Raw manifest files, and apply them with `kubectl apply -f <name>.yaml` or you can use Helm charts, which are packaged *applications* and you use the helm CLI to install them.

There are of course other systems, but I primerly use the above. 

Then there's one level up, which consumes the manifests (be them helm or raw) called GitOps. I've installed a system called Flux which enables you to declare in a girt repo how you want things to look, then Flux will reconcile everything and deploy the changes you made in the Git repo. 

## Things installed

In the cluster I've got the below installed

#### Cloudflared

Cloudflared is a system from Cloudflare which allows you to use their tunnels system to send traffic back in to your network without having to port forward and open up your network.

I've custom built a helm chart that sets up a `ExternalName` service in the cloudflared namespace, which then points to an actual service name in the cluster. 

This does seem like an anti-pattern, but it allows you to simply go `kubectl get svc` in the `clouflared` namespac and see what's being *exposed*

This means the `values.yaml` file looks like the below

    services:
      http:
        - domain: example.breadinfra.net
          svc: podinfo
          namespace: podinfo

This is then fronted by a Terraform module pre-configured to create DNS records with the tunnel ID.

I've put together some documentation on a stripped down version, but if you are interested in the helm chart, please get in contact and I am happy to opensource it 
[

Cloudflare Tunnels on k3s - breadNET Documentation

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/kubernetes/k3s/cloudflare-tunnels-on-k3s.png)
](https://documentation.breadnet.co.uk/kubernetes/k3s/cloudflare-tunnels-on-k3s/?utm_source&#x3D;breadnet&amp;utm_medium&#x3D;blog&amp;utm_campaign&#x3D;kubernetes%20at%20home)
This is managed via Flux

#### PiHole

Pihole is an adblocking and DNS server that lots of people in the self hosting community are using. I've deployed this in to my cluster via Flux. This gets a Service address of `172.16.0.1` which is then configured via the router to be handed out to all clients to use for DNS resolution

    ➜ k get svc    
    NAME             TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    pihole-dhcp      LoadBalancer   10.43.212.91    172.16.0.1    67:32594/UDP                 9d
    pihole-dns-tcp   LoadBalancer   10.43.51.136    172.16.0.1    53:30410/TCP                 9d
    pihole-dns-udp   LoadBalancer   10.43.123.66    172.16.0.1    53:31204/UDP                 9d
    pihole-web       LoadBalancer   10.43.164.153   172.16.0.1    80:31832/TCP,443:30309/TCP   9d
    

This is managed by Flux, so when I get a new Block list, I update it in Git and the container rolls

### Metallb

Metallb is a load balancer (I suppose) system that is often deployed to on-premise Kubernetes clusters that acts as a load balancer

> MetalLB is a load-balancer implementation for bare metal [Kubernetes](https://kubernetes.io/) clusters, using standard routing protocols.

This is used to allow us to assign IP address to Services and service type Load balancers.

Eventually I plan to configure it to use BGP to get IP address, but I dont know Junos very well or BGP

### Nginx Ingress Controller

Nginx ingress controller is a *flavour* of NGINX (the popular reverse proxy and web server) designed specifically for Kubernetes. This is used for `kind: Ingress` objects where you can configure Host paths, host names and SSL. 

This is managed with Flux

### Snipe IT

SnipeIT is a system designed to manage IT inventory, more so tracking the physical Assets like their purchase cost, warranty, Invoices, who the device is assigned to, how much it deprecates. 

I've written a custom helm chart for this.

This is managed with flux

### Status page

Status page is using [gatus.io](https://gatus.io) in a self built helm chart to host an internal status page with (currently) 3 resources. Eventually I plan to make this public behind Cloudflare Tunnels, but I need to fix the helm chart.

One thing is this is pulling an AWS (Hosting the status page on your infrastructure) - so for the time being this will only serve as my status page for in cluster things
![](__GHOST_URL__/content/images/2023/11/image.png)
This is managed with Flux

### Grocy

Grocy is a PHP app designed to help you manage your kitchen inventory. I've run this off and on for quite a while. The main thing that's stopping me from really commiting to it is the Developer's hate towards an external database. Meaning I have to persist the sqlite database on the cluster, and we all know that persistence is Kubernetes gets painful. 

This seaways very nicely on to

## The Persistence server

This server is my hacky solution to dealing with running persistent workloads in Kubernetes. 

The server is an Intel i5 with 8gb ram and a 128GB ssd. 

I've installed the below services dirctly on to the node, as opposed to being in podman

- MariaDB
- NFS

The NFS export is setup that it can be used as persistent Volumes in the cluster for things like Media servers (Coming soon) and Image uploads to applications (Snipe, Grocy etc)

I will need to look at installing some other things like:

- MongoDB
- Postgresql 

### Where are the helm charts stored

I have a [Taskfile](taskfile.dev/) in the monorepo that packages the helm chart as an OCI artifact and pushes it to Google Artifact Registry. 

In the cluster, I have then configured flux to use a custom built credential helper 
[

Authenticate flux with Google Artifact Registry - breadNET Documentation

breadNET Documentation

![](https://documentation.breadnet.co.uk/favicon.ico)logo

![](https://documentation.breadnet.co.uk/assets/images/social/kubernetes/flux/flux-artifact-registry-google-auth.png)
](https://documentation.breadnet.co.uk/kubernetes/flux/flux-artifact-registry-google-auth/)
## What the flux 

I've mentioned that I use Flux to manage almost all the deployments, but what actually is flux.

Flux is a GitOps toolkit [(GOTK)](https://pkg.go.dev/github.com/fluxcd/toolkit/cmd/gotk)  from Weave Works, it allows you to declarativly descibe the state of the cluster and then sync that declaration to the cluster. Sure, a simple solution would be a cron job doing `git clone && kubectl apply -f **.yaml*`but this allows for logging and structured config.

This is a screenshot from the repo where I configure the flux system, and the deployments
![](__GHOST_URL__/content/images/2023/11/image-1.png)
`flux-system` - this contains all the Flux config. It's a brain bender, but flux manages it's self via it's own repo. 

`HelmRelease` - Deploys the helm chars from the HelmRepositories I specify. Here you can also pass the values as well as what namespace and version of the chart to use

`HelmRepository` - This is where we tell flux where to get the helm charts we want to use later. Flux supports Cloud storage buckets, OCI (I use this one personally) and HTTPS endpoints, provided there is an `index.yaml` file

`namespaces` - Defines the namespaces in the cluster.

To create a new resource, you just commit a file in the `k3s/*` directory and flux will build it. At work I have built a lot more complex solution for this, but at home I don't need something super complicated.

## Things I would do differently

So far I would stick with this design. It's quite clean and for me, makes sense. Everything is in Git, it hardly uses much power, and it's HA. What more could you want from a small cluster.

If I could change something, it would be where it's physically positioned. On top of the water heater is not amazing

## Talk is cheap, show me the cluster

Something to note is, this is a small cluster. It runs a few services and nothing more, nothing less. I am not running HPC here.

If you are worried about the heat the water heater puts off, dont be. That gap between the nodes is enough actually to keep them at a happy enough temperature

    root@k3s-01:~# sensors
    coretemp-isa-0000
    Adapter: ISA adapter
    Package id 0:  +43.0°C  (high = +84.0°C, crit = +100.0°C)
    Core 0:        +41.0°C  (high = +84.0°C, crit = +100.0°C)
    Core 1:        +40.0°C  (high = +84.0°C, crit = +100.0°C)
    
    acpitz-acpi-0
    Adapter: ACPI interface
    temp1:        +27.8°C  (crit = +119.0°C)
    temp2:        +29.8°C  (crit = +119.0°C)
    
    pch_skylake-virtual-0
    Adapter: Virtual device
    temp1:        +53.5°C  
    
    root@k3s-01:~# 
    

If these look a little high to you, something to note is these are *consumer* devices, and designed that they can be given to the average joe who will put the computer down the back of their desk with -1 airflow and 200 cubic meters of dust flakes.

Now I've finished justifying the decision, let me show you the cluster

### The cluster and it's supporting infra
![](__GHOST_URL__/content/images/2023/11/cluster.jpg)
Some more justifying the terrible placement

- The router (Black box tied to the copper pipe) techniaclly is water cooled. I know this is really less than ideal, but this is the only place I could put it that I had access to, and kept it cool. You may laugh, but since putting it there, it actually reduces the temprature of the router, really letting me get all 110mbps I paid for. 

### Cluster from the top
![](__GHOST_URL__/content/images/2023/11/cluster-top.jpg)
### Switch
![](__GHOST_URL__/content/images/2023/11/switch.jpg)
The Switch sees a constant load of about 2-5mbps when the cluster is just chilling
![](__GHOST_URL__/content/images/2023/11/image-2.png)
### The new router
![](__GHOST_URL__/content/images/2023/11/router.jpg)
This is the Juniper SRX-330 I have purchased, I need to learn how to use it. Currently I have PPPoE setup on `ge-0/0/0` (White ethernet) and then setting up the servers *lan* on `ge-0/0/1` (trunk port) to the switch, where the rest of my devices will connect to, and then anything else can go in to the router using an `irb`

This overall leaves the network looking like the below
![](__GHOST_URL__/content/images/2023/11/simple-network-2.png)
---

I hope you've enjoyed this, if so, or if not, please feel free to get in contact. 

You can contract me to set up a Kubernetes cluster in your house, provided you pay my petrol (I have a Costco membership) and feed me. 
