.PHONY: build app start remove status stopall run scrapyd pyclean

build:
	docker-compose build crawler

app:
	docker-compose up -d

start:
	docker-compose up

remove:
	docker-compose stop && docker-compose rm -f

down:
	docker-compose down

status:
	docker-compose ps

stopall:
	docker stop $(docker ps -a -q)

run:
	docker-compose run --service-ports crawler scrapy crawl $(filter-out $@,$(MAKECMDGOALS))

scrapyd:
	docker-compose run --service-ports crawler scrapyd

bash:
	docker-compose run --service-ports crawler /bin/bash

pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
