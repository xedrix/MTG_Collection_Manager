import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

face_to_face_link = "https://buylist.facetofacegames.com/"
four_oh_one_games_link = "http://www.401games.ca/buylists/mtg"
wizards_tower_link = "https://www.kanatacg.com/buylist"

card_list = [
    {
        "Name": "Aetherflux Reservoir",
        "Condition": "NM",
        "Edition": "Kaladesh",
        "Quantity": 1
    },
    {
        "Name": "Ajani Unyielding",
        "Condition": "PL",
        "Edition": "Aether Revolt",
        "Quantity": 1
    },
]

os.environ['PATH'] += r"C:/Users/Xedrix/PycharmProjects/Web Drivers"
driver = webdriver.Chrome()

# TODO finish filling in the buylist THEN login due to F2F bug
"""
face_to_face_username = input("What is the email address of your Face to Face Games account?")
face_to_face_password = input("What is the password for your Face to Face Games account?")

driver.get("https://buylist.facetofacegames.com/login.php")
face_email_input = driver.find_element(By.ID, "login_email")
face_email_input.send_keys(face_to_face_username)
face_password_input = driver.find_element(By.ID, "login_pass")
face_password_input.send_keys(face_to_face_password)
face_password_input.submit()
print("Face to Face Games Login success")
"""

driver.get(face_to_face_link)
driver.implicitly_wait(5)
text_box = driver.find_element(By.CLASS_NAME, "form-input")
text_box.send_keys(card_list[0]["Name"])
text_box.submit()
correct_card_element = driver.find_elements(By.CLASS_NAME, "card-set")



"""
WebDriverWait(driver, 30).until(
    EC.text_to_be_present_in_element(
        (By.CLASS_NAME, "form-input")  # element filtration
          # the expected text
    )
)
"""
