from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Initialize the WebDriver (use the path to your WebDriver executable if needed)
driver = webdriver.Chrome()  # or webdriver.Firefox()

# Open Facebook login page
driver.get('https://www.facebook.com/')

# Log in to Facebook
email_element = driver.find_element_by_id('email')
password_element = driver.find_element_by_id('pass')
login_button = driver.find_element_by_name('login')

email_element.send_keys('YOUR_EMAIL')
password_element.send_keys('YOUR_PASSWORD')
login_button.click()

# Wait for login to complete
time.sleep(5)

# Open Messenger
driver.get('https://www.facebook.com/messages/')

# Wait for Messenger to load
time.sleep(5)

# Search for the recipient
search_box = driver.find_element_by_xpath('//input[@placeholder="Search Messenger"]')
search_box.send_keys('Recipient Name')
time.sleep(2)
search_box.send_keys(Keys.RETURN)

# Wait for chat to load
time.sleep(5)

# Type and send the message
message_box = driver.find_element_by_xpath('//div[@contenteditable="true"]')
message_box.send_keys('Hello, this is a test message!')
message_box.send_keys(Keys.RETURN)

# Wait for a moment
time.sleep(5)

# Close the browser
driver.quit()
