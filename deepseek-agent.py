import datetime
import json
import os

from dotenv import load_dotenv
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_BASE_URL")
)

# travily搜索引擎
# tavily = TavilySearchResults(max_results=5)
tavily = TavilySearch(
    search_depth="basic", max_results=3, include_answer=True, include_links=True
)
tavily.description = "这是一个类似谷歌和百度的搜索引擎，搜索知识、天气、股票、电影、小说、百科等都是支持的哦，如果你不确定就应该搜索一下，谢谢！"

# 工具列表
tools = [
    tavily,
]


def call_llm(query):
    """
    完整的LLM交互流程：
    1. 调用LLM获取工具调用指令
    2. 解析并执行工具调用
    3. 返回最终结果
    """

    try:
        print(666)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": query},
            ],
            stream=False,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        # 新增：打印异常信息，便于调试
        print(f"调用LLM失败：{str(e)}")
        return str(e)


# 工具列表
tools = [
    tavily,
]

tool_names = "or".join([tool.name for tool in tools])  # 拼接工具名
tool_descs = []  # 拼接工具详情
for t in tools:
    args_desc = []
    for name, info in t.args.items():
        # print(
        #     f"name: {name}, info: {info["description"] if "description" in info else ""}"
        # )
        args_desc.append(
            {
                "name": name,
                "description": info["description"] if "description" in info else "",
                "type": info["type"] if "type" in info else "",
            }
        )
    args_desc = json.dumps(args_desc, ensure_ascii=False)
    tool_descs.append("%s: %s,args: %s" % (t.name, t.description, args_desc))
tool_descs = "\n".join(tool_descs)

today = datetime.datetime.now().strftime("%Y-%m-%d")
prompt_template = """Today is {today}. Please Answer the following questions as best you can. You have access to the following tools:

{tool_descs}

These are chat history before:
{chat_history}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {query}
"""

# 对话历史
my_history = []

if __name__ == "__main__":
    print("=== 简易AI Agent ===")
    print("输入exit退出程序\n")
    while True:
        user_input = input("请输入您的问题: ")
        user_input = user_input.strip().lower()
        print("\n".join(my_history))
        query = prompt_template.format(
            today={today},
            tool_names={tool_names},
            query={user_input},
            chat_history={"\n".join(my_history)},
            tool_descs=tool_descs
        )
        if user_input:
            if user_input == "exit":
                print("已退出")
                break
            else:
                # call_llm(query)
                final_answer = call_llm(query=query)
                my_history.append(user_input + final_answer)
        else:
            print("请输入您的问题")
