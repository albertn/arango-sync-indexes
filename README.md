Arangodb sync indexes
========
We use ArangoDB master-slave replication setup based on documentation here_. 

.. _here: https://docs.arangodb.com/3.2/Manual/Administration/Replication/Asynchronous/

in our application.

Limitation with this replication is, it didn't replicate index in each collection from master to the slave(s) instance(s).

This script help us to mitigate that limitation, it will sync indexes based on master instance to each collection with type 'document' in slave instance(s).


Installation
-------------
.. code:: shell

pip install pyArango


Initialization
---------------

Set:
MASTER = 'http://masterdb.com:8529'
SLAVE1 = 'http://slavedb:8529'
SLAVE2 = 'http://slavedb2:8529'

.. code:: shell

python script.py
