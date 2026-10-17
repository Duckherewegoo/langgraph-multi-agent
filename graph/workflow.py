"""
工作流定义
使用LangGraph构建多智能体协作写作工作流
"""

from langgraph.graph import END, StateGraph

from agents.editor import EditorAgent
from agents.researcher import ResearchAgent
from agents.reviewer import ReviewerAgent
from agents.writer import WriterAgent

from .config import WorkflowConfig
from .helper import agent_state_to_state as _agent_state_to_state
from .helper import state_to_agent_state as _state_to_agent_state
from .state import WorkflowState


def create_workflow(config: WorkflowConfig):
    """
    创建多智能体协作写作工作流

    Args:
        config: 工作流配置

    Returns:
        编译后的LangGraph工作流
    """
    # 初始化各个智能体
    researcher = ResearchAgent(
        llm=config.llm,
        **(config.researcher_config or {}),
    )

    writer = WriterAgent(
        llm=config.llm,
        **(config.writer_config or {}),
    )

    reviewer = ReviewerAgent(
        llm=config.llm,
        **(config.reviewer_config or {}),
    )

    editor = EditorAgent(
        llm=config.llm,
        **(config.editor_config or {}),
    )

    # 定义节点函数
    async def research_node(state: WorkflowState) -> WorkflowState:
        """研究节点"""
        agent_state = _state_to_agent_state(state)
        result = await researcher.run(agent_state)
        return _agent_state_to_state(result, state)

    async def write_node(state: WorkflowState) -> WorkflowState:
        """写作节点"""
        agent_state = _state_to_agent_state(state)
        result = await writer.run(agent_state)
        return _agent_state_to_state(result, state)

    async def review_node(state: WorkflowState) -> WorkflowState:
        """审核节点"""
        agent_state = _state_to_agent_state(state)
        result = await reviewer.run(agent_state)
        return _agent_state_to_state(result, state)

    async def edit_node(state: WorkflowState) -> WorkflowState:
        """编辑节点"""
        agent_state = _state_to_agent_state(state)
        result = await editor.run(agent_state)
        return _agent_state_to_state(result, state)

    # 定义条件边函数
    def should_continue_writing(state: WorkflowState) -> str:
        """
        判断是否继续写作（审核后是否需要修改）

        Args:
            state: 当前状态

        Returns:
            下一个节点名称
        """
        needs_revision = state.get("metadata", {}).get("needs_revision", False)
        iteration_count = state.get("iteration_count", 0)
        max_iterations = state.get("max_iterations", 3)

        if needs_revision and iteration_count < max_iterations:
            return "write"
        else:
            return "edit"

    # 创建状态图
    workflow = StateGraph(WorkflowState)

    # 添加节点
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    workflow.add_node("review", review_node)
    workflow.add_node("edit", edit_node)

    # 设置入口点
    workflow.set_entry_point("research")

    # 添加边
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "review")

    # 添加条件边（审核后决定是继续修改还是进入编辑）
    workflow.add_conditional_edges(
        "review",
        should_continue_writing,
        {
            "write": "write",
            "edit": "edit",
        },
    )

    workflow.add_edge("edit", END)

    # 编译工作流
    compiled_workflow = workflow.compile()

    return compiled_workflow
