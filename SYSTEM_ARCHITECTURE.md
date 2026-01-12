# System Architecture Overview

## 🏗️ Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Lovable Clone - Full System                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      User Interfaces                              │
├─────────────────────┬───────────────────────────────────────────┤
│  Web UI (NEW)       │      Command Line (CLI)                    │
│  (Streamlit)        │      (main.py)                             │
│                     │                                             │
│ • Prompt Input      │   • Interactive prompt                     │
│ • Real-time View    │   • Terminal output                        │
│ • History Browser   │   • Recursion limit args                  │
│ • Formatted Output  │   • Basic logging                          │
└─────────────────────┴───────────────────────────────────────────┘
                             ↓
         ┌───────────────────────────────────────────┐
         │    Agent Orchestration (graph.py)         │
         │    - Workflow management                  │
         │    - State passing                        │
         │    - Conditional logic                    │
         └───────────────────────────────────────────┘
                             ↓
        ┌────────────────────────────────────────────────────┐
        │            Multi-Agent System                       │
        ├──────────────┬──────────────┬──────────────────────┤
        │  Planner     │ Architect    │ Coder (Iterative)    │
        │              │              │                      │
        │ • Input      │ • Task       │ • File Reading       │
        │   Analysis   │   Breakdown  │ • Code Generation    │
        │ • Feature    │ • Step       │ • File Writing       │
        │   Planning   │   Planning   │ • Dependency Mgmt    │
        │ • Tech Stack │ • File Lists │ • Loop Control       │
        │   Selection  │              │                      │
        └──────────────┴──────────────┴──────────────────────┘
                             ↓
        ┌───────────────────────────────────────────────────┐
        │         LLM Integration (Google Gemini)            │
        │  - Structured output (Pydantic models)             │
        │  - Tool use and agent actions                      │
        │  - Context management                             │
        └───────────────────────────────────────────────────┘
                             ↓
        ┌───────────────────────────────────────────────────┐
        │         File System Tools (tools.py)               │
        │  - Read/Write operations                           │
        │  - Path validation & security                      │
        │  - Directory management                           │
        └───────────────────────────────────────────────────┘
                             ↓
        ┌───────────────────────────────────────────────────┐
        │       Generated Project Output                     │
        │  - generated_project/ directory                    │
        │  - All code files                                  │
        │  - Full project structure                         │
        └───────────────────────────────────────────────────┘
```

## 📊 Data Flow - Streamlit UI Path

```
User Input (Text Area)
    ↓
[Run Agent Button]
    ↓
Streamlit App (streamlit_app.py)
    ↓
Initialize Agent State
    ↓
Invoke Agent Graph
    ↓
├─→ Planner Agent
│   └─→ Generate Plan (Pydantic Model)
│       └─→ Update Status Placeholder
│
├─→ Architect Agent
│   └─→ Create Tasks (List of ImplementationTask)
│       └─→ Update Status Placeholder
│
└─→ Coder Agent (Iterative)
    └─→ Process Each Task
        ├─→ Read File
        ├─→ Generate Code
        ├─→ Write File
        └─→ Loop Until Complete
            └─→ Update Status Placeholder
    ↓
Display Results in Tabs
    ├─→ Plan Tab (Project Details)
    ├─→ Architecture Tab (Implementation Steps)
    ├─→ Code Tasks Tab (Individual Tasks)
    └─→ Full State Tab (JSON Output)
    ↓
Save to Execution History
    ↓
Ready for Next Execution
```

## 🔄 Execution Stages

### Stage 1: Planning (Planner Agent)
```
Input:  Raw user requirements
Process: Analyze and structure requirements
Output: Plan Model containing:
  - Project name & description
  - Technology stack
  - Feature list
  - Required files
```

### Stage 2: Architecture (Architect Agent)
```
Input:  Project plan from Stage 1
Process: Break down into implementation tasks
Output: TaskPlan containing:
  - List of implementation steps
  - File paths for each step
  - Detailed task descriptions
```

### Stage 3: Coding (Coder Agent - Iterative)
```
Loop through each implementation step:
  Input:  Current task from architecture
  Process: 
    1. Read existing file content
    2. Generate code using LLM
    3. Write/update file
    4. Move to next task
  Output: Generated code files
```

## 📁 File Organization

```
Lovable_Clone/
├── 🎨 User Interface Layer
│   ├── streamlit_app.py          # Web UI (NEW)
│   ├── main.py                   # CLI interface
│   └── setup_streamlit.py        # Setup helper (NEW)
│
├── 🤖 Agent System
│   └── Agent/
│       ├── graph.py              # Workflow orchestration
│       ├── states.py             # Data models
│       ├── prompts.py            # LLM prompts
│       ├── tools.py              # File I/O & tools
│       └── __init__.py           # Package exports
│
├── ⚙️ Configuration
│   ├── pyproject.toml            # Project config + dependencies
│   ├── requirements.txt          # Pip requirements (NEW)
│   └── .env                      # Environment variables
│
└── 📚 Documentation
    ├── README.md                 # Main documentation
    ├── STREAMLIT_GUIDE.md        # UI guide (NEW)
    ├── QUICK_START_STREAMLIT.md  # Quick reference (NEW)
    ├── STREAMLIT_IMPLEMENTATION.md # Technical details (NEW)
    └── Other guides...
```

## 🔐 Security Features

1. **Path Validation**: All file operations validated to prevent directory traversal
2. **Sandboxing**: Generated projects stored in `generated_project/` directory
3. **Input Validation**: All user inputs validated before processing
4. **Error Handling**: Comprehensive exception handling prevents crashes
5. **Logging**: Detailed logs for security auditing

## ⚡ Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Planning | ~5-10s | LLM analysis of requirements |
| Architecture | ~3-5s | Task breakdown |
| Coding | Varies | Depends on project complexity |
| UI Rendering | <1s | Streamlit's reactive engine |
| History Load | <100ms | In-memory storage |

## 🎯 Key Design Decisions

### 1. Why Streamlit?
- Rapid UI development without JavaScript
- Built-in state management
- Real-time updates with placeholders
- Session persistence
- Easy deployment options

### 2. Why TypedDict for State?
- LangGraph compatibility
- Type safety without overhead
- Clear state structure
- Easy serialization

### 3. Why Pydantic Models?
- Built-in validation
- Automatic JSON serialization
- IDE autocomplete support
- Type hints throughout

### 4. Why Google Gemini?
- High quality output
- Structured output support
- Cost-effective pricing
- Reliable API

## 🔄 Workflow Comparison

### Before (CLI Only)
```
User Input → JSON Output → Manual Inspection
```

### After (With Streamlit)
```
User Input → Real-time Progress → Formatted Tabs → History Tracking
```

## 🚀 Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud
```bash
streamlit cloud deploy
```

### Docker Container
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 📈 Metrics & Monitoring

The Streamlit UI automatically tracks:
- Execution count
- Execution time
- Success/failure rate
- Error types
- History size

All stored in session state and local browser storage.

## 🔮 Future Enhancements

1. **Database Integration**: Persist history to database
2. **User Authentication**: Multi-user support
3. **Project Viewing**: Browse generated files in UI
4. **Real-time Logs**: Stream agent logs live
5. **Undo/Redo**: Modify generated code
6. **Export Options**: Download project as ZIP
7. **AI Refinement**: Iterate on generated code
8. **Collaboration**: Share projects with team

## 📞 Support Resources

- **Documentation**: See STREAMLIT_GUIDE.md
- **Quick Start**: See QUICK_START_STREAMLIT.md
- **Implementation Details**: See STREAMLIT_IMPLEMENTATION.md
- **Main README**: See README.md
- **Source Code**: Check streamlit_app.py with comments

---

This architecture provides a robust, scalable foundation for interactive AI-driven project generation with both CLI and web UI options!
