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
Run a command:

`make crawler` or `docker-compose build crawler`

####4.) Run a spider
Run a command:

`make run spiderdomain` or `docker-compose run crawler scrapy crawl spiderdomain`

###Manual
**TESTED ON:** Ubuntu 16.04
####1.) Install libraries required by pyquery and scrapy (both of them use lxml and lxml if some sys libraries will be missing)
Run following command:

`sudo apt-get install -y python3-pip python3-dev python3-lxml-dbg build-essential libssl-dev libffi-dev`

####2.) Install python libraries
Make sure that you are using python 3.5.

Open terminal and open project directory (root of the project). Then run following command:
`pip install -r requirements.txt`

####3.) Run a spider
Test out a spider. Run following command:

`scrapy crawl musiciansfriend.com`

##DEPLOYMENT

###scrapinghub

####1.) Login and create project
- First you need to login/register to the spider manager on a [scrapinghub](https://dash.scrapinghub.com/account/login/) website. To
run one spider simultaneously they don't charge and also don't ask for any credit card.
- Then you create a project if it's not already created.
- Select a project that you created and click `Code & Deploys` on the left menu.
- At the bottom of the page you have **Api Key** and **project ID**.

####2.) Api Key and project ID to ENV variables
Now copy paste **Api Key** and **project ID** from the `Code & Deploys` page on scrapinhub and set them as ENV variables.
export SHUB_APIKEY=yourverylooooooongapikey
export SHUB_PROJECT_ID=numericid

####3.) Deploy
Deploy crawler code to the scraping hub. Run following command:

`make deploy`
####4.) Run a spider on scrapinghub
Code has been deployed and you can run spiders on scrapinghub. For any more
info about scrapinghub, please read their [documentation](http://doc.scrapinghub.com/dash.html).
