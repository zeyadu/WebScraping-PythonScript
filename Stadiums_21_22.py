import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#Open browser
#Example:
#path of chrome driver in order to utilize service
s = Service('C:/Users/.../chromedriver_win32/chromedriver')
driver = webdriver.Chrome(service=s)

url='https://www.premierleague.com/clubs'
driver.get(url)

# Accept on Cookies
time.sleep(5)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()
time.sleep(3)

i = 1

#Loop over all clubs and obtain stadium information
stadium_list = []
while i < 21:
    time.sleep(4)
    x = str(i)
    print(x)

    stadium_name = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[1]/div/ul/li[" + \
      x + "]/a/div[3]/div[2]/div").text
  #  print(stadium_name)
    
    club_link_xpath = "/html/body/main/div[2]/div/div/div[1]/div/ul/li[" + \
      x + "]/a/div[3]/div[3]/span"      
    club_link = driver.find_element(By.XPATH,club_link_xpath)
    club_link.click()
    time.sleep(4)

    stadium_link_xpath = "/html/body/main/nav/ul/li[7]/a"
    stadium_link = driver.find_element(By.XPATH,stadium_link_xpath)
    stadium_link.click()
    time.sleep(2)

    info_link_xpath = "/html/body/main/div[3]/div[2]/div/ul/li[2]"
    info_link = driver.find_element(By.XPATH,info_link_xpath)
    info_link.click()    
    time.sleep(4)   

    capacity = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[1]").text
    capacity = capacity.lstrip("Capacity: ")
    capacity = capacity.lstrip("Tottenham Hotspur Stadium capacity: ")
  #  print(capacity)

    record_attendance = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[2]/strong").text
  #  print(record_attendance)
    if record_attendance == "Opened:" or record_attendance == "Built:":
        record_attendance = ""
        Opened = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[2]").text
        Opened = Opened.lstrip("Opened: ")
        Opened = Opened.lstrip("Built: ")                
        Pitch_size = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[3]").text
        Pitch_size = Pitch_size.lstrip("Pitch size: ")
        Stadium_address = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[4]").text
        Stadium_address = Stadium_address.lstrip("Stadium address: ")
        stad_dict = {
            "Name: ": stadium_name,
            "Capacity:": capacity,
            "Record PL attendance:":" ",
            "Built:": Opened,
            "Pitch size:": Pitch_size,
            "Stadium address:" : Stadium_address 
        }
        print(stadium_name, capacity, record_attendance, Opened, Pitch_size, Stadium_address)        
    else:
        record_attendance = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[2]").text
        record_attendance = record_attendance.lstrip("Record PL attendance: ")
        Built = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[3]").text
        Built = Built.lstrip("Built: ")        
        Pitch_size = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[4]").text
        Pitch_size = Pitch_size.lstrip("Pitch size: ")
        Stadium_address = driver.find_element(By.XPATH,"/html/body/main/div[3]/div[3]/div[2]/p[5]").text
        Stadium_address = Stadium_address.lstrip("Stadium address: ")
        stad_dict = {
            "Name: ": stadium_name,
            "Capacity:": capacity,
            "Record PL attendance:": record_attendance,
            "Built:": Built,
            "Pitch size:": Pitch_size,
            "Stadium address:" : Stadium_address 
        }
        print(stadium_name, capacity, record_attendance, Built, Pitch_size, Stadium_address)

    stadium_list.append(stad_dict)
    time.sleep(2)

    driver.back()
    time.sleep(4)
    driver.back()
    i = i + 1

#Create a DataFrame and Export CSV
df = pd.DataFrame(stadium_list)
df.to_csv(r'Stadiums_21_22.csv',index=True)
