import openai

class OpenaiChatModule:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.conversation = [
                                {"role": "system", "content": "你的名字叫robot,你是语音助手，给我的对话要简略，最好在20字以内"} # 初始值，身份设定
                            ]

    # 调用chatgpt原生接口，不做任何修改
    def chat_with_model(self, text):
        openai.api_key = self.openai_api_key
        text = text.replace('\n', ' ').replace('\r', '').strip()  # 文本处理，换行符和回车符替换为空格
        if len(text) == 0:
            return
        print(f'chatGPT Q:{text}')
        self.conversation.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(        # ChatCompletion有记忆功能
            model="gpt-3.5-turbo",
            messages=self.conversation,
            max_tokens=2048,
            temperature=0.1, # GPT模型创造力

        )
        reply = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": reply}) # 把新回复的消息也加入conversation变量里，就会记住之前讲过什么
        print(f'chatGPT A:{reply}')
        return reply

if __name__ == '__main__':
    openai_api_key = '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'

    openaichatmodule = OpenaiChatModule(openai_api_key)
    print(openaichatmodule.chat_with_model('你好，你叫什么?'))
    print(openaichatmodule.chat_with_model('评价一下洛阳'))
    print(openaichatmodule.chat_with_model('和密云进行对比'))
