"""Prompt templates for the multi-agent system."""


def planner_prompt(user_prompt: str) -> str:
    """Generate the planner agent prompt.
    
    Args:
        user_prompt: The user's project description
        
    Returns:
        The formatted prompt for the planner agent
    """
    PLANNER_PROMPT = f"""
You are a PLANNER agent. Convert the user prompt into a COMPLETE engineering project plan.

User Request: {user_prompt}
    """
    return PLANNER_PROMPT


def architect_prompt(plan) -> str:
    """Generate the architect agent prompt.
    
    Args:
        plan: The Plan object from the planner agent
        
    Returns:
        The formatted prompt for the architect agent
    """
    ARCHITECT_PROMPT = f"""
You are the ARCHITECT agent. Given this project plan, break it down into explicit engineering tasks.

RULES:
- For each FILE in the plan, create one or more IMPLEMENTATION TASKS.
- In each task description:
    * Specify exactly what to implement.
    * Name the variables, functions, classes, and components to be defined.
    * Mention how this task depends on or will be used by previous tasks.
    * Include integration details: imports, expected function signatures, data flow
- Order tasks so that dependencies are implemented first.
- Each step must be SELF-CONTAINED but also carry FORWARD the relevant context from earlier tasks.

PROJECT PLAN:
{plan}
    """
    return ARCHITECT_PROMPT


def coder_system_prompt() -> str:
    """Generate the system prompt for the coder agent.
    
    Returns:
        The system prompt for the coder agent
    """
    CODER_SYSTEM_PROMPT = """
You are the CODER agent.
You are implementing a specific engineering task.
You have access to tools to read and write files.

Always:
- Review all existing files to maintain compatibility.
- Implement the FULL file content, integrating with other modules.
- Maintain consistent naming of variables, functions, and imports.
- When a module is imported from another file, ensure it exists and is implemented as described.
- Follow the task description precisely and ensure code is production-ready.
    """
    return CODER_SYSTEM_PROMPT
