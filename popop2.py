import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time

print('import successful')

# add your paths here
firefox_binary_path = r"D:\browsers\Mozilla Firefox\firefox.exe"
geckodriver_path = r"D:\projects\pythonsca\geckodriver.exe"

# add your website url and xpaths here
website_url = 'https://www.file-upload.org/users/Gdr5'
image_xpath = r'''//body/section[@class='page-content']/div[@class='container']/div[@class='row']/div[@class='col-sm-9']/div[@id='files_list']//img[@class='cat_img']'''
next_button_xpath = r'''//body/section[@class='page-content']/div[@class='container']/div[@class='row']/div[@class='col-sm-9']//div[@id='files_paging']//a[@class='next']'''

options = Options()
options.binary_location = firefox_binary_path
driver = webdriver.Firefox(options=options)

# value of this variable increments by one when next button is clicked, 
# added for ease in saving images names
pagecountnum = 1

# Navigate to the webpage
driver.get(website_url)
print('visited url successfully')

# Function to download images from the current page
def download_images():
    image_elements = driver.find_elements(By.XPATH, image_xpath)
    for index, img in enumerate(image_elements):
        image_url = img.get_attribute('src')
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f'image_{pagecountnum}_{index}.png', 'wb') as file:
                file.write(response.content)
                print('download successful')

# Start with the first page

print('first page successfully downloaded')
download_images()

# Loop to move to the next page and download images
while True:
    try:
        # Wait for the next button to be clickable
        print('Waiting for the next button to be clickable')
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        )
        # Click the next button
        print('clicking next button')
        next_button.click()

        print('clicked next button successfully')
        pagecountnum += 1
        print(pagecountnum)
        
        # Wait for the page to load
        print("sleeping for next page to load")
        time.sleep(10)
        print("sleeping complete")
        
        # Download images from the new page
        
        print('download function called')
        download_images()
    except:
        # If the next button is not found or not clickable, break the loop
        print("Reached the last page or encountered an error.")
        break

# Close the WebDriver

print('closing webdriver')
driver.quit()
