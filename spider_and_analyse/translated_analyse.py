import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用Agg后端
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
from wordcloud import WordCloud
import re

# 读取翻译完成的CSV文件
csv_file = "nature_articles_analysis_translated.csv"
df = pd.read_csv(csv_file)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 扩展停用词列表
stopwords = set([
    "在", "这里", "文章", "下载", "参考资料", "我们", "表明", "其中", "因此", "然而", "这个", 
    "为了", "关于", "基于", "通过", "使用", "对于", "研究", "结果", "影响", "本文", "分析", 
    "实验", "数据", "方法", "系统", "和", "的", "是", "了", "与", "对", "中", "以", "也", 
    "与", "但", "对", "将", "为", "可", "该", "与", "等", "有", "并", "进行", "采用", "通过",
    "可以", "使", "该", "此", "不同", "相关", "某些", "进行", "具体来说", "重要", "影响", "显著",
    "显著地", "显著性", "表明", "为了", "这些", "能够", "显示", "较高", "通过", "被", "一种",
    "在这里","文章","下载","参考资料","我们","表明","其中","因此","然而","这个","为了","关于",
    "我们表明","众所周知","这里","这些","这种","这样","这个","这些","这样","这种","这里","这里",
    "文章谷歌学术","学术谷歌文章","下载参考资料","有趣的是","为了解决这个问题","迄今为止","年","倍",
    "在本研究中","在本文中","分钟","这是","下载参考文献","污染至关重要",
])

# 1. 统计每年发布的文章数量
articles_per_year = df['Year'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
sns.barplot(x=articles_per_year.index, y=articles_per_year.values, palette="viridis")
plt.title('每年发布的文章数量', fontsize=14)
plt.xlabel('年份', fontsize=12)
plt.ylabel('文章数量', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.savefig('articles_per_year_zh.png')  # 保存图表为文件
plt.close()

# 2. 查看文章标题中最常出现的词语
all_titles = ' '.join(df['Title_Chinese'].tolist())
words = all_titles.split()
word_freq = Counter(words)
common_words = word_freq.most_common(20)

plt.figure(figsize=(14, 8))
sns.barplot(x=[word for word, freq in common_words], y=[freq for word, freq in common_words], palette="viridis")
plt.title('文章标题中最常出现的词语', fontsize=14)
plt.xlabel('词语', fontsize=12)
plt.ylabel('频率', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.savefig('common_words_in_titles_zh.png')  # 保存图表为文件
plt.close()

# 3. 按年份查看文章摘要中的关键词频率
def extract_chinese(text):
    chinese_text = re.sub(r'[^\u4e00-\u9fff]+', ' ', text)  # 仅保留中文字符
    return chinese_text

all_abstracts = ' '.join(df['Abstract_Chinese'].apply(extract_chinese).tolist())
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white', stopwords=stopwords).generate(all_abstracts)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('文章摘要的词云图', fontsize=14)
plt.axis('off')
plt.savefig('word_cloud_of_abstracts_zh_filtered.png')  # 保存图表为文件
plt.close()

print("All charts have been saved as image files.")
