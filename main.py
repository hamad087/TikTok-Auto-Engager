import json
import random
import time
from selenium import webdriver
from openai import OpenAI

class TikTokBot:
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)
        
        self.ai = OpenAI(api_key=self.config["openai_key"])
        self.drivers = [self._init_driver() for _ in range(2)]
    
    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def generate_content(self, video_url):
        response = self.ai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد TikTok محترف. أنشئ محتوى تفاعليًا."},
                {"role": "user", "content": f"حلل هذا الفيديو: {video_url}"}
            ]
        )
        return response.choices[0].message.content

    def engage(self, video_url):
        content = self.generate_content(video_url)
        for driver in self.drivers:
            try:
                driver.get(video_url)
                time.sleep(random.randint(2, 5))
                like_btn = driver.find_element("xpath", "//div[@aria-label='إعجاب']")
                like_btn.click()
                time.sleep(1)
                print(f"تم التفاعل مع الفيديو: {video_url}")
            except Exception as e:
                print(f"خطأ: {str(e)}")

if __name__ == "__main__":
    bot = TikTokBot()
    video_url = input("أدخل رابط فيديو TikTok: ")
    bot.engage(video_url)
