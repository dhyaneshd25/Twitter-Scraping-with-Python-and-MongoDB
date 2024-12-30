import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Set up ProxyMesh
PROXY = "http://123.456.789.0:8080"
options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server={PROXY}')

# Initialize MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["trending_topics"]
collection = db["topics"]

def scrape_twitter():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://twitter.com/login")
    
    # Log in to Twitter
    username = "your_twitter_username"
    password = "your_twitter_password"
    driver.find_element(By.NAME, "session[username_or_email]").send_keys(username)
    driver.find_element(By.NAME, "session[password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button']").click()
    time.sleep(5)  # Wait for the page to load

    # Fetch trending topics
    trends = driver.find_elements(By.XPATH, "//div[@data-testid='trend']")
    top_trends = [trend.text for trend in trends[:5]]
    ip_used = requests.get("https://api.ipify.org").text  # Get current IP address

    # Save to MongoDB
    unique_id = str(int(time.time()))
    record = {
        "_id": unique_id,
        "trend1": top_trends[0] if len(top_trends) > 0 else "",
        "trend2": top_trends[1] if len(top_trends) > 1 else "",
        "trend3": top_trends[2] if len(top_trends) > 2 else "",
        "trend4": top_trends[3] if len(top_trends) > 3 else "",
        "trend5": top_trends[4] if len(top_trends) > 4 else "",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_used,
    }
    collection.insert_one(record)
    
    driver.quit()
    return record

if __name__ == "__main__":
    print(scrape_twitter())
