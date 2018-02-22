import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict


def extract_data(urls, teams, driver):
    result = defaultdict(dict)

    for url in urls:
        print('Loading website {} ...'.format(url))
        t0 = time.time()
        driver.get(url)
        print('Loaded [{:.1f} s]'.format(time.time() - t0))

        for close_btn in ['//*[contains(@class, "cookie-notice__close-icon")]',
                          '//*[text() = "Ok, I got it."]',
                          '//*[text() = "Ok, I get it"]',
                          '(//*[contains(@class, "popupBtn linkable")])[1]',
                          "//*[contains(@class, 'outright-item-grid-list__show-more')]"]:
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, close_btn))).click()
            except:
                pass

        for t in teams:
            i = 0
            found = False
            while not found:
                i += 1
                xpath = '(//*[contains(text(), "{}")]'.format(t) + '/..' * i + ')'

                for j, elem in enumerate(WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))):
                    if elem.get_attribute('tagName') in ['BODY', 'SCRIPT', 'HTML']:
                        continue

                    xpath2 = '{}[{}]//*[boolean(number(substring-after(text(), "/")) and number(substring-before(text(), "/")))]'.format(xpath, j + 1)
                    try:
                        elem2 = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, xpath2)))
                    except:
                        continue

                    if len(elem2) > 1:
                        continue

                    result[url][t] = elem2[0].text
                    found = True
                    break

    return result