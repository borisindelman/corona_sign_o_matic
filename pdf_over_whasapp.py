import win32gui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

send_to = 'John Smith'
attach_name = "GyG Recibo_00741.pdf"

# Lets use Chrome as web browser
web_driver = webdriver.Chrome('ChromeDriver')

# Open WhatsApp Web
web_driver.get('http://web.whatsapp.com')
web_driver.implicitly_wait(100)   # seconds

# Find destinatary
new_chat = web_driver.find_element_by_id('input-chatlist-search')
new_chat.send_keys(send_to, Keys.ENTER)

# Press Attach button
button = web_driver.find_elements_by_xpath('//*[@id=\"main\"]/header/div[3]/div/div[2]/div/span')
button[0].click()

# Press Document button
inp_xpath = '//*[@id=\"main\"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button'
button = web_driver.find_elements_by_xpath(inp_xpath)
button[0].click()

# Loop until Open dialog is displayed (my Windows version is in Spanish)
hdlg = 0
while hdlg == 0:
    hdlg = win32gui.FindWindow(None, "Abrir")

time.sleep(1)   # second. This pause is needed

# Set filename and press Enter key
hwnd = win32gui.FindWindowEx(hdlg, 0, 'ComboBoxEx32', None)
hwnd = win32gui.FindWindowEx(hwnd, 0, 'ComboBox', None)
hwnd = win32gui.FindWindowEx(hwnd, 0, 'Edit', None)

filename = attach_path + attach_name
win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, filename)

# Press Save button
hwnd = win32gui.FindWindowEx(hdlg, 0, 'Button', '&Abrir')

win32gui.SendMessage(hwnd, win32con.BM_CLICK, None, None)