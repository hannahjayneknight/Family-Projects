from selenium import webdriver      
  
# For using sleep function because selenium  
# works only when the all the elemets of the  
# page is loaded. 
import time  
   
from selenium.webdriver.common.keys import Keys  
  
# Creating an instance webdriver 
browser = webdriver.Chrome('/Users/hannahjayneknight/Desktop/chromedriver') 
browser.get('https://www.twitter.com/login') 
  
username = browser.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]') 

# Enter User Name 
username.send_keys('KnightHannahJ')
username.send_keys(Keys.TAB)

# Reads password from a text file because 
# saving the password in a script is just silly. 
with open('twitter_password.txt', 'r') as myfile:   
    Password = myfile.read().replace('\n', '') 
  
enter_password = browser.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[2]/label/div/div[2]') 
enter_password.send_keys(Password)
username.send_keys(Keys.ENTER)


print("Login Sucessful") 
 
  
elem = browser.find_element_by_name("q") 
elem.click() 
elem.clear() 
  
elem.send_keys("Geeks for geeks ") 
  
# using keys to send special KEYS  
elem.send_keys(Keys.RETURN)  
  
print("Search Sucessfull") 
  
# closing the browser 
browser.close() 