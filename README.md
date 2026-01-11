# Lovable Clone - Engineering Project Planner

A multi-agent system powered by LangGraph and Groq that automatically plans, architects, and implements software projects based on natural language descriptions.

## Features

- **Planner Agent**: Converts user requirements into a comprehensive project plan
- **Architect Agent**: Breaks down the project into explicit implementation tasks
- **Coder Agent**: Implements each task by generating and integrating code files
- **Safety Mechanisms**: Path validation to prevent directory traversal attacks
- **Comprehensive Logging**: Built-in logging for debugging and monitoring

## Project Structure

```
.
├── main.py                 # Entry point for the application
├── pyproject.toml         # Project configuration and dependencies
├── README.md              # This file
├── Agent/
│   ├── __init__.py       # Package initialization with exports
│   ├── graph.py          # Multi-agent workflow orchestration
│   ├── states.py         # Pydantic models for type-safe state management
│   ├── tools.py          # File I/O and command execution tools
│   └── prompts.py        # LLM prompt templates
└── generated_project/     # Output directory for generated projects
```

## Installation

### Prerequisites
- Python 3.14+
- uv (recommended) or pip for package management

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd Lovable_Clone

# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using uv
uv pip install -e .

# Or using pip
pip install -e .

# Set up environment variables
cp .env.example .env  # If provided
# Edit .env with your Groq API key
```

## Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

## Usage

### Running the Application

```bash
python main.py [--recursion-limit N]
```

### Options

- `--recursion-limit`, `-r`: Maximum recursion depth for agent loops (default: 100, max: 1000)

### Example

```bash
# Run with default settings
python main.py

# Specify custom recursion limit
python main.py --recursion-limit 50
```

### Interactive Usage

```
$ python main.py
What would you like to build: A REST API for managing tasks with authentication

[The agent will then:
1. Create a project plan
2. Break it into implementation tasks
3. Generate all necessary code files]

Final State: {...}
```

## Architecture

### Agent Workflow

1. **Planner Node**: Receives user input and generates a structured project plan including:
   - Project name and description
   - Technology stack
   - Feature list
   - File structure

2. **Architect Node**: Transforms the plan into implementation tasks with:
   - Specific file paths
   - Detailed task descriptions
   - Dependency information

3. **Coder Node**: Implements tasks iteratively by:
   - Reading existing files
   - Writing new code
   - Managing project structure

### State Management

The system uses `AgentState` (TypedDict) to maintain context through the workflow:

```python
class AgentState(TypedDict):
    user_prompt: str              # Original user request
    project_plan: Plan            # Structured project plan
    architect_plan: List[str]     # Implementation tasks
    coder_state: CoderState       # Current coding state
    status: str                   # Workflow status
```

### Safety Features

- **Path Validation**: All file operations are sandboxed within `generated_project/`
- **Directory Traversal Prevention**: Automatic validation prevents accessing files outside project root
- **Error Handling**: Comprehensive exception handling with detailed logging
- **Input Validation**: All user inputs are validated before processing

## Code Quality Improvements

### Recent Enhancements

1. **Imports Management**
   - Replaced wildcard imports with explicit imports
   - Added relative imports for internal modules
   - Improved package organization with `__init__.py`

2. **Type Safety**
   - Added field validators to Pydantic models
   - Improved TypedDict documentation
   - Better type hints throughout

3. **Error Handling**
   - Added input validation in all agents
   - Improved error messages with context
   - Proper exception propagation

4. **Documentation**
   - Comprehensive docstrings for all functions
   - Module-level documentation
   - Clear parameter descriptions

5. **Logging**
   - Structured logging throughout the application
   - Different log levels for different operations
   - Easy debugging and monitoring

6. **Code Readability**
   - Improved variable naming conventions
   - Better code organization and structure
   - Clearer control flow logic

7. **File Organization**
   - Fixed typos (e.g., "withing" → "within")
   - Improved prompt quality and formatting
   - Better path handling for generated projects

## Troubleshooting

### Import Errors

If you encounter import errors:

```bash
# Ensure you're in the correct directory
cd /path/to/Lovable_Clone

# Reinstall the package
pip install -e .
```

### Groq API Issues

- Verify your API key is set in `.env`
- Check API rate limits
- Ensure network connectivity

### Generated Project Issues

Generated projects are stored in `generated_project/` in the current working directory. Check:
- File permissions
- Disk space availability
- Path syntax for the operating system

## Development

### Adding New Agents

To extend the system with new agents:

1. Create a new function in `graph.py`
2. Add it as a node to the workflow graph
3. Define appropriate state transformations
4. Update prompts in `prompts.py` if needed

### Testing

```bash
# Run tests (if available)
pytest

# Run with verbose logging
python main.py -v
```

## Dependencies

Core dependencies:
- `langchain>=0.3.27` - LLM framework
- `langchain-groq>=0.3.7` - Groq integration
- `langgraph>=0.6.3` - Graph-based workflow
- `pydantic>=2.11.7` - Data validation
- `python-dotenv>=1.1.1` - Environment management

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions:
1. Check existing GitHub issues
2. Review the troubleshooting section
3. Check logs for error details
4. Create a new issue with detailed information

## Future Enhancements

- [ ] Support for multiple LLM providers
- [ ] Project templates and scaffolding
- [ ] Advanced caching mechanisms
- [ ] Interactive project review before generation
- [ ] Multi-language support
- [ ] Integration with version control systems
