# XLIFF Translation Scripts

This directory contains Python scripts for translating Angular i18n XLIFF files using OpenAI's GPT models.

## Files

- **translate_xlf.py** - Main translation script for single files
- **translate_all_locales.py** - Batch script to translate all locale files
- **requirements.txt** - Python dependencies

## Setup

### 1. Install Dependencies

```bash
# Navigate to scripts directory
cd scripts

# Install requirements
pip install -r requirements.txt
```

### 2. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set it as an environment variable:

```bash
# Linux/Mac
export OPENAI_API_KEY='sk-your-api-key-here'

# Windows (CMD)
set OPENAI_API_KEY=sk-your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY='sk-your-api-key-here'
```

Or add it to your `~/.bashrc` or `~/.zshrc` for persistence:
```bash
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Translate a Single File

Basic usage:
```bash
python translate_xlf.py -i ../casino-customer-f/src/locale/messages.fr.xlf -l French
```

With all options:
```bash
python translate_xlf.py \
  --input ../casino-customer-f/src/locale/messages.fr.xlf \
  --language French \
  --output messages.fr.translated.xlf \
  --model gpt-4 \
  --batch-size 10 \
  --delay 1.0 \
  --save-frequency 5
```

### Options

- `-i, --input` - Input XLIFF file (required)
- `-l, --language` - Target language name (required)
- `-o, --output` - Output file path (default: overwrite input)
- `-k, --api-key` - OpenAI API key (default: from env var)
- `-m, --model` - Model to use (default: gpt-3.5-turbo)
  - `gpt-3.5-turbo` - Faster, cheaper
  - `gpt-4` - Higher quality, more expensive
  - `gpt-4-turbo` - Balance of speed and quality
- `-b, --batch-size` - Translations per API call (default: 10)
- `-d, --delay` - Delay between API calls in seconds (default: 1.0)
- `--save-frequency` - Save progress every N batches (default: 5)
- `--no-skip` - Re-translate ALL items even if they have existing translations (default: skip existing)

### Translate All Locale Files

```bash
python translate_all_locales.py
```

This will translate all supported language files:
- French (messages.fr.xlf)
- Spanish (messages.es.xlf)
- German (messages.de.xlf)
- Italian (messages.it.xlf)
- Portuguese (messages.pt.xlf)
- Polish (messages.pl.xlf)
- Swedish (messages.sv.xlf)
- Norwegian (messages.no.xlf)
- Finnish (messages.fi.xlf)

## Key Features

### 🔄 Auto-Resume Capability
The script automatically tracks progress by checking which `<target>` elements already have content. If the script crashes or is interrupted:

1. Simply run the same command again
2. The script will skip already-translated items
3. Translation continues from where it stopped

**Example:**
```bash
# First run (translates 50 items, then crashes)
python translate_xlf.py -i messages.fr.xlf -l French

# Second run (skips the 50 done items, continues with remaining)
python translate_xlf.py -i messages.fr.xlf -l French
```

### 📊 Progress Tracking
- **Two progress bars**: One for batches, one for individual translations
- **Real-time updates**: See translation progress as it happens
- **Statistics**: Shows total items, already translated, remaining, and errors
- **Periodic saves**: File saved every N batches (default: 5) to preserve progress

### 💾 Auto-Save
- Progress saved every 5 batches (configurable with `--save-frequency`)
- Final save at completion
- Safe interruption with Ctrl+C (saves before exit)

## Examples

### Example 1: Basic translation (skips existing by default)

```bash
python translate_xlf.py \
  -i ../casino-customer-f/src/locale/messages.fr.xlf \
  -l French
```

### Example 2: Use GPT-4 for better quality

```bash
python translate_xlf.py \
  -i ../casino-customer-f/src/locale/messages.es.xlf \
  -l Spanish \
  -m gpt-4
```

### Example 3: Re-translate everything (ignore existing translations)

```bash
python translate_xlf.py \
  -i ../casino-customer-f/src/locale/messages.de.xlf \
  -l German \
  --no-skip
```

### Example 4: Test translation without overwriting original

```bash
python translate_xlf.py \
  -i ../casino-customer-f/src/locale/messages.de.xlf \
  -l German \
  -o messages.de.test.xlf
```

### Example 5: Faster batch processing with frequent saves

```bash
python translate_xlf.py \
  -i ../casino-customer-f/src/locale/messages.it.xlf \
  -l Italian \
  -b 20 \
  -d 0.5 \
  --save-frequency 2
```

### Example 6: Resume interrupted translation

```bash
# Script was interrupted? Just run the same command again!
# It will automatically skip already-translated items
python translate_xlf.py -i messages.fr.xlf -l French
```

## Cost Estimation

### GPT-3.5-turbo
- Input: $0.50 / 1M tokens
- Output: $1.50 / 1M tokens
- Average cost per file (100 translations): ~$0.05 - $0.15

### GPT-4
- Input: $10.00 / 1M tokens
- Output: $30.00 / 1M tokens
- Average cost per file (100 translations): ~$1.00 - $3.00

### GPT-4-turbo
- Input: $5.00 / 1M tokens
- Output: $15.00 / 1M tokens
- Average cost per file (100 translations): ~$0.50 - $1.50

**Recommendation**: Use `gpt-3.5-turbo` for general translations, `gpt-4` only for critical or nuanced content.

## How It Works

1. **Parse XML**: Reads the XLIFF file and extracts all `<trans-unit>` elements
2. **Check Progress**: Identifies which `<target>` elements already have content (auto-resume)
3. **Extract Source**: Gets text from `<source>` elements that need translation
4. **Batch Translation**: Groups multiple texts and sends to OpenAI API (efficient API usage)
5. **Update Targets**: Fills `<target>` elements with translations
6. **Periodic Save**: Saves progress every N batches (default: 5) to preserve work
7. **Final Save**: Writes complete file back to XML preserving structure

### Progress Display
```
======================================================================
XLIFF Translation: messages.fr.xlf → French
======================================================================
Total trans-units: 150
Already translated: 50
To translate: 100
======================================================================

Batches:       10%|████                    | 2/20 [00:15<02:30, 8.4s/batch]
Translations:  25%|██████                  | 25/100 [00:15<00:45, 1.6item/s]
💾 Progress saved to messages.fr.xlf
```

### XML Structure

```xml
<trans-unit id="example.id">
  <source>Hello World</source>
  <target>Bonjour le monde</target>
</trans-unit>
```

## Troubleshooting

### Error: "OpenAI API key not provided"
Make sure `OPENAI_API_KEY` environment variable is set:
```bash
echo $OPENAI_API_KEY  # Should print your key
```

### Error: "Rate limit exceeded"
Increase the delay between API calls:
```bash
python translate_xlf.py -i file.xlf -l French -d 2.0
```

### Error: "Module 'openai' not found" or "Module 'tqdm' not found"
Install dependencies:
```bash
pip install -r requirements.txt
```

### Script Crashed or Was Interrupted
**No problem!** Just run the same command again. The script will:
- Detect already-translated items
- Skip them automatically
- Continue from where it stopped

```bash
# Run it again with the exact same command
python translate_xlf.py -i messages.fr.xlf -l French
```

### Want to Start Over from Scratch
Use the `--no-skip` flag to re-translate everything:
```bash
python translate_xlf.py -i file.xlf -l French --no-skip
```

### Poor Translation Quality
Try using GPT-4 instead of GPT-3.5:
```bash
python translate_xlf.py -i file.xlf -l French -m gpt-4
```

### Translations Are Too Literal
The script uses temperature=0.3 for consistency. For more natural translations, edit the script and change `temperature=0.3` to `temperature=0.5` or `0.7`.

### Progress Bars Not Showing
Make sure `tqdm` is installed:
```bash
pip install tqdm
```

## Advanced Usage

### Custom Language

```bash
python translate_xlf.py -i messages.xlf -l "Brazilian Portuguese"
python translate_xlf.py -i messages.xlf -l "Simplified Chinese"
```

### Preserve Backup

```bash
# Create backup
cp ../casino-customer-f/src/locale/messages.fr.xlf ../casino-customer-f/src/locale/messages.fr.xlf.backup

# Translate
python translate_xlf.py -i ../casino-customer-f/src/locale/messages.fr.xlf -l French
```

### Process Multiple Files in Sequence

```bash
#!/bin/bash
for lang in "French:fr" "Spanish:es" "German:de"; do
  IFS=':' read -r language code <<< "$lang"
  python translate_xlf.py \
    -i "../casino-customer-f/src/locale/messages.${code}.xlf" \
    -l "$language" \
    --skip-existing
done
```

## Safety Features

- **Preserves XML structure**: Keeps all attributes, context, and formatting
- **Handles HTML tags**: Preserves `<x>` placeholders and other inline elements
- **Error recovery**: Returns original text if translation fails
- **Skip existing**: Option to only translate empty targets
- **Rate limiting**: Built-in delays to avoid API rate limits
- **Batch processing**: Efficient API usage by grouping translations

## Best Practices

1. **Always backup** original files before translating
2. **Use --skip-existing** to avoid re-translating already done work
3. **Start with one file** to test before batch processing
4. **Review translations** after generation, especially for critical UI text
5. **Use gpt-3.5-turbo** for cost efficiency, gpt-4 for quality
6. **Monitor API usage** at https://platform.openai.com/usage

## Support

For issues or questions:
1. Check this README
2. Review the script help: `python translate_xlf.py --help`
3. Check OpenAI API status: https://status.openai.com/
4. Review OpenAI API docs: https://platform.openai.com/docs

## License

Internal use for casino-customer-f project.
