import requests
from bs4 import BeautifulSoup

def scrape_linkdin_job_details(job_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(job_url, headers=headers)

    if response.status_code != 200:
        return {"error" : "Unable to fetch job details. Check the URL"}
    
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find("h1").text.strip() if soup.find("h1") else "N/A"
    company = soup.find("span" , class_="topcard__flavor").text.strip() if soup.find("span" , class_="topcard__flavor") else "N/A"


    location_tag = soup.find("span" , class_="topcard__flavor topcard__flavor--bullet")
    location = location_tag.text.strip() if location_tag else "N/A"

    job_desc_tag = soup.find("div", class_="show-more-less-html__markup")
    job_description = job_desc_tag.text.strip() if job_desc_tag else "N/A"

    return {
        "title": title,
        "company": company,
        "location": location,
        "job_description": job_description
    }