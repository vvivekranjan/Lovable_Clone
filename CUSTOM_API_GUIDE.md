# Custom API Configuration Guide

## Overview
The Companio application now supports custom API configuration, allowing you to use your own API keys and select your preferred AI model provider on first use.

## Features

### 1. Initial Setup
When you first launch the application, you'll be presented with an API configuration modal where you can:
- Select your preferred API provider (Google, OpenAI, or Anthropic)
- Enter your API key
- Choose your model name

### 2. Supported Providers
The application supports three major AI API providers:

#### Google Generative AI
- **Provider:** google
- **Default Model:** gemini-2.5-flash
- **Get API Key:** [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Available Models:**
  - gemini-2.5-flash (recommended)
  - gemini-2.0-flash
  - gemini-pro

#### OpenAI
- **Provider:** openai
- **Default Model:** gpt-4
- **Get API Key:** [OpenAI Platform](https://platform.openai.com/account/api-keys)
- **Available Models:**
  - gpt-4
  - gpt-4-turbo
  - gpt-3.5-turbo

#### Anthropic
- **Provider:** anthropic
- **Default Model:** claude-3-5-sonnet-20241022
- **Get API Key:** [Anthropic Console](https://console.anthropic.com/)
- **Available Models:**
  - claude-3-5-sonnet-20241022 (recommended)
  - claude-3-opus-20240229
  - claude-3-sonnet-20240229

### 3. Configuration Storage
Your API configuration is securely stored locally in:
- **Windows:** `C:\Users\<YourUsername>\.companio\config.json`
- **macOS:** `~/.companio/config.json`
- **Linux:** `~/.companio/config.json`

The configuration file contains:
```json
{
  "api_provider": "google",
  "api_key": "your-api-key-here",
  "model_name": "gemini-2.5-flash"
}
```

### 4. Changing API Configuration
After initial setup, you can change your API settings anytime by:
1. Going to the sidebar in the Streamlit app
2. Clicking "🔄 Change API Settings"
3. Entering your new API details
4. Clicking "✅ Save Configuration"

## Environment Variables

You can also set your API key via environment variables. The application will use environment variables if no configuration file exists:
- **Google:** `GOOGLE_API_KEY`
- **OpenAI:** `OPENAI_API_KEY`
- **Anthropic:** `ANTHROPIC_API_KEY`

## Security Notes
- API keys are stored locally on your machine
- Keys are never shared or transmitted to external services
- Always keep your API keys confidential
- If you suspect your key has been compromised, regenerate it in your provider's console

## Troubleshooting

### "Invalid API Key" Error
- Verify your API key is correct
- Ensure the key is for the selected provider
- Check that your account has sufficient credits/quota

### "Model Not Found" Error
- Verify the model name is spelled correctly
- Ensure the model is available in your account's region
- Check the provider's documentation for available models

### Configuration Not Saving
- Ensure the `.companio` directory can be created in your home folder
- Check file permissions in your home directory
- Restart the application after saving

## Examples

### Using Google's Gemini
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Select "google" as provider
3. Paste your API key
4. Enter model: `gemini-2.5-flash`

### Using OpenAI's GPT-4
1. Get API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Select "openai" as provider
3. Paste your API key
4. Enter model: `gpt-4`

### Using Anthropic's Claude
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Select "anthropic" as provider
3. Paste your API key
4. Enter model: `claude-3-5-sonnet-20241022`

## API Configuration Module

The configuration is managed through the `Agent/config.py` module. Key functions:

- `is_configured()` - Check if API is properly configured
- `load_config()` - Load current configuration
- `save_config(config)` - Save configuration
- `update_api_config(provider, key, model)` - Update API settings
- `get_api_provider()` - Get current provider
- `get_api_key()` - Get current API key
- `get_model_name()` - Get current model name

## What's Next?
Once configured, you can use the Companio application to:
- Plan your engineering projects
- Generate architectural solutions
- Write production-ready code
