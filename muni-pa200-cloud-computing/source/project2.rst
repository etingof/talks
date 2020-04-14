
MUNI PA200 project 2
====================

The plot
--------

You are an IT technician at a small company. Your employer needs to establish
its presence on the Internet. For that purpose, they purchased a service from
some IaaS company and want to set up a web-site with a content management system
(CMS) there. Incidentally, IaaS software is OpenStack.

Your assignment is to implement automatic and repeatable deployment of the
entire Web/CMS system on the OpenStack cloud.

Technical requirements
----------------------

To ensure repeatable and automated deployment of the infrastructure, you
should rely on the OpenStack HEAT for deployment orchestration. Your
project 2 task boils down to creating and instantiating a HOT template
which deploys the `Wordpress <https://en.wikipedia.org/wiki/WordPress>`_
application.

Your installation should span across two OpenStack instances - one for hosting
the SQL database (e.g. MariaDB), the other for the WordPress system.

Both instances can use any Linux OS image available on the cloud. The kind of
the image should be made configurable at the deployment time. The choice of
the image should go through some validation to make sure the chosen image
exists in the OpenStack Glance image repository.

The VM flavors being used by both instances should be made configurable at the
deployment time. The choice of flavour should go through some validation to make
sure the chosen flavor exists in OpenStack Nova.

Configurable HOT template parameters should have some reasonable defaults
where it makes sense. Though the use of environment file is encouraged for
easier deployment customization.

The SSH key should be injected into both instances at the deployment time
to enable admin access to the instances.

Configuration that needs to be shared between instances (such as DBMS address,
credentials etc) should be transferred through cloud-init.

Successfully instantiated HOT template should report the URL of the WordPress
site. The site should be available for browsing over public Internet.

.. note::

   No DNS name is required, just IP address would suffice.

DB instance requirements
++++++++++++++++++++++++

DB instance should have around 1GB of RAM. DB instance should mount a 1GB block
storage volume, allocated by OpenStack Cinder, to keep the DB files on a
separate persistent volume.

All DBMS credentials should be made configurable at the deployment time and pass
through some validation to ensure reasonably strong passwords.

Web instance requirements
+++++++++++++++++++++++++

Web instance should have around 1GB of RAM and no external storage
configured. Web instance should have a floating IP assigned, so that it
becomes available over the Internet.

Web instance should have a security group applied that protects OS services
from attacks over the Internet. Though HTTP and SSH services should be
made accessible.

.. note::

    Floating IP and security groups are OpenStack terms that refer to
    public IP address and firewall rules respectively.

Expected outcome
----------------

Project result should be uploaded as a HOT template file (.yaml) along with
a sample environment file to the homework vault at MUNI IS.

Your teacher will evaluate your work by running your HOT template in his
OpenStack project to see if it works or not quite.

.. warning::

    Make sure to remove any sensitive information from the uploaded files!

Project results submission deadline is **15.5.2020**.

MUNI OpenStack access
---------------------

You should register at
`MetaCentrum <https://metavo.metacentrum.cz/osobniv3/wayf/proxy.jsp?locale=en&target=https%3A%2F%2Fperun.cesnet.cz%2Ffed%2Fregistrar%2F%3Fvo%3Dmeta%26locale%3Den>`_
to get your
`personal OpenStack project <https://cloud.gitlab-pages.ics.muni.cz/documentation/quick-start/>`_.
This process is automatic and immediate.
