from selenium import webdriver
import json
import time
import os
import sys

def get_driver():
   return webdriver.Firefox(executable_path=r'geckodriver.exe')

def get_data(driver):
    articles = []
    authors = driver.find_elements_by_class_name('authors')
    titles = driver.find_elements_by_class_name('title-link')
    links = driver.find_elements_by_class_name('title-link')
    years = driver.find_elements_by_xpath("//div[@class='color-grey-dark']/b")
    article_types = driver.find_elements_by_class_name('articletype')

    driver = get_driver()
    for i in range(len(links)):
        url = links[i].get_attribute("href")
        driver.get(url)
        abstracts = driver.find_elements_by_class_name('art-abstract')
        keywords = driver.find_elements_by_class_name('art-keywords')
        pubhistory = driver.find_elements_by_class_name('pubhistory')
        a_links = driver.find_elements_by_xpath("//div[@class='art-authors']/a")
        affiliations = driver.find_elements_by_class_name('art-affiliations')

        articles.append({
        "title": titles[i].text,
        "authors": authors[i].text[3:],
        "affiliations": check(affiliations),
        "year": years[i].text,
        "url": url,
        "article type": article_types[i].text,
        "abstract": check(abstracts),
        "keywords": check(keywords),
        "publication history": check(pubhistory)
        })
        save_file(articles[i], 'Article'+str(i+1))

    return articles

def check(data):
    try:
        data = data[0].text
    except:
        data = "No information"
    return data

def save_file(data, file_name):
    os.chdir(r"C:\Users\polina.st\PycharmProjects\lab\articles")
    path = sys.path[0] + '/' + 'articles' + '/' + file_name + '.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def site_login(driver):
    driver.get("https://login.mdpi.com/login")
    driver.find_element_by_id("username").send_keys("stepanopolina@yandex.ru")
    driver.find_element_by_id("password").send_keys("Password1!")
    driver.find_element_by_class_name("button--login").click();

if __name__ == '__main__':
    driver = get_driver()
    driver.get("https://www.mdpi.com/search?q=&journal=BDCC&sort=pubdate&page_count=200")
    time.sleep(10)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    articles = get_data(driver)
    driver.close()
