.PHONY : crawler

crawler :
	docker-compose build crawler

run :
	docker-compose run crawler scrapy crawl $(filter-out $@,$(MAKECMDGOALS))

deploy :
	shub login
	shub deploy-reqs $(SHUB_PROJECT_ID)
	shub deploy $(SHUB_PROJECT_ID)
	rm -r build
	rm -r project.egg-info
	rm -f setup.py
	rm -f scrapinghub.yml
	shub logout

pyclean :
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
