# Quick Start Guide - XLIFF Translation

## 1-Minute Setup

### Install Dependencies
```bash
cd scripts
pip install -r requirements.txt
```

### Set API Key
```bash
export OPENAI_API_KEY='sk-your-api-key-here'
```

### Run Translation
```bash
# Translate French file
python translate_xlf.py -i ../casino-customer-f/src/locale/messages.fr.xlf -l French

# Or translate all languages at once
python translate_all_locales.py
```

## What You'll See

```
======================================================================
XLIFF Translation: messages.fr.xlf → French
======================================================================
Total trans-units: 150
Already translated: 0
To translate: 150
======================================================================

Batches:       45%|█████████           | 9/20 [01:30<01:50, 10.0s/batch]
Translations:  60%|████████████        | 90/150 [01:30<01:00, 1.0item/s]
💾 Progress saved to messages.fr.xlf
```

## Key Features

✅ **Auto-Resume** - If it crashes, just run again! Progress is saved.
✅ **Progress Bars** - See real-time translation progress
✅ **Auto-Save** - Saves every 5 batches by default
✅ **Skip Existing** - Only translates empty targets by default
✅ **Cost Efficient** - Batch processing reduces API calls

## Common Commands

```bash
# Basic usage (recommended)
python translate_xlf.py -i messages.fr.xlf -l French

# Use GPT-4 for better quality
python translate_xlf.py -i messages.fr.xlf -l French -m gpt-4

# Faster processing
python translate_xlf.py -i messages.fr.xlf -l French -b 20 -d 0.5

# Force re-translate everything
python translate_xlf.py -i messages.fr.xlf -l French --no-skip

# Translate all languages
python translate_all_locales.py
```

## If Something Goes Wrong

**Script crashed?**
```bash
# Just run it again - it will resume automatically!
python translate_xlf.py -i messages.fr.xlf -l French
```

**Rate limit error?**
```bash
# Slow down API calls
python translate_xlf.py -i messages.fr.xlf -l French -d 2.0
```

**Want fresh start?**
```bash
# Re-translate everything
python translate_xlf.py -i messages.fr.xlf -l French --no-skip
```

## Cost Estimation

- **Small file (50 items)**: ~$0.02 - $0.05 (GPT-3.5-turbo)
- **Medium file (200 items)**: ~$0.10 - $0.20 (GPT-3.5-turbo)
- **Large file (500 items)**: ~$0.25 - $0.50 (GPT-3.5-turbo)

GPT-4 costs about 20x more but provides better quality.

## Need Help?

Full documentation: `README_TRANSLATION.md`

Command help:
```bash
python translate_xlf.py --help
```

That's it! Happy translating! 🚀
