# Streamlit UI Guide

## Overview
The Streamlit UI provides a user-friendly interface to interact with the AI Agent Debugger. Instead of running the agent from the command line with `python main.py`, you can now use a web-based interface that shows real-time progress and detailed results.

## Features

### 🎯 Main Features
- **Interactive Prompt Input**: Enter your project description in a text area
- **Real-time Progress**: Watch as the agent progresses through planning, architecture, and coding stages
- **Detailed Output Views**: See results organized in tabs:
  - **Plan Tab**: View the project plan with name, description, tech stack, and features
  - **Architecture Tab**: See the breakdown of implementation steps
  - **Code Tasks Tab**: Examine individual coding tasks with descriptions
  - **Full State Tab**: Inspect the complete JSON state

### ⚙️ Settings Panel
Located in the sidebar, you can:
- Adjust the **Recursion Limit** (10-1000, default: 100) to control how deep the agent can recurse
- View **Execution History** with quick access to previous runs
- **Clear History** to reset all past executions

## How to Use

### Starting the Streamlit App

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. The app will open in your default browser at `http://localhost:8501`

### Running an Execution

1. **Enter Project Description**: Type what you want to build in the text area
   - Example: "Build a todo list app with React frontend and Python Flask backend with database"

2. **Adjust Settings (Optional)**: 
   - Use the sidebar to change the recursion limit if needed
   - Default is 100, which works for most projects

3. **Click "Run Agent"**: Press the 🚀 Run Agent button to start execution

4. **Watch Progress**: The UI will show:
   - Status indicator (yellow for running, green for completed)
   - Progress bar
   - Status messages and logs

5. **View Results**: Once complete, results are displayed in tabs

### Viewing History

- The sidebar automatically logs all executions with timestamps
- Click on any historical execution to view its results
- Click "Clear History" to reset the history

## Project Structure

```
streamlit_app.py          # Main Streamlit application
pyproject.toml           # Updated dependencies (includes streamlit)
main.py                  # Original CLI interface (still available)
Agent/
  ├── graph.py           # Agent workflow graph
  ├── states.py          # State definitions
  ├── prompts.py         # LLM prompts
  ├── tools.py           # Agent tools
  └── __init__.py
```

## Environment Variables

The app uses the same environment variables as the CLI version:
- `GOOGLE_API_KEY`: Your Google Generative AI API key (required)

Make sure your `.env` file is configured correctly.

## Example Prompts

Here are some good example prompts to try:

1. **Web Application**:
   > "Build a personal finance tracker web app with React frontend, Node.js backend, and MongoDB database"

2. **Data Processing**:
   > "Create a Python data pipeline that reads CSV files, performs analysis, and generates visualizations"

3. **System Tool**:
   > "Build a CLI tool for managing Docker containers with Python and Click framework"

4. **Full Stack Project**:
   > "Build a social media app with user authentication, posts, comments, and likes using React, Node.js, and PostgreSQL"

## Execution Details

When you run an execution, the agent performs three main stages:

1. **Planning (Stage 1/3)**: 
   - Analyzes your requirements
   - Creates a comprehensive project plan
   - Identifies all files needed

2. **Architecture (Stage 2/3)**:
   - Breaks down the project into implementation steps
   - Creates detailed task descriptions
   - Plans file modifications

3. **Coding (Stage 3/3)**:
   - Implements each task
   - Reads existing content
   - Writes/modifies files as needed

## Output Tabs Explained

### Plan Tab
Shows the structured project plan including:
- Project name
- Description
- Technology stack
- List of features
- Files to be created/modified

### Architecture Tab
Displays implementation steps that break down the project into manageable tasks.

### Code Tasks Tab
Detailed view of each coding task with:
- File path to be modified
- Specific task description
- Task number and status

### Full State Tab
Complete JSON representation of:
- Execution timestamp
- User prompt
- All agent stages and outputs
- Final state information

## Performance Tips

1. **Start with Simpler Prompts**: Begin with smaller projects to test the system
2. **Adjust Recursion Limit**: 
   - Use lower values (50-100) for simpler projects
   - Use higher values (200-500) for complex projects
3. **Check API Quotas**: Ensure your Google API key has sufficient quota
4. **Monitor Logs**: Check the browser console for detailed logs

## Troubleshooting

### App Won't Start
- Ensure all dependencies are installed: `pip install streamlit langchain langgraph`
- Check that your Python version is 3.11 or higher

### Agent Errors
- Check your `.env` file for the correct `GOOGLE_API_KEY`
- Verify internet connection (required for Google API)
- Check error message in the "Full Error Traceback" expandable section

### Slow Performance
- Reduce the recursion limit
- Use simpler project descriptions
- Check your internet connection

## Keyboard Shortcuts

- Ctrl+C: Stop the current execution (in terminal)
- Click on history items to quickly view past results

## Comparison with CLI

| Feature | CLI (main.py) | Streamlit UI |
|---------|---------------|--------------|
| Input | Command line prompt | Text area input |
| Progress Tracking | Basic logging | Real-time visual feedback |
| Output Display | JSON dump | Organized tabs with formatting |
| History | None | Automatic with quick access |
| Customization | Limited | Full sidebar controls |
| User Experience | Developer-focused | User-friendly interface |

## Advanced Features

### Execution History
- Each execution is automatically saved with timestamp
- Access up to 10+ executions from the sidebar
- Useful for comparing different project approaches

### State Inspection
- View the complete agent state in JSON format
- Useful for debugging and understanding agent behavior
- Shows exactly what each stage produced

### Error Handling
- Detailed error messages with full tracebacks
- Non-breaking errors allow partial result viewing
- Clear indication of failure status

---

Enjoy using the AI Agent Debugger with Streamlit! 🚀
