from typing import TypedDict, List
# from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.globals import set_verbose, set_debug
from langchain.agents import create_agent
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from .prompts import planner_prompt, architect_prompt, coder_system_prompt
from .states import Plan, TaskPlan, CoderState
from .tools import read_file, write_file, list_files, get_current_directory, init_project_root
from .config import get_api_provider, get_api_key, get_model_name

load_dotenv()

set_debug(True)
set_verbose(True)

# Initialize project root at startup
init_project_root()


def initialize_llm():
    """Initialize the LLM based on configuration.
    
    Returns:
        Initialized language model instance
    """
    api_provider = get_api_provider()
    api_key = get_api_key()
    model_name = get_model_name()
    
    if api_provider == "openai":
        return ChatOpenAI(api_key=api_key, model=model_name)
    elif api_provider == "anthropic":
        return ChatAnthropic(api_key=api_key, model=model_name)
    elif api_provider == "google":
        return ChatGoogleGenerativeAI(api_key=api_key, model=model_name)
    elif api_provider == "llama":
        # Llama via Groq or Together AI
        from langchain_groq import ChatGroq
        return ChatGroq(api_key=api_key, model=model_name)
    elif api_provider == "qwen":
        # Qwen models via OpenAI-compatible API
        return ChatOpenAI(
            api_key=api_key,
            model=model_name,
            base_url="https://api.openai.com/v1"  # Can be customized for Qwen endpoint
        )
    elif api_provider == "deepseek":
        # Deepseek models via OpenAI-compatible API
        return ChatOpenAI(
            api_key=api_key,
            model=model_name,
            base_url="https://api.deepseek.com/v1"
        )
    else:
        # Default to Google
        return ChatGoogleGenerativeAI(api_key=api_key, model=model_name)


# Initialize LLM with configured API
llm = initialize_llm()


class AgentState(TypedDict):
    """State maintained throughout the agent workflow."""
    user_prompt: str
    project_plan: Plan
    architect_plan: List[str]  # List of implementation tasks
    coder_state: CoderState
    status: str  # Tracking agent status

def planner_agent(state: AgentState) -> AgentState:
    """Convert the user prompt into a COMPLETE engineering project plan."""

    user_input = state.get("user_prompt", "").strip()
    if not user_input:
        raise ValueError("User prompt cannot be empty.")
    
    response = llm.with_structured_output(Plan).invoke(planner_prompt(user_input))
    if response is None:
        raise ValueError("Planner did not return a valid response.")
    state["project_plan"] = response
    return state

def architect_agent(state: AgentState) -> AgentState:
    """Break down the project plan into explicit engineering tasks."""

    if not isinstance(state.get("project_plan"), Plan):
        raise ValueError("Invalid project plan from planner agent.")
    
    response = llm.with_structured_output(TaskPlan).invoke(architect_prompt(state["project_plan"]))
    if response is None:
        raise ValueError("Architect did not return a valid response.")
    state["architect_plan"] = response.implementation_steps
    return state

def coder_agent(state: AgentState) -> AgentState:
    """Write complete code for the specific engineering task."""

    coder_state = state.get("coder_state")
    if coder_state is None:
        architect_plan = state.get("architect_plan", [])
        if not architect_plan:
            raise ValueError("No architecture plan available for coder agent.")
        task_plan = TaskPlan(implementation_steps=architect_plan)
        coder_state = CoderState(task_plan=task_plan, current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    
    # Check if all tasks are completed
    if coder_state.current_step_idx >= len(steps):
        state["status"] = "DONE"
        return state
    
    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.invoke({"path": current_task.filepath})
    
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )
    system_prompt = coder_system_prompt()

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_agent(llm, coder_tools)
    react_agent.invoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    })

    coder_state.current_step_idx += 1
    state["coder_state"] = coder_state
    return state

def _should_continue_coding(state: AgentState) -> str:
    """Determines whether to continue coding or finish."""
    coder_state = state.get("coder_state")
    if coder_state is None:
        return "coder"
    
    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return "END"
    return "coder"


# Build the agentic workflow graph
graph = StateGraph(AgentState)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    _should_continue_coding,
    {"coder": "coder", "END": END}
)

graph.set_entry_point("planner")

agent = graph.compile()
