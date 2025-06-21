from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import yagmail
import os
from dotenv import load_dotenv


website = "https://www.indiatoday.in/"
path = "/usr/bin/chromedriver"
serv = Service(executable_path=path) 
driver = webdriver.Chrome(service=serv)

driver.get(website)


containers=driver.find_elements(by="xpath",value='//div[@class="B1S3_content__wrap__9mSB6"]')

data={"heading":[],"subs":[],"links":[]}

for container in containers:
    heading=container.find_element(by="xpath",value='./h2').text
    subs=container.find_element(by="xpath",value='./div/p').text
    link=container.find_element(by="xpath",value='./h2/a').get_attribute("href")
    # print(f"Heading : {heading}\nsubs : {subs}\n")
    data['heading'].append(heading)
    data['subs'].append(subs)
    data['links'].append(link)



df=pd.DataFrame(data)
df.to_csv("news.csv",index=False)



msg_body="📰 *Here is your daily news summary:*\n\n"        # title

for i,row in df.iterrows():
    msg_body += f"{i+1}). {row['heading']}\n   {row['subs']}\n\n"





load_dotenv(dotenv_path=".env")

sender_email = os.getenv("EMAIL_USER")
app_password = os.getenv("EMAIL_PASSWORD")

if not sender_email or not app_password:
    raise Exception("EMAIL_USER or EMAIL_PASSWORD not loaded. Check your .env file.")


yag=yagmail.SMTP(user=sender_email,password=app_password)

eamils=[
    "23052757@kiit.ac.in"
    ]

for i, address in enumerate(eamils):
    yag.send(

        to=address,
        subject="🗞️ Daily News Digest",
        contents=msg_body
    )

    print("✅ Email sent successfully!")
