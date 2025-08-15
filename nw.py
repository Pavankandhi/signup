import argparse
import random
import string
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, WebDriverException

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    return ''.join(random.choices(chars, k=length))

def wait_and_click(driver, wait, selectors):
    for method, selector in selectors:
        try:
            element = wait.until(EC.element_to_be_clickable((method, selector)))
            element.click()
            print(f"[+] Clicked: {selector}")
            return True
        except:
            continue
    print("[X] Could not click element.")
    return False

def wait_for_page_load(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        print("[+] Page loaded successfully")
    except TimeoutException:
        print("[!] Timeout waiting for page to load")

def wait_for_any_element(driver, wait, selectors):
    for _ in range(20):  
        for method, selector in selectors:
            try:
                element = driver.find_element(method, selector)
                if element.is_displayed():
                    return True
            except:
                pass
        time.sleep(1)
    return False

def wait_and_type(driver, wait, selectors, text):
    for method, selector in selectors:
        try:
            print(f"[*] Attempting to fill {selector} with {text}")
            element = wait.until(EC.presence_of_element_located((method, selector)))
            element.clear()
            element.send_keys(text)
            time.sleep(1)  
            if element.get_attribute('value') == text:
                print(f"[+] Successfully filled: {selector} with {text}")
                return True
            else:
                print(f"[!] Element filled, but value doesn't match. Current value: {element.get_attribute('value')}")
        except TimeoutException:
            print(f"[!] Timeout while waiting for element: {selector}")
        except ElementNotInteractableException:
            print(f"[!] Element not interactable: {selector}")
        except NoSuchElementException:
            print(f"[!] Element not found: {selector}")
        except WebDriverException as e:
            print(f"[!] WebDriver exception: {str(e)}")
        except Exception as e:
            print(f"[!] Unexpected error filling {selector}: {str(e)}")
    print(f"[X] Could not fill element with: {text}")
    return False

def main(email):
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  
    
    # Set Chrome binary location for Railway
    options.binary_location = "/usr/bin/google-chrome-stable"
    
    # Configure for Railway environment
    service = Service(executable_path="/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.Sai.com/signup")

    # [Rest of the code remains the same as your original file]
    # ... (all your existing steps)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sai Signup Automation")
    parser.add_argument("email", help="Email to use for signup")
    args = parser.parse_args()
    main(args.email)