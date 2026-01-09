# ⚠️ IMPORTANT SECURITY NOTICE

## You Shared Your API Key Publicly!

You just shared your OpenAI API key in plain text. This is a serious security risk!

### Immediate Actions Required:

1. **Go to OpenAI Platform**: https://platform.openai.com/api-keys
2. **Find your key** (starts with `sk-proj-ISwVWByW2...`)
3. **Click "Revoke"** to disable it immediately
4. **Create a NEW key** and keep it secure

## Why This Matters

- Anyone who saw that key can use YOUR OpenAI credits
- Your API usage could be abused
- You could be charged for unauthorized usage
- The key is now in chat history and potentially logs

## How to Use API Keys Securely

### ❌ NEVER DO THIS:
```bash
# Don't hardcode in files
api_key = "sk-proj-ISwVWByW2..."

# Don't share in chat
# Don't commit to git
# Don't share in screenshots
```

### ✅ ALWAYS DO THIS:
```bash
# Use environment variables
export OPENAI_API_KEY='your-new-key-here'

# Or add to your shell profile (recommended)
echo 'export OPENAI_API_KEY="your-new-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Safe Testing Procedure

After you create a NEW key:

### Step 1: Set Environment Variable
```bash
# Set the key (replace with your NEW key)
export OPENAI_API_KEY='sk-your-new-key-here'

# Verify it's set
echo $OPENAI_API_KEY
```

### Step 2: Run Test Script
```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts
python test_openai_connection.py
```

### Step 3: If Test Passes, Run Translation
```bash
python translate_xlf.py \
  -i ../casino-customer-f/src/locale/messages.fr.xlf \
  -l French
```

## Best Practices

1. **Never share API keys** in chat, email, or public forums
2. **Always use environment variables** for sensitive data
3. **Rotate keys regularly** (every 90 days)
4. **Set usage limits** on OpenAI dashboard
5. **Monitor usage** regularly
6. **Use .gitignore** to exclude any files with keys
7. **Revoke immediately** if key is compromised

## Next Steps

1. ✅ Revoke the old key (the one you shared)
2. ✅ Create a new key
3. ✅ Set it as environment variable
4. ✅ Run test script: `python test_openai_connection.py`
5. ✅ If successful, run translation script

---

**Remember**: API keys are like passwords. Never share them!
