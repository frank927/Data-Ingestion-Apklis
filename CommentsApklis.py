from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from ApklisSQLITE import *
import re

commentslist=[]
extra=[]
filtro=[]

path='C:\webdriver\chromedriver.exe'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url='https://apklis.cu/applications'

driver.get(url)

driver.maximize_window()


def getComments():
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    comments = soup.find_all('div',{'class':'review-comment ng-trigger ng-trigger-collapseAnimation'})

    for data in comments:
        
        commentslist.append(data.get_text())
    
    for i in commentslist:
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        filtro.append(emoji_pattern.sub(r'', i))
    
    name= soup.find('h5',{'class':'app-name'}).text  
    cursor.execute("INSERT OR REPLACE INTO Comments (AppName, Comments, Num, Score, LastUpdate, Version) VALUES (?, ?, ?, ?, ?, ?)", (name,str(filtro), str(len(filtro)),str(extra[2]),str(extra[1]),str(extra[0])))
    connection.commit()
    del name  
    commentslist.clear()
    extra.clear()
    filtro.clear()
    
def getExtra():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    commets = soup.find_all('div', {'class':'ui-g-12 ui-md-lg-8 ui-lg-8 ui-xl-9'})
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//p[@class='version']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//p[@class='updated']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//h1")))
    
    for i in commets:
        version=i.find('p', {'class':'version'}).text

        last=i.find('p', {'class':'updated'}).text

        score=i.find('h1').text

        v=version.find(':')
        ve=version[v+1:len(version)]
        l=last.find(':')
        la=last[l+1:len(last)]
 
        extra.append(ve)
        extra.append(la)
        extra.append(score)
    
def getData():
 for i in range(10000):
   sleep(2)  
   page=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
   page.send_keys(Keys.END)
   sleep(2)
   page=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
   page.send_keys(Keys.END)
   getExtra()
   sleep(1)
   WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,"//div[@class='all']")))
   if(driver.find_element(By.XPATH,"//div[@class='all']").is_displayed()==True):
       sleep(1)
       WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='all']"))).click()
       sleep(2)
   elif(i==0):
       getComments()
       sleep(2)
       break
   else:
       getComments()
       sleep(2)
       driver.back()
       sleep(2)
       break 

apps=[]
rating=[]
soup = BeautifulSoup(driver.page_source, 'html.parser')

apks = soup.find_all('div', {'class':'ui-xs-3 img-card ng-star-inserted'})
points=soup.find_all('div', {'class':'rating-box'})

for link in apks:
      src=link.find('img')['src']
      apps.append(src)

for r in points:
      num=r.text
      rating.append(float(num))

for app,point in zip(apps, rating):
    if(point > 0.0):
        element= WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,f"//img[starts-with(@src,'{app}')]")))
        webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
        
        getData()
        driver.back()
        
      
 
driver.quit() 