#CRAWLER APPLICATION

##INSTALATION

###Docker
Currently not supported, but will come soon.

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
