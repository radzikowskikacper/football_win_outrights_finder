import sys

from sportech.challenge.finder import link_finder, google as google_finder
from sportech.challenge.extractor import selenium_extractor
from selenium import webdriver


if len(sys.argv) > 1:
    teams = sys.argv[1:]
else:
    teams = ['Germany', 'Spain']

source_websites = [
    #'https://sports.williamhill.com',
    #'https://paddypower.com',
    'https://m.skybet.com',
    # 'https://www.bet365.com/'
]

proxy = 'localhost:8081'
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", proxy.split(':')[0])
profile.set_preference("network.proxy.socks_port", int(proxy.split(':')[1]))
profile.set_preference("network.proxy.socks_version", 5)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile)
driver.maximize_window()

# locating target link with outrights using Google
# ret = {src: google_finder.search('{} world cup 2018 win outrights'.format(src))[0]}
# locating by simple searching over website
ret = link_finder.find_target_link(source_websites, driver)
print('Found outrights target links:\n' + '\n'.join(['{}: {}'.format(url, ret[url]) for url in ret]))

results = selenium_extractor.extract_data(ret.values(), teams, driver)
driver.quit()

for url in source_websites:
    print('Outrights from {}:'.format(url))
    print('\n'.join(['{}: {}'.format(team, results[ret[url]][team]) for team in teams]))