Living Literature Reviews
=========              
A way to represent literature reviews in a machine-interpretable and easy updateable manner using Nanopublications.

## Introduction
This repository is part of the Living Literature Reviews paper written by Michel Wijkstra, Timo Lek, Tobias Kuhn, Kasper Welbers, and Mickey Steijaert (VU University Amsterdam).

## Content
* The public nanopublications that are generated as part of this project can be found in the 'np' directory.
* The data that is used to generate the nanopublications can be found in the 'Data' directory.
* The code that is used to generate the nanopublications can be found in the 'src' directory.
* The np script to use the java-nanopublication library can also be found in the 'src' directory. (https://github.com/Nanopublication/nanopub-java)
* The docker-compose file that is used to start and create the Virtuose container to load the nanopublication and query them can be found in the 'src' directory. (https://hub.docker.com/r/tenforce/virtuoso/)
* The docker-compose file that is used to run the website, consisting of three connected containers, can be found in the upper directory.
* Example templates for Nanobench can be found in the 'nanobench-templates' directory. (https://github.com/peta-pico/nanobench)


## Getting Started
NOTE: Since the np script of the java-nanopublication library is only working on Linux, the code also has to be executed on a Linux Operating System. Furthermore, Python 3.6, 'curl' and Java have to be installed. It is assumed that the 'np' script of the java-nanopublication library is present in the 'Documents' directory of the user.

### Step 1:
Running the code is straight forward. One only has to execute the 'run.sh' inside the 'src' directory.
On the first time that the np script is used it will download the most recent .jar library to execute the commands.

### Step 2:
Once the bash file has been executed all the nanopublications will be saved as NQuads in the 'src/data/toLoad' directory. These can now be queried using Virtuoso. To launch Virtuoso you can type 'docker-compose up' in the 'src' directory. The TriG varient of the nanopublications, trusty and non-trusty are also saved in the 'np' directory. This makes it easier to see what kind of queries are possible on the given data.
NOTE: For Virtuoso container to work Docker has to be installed.

### Step 3
Once the container is active, you can go to 'localhost:8890/sparql' in the browser and execute the queries in the 'queries' directory.
NOTE: Some queries make use of of specific Trusty URIs that can change when the nanopublications are generated again. The correct URIs can therefore be found in the trusty files in 'np' directory.
