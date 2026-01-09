#!/usr/bin/env python3
"""
XLIFF Translation Script using Claude AI (Anthropic)

This script translates XLIFF (.xlf) files from source language to target language
using Anthropic's Claude models. Features include:
- Auto-resume capability (tracks progress via target elements)
- Real-time progress bars (batch and item level)
- Automatic periodic saving
- Batch processing for efficiency
- Preserves XML structure

Usage:
    python translate_xlf_claude.py --input messages.fr.xlf --language French
    python translate_xlf_claude.py --input messages.es.xlf --language Spanish --model claude-3-5-sonnet-20241022
    python translate_xlf_claude.py --input messages.de.xlf --language German --batch-size 20

Features:
    - Automatically skips already-translated items (resume on crash)
    - Saves progress every 5 batches (configurable)
    - Shows dual progress bars (batches + individual translations)
    - Safe Ctrl+C interruption (saves before exit)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple
import time
from xml.etree import ElementTree as ET

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed. Install with: pip install anthropic")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    print("Error: tqdm package not installed. Install with: pip install tqdm")
    sys.exit(1)


class XLIFFTranslatorClaude:
    """Handles translation of XLIFF files using Claude AI API"""

    # XML namespace for XLIFF
    XLIFF_NS = "urn:oasis:names:tc:xliff:document:1.2"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-haiku-4-5-20251001",
        batch_size: int = 10,
        delay: float = 1.0
    ):
        """
        Initialize the translator.

        Args:
            api_key: Anthropic API key (if None, reads from ANTHROPIC_API_KEY env var)
            model: Claude model to use (claude-haiku-4-5-20251001, claude-3-5-sonnet-20241022, etc.)
            batch_size: Number of translations to process in one API call
            delay: Delay in seconds between API calls to avoid rate limits
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not provided. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter"
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.batch_size = batch_size
        self.delay = delay

        # Register namespace to preserve xmlns in output
        ET.register_namespace('', self.XLIFF_NS)

    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate a single text using Claude API.

        Args:
            text: Text to translate
            target_language: Target language (e.g., 'French', 'Spanish')

        Returns:
            Translated text
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                system=f"You are a professional translator. Translate the given text to {target_language}. "
                       f"Preserve any HTML tags, placeholders, or special formatting. "
                       f"Only return the translation, no explanations.",
                messages=[
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )

            translation = message.content[0].text.strip()
            return translation

        except Exception as e:
            print(f"Error translating text '{text[:50]}...': {e}")
            return text  # Return original on error

    def translate_batch(self, texts: List[str], target_language: str) -> List[str]:
        """
        Translate multiple texts in a single API call for efficiency.

        Args:
            texts: List of texts to translate
            target_language: Target language

        Returns:
            List of translated texts
        """
        if not texts:
            return []

        # Create a numbered list for batch translation
        numbered_texts = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts)])

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                system=f"You are a professional translator. Translate each numbered item to {target_language}. "
                       f"Preserve any HTML tags, placeholders, or special formatting. "
                       f"Return only the translations in the same numbered format, one per line.",
                messages=[
                    {
                        "role": "user",
                        "content": numbered_texts
                    }
                ]
            )

            translation_text = message.content[0].text.strip()

            # Parse the numbered response
            translations = []
            for line in translation_text.split('\n'):
                line = line.strip()
                if line:
                    # Remove number prefix (e.g., "1. ", "2. ")
                    if '. ' in line:
                        translation = line.split('. ', 1)[1]
                        translations.append(translation)
                    else:
                        translations.append(line)

            # Ensure we have the same number of translations
            if len(translations) != len(texts):
                print(f"Warning: Expected {len(texts)} translations but got {len(translations)}")
                # Fall back to original texts for missing translations
                while len(translations) < len(texts):
                    translations.append(texts[len(translations)])

            return translations

        except Exception as e:
            print(f"Error in batch translation: {e}")
            return texts  # Return originals on error

    def extract_translations(self, root: ET.Element, skip_existing: bool = False) -> List[Tuple[ET.Element, ET.Element, str]]:
        """
        Extract all trans-units with source and target elements.

        Args:
            root: Root XML element
            skip_existing: If True, skip targets that already have content

        Returns:
            List of tuples (trans_unit, target_element, source_text)
        """
        translations = []

        # Find all trans-unit elements
        for trans_unit in root.iter(f'{{{self.XLIFF_NS}}}trans-unit'):
            source_elem = trans_unit.find(f'{{{self.XLIFF_NS}}}source')
            target_elem = trans_unit.find(f'{{{self.XLIFF_NS}}}target')

            if source_elem is not None and target_elem is not None:
                # Get source text (including any child elements)
                source_text = self._get_element_text(source_elem)
                if source_text.strip():
                    # Check if target already has content
                    target_text = self._get_element_text(target_elem)
                    if skip_existing and target_text.strip():
                        continue  # Skip this one, already translated

                    translations.append((trans_unit, target_elem, source_text))

        return translations

    def _get_element_text(self, element: ET.Element) -> str:
        """
        Get text from element including nested tags.

        Args:
            element: XML element

        Returns:
            Text content
        """
        # Use tostring to preserve inner XML structure
        text = ET.tostring(element, encoding='unicode', method='xml')
        # Extract content between tags
        text = text.split('>', 1)[1].rsplit('<', 1)[0] if '>' in text else ''
        return text.strip()

    def _set_element_text(self, element: ET.Element, text: str):
        """
        Set text for element, preserving any inner XML.

        Args:
            element: XML element
            text: Text to set
        """
        # Clear existing content
        element.text = None
        element.tail = None
        for child in list(element):
            element.remove(child)

        # Parse the text as XML fragment to handle inner tags
        try:
            # Wrap in temporary element to parse
            wrapped = f'<temp>{text}</temp>'
            temp = ET.fromstring(wrapped)
            element.text = temp.text
            element.tail = None
            for child in temp:
                element.append(child)
        except ET.ParseError:
            # If not valid XML, just set as text
            element.text = text

    def translate_file(
        self,
        input_file: Path,
        target_language: str,
        output_file: Optional[Path] = None,
        skip_existing: bool = True,
        save_frequency: int = 5
    ) -> dict:
        """
        Translate an XLIFF file with progress tracking and auto-save.

        Args:
            input_file: Path to input XLIFF file
            target_language: Target language name (e.g., 'French', 'Spanish')
            output_file: Path to output file (defaults to overwriting input)
            skip_existing: If True, skip trans-units that already have content in target
            save_frequency: Save file every N batches (default: 5)

        Returns:
            Dictionary with translation statistics
        """
        print(f"\n{'='*70}")
        print(f"XLIFF Translation (Claude AI): {input_file.name} → {target_language}")
        print(f"Model: {self.model}")
        print(f"{'='*70}")

        # Parse XML
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Extract all translation units (with skip_existing logic)
        all_trans_units = self.extract_translations(root, skip_existing=False)
        trans_units_to_process = self.extract_translations(root, skip_existing=skip_existing)

        total_units = len(all_trans_units)
        already_translated = total_units - len(trans_units_to_process)
        to_translate = len(trans_units_to_process)

        print(f"Total trans-units: {total_units}")
        print(f"Already translated: {already_translated}")
        print(f"To translate: {to_translate}")
        print(f"{'='*70}\n")

        if to_translate == 0:
            print("✓ All translations complete! Nothing to do.")
            return {
                'total': total_units,
                'already_translated': already_translated,
                'translated': 0,
                'errors': 0
            }

        # Determine output path
        output_path = output_file or input_file

        # Process in batches with progress bar
        stats = {
            'total': total_units,
            'already_translated': already_translated,
            'translated': 0,
            'errors': 0
        }

        # Create progress bar for batches
        num_batches = (to_translate + self.batch_size - 1) // self.batch_size
        batch_progress = tqdm(
            total=num_batches,
            desc="Batches",
            unit="batch",
            position=0,
            leave=True
        )

        # Create progress bar for individual translations
        translation_progress = tqdm(
            total=to_translate,
            desc="Translations",
            unit="item",
            position=1,
            leave=True
        )

        try:
            for batch_idx in range(0, to_translate, self.batch_size):
                batch = trans_units_to_process[batch_idx:batch_idx + self.batch_size]
                batch_texts = [source_text for _, _, source_text in batch]

                # Translate batch
                try:
                    translations = self.translate_batch(batch_texts, target_language)

                    # Update XML
                    for (trans_unit, target_elem, source_text), translation in zip(batch, translations):
                        if translation and translation != source_text:
                            self._set_element_text(target_elem, translation)
                            stats['translated'] += 1
                        else:
                            stats['errors'] += 1

                        translation_progress.update(1)

                    batch_progress.update(1)

                    # Save periodically to preserve progress
                    if (batch_idx // self.batch_size + 1) % save_frequency == 0:
                        tree.write(
                            output_path,
                            encoding='UTF-8',
                            xml_declaration=True,
                            method='xml'
                        )
                        tqdm.write(f"💾 Progress saved to {output_path.name}")

                except Exception as e:
                    tqdm.write(f"❌ Error in batch {batch_idx // self.batch_size + 1}: {e}")
                    stats['errors'] += len(batch)
                    translation_progress.update(len(batch))
                    batch_progress.update(1)

                # Rate limiting between batches
                if batch_idx + self.batch_size < to_translate:
                    time.sleep(self.delay)

        except KeyboardInterrupt:
            print("\n\n⚠ Translation interrupted by user!")
            print("Saving progress before exit...")

        finally:
            batch_progress.close()
            translation_progress.close()

        # Final save
        print(f"\n💾 Saving final results to: {output_path}")
        tree.write(
            output_path,
            encoding='UTF-8',
            xml_declaration=True,
            method='xml'
        )

        # Pretty print summary
        print("\n" + "="*70)
        print("TRANSLATION SUMMARY")
        print("="*70)
        print(f"Total trans-units:     {stats['total']}")
        print(f"Already translated:    {stats['already_translated']}")
        print(f"Newly translated:      {stats['translated']}")
        print(f"Errors:                {stats['errors']}")
        completion = ((stats['already_translated'] + stats['translated']) / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"Completion:            {completion:.1f}%")
        print("="*70)

        return stats


def main():
    """Main entry point for CLI usage"""
    parser = argparse.ArgumentParser(
        description='Translate XLIFF files using Claude AI (Anthropic)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate to French
  python translate_xlf_claude.py -i messages.fr.xlf -l French

  # Translate to Spanish with custom API key
  python translate_xlf_claude.py -i messages.es.xlf -l Spanish -k sk-ant-...

  # Use Claude 3 Opus for better quality
  python translate_xlf_claude.py -i messages.de.xlf -l German -m claude-3-opus-20240229

  # Save to different file
  python translate_xlf_claude.py -i messages.xlf -l Italian -o messages.it.xlf

  # Only translate empty targets
  python translate_xlf_claude.py -i messages.fr.xlf -l French
        """
    )

    parser.add_argument(
        '-i', '--input',
        type=Path,
        required=True,
        help='Input XLIFF file path'
    )

    parser.add_argument(
        '-l', '--language',
        type=str,
        required=True,
        help='Target language (e.g., French, Spanish, German, Italian)'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file path (default: overwrite input file)'
    )

    parser.add_argument(
        '-k', '--api-key',
        type=str,
        help='Anthropic API key (default: read from ANTHROPIC_API_KEY env var)'
    )

    parser.add_argument(
        '-m', '--model',
        type=str,
        default='claude-haiku-4-5-20251001',
        help='Claude model to use (default: claude-haiku-4-5-20251001)'
    )

    parser.add_argument(
        '-b', '--batch-size',
        type=int,
        default=10,
        help='Number of translations per API call (default: 10)'
    )

    parser.add_argument(
        '-d', '--delay',
        type=float,
        default=1.0,
        help='Delay in seconds between API calls (default: 1.0)'
    )

    parser.add_argument(
        '--no-skip',
        action='store_true',
        help='Re-translate all items (default: skip items with existing target text)'
    )

    parser.add_argument(
        '--save-frequency',
        type=int,
        default=5,
        help='Save progress every N batches (default: 5)'
    )

    args = parser.parse_args()

    # Validate input file
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Create translator
    try:
        translator = XLIFFTranslatorClaude(
            api_key=args.api_key,
            model=args.model,
            batch_size=args.batch_size,
            delay=args.delay
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Translate file
    try:
        stats = translator.translate_file(
            input_file=args.input,
            target_language=args.language,
            output_file=args.output,
            skip_existing=not args.no_skip,
            save_frequency=args.save_frequency
        )

        print(f"\n✓ Translation complete!")
        sys.exit(0 if stats['errors'] == 0 else 1)

    except Exception as e:
        print(f"\n✗ Translation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
