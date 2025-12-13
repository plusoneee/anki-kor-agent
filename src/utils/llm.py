# src/utils/llm.py
from openai import AsyncAzureOpenAI
from typing import Optional, List, Dict, Any
from src.config import get_env_settings

# 初始化 Azure OpenAI 客戶端
_settings = get_env_settings()
client = AsyncAzureOpenAI(
    azure_endpoint=_settings.endpoint,
    api_key=_settings.api_key,
    api_version=_settings.api_version
)

async def ask_llm(
    *,
    model: str = "gpt-4o-mini",
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.2,
    max_tokens: int = 800,
    **kwargs: Any
) -> str:
    """
    通用型 LLM 呼叫介面。

    Args:
        model: 模型名稱（預設 gpt-4o-mini）
        system_prompt: 系統提示詞
        user_prompt: 使用者提示詞
        messages: 自訂 messages 列表（若提供則覆蓋 system/user）
        temperature: 生成溫度
        max_tokens: 最大 token 數
        kwargs: 傳遞其他 OpenAI API 參數

    Returns:
        str: 模型回傳的主要文字內容
    """

    if not messages:
        if not user_prompt:
            raise ValueError("Either `user_prompt` or `messages` must be provided.")
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ask_llm] Error: {e}")
        raise
