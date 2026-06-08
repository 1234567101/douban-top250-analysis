import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 请求头，伪装浏览器（必须加，否则爬不了）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 存储所有电影信息
movie_list = []

# 爬取10页，一共250条电影
for page in range(0, 10):
    url = f"https://movie.douban.com/top250?start={page*25}"
    print(f"正在爬取第 {page+1} 页：{url}")

    # 发送请求
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    # 提取每部电影信息
    items = soup.find_all("div", class_="item")
    for item in items:
        title = item.find("span", class_="title").text
        score = item.find("span", class_="rating_num").text
        info = item.find("div", class_="bd").p.text.strip()

        # 新增：提取电影类型 genres
        # info 里的格式类似：导演: XXX / 1994 / 剧情 犯罪
        # 我们用 / 分割，取最后一部分，再去掉空格
        genres = "未知"
        if info:
            parts = info.split("/")
            if len(parts) >= 3:
                genres = parts[-1].strip()

        movie_list.append({
            "电影名": title,
            "评分": score,
            "信息": info,
            "类型(genres)": genres
        })

    time.sleep(1)  # 延时，防止被封

# 保存到 CSV 文件
df = pd.DataFrame(movie_list)
df.to_csv("豆瓣电影Top250.csv", index=False, encoding="utf-8-sig")

print("爬取完成！已保存到 豆瓣电影Top250.csv")