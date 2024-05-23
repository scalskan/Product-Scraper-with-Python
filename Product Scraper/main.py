import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Start the WebDriver
#If you want, you can use headless mode to make it run faster.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Create a list to collect product links
product_links = []

# Define the total number of pages
total_pages = 9  # Set the number of pages

# Collect product links by browsing each page
for page in range(1, total_pages + 1):
    url = f'YOURLINK?p={page}'  #Your link
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Scroll down the page to ensure all products are loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)  # Wait for the page to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Collect product links, excluding sponsored products
    products = driver.find_elements(By.CSS_SELECTOR, 'a._LM.JT3_zV')
    for product in products:
        if 'sponsored' not in product.get_attribute('class'):  # Exclude sponsored products
            link = product.get_attribute('href')
            product_links.append(link)

# Close the WebDriver
driver.quit()

# Write the links to an Excel file
df = pd.DataFrame(product_links, columns=['Product Link'])
df.to_excel('yourexcelfilename.xlsx', index=False) #your excel file name

print('Product links have been successfully saved to the Excel file.')
