# Quick Start Guide - Custom API Configuration

## 🚀 Getting Started

### Option 1: Streamlit Web Interface (Recommended for most users)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run streamlit_app.py
```

**What happens:**
- 🖥️ Web browser opens automatically
- ⚙️ You see API Configuration screen on first run
- 📋 Fill in your API provider, key, and model
- ✅ Click "Save Configuration"
- 🎉 Start using the app!

### Option 2: Command Line Interface (for CLI users)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app (first time)
python main.py
```

**What happens:**
- 📝 Interactive setup wizard appears
- 🔢 Choose your API provider (1, 2, or 3)
- 🔑 Paste your API key
- 📊 Confirm model name
- ✅ Start building!

---

## 🔑 Getting Your API Key

### Google (Recommended - Free tier available)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Paste into Companio

**Best Models:**
- `gemini-2.5-flash` (Recommended)
- `gemini-2.0-flash`

### OpenAI
1. Visit: https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key
4. Paste into Companio

**Best Models:**
- `gpt-4` (Most powerful)
- `gpt-4-turbo` (Faster)

### Anthropic
1. Visit: https://console.anthropic.com/
2. Go to "API Keys"
3. Create new key
4. Copy and paste into Companio

**Best Models:**
- `claude-3-5-sonnet-20241022` (Recommended)
- `claude-3-opus-20240229` (Most powerful)

---

## 💻 Using the App

### First Time Setup

**Streamlit:**
```
1. Open http://localhost:8501
2. See "⚙️ API Configuration" modal
3. Select your API provider
4. Enter API key
5. Enter model name
6. Click "✅ Save Configuration"
```

**CLI:**
```
1. Run: python main.py
2. See: "🤖 API Configuration Setup"
3. Choose provider: 1 (Google), 2 (OpenAI), or 3 (Anthropic)
4. Paste API key
5. Confirm model name
6. Enter your project description
```

### After Setup

**Streamlit:**
- Use normally - configuration remembered
- Change settings: Sidebar → "🔄 Change API Settings"

**CLI:**
- Use normally: `python main.py`
- Change settings: `python main.py --setup-api`

---

## 🔄 Changing API Configuration

### Via Streamlit
1. Look at sidebar
2. Find "🔑 API Configuration"
3. Click "🔄 Change API Settings"
4. Enter new details
5. Click "✅ Save Configuration"

### Via CLI
```bash
python main.py --setup-api
```

---

## 📂 Where is My Configuration Stored?

Your API configuration is saved locally (never sent anywhere):

**Windows:**
```
C:\Users\YourName\.companio\config.json
```

**Mac/Linux:**
```
~/.companio/config.json
```

**What's in the file:**
```json
{
  "api_provider": "google",
  "api_key": "your-key-here",
  "model_name": "gemini-2.5-flash"
}
```

---

## ⚡ Quick Tips

### 💡 Best Practices
- ✅ Use different API keys for development and production
- ✅ Keep your API keys secret (don't commit to git)
- ✅ Use .env files for sensitive data in development
- ✅ Regenerate keys if they're compromised

### 🆓 Free Options
- **Google:** Free tier available (Gemini 2.5 Flash)
- **OpenAI:** Free trial credits
- **Anthropic:** Check their pricing

### 🚀 Performance
- **Fastest:** Gemini 2.5 Flash, GPT-4 Turbo
- **Most Powerful:** Claude 3 Opus, GPT-4
- **Best Balance:** Gemini 2.5 Flash, Claude 3.5 Sonnet

---

## ❓ Troubleshooting

### "API Configuration Error"
**Problem:** Can't find my API key
**Solution:** Make sure you're copying the full key with no extra spaces

### "Invalid API Key"
**Problem:** Getting authentication error
**Solution:** 
- Check the key is correct
- Verify it's for the selected provider
- Make sure your account has credits/quota

### "Model Not Found"
**Problem:** Getting model error
**Solution:**
- Double-check model name spelling
- Verify model is available in your region
- Check provider documentation

### Configuration Not Saving?
**Problem:** Changes not persisting
**Solution:**
- Check home directory is writable
- Ensure `.companio` folder can be created
- Restart the application
- Check disk space available

---

## 🎯 Example Setups

### Setup 1: Google Gemini (Recommended)
```
Provider: google
API Key: AIzaSy...
Model: gemini-2.5-flash
```

### Setup 2: OpenAI GPT-4
```
Provider: openai
API Key: sk-proj-...
Model: gpt-4
```

### Setup 3: Anthropic Claude
```
Provider: anthropic
API Key: sk-ant-...
Model: claude-3-5-sonnet-20241022
```

---

## 📚 Next Steps

1. **Configure API** - Follow the setup wizard
2. **Describe Your Project** - Tell Companio what to build
3. **Watch It Work** - Real-time planning and code generation
4. **Review Results** - Check generated code and architecture

---

## 🆘 Need Help?

- **Documentation:** See CUSTOM_API_GUIDE.md for detailed info
- **Implementation Details:** See CUSTOM_API_IMPLEMENTATION.md
- **Issues:** Check troubleshooting section above

---

**Ready to build? Let's go! 🚀**
