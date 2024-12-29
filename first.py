from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import time
import requests
import http.client
import json
from collections import Counter


USERNAME = 'mdimdadulislam_WFvqSw'
ACCESS_KEY = 'Bd3iNyjYCsfyAwhxZWc6'


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')




url = f'https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub'


driver = webdriver.Remote(
    command_executor=url,
    options=options,  
    keep_alive=True
)


#driver = webdriver.Chrome()  

try:
  
    driver.get("https://elpais.com/")
    
    
    time.sleep(2)  
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "didomi-notice"))  
    )

    accept_button = driver.find_element(By.ID,"didomi-notice-agree-button")
    if accept_button:
        accept_button.click()
        print("Cookie closed")

    time.sleep(3)  

    opinion_element = driver.find_element(By.XPATH, "//*[@id='csw']/div[1]/nav/div/a[2]")
    opinion_element.click()
    print("Opinion clicked")

    time.sleep(5)

    articles = driver.find_elements(By.XPATH, "//section/div/article")

    article_headings=[]
    article_paragraphs=[]


    for index, article in enumerate(articles, start=0):

        if index<5:

            article_headings.append(article.find_element(By.TAG_NAME,"h2").text)
            article_paragraphs.append(article.find_element(By.TAG_NAME,"p").text)

            try:

                    image_ele = article.find_element(By.XPATH,".//figure/a/img")
                    if image_ele:
                        img_url= image_ele.get_attribute('src')
                        image_binary_data = requests.get(img_url).content

                        with open(f'article_{index}_image.jpg', 'wb') as file:
                            file.write(image_binary_data)
                            print(f"Image for article {index} downloaded")
            except NoSuchElementException:
                print(f"No image found for article {index}")

    for x in range(5):
        print(f"Article {x} heading: ",article_headings[x])
        print(f"Article {x} Para: ",article_paragraphs[x])
        print("\n")

    time.sleep(2);               






    translated_headers=[]

    conn = http.client.HTTPSConnection("rapid-translate-multi-traduction.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "3753957c06mshe07734d52d17265p16eacejsn22f3b4bf5121",
        'x-rapidapi-host': "rapid-translate-multi-traduction.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    for header in article_headings:

        payload = {"from":"es","to":"en","q":header}

        conn.request("POST", "/t", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()

        translated_headers.append(data.decode("utf-8").replace("[\"","").replace("\"]",""))

        print(data.decode("utf-8").replace("[\"","").replace("\"]",""))

    print(translated_headers)

    all_words = " ".join(translated_headers).split()
    word_counts = Counter(all_words)
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    print("\nRepeated Words in Translated Headers:")
    for word, count in repeated_words.items():
       print(f"{word}: {count}")


finally:
   
    driver.quit()
