#!/usr/bin/env python3
"""
Test script to verify MCP server installation and functionality.
"""

import sys
import os
from pathlib import Path

def test_installation():
    """Test that all components are installed correctly."""
    print("🧪 Testing MCP Server Installation")
    print("=" * 50)
    
    # Test 1: Check if virtual environment is activated
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
    else:
        print("⚠️  Virtual environment not detected (this is okay if running globally)")
    
    # Test 2: Test imports
    try:
        import fastmcp
        print("✅ FastMCP imported successfully")
    except ImportError as e:
        print(f"❌ FastMCP import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    try:
        import httpx
        print("✅ HTTPX imported successfully")
    except ImportError as e:
        print(f"❌ HTTPX import failed: {e}")
        return False
    
    # Test 3: Check MCP server module
    try:
        import mcp_server
        print(f"✅ MCP server module imported: {mcp_server.mcp.name}")
    except ImportError as e:
        print(f"❌ MCP server import failed: {e}")
        return False
    
    # Test 4: Check file structure
    required_files = [
        "mcp_server.py",
        "requirements.txt", 
        "setup.py",
        "test_mcp_client.py",
        "cursor_config.json",
        "README.md"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Test 5: Check current directory path for Cursor config
    current_path = os.getcwd()
    print(f"📍 Current directory: {current_path}")
    print(f"📝 Use this path in your Cursor MCP config:")
    print(f"   {current_path}/mcp_server.py")
    
    print("\n🎉 Installation test completed successfully!")
    print("\n📖 Next Steps:")
    print("1. Copy the absolute path above")
    print("2. Add MCP server to Cursor settings using the path")
    print("3. Start using the MCP tools in Cursor!")
    
    return True

if __name__ == "__main__":
    success = test_installation()
    sys.exit(0 if success else 1)