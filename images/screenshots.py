from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def click_cookie_button(driver):
    # Liste möglicher Selektoren für Cookie-Buttons
    selectors = [
        "button[id*='cookie']",
        "button[class*='cookie']",
        "a[id*='cookie']",
        "a[class*='cookie']",
        "button[id*='consent']",
        "button[class*='consent']",
        "#cookie-consent button",
        ".cookie-consent button",
        "#gdpr-consent button",
        ".gdpr-consent button"
    ]
    
    for selector in selectors:
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            button.click()
            print("Cookie-Button geklickt.")
            time.sleep(1)  # Kurze Pause nach dem Klicken
            return True
        except (TimeoutException, NoSuchElementException):
            continue
    
    print("Kein Cookie-Button gefunden oder konnte nicht geklickt werden.")
    return False

def take_screenshot(url, filename, width=1400):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={width},1080")
    chrome_options.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        click_cookie_button(driver)
        
        time.sleep(2)
        
        # Finde den relevanten Inhalt
        content = driver.find_element(By.TAG_NAME, 'main')
        if not content:
            content = driver.find_element(By.TAG_NAME, 'body')
        
        # Setze die Fenstergröße basierend auf dem Inhalt
        height = content.size['height']
        driver.set_window_size(width, height)
        
        # Scrolle zum Anfang und mache den Screenshot
        driver.execute_script("window.scrollTo(0, 0)")
        content.screenshot(f"{filename}.png")
        print(f"Screenshot von {url} wurde als {filename}.png gespeichert.")
    
    except Exception as e:
        print(f"Fehler beim Aufnehmen des Screenshots von {url}: {str(e)}")
    
    finally:
        driver.quit()

# Liste der URLs und entsprechender Dateinamen
urls_and_names = [
    ("https://www.anaconda.com/download/success", "anaconda-download"),
    ("https://support.apple.com/en-us/116943", "apple-silicon"),
    # Fügen Sie hier weitere URLs und Namen hinzu
]

# Durchlaufen der Liste und Erstellen von Screenshots
for url, name in urls_and_names:
    take_screenshot(url, name)