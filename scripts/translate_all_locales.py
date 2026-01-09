#!/usr/bin/env python3
"""
Batch translate all locale files in the casino-customer-f project.

This script translates all .xlf files in the locale directory to their
respective languages using the translate_xlf.py script.
"""

import os
import sys
from pathlib import Path
import subprocess

# Language mapping: filename -> language name
LANGUAGE_MAP = {
    'messages.fr.xlf': 'French',
    'messages.es.xlf': 'Spanish',
    'messages.de.xlf': 'German',
    'messages.it.xlf': 'Italian',
    'messages.pt.xlf': 'Portuguese',
    'messages.pl.xlf': 'Polish',
    'messages.sv.xlf': 'Swedish',
    'messages.no.xlf': 'Norwegian',
    'messages.fi.xlf': 'Finnish',
}


def main():
    """Translate all locale files"""

    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Get the locale directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    locale_dir = project_root / 'casino-customer-f' / 'src' / 'locale'

    if not locale_dir.exists():
        print(f"Error: Locale directory not found: {locale_dir}")
        sys.exit(1)

    print("="*60)
    print("BATCH TRANSLATION OF ALL LOCALE FILES")
    print("="*60)
    print(f"Locale directory: {locale_dir}")
    print(f"Files to translate: {len(LANGUAGE_MAP)}")
    print("="*60)
    print()

    # Confirm before proceeding
    response = input("Proceed with translation? This will use OpenAI API credits. (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Cancelled.")
        sys.exit(0)

    # Translate each file
    success_count = 0
    failed_files = []

    for filename, language in LANGUAGE_MAP.items():
        file_path = locale_dir / filename

        if not file_path.exists():
            print(f"\n⚠ Warning: File not found, skipping: {filename}")
            continue

        print(f"\n{'='*60}")
        print(f"Translating: {filename} -> {language}")
        print(f"{'='*60}")

        # Run translation script
        try:
            result = subprocess.run([
                sys.executable,
                str(script_dir / 'translate_xlf.py'),
                '-i', str(file_path),
                '-l', language,
                '-m', 'gpt-3.5-turbo',  # Use faster model for batch
                '-b', '15',  # Larger batches
                '-d', '0.5',  # Shorter delay
                '--save-frequency', '3'  # Save more frequently
            ], check=True)

            if result.returncode == 0:
                success_count += 1
                print(f"✓ Successfully translated {filename}")
            else:
                failed_files.append(filename)
                print(f"✗ Failed to translate {filename}")

        except subprocess.CalledProcessError as e:
            failed_files.append(filename)
            print(f"✗ Error translating {filename}: {e}")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            sys.exit(1)

    # Print summary
    print("\n" + "="*60)
    print("BATCH TRANSLATION SUMMARY")
    print("="*60)
    print(f"Total files:       {len(LANGUAGE_MAP)}")
    print(f"Successfully:      {success_count}")
    print(f"Failed:            {len(failed_files)}")

    if failed_files:
        print("\nFailed files:")
        for filename in failed_files:
            print(f"  - {filename}")

    print("="*60)

    sys.exit(0 if len(failed_files) == 0 else 1)


if __name__ == '__main__':
    main()
