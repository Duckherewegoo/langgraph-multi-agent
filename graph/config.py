from typing import Any

from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field


class WorkflowConfig(BaseModel):
    """工作流配置"""
    llm: BaseChatModel = Field(description="语言模型实例")
    max_iterations: int = Field(default=3, description="最大迭代次数")
    researcher_config: dict[str, Any] | None = Field(
        default=None, description="研究智能体配置"
    )
    writer_config: dict[str, Any] | None = Field(
        default=None, description="写作智能体配置"
    )
    reviewer_config: dict[str, Any] | None = Field(
        default=None, description="审核智能体配置"
    )
    editor_config: dict[str, Any] | None = Field(
        default=None, description="编辑智能体配置"
    )
