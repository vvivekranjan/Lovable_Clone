import streamlit as st
import logging
import traceback
from typing import Any, Dict, Generator
import json
from datetime import datetime

from Agent.graph import agent, AgentState
from Agent.states import Plan, TaskPlan, CoderState, ImplementationTask

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

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
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
