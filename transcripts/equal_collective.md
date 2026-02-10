I am one of the core engineers working on designing the entire DataBase-as-a-Service 
(DBaaS) platform. We are working from scratch to replace a fully manual database 
provisioning and operations workflow to an API driven automation in a cloud environment.

The main idea was to understand the existing system and enhance it.
The company has the infrastructure to provide Virtual Machines (VM) - includes the 
Hypervisor Layer, Storages etc. I had to figure out how to layer database provisioning and 
lifecycle management on top of the existing VM provisioning system.
Did some extensive research on control-plane driven DBaaS architectures used by large
cloud providers.

Since DBaaS has a large surface area, I shortlisted only the minimum viable capabilities required
to ship a usable system first.
Because there are a plethora of features and making all of them at once is not possible.

We started with building a POC.
I was responsible for the following features, which I owned:
1. Providing Containerized DB environments, which would be provisioned from the control
plane and is fully API driven.
2. Hypervisor-VM communication
3. DataBase failover behaviour, high availability and monitoring.

Based on this several key decisions were made as to how we can provide these features
based on what we have.
We had VMs, so one of the key decisions was, whether should we have VM-based isolation 
or shared multi-tenant DB cluster, because they both will have completely different
architectures and the overall flow (the core components like backups, failover etc. will
have different methods in shared environments.)
The decision was based on customer workload isolation, reliability expectations, and
operational risk. Based on this we came up with 
different tiers of provisioning like any other provider (e.g. mongo DB).

Then alot of decisions of what to use were made because we cannot go on building 
everything from scratch. Another issue was that the requirements kept on changing.
Any architecture that we proposed to our CTO and team lead, they gave us new constraints
such as not being able to use kubernetes due to internal infrastructure policies, so we 
had to come up with other alternatives. We even had to understand VMware internals and 
how the VM provisioning is happening so that we can automate it and establish a 
communication channel between the VM and hypervisor for executing lifecycle actions 
securely from the control plane.
The work is under progress but we have built a POC that successfully provisions PostgreSQL 
containers and manages the DB lifecycle via an API-driven control plane.

Here is another question:
How has the way you work and learn as an engineer evolved? Tell us about the tools, workflows, and AI assistants you've adopted (or abandoned), and how you decide when something new is worth integrating into how you work. *
We're trying to understand how you evolve as an engineer — not just what you use, but how and why your workflow changes over time. Whether you're drawing from years of work experience, internships, personal projects, or your time learning to code — we want to hear your story.
Some things you might touch on:

Note - Real world examples and specific instances will help and make your answer stronger. We would like you to answer in the context of your experience, personal and real projects you've worked on instead. This is to understand your journey and not a statement on how to use modern tools in AI assisted development.

1. Tools or frameworks you've moved away from, and what pulled you toward the alternatives 
2. How AI assistants (Copilot, Claude, ChatGPT, Cursor, v0, etc.) have entered your workflow — what stuck, what didn't, and why
3. Specific tasks where AI has genuinely changed how you work (not just "it helps me code faster")
4. How you evaluate new tools — do you experiment constantly, wait for others to validate, or something else?
5. What your workflow looked like when you started vs. today, and what drove the biggest shifts

Be concrete. Instead of "I use AI for coding," tell us which assistant, for what kinds of problems, and what you still prefer to do without it.

A note on using AI to answer this: Feel free to use AI assistants to help you format or structure your response - that's part of how you work, and we get that. But the story itself should be yours. We're not looking for a polished essay; we're looking for your actual journey.


For this lets start by mentioning that I see AI as another tool that will do what I tell it to do. But first I have to know things to prompt it, I learnt this the hard way. In my earlier projects for example in case of the RAG pipelines that I built, I tried using multiple AI's and compare the results as to which one worked. Things were very messy, I had to keep track of all the results and things became even more tough to manage, when I tried to add new features like parsing for multiple types of documents or using different type of parser to figure out which one works best, the code base becomes a different type of mess. Earlier my prompts also used to be vague. But I learnt from this mess.
There were times when I thought that I could have done it better or faster, rather than going through this mess of a code, but that was because I couldn't use it properly.
I figured out what to use when, I first made a clear picture of things in my mind before even writing a prompt. I planned everything properly, i.e. basically low level design of things and then used AI to fill those classes. I even tell the AI what logic to implement, I made the AI do the manual work and I do all the thinking part. Also, if I need help in thinking as to how to proceed, then that is a separate concern and is looked by another AI (I prefer chatgpt for talks and researching).
So along the way I discovered Aider which is an AI assistant in the terminal interface that helps with many of things, similar to copilot but with a lot more features and less bloat.
There are many more tools that come up, testing all of them is not feasible, so I wait for a few days and wait for others to test and see the results, so that I can have a gist of what it actually does and then decide whether it's worth giving a try or not.
While trying new tools I first do a basic test on the things I have completed earlier, i.e. this RAG pipeline, that I built. I know all the bottlenecks where earlier I failed and how I have resolved it, so it is quite interesting to see how the new tool is able to solve that. 

