import json
import csv

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pandas import DataFrame

url = "https://www.kufar.by/"

goods = "Fuji"

options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(executable_path="/ChromeDriver/chromedriver")

browser = Chrome(
    service=service,
    options=options,
)


def prepare_to_search(necessary_url: str) -> None:
    """
    Opens url and closes popup windows
    """
    browser.get(necessary_url)
    browser.maximize_window()
    browser.implicitly_wait(2)

    accept_cookies_button = browser.find_element(
        By.XPATH,
        """//*[@id="__next"]/div[3]/div/div[2]/button""",
    )
    accept_cookies_button.click()
    browser.implicitly_wait(2)


def search(goods_name: str) -> None:
    """
    Inputs necessary good to search field and launches search
    """
    input_field = browser.find_element(
        By.XPATH,
        """//*[@id="header"]/div[1]/div[2]/div/div[1]/div/div/input""",
    )
    input_field.clear()
    input_field.send_keys(goods_name)
    browser.implicitly_wait(2)

    search_in_title_only = browser.find_element(
        By.XPATH,
        """//*[@id="header"]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/label"""
    )
    search_in_title_only.click()
    browser.implicitly_wait(5)

    bicycles_category = browser.find_element(
        By.XPATH,
        """//*[@id="header"]/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/div/a[1]/span[1]"""
    )
    bicycles_category.click()
    browser.implicitly_wait(3)


def parser() -> list[list[str]]:
    """
    Finds results of searching and downloads name, price, link, location
    and publication date of goods to the list.
    """
    result = []
    for page in range(1, 3):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        bicycles = soup.findAll("a", class_="styles_wrapper__yaLfq")
        print(f"Start parsing the page number {page}...")
        for bicycle in bicycles:
            name = bicycle.find("div", class_="styles_content__BDDGV").find("h3").get_text()

            price = bicycle.find("div", class_="styles_content__BDDGV"). \
                find("div", class_="styles_top__HNf3a").get_text()

            link = bicycle.get("href")

            location = bicycle.find("div", class_="styles_content__BDDGV"). \
                find("div", class_="styles_secondary__NEYhw"). \
                find("p").get_text()

            publication_date = bicycle.find("div", class_="styles_content__BDDGV"). \
                find("div", class_="styles_secondary__NEYhw"). \
                find("span").get_text()

            result.append([name, price, link, location, publication_date])
        print(f"Finish parsing the page number {page}!!!\nTotal {len(result)} results")
        turn_the_page()
        browser.implicitly_wait(3)
    return result


def turn_the_page():
    next_page = browser.find_element(
        By.CSS_SELECTOR,
        """#main-content > div.styles_container__wYL0x.styles_container-children__VyrUd > div:nth-child(1) > div >
         div.styles_content__right__ddauo > div.styles_listings__pagination__XRjf5 > div.styles_links__wrapper__PSpN7 >
         div > a.styles_link__3MFs4.styles_arrow__r6dv_""",
    )
    next_page.click()
    browser.implicitly_wait(5)


def write_to_csv(data: list) -> None:
    """
    Takes list and writes data from it to file 'results.csv' in .csv format.
    """
    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for i in data:
            writer.writerow(i)


def write_to_json(data: list) -> None:
    """
    Takes list and writes data from it to file 'results.json' in .json format.
    """
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)


def write_to_excel(data: list) -> None:
    """
    Takes list and writes data from it to Excel file 'results.xlsx'.
    """
    headers = ["Name", "Price", "Link", "Location", "Date of publication"]
    data_frame = DataFrame(data, columns=headers)
    data_frame.index += 1
    data_frame.to_excel("results.xlsx")


if __name__ == '__main__':
    try:
        prepare_to_search(url)
        search(goods)
        results = parser()
        if results:
            write_to_csv(results)
            write_to_json(results)
            write_to_excel(results)
    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()
