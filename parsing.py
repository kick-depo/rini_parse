import requests
from bs4 import BeautifulSoup
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36"}

def get_url():
    url = "http://rini.ru/cartridge/all/"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка загрузки. Код: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.select("tr[class='']")
    
    if not data:
        print("Подходящие данные для переменной data не обнаружены")
        return

    for i in data:
        cartridge_title = i.find("div", class_="title")
        if cartridge_title:
            link_tag = cartridge_title.find("a")
            if link_tag and link_tag.get("href"):
                cartridge_link = "http://rini.ru" + link_tag.get("href")
                yield cartridge_link
            else:
                print("Ссылка не найдена")
                continue
        else:
            print("div с тайтлом не найден")
            continue

def extract_price(text):
    match = re.search(r'(\d+)\s*руб\.', text)
    if match:
        return match.group(1)
    return None

def extract_cartridges_data(soup):
    cartridges_data = []
    grid_5_divs = soup.find_all("div", class_="grid_5 omega")
    for grid_5_div in grid_5_divs:
        if not grid_5_div.find("div", class_="analog-title"):
            continue

        analog_titles = grid_5_div.find_all("div", class_="analog-title")
        analog_tables = grid_5_div.find_all("table", class_="analog-table")

        for title, table in zip(analog_titles, analog_tables):
            cartridge_name = title.find("b").text if title.find("b") else "-"
            rows = table.find_all("tr")[2:]
            for row in rows:
                cells = row.find_all("td")
                color = "#000000"
                resource = cells[2].text if len(cells) > 2 else "-"
                compatible_price_1 = cells[3].text if len(cells) > 3 else "-"
                compatible_price_10 = cells[4].text if len(cells) > 4 else "-"
                original_price = cells[5].text if len(cells) > 5 else "-"

                cartridges_data.append((cartridge_name, color, resource, compatible_price_1, compatible_price_10, original_price))

    return cartridges_data

def extarct_slug(cartridge_link):
    pattern = r'([^/]+)/$'
    match = re.search(pattern, cartridge_link)
    if match:
        return match.group(1)
    return None

def normalize_link(slug):
    return "http://rini.ru/" + slug + "/"

def array():
    for cartridge_link in get_url():
        response = requests.get(cartridge_link, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка загрузки страницы {cartridge_link}. Код: {response.status_code}")
            continue
        soup = BeautifulSoup(response.text, "lxml")
        cartridges_data = extract_cartridges_data(soup)
        slug = extarct_slug(cartridge_link)
        formated_link = normalize_link(slug)

        for cartridge_data in cartridges_data:
            name, color, resource, compatible_price_1, compatible_price_10, original_price = cartridge_data
            
            printers = []
            printer_links = soup.find("p", class_="links")
            if printer_links:
                printers.append(printer_links.find("b").text)
                for a_tag in printer_links.find_all("a"):
                    printers.append(a_tag.text)

            yield (name if name else '',
                   compatible_price_1 if compatible_price_1 else '',
                   compatible_price_10 if compatible_price_10 else '',
                   resource if resource else '',
                   color,
                   slug,
                   formated_link,
                   cartridge_link,
                   printers,
                   cartridge_data)

def main():
    cartridge_data_generator = array()
    for i in range(0, 20):
        first_result = next(cartridge_data_generator, None)
        if first_result:
            for item in first_result:
                print(item)
            print("\n")
            print("#" * 20)
            print("\n")
        else:
            print("Нет данных для вывода")

if __name__ == "__main__":
    main()