#!/usr/bin/env python3
"""
Test Claude AI (Anthropic) API Connection

This script tests if your Anthropic API key is working correctly.
Usage: python test_claude_connection.py
"""

import os
import sys

# Test imports
print("Testing imports...")
try:
    from anthropic import Anthropic
    print("✓ anthropic package installed")
except ImportError:
    print("✗ anthropic package not installed")
    print("Install with: pip install anthropic")
    sys.exit(1)

# Check API key
print("\nChecking API key...")
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("✗ ANTHROPIC_API_KEY environment variable not set")
    print("\nTo set it:")
    print("  export ANTHROPIC_API_KEY='sk-ant-your-key-here'")
    print("\nTo get an API key:")
    print("  1. Go to https://console.anthropic.com/")
    print("  2. Sign up or log in")
    print("  3. Go to API Keys section")
    print("  4. Create a new API key")
    sys.exit(1)

# Validate key format
if not api_key.startswith('sk-ant-'):
    print("✗ API key doesn't look valid (should start with 'sk-ant-')")
    sys.exit(1)

print(f"✓ API key found (starts with: {api_key[:15]}...)")

# Test API connection
print("\nTesting API connection...")
try:
    client = Anthropic(api_key=api_key)

    # Try a simple message
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[
            {"role": "user", "content": "Say 'Connection successful!' in French"}
        ]
    )

    result = message.content[0].text
    print(f"✓ API connection successful!")
    print(f"✓ Test translation: {result}")

    # Show usage
    print(f"\nAPI Usage for this test:")
    print(f"  Input tokens: {message.usage.input_tokens}")
    print(f"  Output tokens: {message.usage.output_tokens}")
    print(f"  Model: {message.model}")

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("Your Claude AI API is working correctly.")
    print("You can now run the translation script:")
    print("  python translate_xlf_claude.py -i messages.fr.xlf -l French")
    print("="*60)

except Exception as e:
    print(f"✗ API connection failed: {e}")
    print("\nPossible issues:")
    print("  1. Invalid API key")
    print("  2. No credits in your Anthropic account")
    print("  3. Network connectivity issues")
    print("  4. API key has been revoked")
    sys.exit(1)
