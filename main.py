from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
# from dotenv import load_dotenv
import requests
import csv
import re

chrome_drive_path = r"C:\Users\Zach\Desktop\chromedriver_win32\chromedriver.exe"

final_rock_names = []
rock_hrefs = []
final_images = []
final_prices = []

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=Service(executable_path=chrome_drive_path, log_path="NUL"))
driver.get('https://jbauctions.hibid.com/catalog/466998/henry-and-ferne-brewer-agate-and-jasper-bulk-sale-pt-2')

time.sleep(3)
# Find the names of the auctions
rocks = driver.find_elements(By.CLASS_NAME, "lot-title")
print(len(rocks))

# Find the images
images = driver.find_elements(By.TAG_NAME, 'img')
images = images[1:-1]
print(len(images))

href_to_rocks = driver.find_elements(By.CSS_SELECTOR, 'a[class="lot-number-lead lot-link lot-title-ellipsis lot-preview-link link mb-1 ng-star-inserted"]')

for href in href_to_rocks:
    rock_hrefs.append(href.get_attribute('href'))

for rock in rocks:
    # print(rock.get_attribute('href'))
    final_rock_names.append(rock.text)


print(rock_hrefs)
# for count, image in enumerate(images):
#     src = image.get_attribute('src')
#     final_images.append(src)




# testfile.retrieve(URL, image_name)


# Could do it where I grab all of the links to the devices and then just open each link
##

time.sleep(2)
for count, href in enumerate(rock_hrefs):

    driver.get(href) # Gets the URL from the list
    try:
        # Checks if there is a newsletter button
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-secondary ng-star-inserted"]').click()
    except NoSuchElementException:
        print("There is no newsletter button")
        pass
    # Parces the URL to get the ID of the item
    current_url = driver.current_url
    current_id = current_url.split('/')[4]
    rock_image_test = []
    click_rock_image = driver.find_element(By.XPATH,
                                           f'//*[@id="lot-details-{current_id}"]/div[1]/div[1]/app-lot-image-gallery/div/div[1]/ngx-gallery/div/ngx-gallery-image/div/div[1]/div').click()

    time.sleep(2)
    # Goes through the Gallery. Max 10 pictures
    for gallery_images in range(0, 10):
        rock_image_test.append(driver.find_element(By.CSS_SELECTOR,
                                                   'img[class="ngx-gallery-preview-img ngx-gallery-center animation ng-star-inserted ngx-gallery-active"]').get_attribute(
            'src'))
        time.sleep(1)
        click_next = driver.find_element(By.XPATH,
                                         f'//*[@id="lot-details-{current_id}"]/div[1]/div[1]/app-lot-image-gallery/div/div[1]/ngx-gallery/div/ngx-gallery-preview/ngx-gallery-arrows/div[2]/div/i').click()
        time.sleep(2)
        # print(rock_image_test)
    final_images.append([*set(rock_image_test)])
    time.sleep(1)
    print(f"This is the current images{final_images[count]}\nThis is the current name{final_rock_names[count]}")

    with open('rocks.csv', 'a', newline='') as csvfile:
        rockwriter = csv.writer(csvfile)
        input_data = [final_rock_names[count]]
        for image_count, images in enumerate(final_images[count]):
            input_data.append(images)
            data = requests.get(images).content
            cleaned_up_image_name = ''.join(re.findall(r'[a-zA-Z-\d]+', final_rock_names[count]))
            f = open(f"./photos/{cleaned_up_image_name}_{image_count}.jpg", "wb")
            f.write(data)
            f.close()
        rockwriter.writerow(input_data)
        csvfile.close()


URL = "https://cdn.hibid.com/img.axd?id=7821513987&wid=&rwl=false&p=&ext=&w=0&h=0&t=&lp=&c=true&wt=false&sz=MAX&checksum=w5tkAuyzMuAGCdhRQj2J1Vbxy1iMFA6G"
data = requests.get(URL).content



print(final_rock_names)
print(final_images)
