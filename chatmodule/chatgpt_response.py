import openai

# 设置您的OpenAI API密钥
openai.api_key = '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'

def generate_chat_response(prompt, max_tokens=150, temperature=0.7):
    response = openai.Completion.create(
        engine="text-davinci-002",  # 中文模型引擎
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    text = response['choices'][0]['text']
    print(text.encode('utf-8').decode())  # 使用utf-8编码格式来正确处理中文文本


# 输入问题或指令（中文）
user_input = "你好，给我讲一个有趣的故事。"

# 获取完整回复（非流式响应）
generate_chat_response(user_input, max_tokens=500)  # 增大max_tokens的值


