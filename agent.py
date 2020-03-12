from selenium import webdriver
import json

def get_driver():
   return webdriver.Firefox(executable_path=r'geckodriver.exe')

def get_data(driver):
    driver.get("https://www.mdpi.com/search?q=&journal=BDCC&sort=pubdate&page_count=200")
    articles = []
    authors = driver.find_elements_by_class_name('authors')
    titles = driver.find_elements_by_class_name('title-link')
    links = driver.find_elements_by_xpath("//div[@class='color-grey-dark']/a")
    years = driver.find_elements_by_xpath("//div[@class='color-grey-dark']/b")
    article_types = driver.find_elements_by_class_name('articletype')

    for i in range(len(titles)):
        articles.append({
        "title": titles[i].text,
        "authors": authors[i].text[3:],
        "year": years[i].text,
        "url": links[i].text,
        "article type": article_types[i].text
    })

    return articles

def save_file(data):
    with open('data.json', 'w', encoding = 'utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    driver = get_driver()
    articles = get_data(driver)
    driver.close()
    save_file(articles)