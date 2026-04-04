from __future__ import annotations

from dataclasses import dataclass
import re

@dataclass(frozen=True)
class RouteDecision:
    """
    路由决策结果。
    为什么不用 dict？
    因为 dataclass 可读性更好，字段也更固定，不容易拼错 key。
    """
    intent: str
    path: str
    confidence: float
    reason: str

def detect_route(message:str) -> RouteDecision:
    """
    根据用户输入，判断应该走哪条路径。

    今天先用最简单的规则：
    - greet: 打招呼
    - task_create: 创建任务
    - task_query: 查询任务
    - kb_qa: 知识问答
    - unknown: 暂时不知道怎么处理
    """
    text = message.strip().lower()

    #1.打招呼
    if any(keyword in text for keyword in ['你好',"hello",'hi','hey']):
        return RouteDecision(
            intent="greet",
            path = "direct_answer",
            confidence=0.99,
            reason="命中了问候关键词",
        )
    #2.查询任务
    # 这个判断放在知识问答前面，
    # 因为“任务状态怎么查”里也有“怎么”，容易被误判成 kb_qa。
    if any(keyword in text for keyword in ["查任务", "任务状态", "任务进度", "task status", "任务查询"]):
        return RouteDecision(
            intent="task_query",
            path="task_query",
            confidence=0.90,
            reason="命中了任务查询关键词",
        )
    # 补一个简单的任务编号识别

    # 3. 创建任务
    if any(keyword in text for keyword in ["创建任务", "新建任务", "提个任务", "报个bug", "提个bug", "帮我记个任务"]):
        return RouteDecision(
            intent="task_create",
            path="task_create",
            confidence=0.93,
            reason="命中了任务创建关键词",
        )
    if re.search(r"(task|bug)-?\d+",text):
        return RouteDecision(
            intent="task_query",
            path="task_query",
            confidence=0.92,
            reason="命中了任务编号模式",
        )

    # 4. 知识问答
    if any(keyword in text for keyword in ["流程", "规范", "怎么", "如何", "为什么", "文档", "说明", "步骤", "排查"]):
        return RouteDecision(
            intent="kb_qa",
            path="kb_search",
            confidence=0.85,
            reason="命中了知识问答关键词",
        )
    # 5. 默认兜底
    return RouteDecision(
        intent="unknown",
        path="fallback",
        confidence=0.30,
        reason="没有命中任何明确规则，走兜底路径",
    )



























