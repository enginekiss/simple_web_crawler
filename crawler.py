import requests
from bs4 import BeautifulSoup
import csv
from dotenv import load_dotenv
import os

load_dotenv()

# 从环境变量获取TARGET_URL
TARGET_URL = os.getenv('TARGET_URL')
if not TARGET_URL:
    print('未设置TARGET_URL环境变量')
    exit(1)

print(f"当前使用的TARGET_URL: {TARGET_URL}")

# 星辰变各季URL示例，动态生成
xiuzhenchuan_urls = [
    f'{TARGET_URL}/xingchenbian/season1',  # 第1季
    f'{TARGET_URL}/xingchenbian/season2',  # 第2季
    f'{TARGET_URL}/xingchenbian/season3',  # 第3季
    f'{TARGET_URL}/xingchenbian/season4',  # 第4季
    f'{TARGET_URL}/xingchenbian/season5'   # 第5季
]

print(f"生成的星辰变各季URL: {xiuzhenchuan_urls}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def crawl_website(url):
    print(f"正在请求URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f'请求出错: {e}')
        return None


def extract_data(soup):
    if soup:
        # 示例：提取所有链接
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                links.append(href)
        return links
    return []


def save_data(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item])


if __name__ == '__main__':
    target_url = os.getenv('TARGET_URL')
    if target_url:
        soup = crawl_website(target_url)
        data = extract_data(soup)
        save_data(data, 'output.csv')

    # 爬取星辰变各季内容
    for url in xiuzhenchuan_urls:
        soup = crawl_website(url)
        data = extract_data(soup)
        save_data(data, 'output.csv')