from __future__ import annotations

from openai import OpenAI

from app.core.config import get_settings
from app.kb.retriever import KBSearchResult

class LLMClient:
    """
    一个最小可用的LLM客户端
    当前只负责知识问答场景的回答生成
    """

    def __init__(self)->None:
        self.settings = get_settings()

        self.enabled = bool(
            self.settings.llm_enabled and self.settings.openai_api_key
        )

        self.client:OpenAI|None =None

        if self.enabled:
            client_kwargs = {
                "api_key" : self.settings.openai_api_key,
            }

            if self.settings.openai_base_url:
                client_kwargs["base_url"] = self.settings.openai_base_url
            self.client = OpenAI(**client_kwargs)

    def generate_kb_answer(self,question:str,results:list[KBSearchResult])->str|None:
        """
        尝试基于知识检索结果调用 LLM 生成回答。
        如果：
        - 没开启 LLM
        - 没有 API key
        - 没有检索结果
        - 调用失败
        都返回 None，让上层走 fallback。
        """
        if not self.enabled or self.client is None:
            return None

        if not results:
            return None

        context_blocks:list[str] = []
        for index,item in enumerate(results,start=1):
            context_blocks.append(
                f"[文档{index}]\n"
                f"标题：{item.title}\n"
                f"来源：{item.source}\n"
                f"内容：{item.content}\n"
            )
        context = "\n".join(context_blocks)

        system_prompt = (
            "你是一个面向工程协作场景的知识问答助手。"
            "请严格基于给定文档回答，不要编造。"
            "回答尽量简洁、直接、可执行。"
        )

        user_prompt = (
            f"用户问题：{question}\n\n"
            f"可用文档如下：\n{context}\n\n"
            "请基于这些文档回答。"
            "如果文档不能直接回答，就明确说没有直接信息。"
        )

        try:
            response = self.client.chat.completions.create(
                model = self.settings.openai_model,
                messages=[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":user_prompt},
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content
            if not content:
                return None
            return content.strip()
        except Exception:
            return None
























