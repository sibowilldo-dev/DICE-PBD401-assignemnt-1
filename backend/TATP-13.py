import requests
import json
from sqlalchemy.orm import sessionmaker
from models import appl

# Set the API endpoint for the job feed
job_feed_url = "https://example.com/api/job_feed"

# Make a request to the job feed API and parse the response as JSON
response = requests.get(job_feed_url)
job_feed = json.loads(response.content)

# Iterate over the job listings and print their titles and descriptions
for job in job_feed:
    print("Job title:", job["title"])
    print("Job description:", job["description"])
    print()
