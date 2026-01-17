import streamlit as st
import logging
import traceback
from typing import Any, Dict, Generator
import json
from datetime import datetime

from Agent.graph import agent, AgentState, initialize_llm
from Agent.states import Plan, TaskPlan, CoderState, ImplementationTask
from Agent.config import is_configured, load_config, update_api_config, get_api_provider, get_api_key, get_model_name

# Configure page
st.set_page_config(
    page_title="Companio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom CSS for better UI
st.markdown("""
<style>
    .status-running {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .status-completed {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .status-error {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .task-item {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .plan-section {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .code-section {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "execution_history" not in st.session_state:
    st.session_state.execution_history = []
if "current_execution" not in st.session_state:
    st.session_state.current_execution = None
if "agent_state" not in st.session_state:
    st.session_state.agent_state = None
if "api_configured" not in st.session_state:
    st.session_state.api_configured = is_configured()
if "show_api_config" not in st.session_state:
    st.session_state.show_api_config = not is_configured()


def show_api_configuration_modal():
    """Display API configuration modal."""
    st.markdown("""
    <style>
        .api-config-container {
            background-color: #f0f2f6;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .api-config-title {
            color: #1f77b4;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="api-config-container">', unsafe_allow_html=True)
    st.markdown('<div class="api-config-title">⚙️ API Configuration</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome! Before we get started, please configure your AI API settings.
    You'll need to provide your API key and choose a model.
    """)
    
    # API Provider Selection
    api_provider = st.selectbox(
        "Select API Provider",
        ["google", "openai", "anthropic"],
        help="Choose your AI API provider"
    )
    
    # API Key Input
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="Enter your API key here",
        help="Your API key will be securely stored locally"
    )
    
    # Model Name Input
    model_suggestions = {
        "google": "gemini-2.5-flash",
        "openai": "gpt-4",
        "anthropic": "claude-3-5-sonnet-20241022"
    }
    
    default_model = model_suggestions.get(api_provider, "")
    model_name = st.text_input(
        "Model Name",
        value=default_model,
        placeholder="e.g., gpt-4, claude-3-opus-20240229, gemini-2.5-flash",
        help="Enter the model name/ID you want to use"
    )
    
    # Information section
    st.info("""
    **How to get your API key:**
    - **Google:** Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    - **OpenAI:** Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
    - **Anthropic:** Visit [Anthropic Console](https://console.anthropic.com/)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Save Configuration", use_container_width=True, key="save_api_config"):
            if not api_key or not model_name:
                st.error("❌ Please fill in all fields")
            else:
                try:
                    update_api_config(api_provider, api_key, model_name)
                    st.session_state.api_configured = True
                    st.session_state.show_api_config = False
                    st.success("✅ Configuration saved successfully!")
                    # Reinitialize LLM with new config
                    from Agent import graph
                    graph.llm = initialize_llm()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving configuration: {str(e)}")
    
    with col2:
        if st.button("🔄 Edit Existing", use_container_width=True, key="edit_api_config"):
            # Load current config
            config = load_config()
            st.session_state.show_api_config = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# Show API configuration modal if not configured
if st.session_state.show_api_config or not st.session_state.api_configured:
    show_api_configuration_modal()
    st.stop()


# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Configuration section
    st.subheader("🔑 API Configuration")
    current_provider = get_api_provider()
    current_model = get_model_name()
    st.info(f"""
    **Current Configuration:**
    - Provider: {current_provider.upper()}
    - Model: {current_model}
    """)
    
    if st.button("🔄 Change API Settings", use_container_width=True, key="sidebar_api_config"):
        st.session_state.show_api_config = True
        st.rerun()
    
    st.divider()
    
    recursion_limit = st.slider(
        "Recursion Limit",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        help="Maximum recursion limit for agent processing"
    )
    
    st.divider()
    st.title("Execution History")
    
    if st.session_state.execution_history:
        for i, execution in enumerate(reversed(st.session_state.execution_history)):
            if st.button(
                f"Execution {len(st.session_state.execution_history) - i}",
                key=f"hist_{i}",
                use_container_width=True
            ):
                st.session_state.current_execution = len(st.session_state.execution_history) - i - 1
    else:
        st.info("No execution history yet")

# Main content
st.title("🤖 Companio")
st.markdown("Watch your AI agent work in real-time as it plans and builds your project.")

# Input section
st.subheader("📝 Project Description")
user_prompt = st.text_area(
    "What would you like to build?",
    placeholder="e.g., Build a todo list web app with React and Node.js backend...",
    height=150,
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 4])
with col1:
    run_button = st.button("🚀 Run Agent", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Clear History", use_container_width=True)

if clear_button:
    st.session_state.execution_history = []
    st.session_state.current_execution = None
    st.session_state.agent_state = None
    st.rerun()

# Execution handling
if run_button:
    if not user_prompt.strip():
        st.error("❌ Please enter a project description")
    else:
        try:
            # Create placeholders for dynamic updates
            status_placeholder = st.empty()
            progress_placeholder = st.empty()
            logs_placeholder = st.empty()
            
            execution_log = {
                "timestamp": datetime.now().isoformat(),
                "prompt": user_prompt,
                "stages": {
                    "planner": {"status": "pending", "output": None},
                    "architect": {"status": "pending", "output": None},
                    "coder": {"status": "pending", "iterations": []}
                },
                "final_state": None,
                "error": None
            }
            
            # Planner stage
            status_placeholder.markdown(
                '<div class="status-running">🔄 Stage 1/3: Planning...</div>',
                unsafe_allow_html=True
            )
            progress_placeholder.progress(0.33)
            
            logs_placeholder.info("Analyzing your project requirements...")
            
            # Run the agent
            try:
                final_state = agent.invoke(
                    {"user_prompt": user_prompt},
                    {"recursion_limit": recursion_limit}
                )
                
                # Update execution log
                execution_log["final_state"] = {
                    "status": final_state.get("status", "completed"),
                    "project_plan": None,  # Will be serialized below
                    "architect_plan": final_state.get("architect_plan", []),
                    "coder_iterations": len(final_state.get("coder_state", CoderState(task_plan=TaskPlan(implementation_steps=[]))).task_plan.implementation_steps)
                    if final_state.get("coder_state") else 0
                }
                
                # Serialize Plan object if it exists
                if isinstance(final_state.get("project_plan"), Plan):
                    plan = final_state["project_plan"]
                    execution_log["final_state"]["project_plan"] = {
                        "name": plan.name,
                        "description": plan.description,
                        "techstack": plan.techstack,
                        "features": plan.features,
                        "files": plan.files
                    }
                
                execution_log["stages"]["planner"]["status"] = "completed"
                execution_log["stages"]["architect"]["status"] = "completed"
                execution_log["stages"]["coder"]["status"] = "completed"
                
                # Update session state
                st.session_state.agent_state = final_state
                st.session_state.execution_history.append(execution_log)
                
                # Display results
                status_placeholder.markdown(
                    '<div class="status-completed">✅ All stages completed successfully!</div>',
                    unsafe_allow_html=True
                )
                progress_placeholder.progress(1.0)
                logs_placeholder.success("Agent execution completed!")
                
                # Show results
                st.divider()
                st.subheader("📊 Execution Results")
                
                tabs = st.tabs(["Plan", "Architecture", "Code Tasks", "Full State"])
                
                with tabs[0]:
                    if isinstance(final_state.get("project_plan"), Plan):
                        plan = final_state["project_plan"]
                        st.markdown(f'<div class="plan-section">', unsafe_allow_html=True)
                        st.write(f"**Project Name:** {plan.name}")
                        st.write(f"**Description:** {plan.description}")
                        st.write(f"**Tech Stack:** {plan.techstack}")
                        st.write(f"**Features:**")
                        for feature in plan.features:
                            st.write(f"  - {feature}")
                        st.write(f"**Files to Create:**")
                        for file in plan.files:
                            st.write(f"  - {file}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No project plan available")
                
                with tabs[1]:
                    architect_plan = final_state.get("architect_plan", [])
                    if architect_plan:
                        st.markdown(f'<div class="plan-section">', unsafe_allow_html=True)
                        st.write(f"**Total Implementation Steps:** {len(architect_plan)}")
                        for i, step in enumerate(architect_plan, 1):
                            st.markdown(f'<div class="task-item">', unsafe_allow_html=True)
                            st.write(f"**Step {i}:** {step}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No architecture plan available")
                
                with tabs[2]:
                    coder_state = final_state.get("coder_state")
                    if coder_state and isinstance(coder_state, CoderState):
                        steps = coder_state.task_plan.implementation_steps
                        st.markdown(f'<div class="code-section">', unsafe_allow_html=True)
                        st.write(f"**Total Code Tasks:** {len(steps)}")
                        st.write(f"**Current Step Index:** {coder_state.current_step_idx}")
                        
                        for i, task in enumerate(steps, 1):
                            with st.expander(f"Task {i}: {task.filepath}"):
                                st.write(f"**File Path:** {task.filepath}")
                                st.write(f"**Description:**")
                                st.write(task.task_description)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No coder state available")
                
                with tabs[3]:
                    st.json(execution_log, expanded=False)
                
            except Exception as e:
                execution_log["error"] = str(e)
                st.session_state.execution_history.append(execution_log)
                
                status_placeholder.markdown(
                    '<div class="status-error">❌ Error occurred during execution</div>',
                    unsafe_allow_html=True
                )
                
                st.error(f"An error occurred: {str(e)}")
                with st.expander("📋 Full Error Traceback"):
                    st.code(traceback.format_exc())
                    
        except KeyboardInterrupt:
            st.warning("⚠️ Operation cancelled by user")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.code(traceback.format_exc())

# Display current execution if selected from history
if st.session_state.current_execution is not None:
    st.divider()
    st.subheader("📜 Historical Execution")
    
    exec_index = st.session_state.current_execution
    if exec_index < len(st.session_state.execution_history):
        execution = st.session_state.execution_history[exec_index]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Timestamp:** {execution['timestamp']}")
        with col2:
            if execution['error']:
                st.write(f"**Status:** ❌ Error")
            else:
                st.write(f"**Status:** ✅ Completed")
        
        st.write(f"**Prompt:** {execution['prompt']}")
        
        if execution['final_state']:
            st.json(execution['final_state'])

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 30px; padding: 20px;">
    <p>🤖 AI Agent Debugger | Real-time project planning and code generation</p>
    <p style="font-size: 12px;">Watch the agent analyze requirements, architect solutions, and generate code</p>
</div>
""", unsafe_allow_html=True)
