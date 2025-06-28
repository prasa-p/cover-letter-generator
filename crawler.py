from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def crawl(url):
    print("crawl is running")

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    title = soup.find_all("title")

    find_body = soup.find_all(class_="show-more-less-html__markup")

    item = find_body[0]
    body = item.get_text(separator=' ')
    return body
