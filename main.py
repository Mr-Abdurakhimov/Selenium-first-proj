from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import json


def GetHtmlSource(url):
    path = "C:\Selenium\msedgedriver.exe"
    driver = webdriver.Edge(executable_path=path)
    count = 1
    try:
        driver.get(url=url)
        time.sleep(3)
        while True:
            time.sleep(2)
            print(f"Поликлиника №{count}")
            finder = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")
            if driver.find_elements(By.CLASS_NAME, "hasmore-text"):
                with open("index.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                    break
            else:
                count += 1
                chain = ActionChains(driver)
                chain.move_to_element(finder).perform()

    except:
        print("sth went wrong")
    finally:
        driver.quit()
        driver.close()


def GetInfo():
    with open("index.html", encoding="utf-8") as f:
        src = f.read()
    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all(class_="js-results-item")
    info_list = []
    for i in cards:
        try:
            title = i.find(class_="minicard-item__title").text.strip()
        except:
            title = "No title"
        try:
            link = i.find(class_="minicard-item__title").find("a").get("href")
        except:
            link = "No link"
        try:
            address = i.find(class_="minicard-item__address").find("span", class_="address").text.strip()
        except:
            address = "No address"
        info_list.append({"title": title, "link": link, "address": address})
    with open("info.json", "w", encoding="utf-8") as file:
        json.dump(info_list, file, ensure_ascii=False, indent=4)


def Main():
    url = "https://spb.zoon.ru/medical/type/detskaya_poliklinika/"
    # GetHtmlSource(url)
    GetInfo()


if __name__ == "__main__":
    Main()
