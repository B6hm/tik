import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 أهلاً بك! لنبدأ نقل اسم مستخدم TikTok.\nأرسل إيميل الحساب A:")
    user_data[message.chat.id] = {}

@bot.message_handler(func=lambda m: True)
def collect_info(message):
    uid = message.chat.id
    state = user_data.get(uid, {})

    if "email_a" not in state:
        state["email_a"] = message.text
        bot.send_message(uid, "🔐 أرسل كلمة مرور حساب A:")
    elif "pass_a" not in state:
        state["pass_a"] = message.text
        bot.send_message(uid, "📩 أرسل إيميل الحساب B:")
    elif "email_b" not in state:
        state["email_b"] = message.text
        bot.send_message(uid, "🔐 أرسل كلمة مرور حساب B:")
    elif "pass_b" not in state:
        state["pass_b"] = message.text
        bot.send_message(uid, "📛 أرسل اسم المستخدم الذي تريد نقله:")
    elif "target_username" not in state:
        state["target_username"] = message.text
        bot.send_message(uid, "🔄 أرسل الاسم المؤقت لحساب A:")
    elif "temp_username" not in state:
        state["temp_username"] = message.text
        bot.send_message(uid, "🚀 جاري تنفيذ النقل، انتظر لحظات...")

        try:
            do_username_transfer(state)
            bot.send_message(uid, "✅ تم نقل الاسم بنجاح!")
        except Exception as e:
            bot.send_message(uid, f"❌ حدث خطأ أثناء النقل: {e}")
        finally:
            user_data.pop(uid, None)

def do_username_transfer(data):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # تسجيل دخول حساب A
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(5)
    driver.find_element(By.NAME, "email").send_keys(data["email_a"])
    driver.find_element(By.NAME, "password").send_keys(data["pass_a"])
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(6)

    # تغيير الاسم في A إلى مؤقت
    driver.get("https://www.tiktok.com/settings/profile")
    time.sleep(5)
    username_input = driver.find_element(By.NAME, "uniqueId")
    username_input.clear()
    username_input.send_keys(data["temp_username"])
    driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
    time.sleep(4)

    # تسجيل دخول حساب B
    driver.delete_all_cookies()
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(5)
    driver.find_element(By.NAME, "email").send_keys(data["email_b"])
    driver.find_element(By.NAME, "password").send_keys(data["pass_b"])
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(6)

    # تغيير الاسم في B إلى الاسم المستهدف
    driver.get("https://www.tiktok.com/settings/profile")
    time.sleep(5)
    username_input = driver.find_element(By.NAME, "uniqueId")
    username_input.clear()
    username_input.send_keys(data["target_username"])
    driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
    time.sleep(3)

    driver.quit()

bot.polling()
