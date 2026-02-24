import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

EMAIL = "medebhavani@gmail.com"
APP_PASSWORD = os.environ.get("GMAIL_PASSWORD")

KEYWORDS = ["KYC", "Sanctions", "AML", "Financial Crime"]

def search_jobs():
    jobs = []
    urls = [
        "https://boards.greenhouse.io/stripe",
        "https://boards.greenhouse.io/revolut",
        "https://boards.greenhouse.io/wise",
        "https://boards.greenhouse.io/coinbase"
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                title = a.text.strip()
                link = a.get("href")
                if title and link and any(k.lower() in title.lower() for k in KEYWORDS):
                    if not link.startswith("http"):
                        link = url + link
                    jobs.append(f"{title} | {link}")
        except Exception as e:
            print("Error:", e)

    return "\n\n".join(jobs) if jobs else "No new KYC / AML jobs found today."

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "Daily KYC / Sanctions Job Alerts"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, APP_PASSWORD)
    server.sendmail(EMAIL, EMAIL, msg.as_string())
    server.quit()

send_email(search_jobs())
