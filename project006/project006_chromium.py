from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import json


def main(output_filename):
    # URL strony WP
    url = 'https://www.wp.pl/'

    options = Options()
    # bez tego arguemntu nie działa - ładują się biała karta
    options.add_argument("--remote-debugging-port=9222") 
    # options.headless = True  # Uruchomienie w trybie headless (bez okna)
    options.binary_location = ""

    service = Service('./chromedriver/chromedriver')

    # # Uruchomienie przeglądarki
    driver = webdriver.Chrome(service=service, options=options)

    # # Wejście na stronę
    driver.get(url)
    print(url)

    try:
        accept_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'AKCEPTUJĘ I PRZECHODZĘ DO SERWISU')]")))
        accept_button.click()
    except Exception as e:
        print("Brak przycisku akceptacji lub inny błąd:", e)

    try:
        skip_ad_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "a[title='Przejdź teraz ›']")))
        skip_ad_button.click()
    except Exception as e:
        print("Brak okna z reklamą lub błąd:", e)

    try:
        menu_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@for="menu-toggle-button"]')))
        menu_button.click()
    except:
        print('error')


    # # Poczekaj, aż element menu 'TECHNOLOGIA' będzie widoczny i kliknij
    tech_menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Technologia']")))
    tech_menu.click()

    time.sleep(3)

    # Scrollujemy stronę w dół, aby załadować więcej artykułów
    for _ in range(10):  # Przewiniemy stronę 10 razy
        driver.execute_script("window.scrollBy(0, 500);")
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)

    articles = driver.find_elements(By.CSS_SELECTOR, "div.PFak1.PFtv")

    article_titles = []
    for article in articles:
        try:
            article_titles.append(article.find_elements("xpath", "./*")[0].find_elements("xpath", "./*")[0].get_attribute("title"))
        except Exception as e:
            print(e)

    # # Zapisz dane do pliku JSON
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(article_titles, f, ensure_ascii=False, indent=4)


    # Po zakończeniu zamykamy przeglądarkę
    driver.close()



if __name__ == '__main__':
    
    output_filename = sys.argv[1]

    main(output_filename = output_filename)