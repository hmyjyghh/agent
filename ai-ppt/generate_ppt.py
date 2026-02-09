# 导入ppt 生成库

def call_llm(topic, page):
    # 设计提示词，让LLM 根据主题生成内容，要求生成json 格式的内容
    # LLM 返回内容后，对格式进行后处理

    return '调用LLM能力返回PPT 内容'

def generate_ppt(content):
    # 生成ppt 文件

    return None


if __name__ == 'main':
    while True:
        topic = input("请任意输入一个ppt 主题")
        page = input("请输入要生成的页数")

        # 生成PPT内容
        ppt_content = call_llm(topic, page)

        # 生成最终的ppt 文件
