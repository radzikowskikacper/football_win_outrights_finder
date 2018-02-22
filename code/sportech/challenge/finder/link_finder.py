import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_target_link(base_urls, driver):
    ret = dict()

    for base_url in base_urls:
        driver.get(base_url)

        #close cookie notice boxes, time zone boxes, etc.
        for close_btn in ['//*[contains(@class, "cookie-notice__close-icon")]',
                          '//*[text() = "Ok, I got it."]',
                          '//*[text() = "Ok, I get it"]',
                          '(//*[contains(@class, "popupBtn linkable")])[1]']:
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, close_btn))).click()
            except:
                pass

        for terms in [['Football', 'Soccer'], ['Tournaments', 'Competitions'], ['World Cup 2018', 'FIFA World Cup 2018'],
                      ['Outright', 'Outrights', 'World Cup 2018 - Outright'], ['World Cup 2018 Winner']]:
            found = False

            for term in terms:
                try:
                    for link in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[text()[contains(., '{}')]]".format(term)))):
                        if link.text == term:
                            try:
                                link.click()
                                time.sleep(5)

                                found = True
                                break
                            except Exception as e:
                                print(e)
                    if found:
                        break
                except:
                    pass

        ret[base_url] = driver.current_url
        print(driver.current_url)
    return ret