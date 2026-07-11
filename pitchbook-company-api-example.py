"""
PitchBook Company API: A Quick Start Example
See more at: https://apify.com/johnvc/pitchbook-company-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/pitchbook-company-api/input-schema?fpr=9n7kx3

This script shows how to call the PitchBook Company API on Apify from Python and
read its structured JSON output. Send one or many public PitchBook company
profile URLs and get one clean row per company (name, industry, employees,
founding year, ownership status, funding and deal history, competitors, and
more).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Kept to a single company URL so your first run stays cheap (you pay per
# company returned). Add more URLs to the list to collect many companies in one
# batch; they are collected in parallel and returned one row each.
run_input = {
    "companyUrls": [
        "https://pitchbook.com/profiles/company/10874-98",
        # "https://pitchbook.com/profiles/company/521432-65",
    ],
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/pitchbook-company-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset
# (apify-client 3.x returns a Run object; use .default_dataset_id, not run["..."])
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} company(ies).\n")

# Show a few key fields from each company.
for item in items:
    print(f"Name:             {item.get('name')}")
    print(f"Industry:         {item.get('primaryIndustry')}")
    print(f"Employees:        {item.get('employees')}")
    print(f"Founded:          {item.get('foundedYear')}")
    print(f"Ownership:        {item.get('ownershipStatus')}")
    print(f"Financing status: {item.get('financingStatus')}")
    print(f"Latest deal type: {item.get('latestDealType')}")
    print(f"Latest deal amt:  {item.get('latestDealAmount')}")
    print(f"URL:              {item.get('companyUrl')}")
    print(f"Summary:          {item.get('summary')}")
    print("-" * 60)
