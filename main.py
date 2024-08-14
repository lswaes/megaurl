from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import cloudscraper
import time

def bypass_ads(url):
    # Setup Chrome options
    chrome_options = uc.ChromeOptions()
    # chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)

    # chrome_options.add_argument("--headless")  # Run in headless mode (optional)

    # Setup Chrome WebDriver
    driver = uc.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # driver = webdriver.Chrome(options=chrome_options)

    # Create a scraper object
    scraper = cloudscraper.create_scraper()

    response = scraper.get(url)
    cookies = response.cookies
    headers = response.headers

    wait = WebDriverWait(driver, 3)
# get.megaurl.in
# Performance & security by Cloudflare
    try:
        # Open the URL
        driver.get(url)
        # Add cookies to Selenium
        for cookie in cookies:
            driver.add_cookie({'name': cookie.name, 'value': cookie.value})
        
        driver.refresh()
        # Handle multiple layers of ads, pop-ups, and new tabs/windows
        original_window = driver.current_window_handle
        
        while True:
            try:
                # Check for pop-ups that open new tabs or windows
                for handle in driver.window_handles:
                    if handle != original_window:
                        driver.switch_to.window(handle)
                        driver.close()
                        driver.switch_to.window(original_window)

                time.sleep(16)

                # Example: Wait and click the "Skip Ad" button if it exists
                try:
                    cont_button = wait.until(EC.element_to_be_clickable((By.ID, "monetiza")))
                    if cont_button.is_displayed():
                        cont_button.click()
                        print("Continue button clicked.")
                except Exception as e:
                    print("Skip Continue button not found or not clickable. Bypassing...")
                try:
                    unlock_button = wait.until(EC.element_to_be_clickable((By.ID, "monetiza-snp")))
                    if unlock_button.is_displayed():
                        unlock_button.click()
                        print("Unlock button clicked.")
                except Exception as e:
                    print("Skip Unlock button not found or not clickable. Bypassing...")

                # If you have to deal with pop-ups on the same page, close them
                try:
                    close_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Close') or contains(text(),'No Thanks')]")
                    if close_buttons.is_displayed():
                        for btn in close_buttons:
                            btn.click()
                        print("Popup Closed button clicked.")
                except Exception as e:
                    print("Closed button not found or not clickable. Bypassing...")

                try:
                    getlink_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btn6' and @class='yu-btn yu-blue']")))
                    if getlink_button.is_displayed():
                        getlink_button.click()
                        print("GetLink button clicked.")
                except Exception as e:
                    print("GetLink button not found or not clickable. Bypassing...")

                # Wait for any redirection or more ads
                time.sleep(3)

            except Exception as e:
                # If no more skip buttons, pop-ups, or new windows are found, break the loop
                break

        # After handling all ads, pop-ups, and new tabs/windows, get the final URL
        final_url = driver.current_url
        return final_url

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        driver.quit()
# Example usage
url = 'http://go.megaurl.in/NMT-worship-guitar'
final_url = bypass_ads(url)
print("Final URL:", final_url)

