#CRAWLER APPLICATION

##INSTALATION

###Docker
**TESTED ON:** Ubuntu 16.04
####1.) Install docker (if it's not already installed)
If you have ubuntu version 16.04 then there is no need to install docker.

For installation procedure please visit [docker website](https://docs.docker.com/engine/installation/)

####2.) Install docker compose (if it's not already installed)
For installation procedure please visit [docker website](https://docs.docker.com/compose/install/)

####3.) Build image and container
Run a command: `docker-compose build crawler`

####4.) Run a spider
Run a command: `docker-compose run crawler scrapy crawl spiderdomain`


###Manual (Tested on ubuntu 16.04)
####1.) Install libraries required by pyquery and scrapy (both of them use lxml and lxml if some sys libraries will be missing)
Run following command:

`sudo apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev libffi-dev python3-pip libssl-dev`

####2.) Install python libraries
Make sure that you are using python 3.5.

Open terminal and open project directory (root of the project). Then run following command:
`pip install -r requirements.txt`

####3.) Run a spider
Test out a spider. Run following command:

`scrapy crawl musiciansfriend.com`
