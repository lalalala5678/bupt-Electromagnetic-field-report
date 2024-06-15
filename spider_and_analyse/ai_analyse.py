import openai
import pandas as pd

# 设置您的OpenAI API密钥
openai.api_key = "dsa"

# 读取爬取的CSV文件
csv_file = "nature_articles.csv"
df = pd.read_csv(csv_file)

# 准备分析数据
abstracts = df['Abstract'].tolist()

# 定义一个函数来调用OpenAI API进行分析
def analyze_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that helps analyze scientific text."},
            {"role": "user", "content": f"Analyze the following text and provide a summary, key topics, and sentiment analysis:\n\n{text}"}
        ],
        max_tokens=200,
        temperature=0.5,
    )
    return response.choices[0].message['content'].strip()

# 对每篇摘要进行分析
analysis_results = [analyze_text(abstract) for abstract in abstracts]

# 将分析结果添加到DataFrame中
df['Analysis'] = analysis_results

# 将分析结果保存到新的CSV文件
output_csv_file = "nature_articles_analysis.csv"
df.to_csv(output_csv_file, index=False)

print(f"Analysis results have been saved to {output_csv_file}")
