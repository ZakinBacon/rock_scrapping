from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
# from dotenv import load_dotenv
import requests
import os
import csv


chrome_drive_path = r"C:\Users\Zach\Desktop\chromedriver_win32\chromedriver.exe"

final_rock_names = []
final_images = []
final_prices = []

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=Service(executable_path=chrome_drive_path, log_path="NUL"))
driver.get('https://jbauctions.hibid.com/catalog/466998/henry-and-ferne-brewer-agate-and-jasper-bulk-sale-pt-2')

time.sleep(5)
# Find the names of the auctions
rocks = driver.find_elements(By.CLASS_NAME, "lot-title")
print(len(rocks))

# Find the images
images = driver.find_elements(By.TAG_NAME, 'img')
images = images[1:-1]
print(len(images))


for rock in rocks:
    final_rock_names.append(rock.text)

for count, image in enumerate(images):
    src = image.get_attribute('src')
    final_images.append(src)

# time.sleep(2)
# rock_link = driver.find_element(By.CSS_SELECTOR, 'a[class="lot-number-lead lot-link lot-title-ellipsis lot-preview-link link mb-1 ng-star-inserted"]').click()
# time.sleep(2)
# rock_image_test = []
# rock_gallery = driver.find_element(By.CSS_SELECTOR, 'div[class="ngx-gallery-image ngx-gallery-active ngx-gallery-clickable ng-star-inserted"]')
# print(rock_gallery.get_attribute('style'))


with open('rocks.csv', 'w', newline='') as csvfile:
    rockwriter = csv.writer(csvfile)
    for count, data in enumerate(final_rock_names):
        input_data = [final_rock_names[count], final_images[count]]
        rockwriter.writerow(input_data)
    csvfile.close()

print(final_rock_names)
print(final_images)
