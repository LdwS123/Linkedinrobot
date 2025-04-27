
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"
SEARCH_URL_BASE = "https://www.linkedin.com/search/results/people/?keywords="

def get_credentials():
    username = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    return username, password

def random_delay(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(executable_path=os.path.expanduser('~/chromedriver/chromedriver-mac-x64/chromedriver'))
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        })
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

    driver.implicitly_wait(5)
    return driver

def login(driver, username, password):
    print("Attempting to log in...")
    try:
        driver.get(LINKEDIN_LOGIN_URL)
        random_delay(3, 5)

        try:
            email_signin_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in with email')]"))
            )
            print("Found 'Sign in with email' button, clicking it...")
            email_signin_button.click()
            random_delay(2, 4)
        except (NoSuchElementException, TimeoutException):
            print("No 'Sign in with email' button found, proceeding with regular login...")

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = driver.find_element(By.ID, "password")
        username_field.clear()
        password_field.clear()
        random_delay(1, 2)

        print("Entering credentials...")
        for char in username:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        random_delay(1, 2)
        
        for char in password:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        random_delay(1, 2)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        
        print("Clicking login button...")
        login_button.click()
        random_delay(5, 8)

        if "feed" in driver.current_url or "login" not in driver.current_url:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "global-nav-search"))
                )
                print("Login successful!")
                return True
            except TimeoutException:
                print("Login might have failed or landed on an unexpected page.")
                return False
        else:
            print("Login failed.")
            return False
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False

def search_and_connect(driver, companies, connect_limit_per_company=5, total_connect_limit=20):
    total_connection_attempts = 0

    for company in companies:
        if total_connection_attempts >= total_connect_limit:
            print(f"Limite totale de connexions atteinte ({total_connect_limit}). Arrêt.")
            break

        print(f"--- Recherche de personnes chez {company} ---")
        driver.get(f"https://www.linkedin.com/search/results/people/?keywords={company}")
        random_delay(4, 7)

        company_connections = 0
        page = 1
        while company_connections < connect_limit_per_company and total_connection_attempts < total_connect_limit:
            for scroll_attempt in range(8):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                random_delay(1, 2)

            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"Nombre total de boutons sur la page : {len(all_buttons)}")
            for b in all_buttons:
                try:
                    print("Texte bouton :", b.text)
                except:
                    pass

            try:
                connect_buttons = driver.find_elements(
                    By.XPATH, "//button[contains(@class, 'artdeco-button') and (contains(., 'Se connecter') or contains(@aria-label, 'Se connecter'))]"
                )
                print(f"{len(connect_buttons)} boutons 'Se connecter' trouvés sur la page {page}.")
                for btn in connect_buttons:
                    if company_connections >= connect_limit_per_company or total_connection_attempts >= total_connect_limit:
                        break
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                        random_delay(1, 2)
                        if btn.is_enabled() and btn.is_displayed():
                            btn.click()
                            print("Clic sur 'Se connecter'.")
                            random_delay(2, 4)

                            sent = False
                            try:
                                send_now = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Envoyer maintenant')]"))
                                )
                                send_now.click()
                                print("Invitation envoyée (Envoyer maintenant).")
                                sent = True
                            except:
                                try:
                                    send_btn = WebDriverWait(driver, 3).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Envoyer')]"))
                                    )
                                    send_btn.click()
                                    print("Invitation envoyée (Envoyer).")
                                    sent = True
                                except:
                                    print("Impossible de trouver le bouton d'envoi.")
                            if sent:
                                company_connections += 1
                                total_connection_attempts += 1
                                random_delay(5, 10)

                            try:
                                close_btn = driver.find_element(By.XPATH, "//button[@aria-label='Ignorer']")
                                close_btn.click()
                                random_delay(1, 2)
                            except:
                                pass
                    except Exception as e:
                        print(f"Erreur lors du clic sur 'Se connecter' : {e}")
                        continue
                try:
                    next_btn = driver.find_element(By.XPATH, "//button[@aria-label='Suivant']")
                    if next_btn.is_enabled():
                        print("Page suivante...")
                        driver.execute_script("arguments[0].click();", next_btn)
                        page += 1
                        random_delay(5, 8)
                        continue
                    else:
                        print("Plus de pages.")
                        break
                except:
                    print("Bouton 'Suivant' non trouvé ou non cliquable. Fin de la pagination.")
                    break
            except Exception as e:
                print(f"Erreur lors de la recherche : {e}")
                break
    print(f"--- Recherche et connexion terminées ---")
    print(f"Nombre total de demandes de connexion envoyées : {total_connection_attempts}")

if __name__ == "__main__":
    print("--- LinkedIn Automation Bot ---")
    print("Disclaimer: Use responsibly and at your own risk.")

    target_companies = [
        "Current",
        "Chime",
        "Varo Bank",
        "N26",
        "Revolut",
        "Monzo",
        "Brex",
        "Ramp",
        "Mercury",
        "Stripe",
        "Plaid",
    ]

    CONNECT_LIMIT_PER_COMPANY = 3
    TOTAL_CONNECT_LIMIT = 15

    linkedin_username, linkedin_password = get_credentials()

    if not linkedin_username or not linkedin_password:
        print("Username or password not provided. Exiting.")
        exit()

    driver = None
    try:
        print("Setting up browser...")
        driver = setup_driver()

        if driver:
            if login(driver, linkedin_username, linkedin_password):
                random_delay(3, 5)
                search_and_connect(
                    driver,
                    target_companies,
                    connect_limit_per_company=CONNECT_LIMIT_PER_COMPANY,
                    total_connect_limit=TOTAL_CONNECT_LIMIT
                )
            else:
                print("Exiting due to login failure.")
        else:
            print("WebDriver setup failed. Exiting.")

    except Exception as e:
        print(f"--- An unexpected error occurred ---")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()
        print("Bot finished.")
