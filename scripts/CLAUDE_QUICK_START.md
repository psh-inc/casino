# Claude AI Translation - Quick Start

## 🚀 30-Second Setup

### 1. Get API Key
Go to https://console.anthropic.com/ → API Keys → Create Key

### 2. Install & Test

```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts

# Activate virtual environment
source venv/bin/activate

# Install Claude SDK
pip install anthropic

# Set API key (replace with your actual key)
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Test connection
python test_claude_connection.py
```

### 3. Translate All Files

```bash
python translate_all_locales_claude.py
```

**That's it!** 🎉

---

## One-Line Command (Copy-Paste)

```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts && \
source venv/bin/activate && \
export ANTHROPIC_API_KEY='sk-ant-your-key-here' && \
python translate_all_locales_claude.py
```

**⚠️ Replace `sk-ant-your-key-here` with your actual API key!**

---

## What You'll See

```
============================================================
BATCH TRANSLATION WITH CLAUDE AI
============================================================
Locale directory: ../casino-customer-f/src/locale
Files to translate: 9
Model: claude-haiku-4-5-20251001 (Haiku 4.5)
============================================================

Proceed with translation? This will use Claude API credits. (y/N): y

======================================================================
XLIFF Translation (Claude AI): messages.fr.xlf → French
Model: claude-haiku-4-5-20251001
======================================================================
Total trans-units: 150
Already translated: 0
To translate: 150
======================================================================

Batches:       40%|████████            | 8/20 [01:20<02:00, 10.0s/batch]
Translations:  53%|██████████          | 80/150 [01:20<01:10, 1.0item/s]
💾 Progress saved to messages.fr.xlf
```

---

## Model Information

**Default Model**: `claude-haiku-4-5-20251001` (Claude Haiku 4.5)

### Why Haiku 4.5?
- ✅ **Fastest** - Blazing fast responses
- ✅ **Cheapest** - ~$0.01 per file
- ✅ **Great Quality** - Excellent for translations
- ✅ **Latest** - Newest Claude model (Oct 2024)

### Cost Estimate
- **Per file (150 items)**: ~$0.01
- **All 9 languages**: ~$0.10
- **Much cheaper than GPT!**

---

## Available Models

Change model with `-m` flag:

```bash
# Use default Haiku 4.5 (fastest, cheapest)
python translate_xlf_claude.py -i messages.fr.xlf -l French

# Use Sonnet 3.5 (better quality, more expensive)
python translate_xlf_claude.py -i messages.fr.xlf -l French -m claude-3-5-sonnet-20241022

# Use Opus (best quality, most expensive)
python translate_xlf_claude.py -i messages.fr.xlf -l French -m claude-3-opus-20240229
```

| Model | Speed | Quality | Cost/file | Best For |
|-------|-------|---------|-----------|----------|
| **Haiku 4.5** (default) | ⚡⚡⚡ | ⭐⭐⭐⭐ | $0.01 | General use |
| Sonnet 3.5 | ⚡⚡ | ⭐⭐⭐⭐⭐ | $0.16 | High quality |
| Opus | ⚡ | ⭐⭐⭐⭐⭐ | $0.80 | Critical content |

---

## Common Commands

```bash
# Translate all languages (recommended)
python translate_all_locales_claude.py

# Translate single file
python translate_xlf_claude.py -i ../casino-customer-f/src/locale/messages.fr.xlf -l French

# Test API connection first
python test_claude_connection.py

# Use better model for one file
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.fr.xlf \
  -l French \
  -m claude-3-5-sonnet-20241022
```

---

## Key Features

✅ **Auto-Resume** - Script crashed? Just run again, it continues where it stopped
✅ **Progress Bars** - See real-time progress
✅ **Auto-Save** - Saves every 5 batches
✅ **Smart Skip** - Only translates empty items
✅ **Fast** - Haiku 4.5 is incredibly fast
✅ **Cheap** - ~$0.10 for all 9 languages

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key'
```

### "anthropic package not installed"
```bash
pip install anthropic
```

### Want to re-translate everything?
```bash
python translate_xlf_claude.py -i messages.fr.xlf -l French --no-skip
```

### Script crashed?
Just run the same command again - it will resume!

---

## Full Documentation

- **Detailed Guide**: `CLAUDE_GUIDE.md`
- **Script Help**: `python translate_xlf_claude.py --help`
- **Anthropic Docs**: https://docs.anthropic.com/

---

## Security Note

**Never share your API key publicly!**

Always use environment variables:
```bash
# Good ✅
export ANTHROPIC_API_KEY='sk-ant-...'

# Bad ❌
python script.py --api-key 'sk-ant-...'  # Don't do this!
```

---

## Summary

Claude Haiku 4.5 is:
- **10x cheaper** than GPT-4
- **Comparable to GPT-3.5** in cost
- **Better quality** than GPT-3.5
- **Faster** than most models
- **Perfect for translations**

**Ready to translate?**
```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts && \
source venv/bin/activate && \
export ANTHROPIC_API_KEY='sk-ant-your-key-here' && \
python translate_all_locales_claude.py
```

🎉 **Happy translating!**
