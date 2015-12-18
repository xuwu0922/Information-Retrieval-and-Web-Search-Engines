# Created by Xu Wu

from nutch.nutch import Nutch
from nutch.nutch import SeedClient
from nutch.nutch import Server
from nutch.nutch import JobClient
from nutch.nutch import CrawlClient
import nutch

#intial a sample of 3 rounds
state_rounds=3
nt = Nutch() #initail the nutch
job_client=nt.Jobs("crawpy1") #create a job client

#create a sample seed list 
seed_client = SeedClient(nt.server)
seed_urls=('http://www.ncgunads.com','http://www.newmexicoguntrader.com','http://www.nextechclassifieds.com','http://www.sanjoseguntrader.com','http://www.tell-n-sell.com')
_seed= seed_client.create('espn-seed',seed_urls)


#intial a crawl client with the seed and job client
crawl_client=nt.Crawl(_seed,seed_client,job_client,state_rounds)

# loop to process the crawling
current_job=job_client.inject(_seed,None)

while current_job!=None:
	while current_job.info()['state']== 'RUNNING':
		continue
	current_job=crawl_client._nextJob(current_job)
