# Custom API Configuration - System Flow

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPANIO APPLICATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           USER INTERFACE LAYER                        │   │
│  │  ┌────────────────────┬────────────────────────────┐ │   │
│  │  │  Streamlit Web UI  │   Command Line Interface  │ │   │
│  │  │  (streamlit_app.py)│   (main.py)               │ │   │
│  │  └────────────────────┴────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      CONFIGURATION MANAGEMENT LAYER                  │   │
│  │  (Agent/config.py)                                   │   │
│  │  ├─ Load/Save Configuration                          │   │
│  │  ├─ Validate API Settings                            │   │
│  │  └─ Environment Variable Support                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        LOCAL STORAGE (~/.companio/config.json)      │   │
│  │  {                                                   │   │
│  │    "api_provider": "google|openai|anthropic",       │   │
│  │    "api_key": "your-api-key",                       │   │
│  │    "model_name": "model-identifier"                 │   │
│  │  }                                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         LLM INITIALIZATION LAYER                      │   │
│  │  (Agent/graph.py - initialize_llm())                │   │
│  │  ├─ Read Configuration                               │   │
│  │  ├─ Select Provider                                  │   │
│  │  └─ Instantiate LLM                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         API PROVIDER LAYER                            │   │
│  │  ┌──────────────┬──────────────┬──────────────┐      │   │
│  │  │    Google    │    OpenAI    │  Anthropic   │      │   │
│  │  │  Generative  │              │              │      │   │
│  │  │     AI       │              │              │      │   │
│  │  └──────────────┴──────────────┴──────────────┘      │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           AGENT WORKFLOW                              │   │
│  │  (Agent/graph.py - planner → architect → coder)      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 User Flow Diagram

### First Time - Streamlit Web UI

```
START
  │
  ├─→ Launch: streamlit run streamlit_app.py
  │
  ├─→ Check Configuration
  │    └─→ is_configured() → False
  │
  ├─→ Display API Configuration Modal
  │    │
  │    ├─→ Select Provider: [Google ▼]
  │    ├─→ Enter API Key: [••••••••]
  │    ├─→ Enter Model: [gemini-2.5-flash]
  │    │
  │    └─→ Click "✅ Save Configuration"
  │
  ├─→ Save to ~/.companio/config.json
  │
  ├─→ Reinitialize LLM
  │
  └─→ Display Main Application
      │
      ├─→ Sidebar shows current configuration
      ├─→ User can click "🔄 Change API Settings" to modify
      │
      └─→ Ready for project input!
```

### First Time - CLI Interface

```
START
  │
  ├─→ Run: python main.py
  │
  ├─→ Check Configuration
  │    └─→ is_configured() → False
  │
  ├─→ Display Setup Wizard
  │    │
  │    ├─→ "Select provider (1-3):"
  │    │    1. google
  │    │    2. openai
  │    │    3. anthropic
  │    │
  │    ├─→ User enters: 1
  │    │
  │    ├─→ Show: "Get your API key: https://..."
  │    ├─→ Prompt: "Enter your google API key:"
  │    │
  │    ├─→ User enters: AIzaSy...
  │    │
  │    ├─→ Prompt: "Enter model name (default: gemini-2.5-flash):"
  │    │
  │    ├─→ User enters: [blank or custom model]
  │    │
  │    └─→ "✅ Configuration saved successfully!"
  │
  ├─→ Save to ~/.companio/config.json
  │
  ├─→ Prompt: "What would you like to build:"
  │
  └─→ Agent processes request!
```

### Subsequent Uses - Both Interfaces

```
START
  │
  ├─→ Application launches
  │
  ├─→ Check Configuration
  │    └─→ is_configured() → True
  │
  ├─→ Load config from ~/.companio/config.json
  │
  ├─→ Initialize LLM with saved settings
  │
  ├─→ Show main application immediately
  │
  └─→ (Optional) User can change settings anytime
     ├─→ Streamlit: Sidebar → "🔄 Change API Settings"
     └─→ CLI: python main.py --setup-api
```

## 📦 Component Dependencies

```
User Interface (streamlit_app.py / main.py)
         ↓
Configuration Module (Agent/config.py)
         ↓
File System (~/.companio/config.json)
         ↓
LLM Factory (initialize_llm in Agent/graph.py)
         ↓
Provider Libraries:
├─ langchain-google-genai (ChatGoogleGenerativeAI)
├─ langchain-openai (ChatOpenAI)
└─ langchain-anthropic (ChatAnthropic)
         ↓
AI Provider APIs (Google, OpenAI, Anthropic)
```

## 🔐 Security Flow

```
User enters API Key
    ↓
[Validation Check]
    ├─→ Key not empty? ✓
    ├─→ Model name provided? ✓
    │
    └─→ All valid? → YES
           ↓
    [Encrypt if needed] (Optional: User can add encryption)
           ↓
    [Save to local ~/.companio/config.json]
           ↓
    [File permissions: 600 (user read/write only)]
           ↓
    [Load when needed]
           ↓
    [Pass to LLM provider]
           ↓
    [Never logged or transmitted elsewhere]
```

## 🔄 Configuration Update Flow

```
User clicks "🔄 Change API Settings"
    ↓
Show Configuration Modal/Wizard
    ↓
User enters new provider/key/model
    ↓
[Validation]
    ├─→ Valid? → YES
    │        ↓
    │   update_api_config(provider, key, model)
    │        ↓
    │   Save to ~/.companio/config.json
    │        ↓
    │   Reinitialize LLM
    │        ↓
    │   ✅ Success message
    │        ↓
    │   Reload application
    │
    └─→ Invalid? → NO
             ↓
         ❌ Show error message
             ↓
         Ask user to correct input
```

## 📊 Data Storage Schema

```
~/.companio/config.json
┌────────────────────────────────────────┐
│ {                                      │
│   "api_provider": "google",            │ ← Provider type
│   "api_key": "AIzaSy...",              │ ← Sensitive (local only)
│   "model_name": "gemini-2.5-flash"     │ ← Model identifier
│ }                                      │
└────────────────────────────────────────┘
```

## 🔌 Provider Integration Points

```
GOOGLE GENERATIVE AI
├─ Library: langchain-google-genai
├─ Class: ChatGoogleGenerativeAI
├─ Required: api_key parameter
├─ Model param: model="gemini-2.5-flash"
└─ Endpoint: Google AI API

OPENAI
├─ Library: langchain-openai
├─ Class: ChatOpenAI
├─ Required: api_key parameter
├─ Model param: model="gpt-4"
└─ Endpoint: OpenAI API

ANTHROPIC
├─ Library: langchain-anthropic
├─ Class: ChatAnthropic
├─ Required: api_key parameter
├─ Model param: model="claude-3-5-sonnet-20241022"
└─ Endpoint: Anthropic API
```

## 🚀 Initialization Sequence

```
Application Startup
    ↓
[1. Import Modules]
    ├─ streamlit_app.py or main.py
    ├─ Agent.config
    ├─ Agent.graph
    └─ Agent.states
    ↓
[2. Initialize Session State] (Streamlit only)
    ├─ execution_history = []
    ├─ api_configured = is_configured()
    └─ show_api_config = not is_configured()
    ↓
[3. Check Configuration]
    ├─→ Configuration exists?
    │        ├─ YES → Load and validate
    │        └─ NO → Show setup wizard
    │
    └─→ API key and model valid?
             ├─ YES → Continue
             └─ NO → Show error, ask to reconfigure
    ↓
[4. Initialize LLM]
    ├─ Call initialize_llm()
    ├─ Get api_provider, api_key, model_name
    ├─ Create appropriate LLM instance
    └─ Set as global llm variable
    ↓
[5. Ready for Use]
    └─ Application fully initialized
```

## 📈 State Management (Streamlit)

```
Session State Structure:
{
  "execution_history": [      # Past executions
    {
      "timestamp": "...",
      "prompt": "...",
      "stages": {...},
      "final_state": {...},
      "error": null/error_msg
    }
  ],
  "current_execution": null,  # Selected from history
  "agent_state": {...},       # Current agent state
  "api_configured": True,     # API is configured
  "show_api_config": False    # Show config modal
}
```

## 🔧 Configuration Functions Map

```
config.py Functions:
├─ ensure_config_dir()          → Create ~/.companio
├─ load_config()                → Read from config.json
├─ save_config(config)          → Write to config.json
├─ get_default_config()         → Return defaults
├─ is_configured()              → Check if ready
├─ get_api_key()                → Return API key
├─ get_model_name()             → Return model name
├─ get_api_provider()           → Return provider
└─ update_api_config(p,k,m)     → Update all three

graph.py Functions:
└─ initialize_llm()             → Create LLM from config
```

---

This visual documentation helps understand how all components work together to provide a seamless API configuration experience!
