# Claude AI Translation Guide

Complete guide for translating XLIFF files using Claude AI (Anthropic).

## Quick Start

### 1. Get Claude API Key

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-`)

### 2. Install Dependencies

```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts

# Activate virtual environment
source venv/bin/activate

# Install Claude SDK
pip install anthropic
```

### 3. Set API Key

```bash
# Set API key (replace with your actual key)
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Verify it's set
echo "Key: ${ANTHROPIC_API_KEY:0:15}..."
```

### 4. Test Connection

```bash
python test_claude_connection.py
```

Expected output:
```
✓ anthropic package installed
✓ API key found
✓ API connection successful!
✓ Test translation: Connexion réussie !
✅ ALL TESTS PASSED!
```

### 5. Translate Files

```bash
# Single file
python translate_xlf_claude.py -i ../casino-customer-f/src/locale/messages.fr.xlf -l French

# All files
python translate_all_locales_claude.py
```

## Why Use Claude?

### Advantages over OpenAI

✅ **Better Translation Quality** - Claude excels at nuanced language tasks
✅ **Longer Context** - Can handle more context per request
✅ **More Natural** - Produces more human-like translations
✅ **Good at Formatting** - Preserves HTML/XML better
✅ **Multilingual Excellence** - Strong performance across languages

### Claude vs GPT Comparison

| Feature | Claude 3.5 Sonnet | GPT-4 | GPT-3.5-turbo |
|---------|-------------------|-------|---------------|
| Quality | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Great | ⭐⭐⭐ Good |
| Speed | ⚡⚡⚡ Fast | ⚡⚡ Medium | ⚡⚡⚡ Fast |
| Context | 200K tokens | 128K tokens | 16K tokens |
| Cost* | $3/$15 | $10/$30 | $0.50/$1.50 |
| Translation | Excellent | Great | Good |

*Per million tokens (input/output)

## Available Claude Models

### claude-3-5-sonnet-20241022 (Recommended - Default)
- **Best for**: General translation, balanced quality/cost
- **Speed**: Fast
- **Quality**: Excellent
- **Cost**: Moderate ($3 input / $15 output per 1M tokens)
- **Use when**: You want the best quality at reasonable cost

### claude-3-opus-20240229
- **Best for**: Critical, nuanced translations
- **Speed**: Medium
- **Quality**: Best
- **Cost**: Higher ($15 input / $75 output per 1M tokens)
- **Use when**: Quality is paramount

### claude-3-haiku-20240307
- **Best for**: Simple, bulk translations
- **Speed**: Very fast
- **Quality**: Good
- **Cost**: Lower ($0.25 input / $1.25 output per 1M tokens)
- **Use when**: Speed and cost matter more than perfection

## Usage Examples

### Basic Translation

```bash
# Translate French file with default model (Sonnet 3.5)
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.fr.xlf \
  -l French
```

### Use Different Models

```bash
# Use Opus for best quality
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.fr.xlf \
  -l French \
  -m claude-3-opus-20240229

# Use Haiku for fast/cheap translation
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.fr.xlf \
  -l French \
  -m claude-3-haiku-20240307
```

### Batch Processing

```bash
# Translate all languages
python translate_all_locales_claude.py
```

### Advanced Options

```bash
# Larger batches, faster processing
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.es.xlf \
  -l Spanish \
  -b 20 \
  -d 0.5

# Save more frequently (every 2 batches)
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.de.xlf \
  -l German \
  --save-frequency 2

# Force re-translate everything
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.it.xlf \
  -l Italian \
  --no-skip
```

## Cost Estimation

### Claude 3.5 Sonnet (Default - Recommended)

For a typical file with 150 translation units:
- Input tokens: ~7,500
- Output tokens: ~9,000
- **Cost per file**: ~$0.16

For all 9 languages:
- **Total cost**: ~$1.44

### Claude 3 Opus (Highest Quality)

For the same 150 units:
- **Cost per file**: ~$0.80
- **Total (9 languages)**: ~$7.20

### Claude 3 Haiku (Fastest/Cheapest)

For the same 150 units:
- **Cost per file**: ~$0.013
- **Total (9 languages)**: ~$0.12

## Command Reference

### Complete Commands (Copy-Paste Ready)

#### Test Connection
```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts && \
source venv/bin/activate && \
export ANTHROPIC_API_KEY='sk-ant-your-key-here' && \
python test_claude_connection.py
```

#### Translate All Files (Sonnet 3.5)
```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts && \
source venv/bin/activate && \
export ANTHROPIC_API_KEY='sk-ant-your-key-here' && \
python translate_all_locales_claude.py
```

#### Single File Translation
```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts && \
source venv/bin/activate && \
export ANTHROPIC_API_KEY='sk-ant-your-key-here' && \
python translate_xlf_claude.py \
  -i ../casino-customer-f/src/locale/messages.fr.xlf \
  -l French
```

## Features

All features from the OpenAI version are included:

✅ **Auto-Resume** - Checks existing translations, skips them
✅ **Progress Bars** - Real-time batch and item progress
✅ **Auto-Save** - Saves every N batches (default: 5)
✅ **Error Handling** - Graceful error recovery
✅ **Batch Processing** - Efficient API usage
✅ **XML Preservation** - Maintains all structure and formatting

## Progress Display

```
======================================================================
XLIFF Translation (Claude AI): messages.fr.xlf → French
Model: claude-3-5-sonnet-20241022
======================================================================
Total trans-units: 150
Already translated: 0
To translate: 150
======================================================================

Batches:       40%|████████            | 8/20 [01:20<02:00, 10.0s/batch]
Translations:  53%|██████████          | 80/150 [01:20<01:10, 1.0item/s]
💾 Progress saved to messages.fr.xlf
```

## Troubleshooting

### Error: "ANTHROPIC_API_KEY environment variable not set"

```bash
# Set the key
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Verify
echo $ANTHROPIC_API_KEY
```

### Error: "anthropic package not installed"

```bash
# Install it
pip install anthropic

# Or reinstall all dependencies
pip install -r requirements.txt
```

### Poor Translation Quality

Try a better model:
```bash
# Use Opus instead of Sonnet
python translate_xlf_claude.py \
  -i messages.fr.xlf \
  -l French \
  -m claude-3-opus-20240229
```

### Rate Limit Errors

Slow down API calls:
```bash
python translate_xlf_claude.py \
  -i messages.fr.xlf \
  -l French \
  -d 2.0  # 2 second delay between batches
```

### Script Crashed Mid-Translation

Just run it again - it will resume automatically:
```bash
# Run the same command again
python translate_xlf_claude.py -i messages.fr.xlf -l French
# It will skip already-translated items
```

## Best Practices

### 1. Start with Sonnet 3.5 (Default)
It offers the best balance of quality, speed, and cost.

### 2. Test First
Always test with `test_claude_connection.py` before bulk translation.

### 3. Use Auto-Resume
Don't use `--no-skip` unless you specifically want to re-translate everything.

### 4. Monitor Costs
Check your usage at: https://console.anthropic.com/settings/usage

### 5. Save API Key Securely
```bash
# Add to your shell profile for persistence
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key"' >> ~/.bashrc
source ~/.bashrc
```

## Comparison with OpenAI

### When to Use Claude:
- ✅ You want better translation quality
- ✅ You need longer context (200K tokens)
- ✅ You prefer more natural-sounding translations
- ✅ You're translating nuanced or creative content

### When to Use OpenAI:
- ✅ You need the absolute lowest cost (GPT-3.5-turbo)
- ✅ You're already using OpenAI for other tasks
- ✅ You prefer GPT-4's specific style

### Cost Comparison (150 items per file, 9 languages)

| Provider | Model | Total Cost | Quality |
|----------|-------|------------|---------|
| Claude | Haiku | ~$0.12 | Good ⭐⭐⭐ |
| OpenAI | GPT-3.5-turbo | ~$1.50 | Good ⭐⭐⭐ |
| **Claude** | **Sonnet 3.5** | **~$1.44** | **Excellent ⭐⭐⭐⭐⭐** |
| OpenAI | GPT-4 | ~$13.50 | Great ⭐⭐⭐⭐ |
| Claude | Opus | ~$7.20 | Best ⭐⭐⭐⭐⭐ |

**Recommendation**: Use Claude Sonnet 3.5 - best quality for the cost!

## Getting Help

- **Script Help**: `python translate_xlf_claude.py --help`
- **Anthropic Docs**: https://docs.anthropic.com/
- **API Console**: https://console.anthropic.com/
- **Pricing**: https://www.anthropic.com/pricing

## Summary

Claude AI offers excellent translation quality at competitive prices. The default model (Sonnet 3.5) provides the best balance for most use cases.

**Quick Command to Get Started:**
```bash
cd /Users/kakha/Code/casino/Software-Engineer-AI-Agent-Atlas/casino/scripts && \
source venv/bin/activate && \
export ANTHROPIC_API_KEY='sk-ant-your-key-here' && \
python translate_all_locales_claude.py
```

Happy translating! 🚀
