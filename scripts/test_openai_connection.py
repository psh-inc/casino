#!/usr/bin/env python3
"""
Test OpenAI API Connection

This script tests if your OpenAI API key is working correctly.
Usage: python test_openai_connection.py
"""

import os
import sys

# Test imports
print("Testing imports...")
try:
    from openai import OpenAI
    print("✓ openai package installed")
except ImportError:
    print("✗ openai package not installed")
    print("Install with: pip install openai")
    sys.exit(1)

# Check API key
print("\nChecking API key...")
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("✗ OPENAI_API_KEY environment variable not set")
    print("\nTo set it:")
    print("  export OPENAI_API_KEY='sk-your-key-here'")
    sys.exit(1)

# Validate key format
if not api_key.startswith('sk-'):
    print("✗ API key doesn't look valid (should start with 'sk-')")
    sys.exit(1)

print(f"✓ API key found (starts with: {api_key[:10]}...)")

# Test API connection
print("\nTesting API connection...")
try:
    client = OpenAI(api_key=api_key)

    # Try a simple completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say 'Connection successful!' in French"}
        ],
        max_tokens=50
    )

    result = response.choices[0].message.content
    print(f"✓ API connection successful!")
    print(f"✓ Test translation: {result}")

    # Show usage
    print(f"\nAPI Usage for this test:")
    print(f"  Prompt tokens: {response.usage.prompt_tokens}")
    print(f"  Completion tokens: {response.usage.completion_tokens}")
    print(f"  Total tokens: {response.usage.total_tokens}")

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("Your OpenAI API is working correctly.")
    print("You can now run the translation script:")
    print("  python translate_xlf.py -i messages.fr.xlf -l French")
    print("="*60)

except Exception as e:
    print(f"✗ API connection failed: {e}")
    print("\nPossible issues:")
    print("  1. Invalid API key")
    print("  2. No credits in your OpenAI account")
    print("  3. Network connectivity issues")
    print("  4. API key has been revoked")
    sys.exit(1)
