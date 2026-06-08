import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from collections import Counter
import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from collections import Counter
import os

# -------------------------- 1. 读取数据与清洗 --------------------------
print("📊 正在读取并清洗数据...")
df = pd.read_csv("豆瓣电影Top250.csv", encoding="utf-8-sig")
print(f"✅ 原始数据量：{len(df)}")
print(f"列名：{df.columns.tolist()}")

# 基础清洗
df = df.drop_duplicates(subset=["电影名"], keep="first")
df = df.dropna(subset=["评分", "类型(genres)"])
df["评分"] = pd.to_numeric(df["评分"], errors="coerce")
df = df.dropna(subset=["评分"])
print(f"✅ 清洗后数据量：{len(df)}")

# 保存清洗后数据
clean_file = "../data/cleaned_豆瓣电影Top250.csv"
df.to_csv(clean_file, index=False, encoding="utf-8-sig")
print(f"💾 清洗后数据已保存为：{clean_file}\n")

# -------------------------- 2. 评分分布直方图 --------------------------
print("📈 正在生成评分分布直方图...")
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

plt.figure(figsize=(10, 6))
plt.hist(df["评分"], bins=12, color="#4CAF50", edgecolor="black", alpha=0.8)
plt.title("豆瓣电影Top250 评分分布直方图", fontsize=15, pad=15)
plt.xlabel("评分", fontsize=12)
plt.ylabel("电影数量", fontsize=12)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("评分分布.png", dpi=300, bbox_inches="tight")
plt.close()
print("✅ 评分分布.png 已保存\n")

# -------------------------- 3. 电影类型占比饼图 --------------------------
print("🥧 正在生成电影类型占比饼图...")
genres_all = []
for g in df["类型(genres)"]:
    genres_all.extend(str(g).split())

genre_count = Counter(genres_all)
genre_df = pd.DataFrame(genre_count.items(), columns=["类型", "数量"])
genre_df = genre_df.sort_values("数量", ascending=False)

# 取前8个类型，其余归为“其他”
top8 = genre_df.head(8)
others_num = genre_df.iloc[8:]["数量"].sum()
labels = list(top8["类型"]) + ["其他"]
sizes = list(top8["数量"]) + [others_num]

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
        colors=plt.cm.Paired.colors, textprops={"fontsize": 10})
plt.title("豆瓣电影Top250 类型分布", fontsize=15, pad=15)
plt.tight_layout()
plt.savefig("类型饼图.png", dpi=300)
plt.close()
print("✅ 类型饼图.png 已保存\n")

# -------------------------- 4. 纯电影词云（仅类型+电影名） --------------------------
print("☁️  正在生成纯电影词云...")
# 合并类型和电影名
text_parts = []
for g, title in zip(df["类型(genres)"], df["电影名"]):
    text_parts.append(str(g))
    text_parts.append(str(title))

all_text = " ".join(text_parts)

# 中文分词
words = jieba.cut(all_text, cut_all=False)
word_str = " ".join(words)

# 自定义停用词（过滤无意义词）
stopwords = {"的", "了", "是", "和", "在", "有", "一个", "也", "都", "就",
              "这", "那", "很", "还", "被", "没有", "电影", "故事", "影片",
              "片", "版", "系列", "第", "部", "之", "篇", "大", "小", "与",
              "上", "下", "中", " ", "/"}

# 生成词云
wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",
    background_color="white",
    width=1000,
    height=800,
    max_words=150,
    stopwords=stopwords,
    max_font_size=150,
    random_state=42
).generate(word_str)

wc.to_file("电影词云.png")
print("✅ 电影词云.png 已保存（只有类型+电影名）\n")

# -------------------------- 5. 结果汇总 --------------------------
print("🎉 全部完成！生成文件：")
print(f"- {clean_file}")
print("- 评分分布.png")
print("- 类型饼图.png")
print("- 电影词云.png")
print("\n💡 高频词Top20（可用于报告分析）：")
top20_words = Counter(word for word in words if word not in stopwords and len(word) > 1).most_common(20)
for word, count in top20_words:
    print(f"  {word}: {count}")