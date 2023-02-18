#!/usr/bin/env python3
# -*-coding:utf-8-*-

# https://github.com/mozilla/geckodriver/releases
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service

# Khai báo thông tin đăng nhập
email = "vungoctruong8x@gmail.com"
password = "Tqvngoogle@89"

# Tạo đối tượng Service với đường dẫn đến trình điều khiển geckodriver
gecko_path = '/home/ngoctruong/SETUP/geckodriver'
service = Service(gecko_path)

# Khởi tạo trình duyệt Firefox với đối tượng Service
driver = webdriver.Firefox(service=service)

# # Khởi tạo trình điều khiển Firefox
# driver = webdriver.Firefox(executable_path='/home/ngoctruong/SETUP/geckodriver')

# Mở trang đăng nhập của OpenAI
driver.get("https://chat.openai.com/api/auth/session")

# Điền thông tin email và bấm nút đăng nhập
email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
email_input.send_keys(email)
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Điền thông tin password và bấm nút continues
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
password_input.send_keys(password)
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Đợi đến khi trang được tải hoàn tất và in ra tiêu đề trang
WebDriverWait(driver, 10).until(EC.title_contains("Dashboard"))
print(driver.title)

# Tắt trình duyệt
driver.quit()
