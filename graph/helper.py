from agents.base_agent import AgentState

from .state import WorkflowState


def state_to_agent_state(state: WorkflowState) -> AgentState:
    """
    将工作流状态转换为智能体状态

    Args:
        state: 工作流状态

    Returns:
        智能体状态
    """
    return AgentState(
        topic=state.get("topic", ""),
        research_notes=state.get("research_notes", []),
        draft_content=state.get("draft_content", ""),
        review_feedback=state.get("review_feedback", ""),
        final_content=state.get("final_content", ""),
        current_step=state.get("current_step", "research"),
        iteration_count=state.get("iteration_count", 0),
        max_iterations=state.get("max_iterations", 3),
        metadata=state.get("metadata", {}),
    )


def agent_state_to_state(agent_state: AgentState, state: WorkflowState) -> WorkflowState:
    """
    将智能体状态更新到工作流状态

    Args:
        agent_state: 智能体状态
        state: 原始工作流状态

    Returns:
        更新后的工作流状态
    """
    return {
        **state,
        "topic": agent_state.topic,
        "research_notes": agent_state.research_notes,
        "draft_content": agent_state.draft_content,
        "review_feedback": agent_state.review_feedback,
        "final_content": agent_state.final_content,
        "current_step": agent_state.current_step,
        "iteration_count": agent_state.iteration_count,
        "max_iterations": agent_state.max_iterations,
        "metadata": agent_state.metadata,
    }


def create_initial_state(
    topic: str,
    max_iterations: int = 3,
) -> WorkflowState:
    """
    创建初始状态

    Args:
        topic: 写作主题
        max_iterations: 最大迭代次数

    Returns:
        初始工作流状态
    """
    return {
        "topic": topic,
        "research_notes": [],
        "draft_content": "",
        "review_feedback": "",
        "final_content": "",
        "current_step": "research",
        "iteration_count": 0,
        "max_iterations": max_iterations,
        "metadata": {},
    }

__all__ = ["agent_state_to_state", "create_initial_state", "state_to_agent_state"]
