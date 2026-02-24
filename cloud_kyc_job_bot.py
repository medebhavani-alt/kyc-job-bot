import requests
from bs4 import BeautifulSoup
import smtplib
import os

# Load secrets from GitHub Actions
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Job search URL
URL = "https://www.indeed.com/jobs?q=kyc+analyst&l=Remote"

def search_jobs():
    print("🔍 Searching jobs...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for job in soup.select(".jobTitle span"):
        title = job.text.strip()
        if "KYC" in title or "AML" in title:
            jobs.append(title)

    return jobs


def send_email(job_list):
    if not EMAIL or not APP_PASSWORD:
        raise Exception("❌ EMAIL or APP_PASSWORD is missing in GitHub Secrets")

    if not job_list:
        job_list = ["No new KYC jobs found today"]

    message = "Subject: Daily KYC Job Alert\n\n"
    message += "\n".join(job_list)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, APP_PASSWORD)
    server.sendmail(EMAIL, EMAIL, message)
    server.quit()

    print("✅ Email sent successfully!")


if __name__ == "__main__":
    jobs = search_jobs()
    send_email(jobs)
