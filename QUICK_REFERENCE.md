# Quick Reference Guide

## Project Structure Overview

```
Lovable_Clone/
├── main.py                      # Entry point
├── pyproject.toml              # Project config
├── README.md                   # Main documentation
├── IMPROVEMENTS.md             # Detailed improvements
├── ENHANCEMENT_SUMMARY.md      # Summary of changes
├── QUICK_REFERENCE.md          # This file
├── .env                        # Environment variables (not committed)
├── .python-version             # Python version specification
├── uv.lock                     # Dependency lock file
├── Agent/                      # Main package
│   ├── __init__.py             # Package initialization (NEW)
│   ├── graph.py                # Multi-agent workflow
│   ├── states.py               # Pydantic models
│   ├── tools.py                # File I/O tools
│   ├── prompts.py              # LLM prompts
│   └── __pycache__/            # Python cache
└── generated_project/          # Output directory
    └── backend/                # Generated project files
```

## Getting Started

### Setup (First Time)

```bash
cd f:\Lovable_Clone

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -e .

# Set environment variables
echo GROQ_API_KEY=your_key > .env
```

### Running the Application

```bash
# Simple run
python main.py

# With custom recursion limit
python main.py --recursion-limit 50

# Show help
python main.py --help
```

## Key Classes and Functions

### Agent States (states.py)
- `Plan` - Project planning data
- `ImplementationTask` - Individual coding task
- `TaskPlan` - Collection of tasks
- `CoderState` - Coder agent state
- `AgentState` - Overall workflow state

### Tools (tools.py)
- `read_file(path)` - Read file from generated project
- `write_file(path, content)` - Write file to generated project
- `list_files(directory)` - List files in directory
- `get_current_directory()` - Get project root
- `run_cmd(cmd, cwd)` - Execute shell command
- `init_project_root()` - Initialize project directory

### Agents (graph.py)
- `planner_agent()` - Convert requirements to plan
- `architect_agent()` - Create implementation tasks
- `coder_agent()` - Write code for tasks

## Common Tasks

### Modify a Prompt

Edit the corresponding function in `prompts.py`:

```python
def planner_prompt(user_prompt: str) -> str:
    """Generate the planner agent prompt."""
    # Edit this string to modify the prompt
    PLANNER_PROMPT = f"""
    Your custom prompt here...
    """
    return PLANNER_PROMPT
```

### Add a New Tool

In `tools.py`, add a new function:

```python
@tool
def my_tool(param: str) -> str:
    """Description of the tool."""
    # Implementation
    return result
```

Then import it in `graph.py`.

### Debug an Issue

1. Check logs in console output
2. Look at generated files in `generated_project/`
3. Run with increased verbosity:
   ```bash
   python main.py  # Logs are printed to console
   ```

### Add Validation to a Field

In `states.py`, add a validator:

```python
class MyModel(BaseModel):
    field: str
    
    @field_validator("field")
    @classmethod
    def validate_field(cls, v):
        if not v:
            raise ValueError("Field cannot be empty")
        return v
```

## Project Generation Workflow

1. **User Input** → `main.py` (entry point)
2. **Planner Agent** → Creates `Plan` object
3. **Architect Agent** → Creates `TaskPlan` with tasks
4. **Coder Agent** → Implements each task
5. **Output** → Files in `generated_project/`

## Environment Variables

```env
# Required
GROQ_API_KEY=sk_live_xxx

# Optional
LANGCHAIN_DEBUG=true
LANGCHAIN_VERBOSE=true
```

## Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -e .` again |
| API errors | Check GROQ_API_KEY in .env |
| File not found | Check `generated_project/` directory |
| Permission denied | Check folder permissions |
| Out of memory | Reduce `--recursion-limit` |

## File Locations

| What | Where |
|------|-------|
| Generated projects | `f:\Lovable_Clone\generated_project\` |
| Project config | `f:\Lovable_Clone\pyproject.toml` |
| Environment vars | `f:\Lovable_Clone\.env` |
| Python cache | `f:\Lovable_Clone\Agent\__pycache__\` |
| Lock file | `f:\Lovable_Clone\uv.lock` |

## Key Improvements (TL;DR)

- ✅ **Better Imports**: No more wildcard imports
- ✅ **Safer**: Input validation and error handling
- ✅ **Documented**: Comprehensive docstrings
- ✅ **Typed**: Full type hints throughout
- ✅ **Logged**: Complete operation logging
- ✅ **Organized**: Proper package structure
- ✅ **Fixed**: `generated_project/` in correct location

## Performance Tips

1. Use lower recursion limits for faster execution
2. Cache results when possible
3. Monitor logs for slow operations
4. Test with small projects first

## Next Steps

1. Read [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed changes
2. Check [README.md](README.md) for full documentation
3. Run `python main.py` to test the system
4. Review generated files in `generated_project/`

## Contact & Support

- Check logs for error details
- Review docstrings in source code
- See README.md troubleshooting section
- Check existing issues on GitHub

---

**Last Updated:** January 11, 2026  
**Python Version:** 3.14+  
**Status:** ✅ All systems enhanced and ready
