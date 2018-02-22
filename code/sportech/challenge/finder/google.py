import requests, re


def search(query):
    req = requests.get('https://www.google.com/search', params={'q': query})
    content = str(req.content)
    regexp = '<div class="g"><h3 class="r"><a href="/url\?q=' + '(.*?)' + '&amp;sa=U&amp;'
    return re.findall(regexp, content)