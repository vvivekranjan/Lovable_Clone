# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Install Dependencies
```bash
pip install -e .
```

Or use the setup script:
```bash
python setup_streamlit.py
```

### Step 2: Set Up Environment
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_key_here
```

### Step 3: Launch the UI
```bash
streamlit run streamlit_app.py
```

The app opens automatically at `http://localhost:8501`

## 💡 Example Usage

1. **Enter a project description:**
   ```
   Build a todo list web app with React frontend and Flask backend
   ```

2. **Click "Run Agent"** button

3. **Watch in real-time** as the agent:
   - 📋 Plans your project
   - 🏗️ Architects the solution  
   - 💻 Generates the code

4. **View results** in organized tabs:
   - Plan details
   - Architecture breakdown
   - Code tasks
   - Full state JSON

## 📚 More Information

- **Full Guide**: Read [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)
- **Documentation**: See [README.md](README.md)
- **CLI Usage**: Run `python main.py --help`

## ⚙️ Troubleshooting

### Port Already in Use?
```bash
streamlit run streamlit_app.py --server.port 8502
```

### API Key Issues?
- Ensure `.env` file exists with correct `GOOGLE_API_KEY`
- Verify API key is valid and has quota

### Dependencies Not Found?
```bash
pip install -e .
streamlit run streamlit_app.py
```

## 🎯 Next Steps

- Try different project prompts
- Explore the execution history
- Adjust recursion limit for complex projects
- Check generated files in `generated_project/` directory

Enjoy! 🎉
