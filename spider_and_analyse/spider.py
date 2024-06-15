import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 创建Session对象
session = requests.Session()

# 设置目标URL
url = "https://www.nature.com/search?q=electromagnetic+field&journal="

# 发起HTTP请求
response = session.get(url, timeout=10)
response.raise_for_status()  # 检查请求是否成功

# 解析HTML内容
soup = BeautifulSoup(response.content, "html.parser")

# 查找所有文章的容器
articles = soup.find_all("article")

# 创建一个列表来存储所有文章的数据
data = []

# 遍历每篇文章并提取标题、链接和年份
for article in articles:
    title_tag = article.find("h3", class_="c-card__title")
    link_tag = article.find("a", class_="c-card__link")
    date_tag = article.find("time")
    
    if title_tag and link_tag and date_tag:
        title = title_tag.get_text(strip=True)
        link = link_tag['href']
        year = date_tag['datetime'][:4]  # 提取年份
        
        # 构造文章的详细页面URL
        article_url = f"https://www.nature.com{link}"
        
        try:
            # 发起请求获取文章详细页面
            article_response = session.get(article_url, timeout=10)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            
            # 查找并提取摘要
            abstract_tag = article_soup.find("div", class_="c-article-section__content")
            
            if abstract_tag:
                abstract = abstract_tag.get_text(strip=True)
            else:
                abstract = "Abstract not found."
            
            # 将文章数据添加到列表中
            data.append({
                "Title": title,
                "URL": article_url,
                "Abstract": abstract,
                "Year": year
            })
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve article: {article_url}")
            print(e)

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 获取当前工作目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 将CSV文件保存到当前工作目录
csv_file = os.path.join(current_directory, "nature_articles.csv")
df.to_csv(csv_file, index=False)

print(f"Data saved to {csv_file}")
