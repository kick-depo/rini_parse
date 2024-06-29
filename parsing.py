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

def extract_original_price(soup):
    tds = soup.find_all('td')

    target_text = "ОРИГИНАЛЬНЫЙ"
    price = None

    for td in tds:
        if td.find(string=re.compile(target_text)):
            price_div = td.find('div', class_='price')
            if price_div:
                price_text = price_div.get_text()
                price_only_numbers = re.sub(r'\D', '', price_text)
                price = int(price_only_numbers)
                break
    return price

def extarct_slug(cartridge_link):
    pattern = r'([^/]+)/$'
    match = re.search(pattern, cartridge_link)
    if match:
        return match.group(1)
    return None

def normalize_link(slug):
    return "http://rini.ru/" + slug + "/"

def extract_resource(soup):
    trs = soup.find_all('tr')

    target_td_text = "Ресурс, страниц"
    resource = None

    for tr in trs:
        tds = tr.find_all('td')
        # Проверяем, если первый <td> содержит нужный текст
        if tds and target_td_text in tds[0].get_text():
            # Получаем текст из второго <td> и удаляем все нецифровые символы
            pages_text = tds[1].get_text()
            pages_only_numbers = re.sub(r'\D', '', pages_text)
            resource = int(pages_only_numbers)
            break
    return resource

def extarct_slug(cartridge_link):
    pattern = r'([^/]+)/$'
    match = re.search(pattern, cartridge_link)
    if match:
        return match.group(1)
    return None

def extract_printers(soup):
    links = []
    item = soup.find('div', class_="grid_5 omega products-by-product")
    item_links_printer = item.find('p', class_="links")
    raw_links = item_links_printer.find_all('a')
    for i in raw_links:
        links.append(i.get_text(strip=True).replace('\xa0', ' '))
    return links

def extract_analogs(soup):
    test = []
    analog_data = []
    grid_5_divs = soup.find_all("div", class_="grid_5 omega")
    
    for grid_5_div in grid_5_divs:
        if not grid_5_div.find("div", class_="analog-title"):
            continue
        analog_titles = grid_5_div.find_all("div", class_="analog-title")
        analog_tables = grid_5_div.find_all("table", class_="analog-table")
        

        for title, table in zip(analog_titles, analog_tables):
            b_tag = title.find("b")
            cartridge_name = b_tag.text.replace('\xa0', ' ') if b_tag else "-"
            cartridge_link = title.find('a').get("href")
            analog_slug = extarct_slug(cartridge_link)
            
            rows = table.find_all("tr")[2:]
            
            for row in rows:
                cells = row.find_all("td")
                color = "#000000"
                resource = cells[2].text if len(cells) > 2 else "-"
                compatible_price_1 = cells[3].text if len(cells) > 3 else "-"
                compatible_price_10 = cells[4].text if len(cells) > 4 else "-"
                original_price = cells[5].text if len(cells) > 5 else "-"
                
                analog_data.append((cartridge_name, analog_slug, color, resource, compatible_price_1, compatible_price_10, original_price))
                
    
    return analog_data


def get_data_from_page():
    for cartridge_link in get_url():
        response = requests.get(cartridge_link, headers=headers)
        # response = requests.get("http://rini.ru/cartridge/hp/cf259x/", headers=headers)
        if response.status_code != 200:
            print(f"Ошибка загрузки страницы {cartridge_link}. Код: {response.status_code}")
            continue
        soup = BeautifulSoup(response.text, "lxml")
        
        raw_title = soup.find('h1', class_="grid_6 omega").text
        title = raw_title[9:] # HP W1106A (106A) БЕЗ ЧИПА
        raw_price = soup.find("div", class_="price").text # 1700 руб.
        price = re.sub(r'\D', '', raw_price) # 1700
        raw_price_10 = soup.find("div", class_="c-gray small").text
        price_10 = extract_price(raw_price_10) # 1600
        price_original = extract_original_price(soup) # 7950
        resource = extract_resource(soup) # 1000
        color = "#000000"
        printers = extract_printers(soup) # массив со списком картриджей (призв. пока пропускаем)
        analogs = extract_analogs(soup) # массив кортежей с аналогами
        
        yield (title,
               price,
               price_10,
               price_original,
               resource,
               color,
               printers,
               analogs)

        
if __name__ == '__main__':
    count = 0
    for data in get_data_from_page():
        title, price, price_10, price_original, resource, color, printers, analogs = data
        print("Title:", title)
        print("Price:", price)
        print("Price for 10 units:", price_10)
        print("Original price:", price_original)
        print("Resource:", resource)
        print("Color:", color)
        print("Printers:", printers)
        print("Analogs:", analogs)
        print("-" * 20)
        if count >= 5:
            break
        count += 1