from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# إعداد المتصفح بدون واجهة (headless)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# ⌨️ إدخال البيانات
email_a = input("Email حساب A: ")
pass_a = input("كلمة مرور A: ")
email_b = input("Email حساب B: ")
pass_b = input("كلمة مرور B: ")
old_username = input("الاسم الحالي (المطلوب نقله): ")
temp_username = input("الاسم المؤقت لحساب A: ")

# ===== تسجيل الدخول إلى حساب A وتغيير الاسم =====
driver.get("https://www.tiktok.com/login/phone-or-email/email")
time.sleep(4)

driver.find_element(By.NAME, "email").send_keys(email_a)
driver.find_element(By.NAME, "password").send_keys(pass_a)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(6)

driver.get("https://www.tiktok.com/settings/profile")
time.sleep(5)

username_input = driver.find_element(By.NAME, "uniqueId")
username_input.clear()
username_input.send_keys(temp_username)
driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
print("[✓] غيّر الاسم في حساب A إلى المؤقت")

# ===== تسجيل الدخول إلى حساب B وتغيير الاسم إلى القديم =====
driver.delete_all_cookies()
driver.get("https://www.tiktok.com/login/phone-or-email/email")
time.sleep(4)

driver.find_element(By.NAME, "email").send_keys(email_b)
driver.find_element(By.NAME, "password").send_keys(pass_b)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(6)

driver.get("https://www.tiktok.com/settings/profile")
time.sleep(5)

username_input = driver.find_element(By.NAME, "uniqueId")
username_input.clear()
username_input.send_keys(old_username)
driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
print("[✓] تم نقل الاسم إلى حساب B بنجاح ✅")

driver.quit()
