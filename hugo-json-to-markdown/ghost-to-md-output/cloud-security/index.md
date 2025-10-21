---
title: Cloud security
slug: cloud-security
date: 2020-09-29T18:22:44.000Z
date_updated: 2021-05-02T01:46:02.000Z
summary: Thinking of moving to the cloud or currently operating on the cloud? Find out how how secure you are.
---

> This is still being written but I think it's important you see it

Well, It's official. I am now a 'Cloud engineer' as far as my company is concerned. Woo!

On the topic of cloud, I should make my first post about something that is usually overloked by companies when migrating to the cloud: **Security**

This is only a guidance and you should consult your SecOps team if you have one, or consider hiring consultants for this. You can get in contact and I can point you towards companies that are good at this.

---

Hopefully this guidance will help you to figure out how confident you are in your clous services being able to securly handle your PII as well as private operatoinal data.

Overall this guidance will be built upon a collection of 14 cloud security principals.

Futher towards the bottom of this post you will find a section about 'Seperation and cloud security'

The extent of your security will be dependant on your responsiblities to yuor department and clients, but will vary significatly dependent on your industry. Most Public cloud providers will have reasonably good default security rules, but your responisbilites will be at largest when managing your own infrastrucute. (IaaS)

---

### How this guidance will work

When you're trying to get a better and clearer picture of the risk you would be taking when adapting can, for the most part, be quite difficult to do jsut due to the complex nature of the cloud. I reccomend you use the cloud security principals later on in this post to better structure your analysis. Below you will first find the 8 step process, follwing this will determin which of the princpals are most effecting you and your requirments, and how cloud providers can meet them.
Most important is that the decisions youmake about the use and configuration of cloud based services *shoudl*be part of your regular risk managment procedures.

---

### Whos is this guidance for?

This guidance is aimed at Enterprise organisations but can be refrenced for Public sector, how ever you should consult your managment before acting.

---

### Making a decision

You should work through the below steps which will help you identify cloud services that meet your secirity requirments for operating on the cloud.

1. **Understand operational requirments**
Understand your ideal use case of the cloud service, consider issues like avaliblity and connectivity. Identify tisks that would be unacceptable should they be realised, and what is ok.
2. **Understand your information**
Identify the type, source and destination of the data that will be stored, processed and transpoted by the cloud service. Understand legal regulations and implications. An example would be storing data on EU citizens would fall under [GDPR](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
3. **Determin relevant security principals**
You know the business requirments, the risks you're willing to/not to take, you've got a clear picture of the information which will be exposed to the service.

Now you will be able to determin which of the cloud security principals are most relevant.
4. **Understand how principals are implimented.**
Find out how your cloud service provider calimes to impliment your security principals that you've previouslt identifeid as relevant. They will have different approaches you should consider and may be able to provide you guidance.
5. **Understand the assurnace offered**
Can your cloud service provider demonstrate the principals that you have identified in step 3 been implimented correctly and to standard? You may want to use external vendors to help uou identify their claims
6. **Identification of additional mitigation that can be applied**
Consider any additioanl measures you or your organization can apply (as a consumer of cloud services) can help to reduce the risk of applications and information.
7. **Consieder remaining risks**
Having worked your way through the above steps, decide weather there are any remaining that need to be addressed, and their importance.
8. **Continue to monitor and manage risks**
Once deployed to the cloud, monthly review weather your services are still meeting your operational needs as well as securty needs.

---

# Implementing the Cloud Security Principles

Seeing as there are 14 principals, I will try and explain what they are, it's goal and how you're able to impliment them. Let's get a crack on!

### 1: Data in transit protection

Users data that is transisting networks should be adequatly secured to prevent tampering and eavesdropping.

It can be a combination of:

- Networ protection: Denying access to networks, securing access layers
- Encryption: Denying attacker the ability to read the data in the first place

**Goals**:

You should be confident that:

- Data in transil is protected when leaving your control and to users
- Transit data is protected internally eg: App to webserver, API endpoints

**Implimentation**

There are many factors to remember when looking in to securing cloud endpoints, but it's imporatnt to remember that at some point the data will leave your VPC or cloud enviroment and will be presented to a user at some point down the line. Securing data in transit can be a hard one but there are key points to look at when securing these. We will first address where an attackor or bad actor would gain access. This could take the form of physical access to hardware, logical access if there is broken code bases or vulnerable software, or between the user and the service.

A simple means to mediating this risk is to emply encryption between endpoins. This should be used between API interfaces, database connections and web conenctions. You would want to use TLS when:

- Access to confidential data is required
- Support authhentication and access control.

A section that can usually be overlooked would be onbaording and offboarding users.
These  processed can usually involve large ammounts of bulk data being moved around, be it copying files to a new starters computer, or offboarding a user where you are taking an image of their account or computer for legal holding. In this case it would be reffered to as 'Transient Data' which should be protected in line with:

### 2: Asset protection and resilience

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!
