from typing import TypedDict


class WorkflowState(TypedDict):
    """工作流状态类型"""
    topic: str
    research_notes: list
    draft_content: str
    review_feedback: str
    final_content: str
    current_step: str
    iteration_count: int
    max_iterations: int
    metadata: dict
