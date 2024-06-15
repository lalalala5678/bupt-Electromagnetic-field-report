import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm

# 初始化翻译器
translator = GoogleTranslator(source='auto', target='zh-CN')

# 读取包含分析结果的CSV文件
csv_file = "nature_articles_analysis.csv"
df = pd.read_csv(csv_file)

# 定义一个函数来翻译文本
def translate_text(text):
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Error translating text: {text}\n{e}")
        return text

# 对DataFrame中的特定列进行翻译并显示进度条
df['Title_Chinese'] = [translate_text(text) for text in tqdm(df['Title'], desc='Translating Titles')]
df['Abstract_Chinese'] = [translate_text(text) for text in tqdm(df['Abstract'], desc='Translating Abstracts')]
df['Analysis_Chinese'] = [translate_text(text) for text in tqdm(df['Analysis'], desc='Translating Analysis')]

# 将翻译结果保存到新的CSV文件
output_csv_file = "nature_articles_analysis_translated.csv"
df.to_csv(output_csv_file, index=False)

print(f"Translated results have been saved to {output_csv_file}")
