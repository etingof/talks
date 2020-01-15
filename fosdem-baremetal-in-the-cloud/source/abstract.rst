
With IaaS, common way to provide compute resources is to ask the hypervisor to
allocate a bunch of VMs for you.

Sometimes, however, allocating a bare metal machine could be essential to
withstand higher workloads or harden data security.

Running a container engine (like k8s) inside of a bare metal machine avoids
double resource management and achieves higher density.

In this talk we will introduce the OpenStack project called Ironic - the bare
metal provisioning and life cycle service that can also act as a hypervisor
for the OpenStack compute service.

We will explain system design, typical hardware management workflow, upcoming
features and future challenges.
