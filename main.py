from scrapy import cmdline
cmdline.execute("scrapy crawl musiciansfriend.com -o file.csv -t csv".split())
