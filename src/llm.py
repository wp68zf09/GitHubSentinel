import requests
import os
import json
from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
from logger import LOG  # 导入日志模块

class LLM:
    def __init__(self):
        self.client =OpenAI(api_key="sk-3e5ff44e82b745a7ab7a748b806951c2", base_url="https://api.deepseek.com")
        # 从TXT文件加载提示信息
        with open("prompts/report_prompt.txt", "r", encoding='utf-8') as file:
            self.system_prompt = file.read()

    # def generate_daily_report(self, markdown_content, dry_run=False):
    #     # 使用从TXT文件加载的提示信息
    #     messages = [
    #         {"role": "system", "content": self.system_prompt},
    #         {"role": "user", "content": markdown_content},
    #     ]

    #     if dry_run:
    #         # 如果启用了dry_run模式，将不会调用模型，而是将提示信息保存到文件中
    #         LOG.info("Dry run mode enabled. Saving prompt to file.")
    #         with open("daily_progress/prompt.txt", "w+") as f:
    #             # 格式化JSON字符串的保存
    #             json.dump(messages, f, indent=4, ensure_ascii=False)
    #         LOG.debug("Prompt已保存到 daily_progress/prompt.txt")

    #         return "DRY RUN"

    #     # 日志记录开始生成报告
    #     LOG.info("使用 GPT 模型开始生成报告。")
        
    #     try:
    #         # 调用OpenAI GPT模型生成报告
    #         response = self.client.chat.completions.create(
    #             model="deepseek-chat",  # 指定使用的模型版本
    #             messages=messages
    #         )
    #         LOG.debug("GPT response: {}", response)
    #         # 返回模型生成的内容
    #         return response.choices[0].message.content
    #     except Exception as e:
    #         # 如果在请求过程中出现异常，记录错误并抛出
    #         LOG.error(f"生成报告时发生错误：{e}")
    #         raise
    def generate_daily_report(self, markdown_content: str, dry_run: bool = False) -> str:
# 使用从TXT文件加载的提示信息
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            # 如果启用了dry_run模式，将不会调用模型，而是将提示信息保存到文件中
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                # 格式化JSON字符串的保存
                json.dump(messages, f, indent=4, ensure_ascii=False)
            LOG.debug("Prompt已保存到 daily_progress/prompt.txt")

            return "DRY RUN"

        LOG.info("正在调用本地 zhaowangGemma3 模型生成报告...")

        try:
            # Ollama 本地API调用（默认端口11434）
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "zhaowangGemma3",
                    "messages": messages,
                    "stream": False,  # 关闭流式输出
                    "options": {
                        "temperature": 0.7,  # 可覆盖Modelfile中的默认参数
                        "num_ctx": 8192     # 上下文窗口大小
                    }
                },
                timeout=300  # 5分钟超时
            )
            response.raise_for_status()

            result = response.json()
            LOG.debug(f"模型原始响应: {json.dumps(result, indent=2)}")
            return result["message"]["content"]

        except requests.exceptions.RequestException as e:
            LOG.error(f"API调用失败: {str(e)}")
            raise RuntimeError(f"模型服务不可用: {e}")
        except KeyError as e:
            LOG.error(f"响应解析失败: {result}")
            raise RuntimeError("模型返回了非标准响应格式")