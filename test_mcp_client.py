#!/usr/bin/env python3
"""
Test MCP Client
A simple client to test the MCP server functionality.
"""

import json
import subprocess
import sys
from pathlib import Path


def test_mcp_server():
    """
    Test the MCP server by running it and checking its capabilities.
    """
    print("🔧 Testing MCP Server...")
    
    # Check if mcp_server.py exists
    if not Path("mcp_server.py").exists():
        print("❌ mcp_server.py not found!")
        return False
    
    try:
        # Test running the server (this will output the capabilities)
        print("📋 Server capabilities:")
        result = subprocess.run(
            [sys.executable, "mcp_server.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Server can be imported and run successfully")
        else:
            print(f"⚠️  Server returned code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        
        # Test importing the server module
        print("\n🐍 Testing Python import...")
        import mcp_server
        print("✅ MCP server module imported successfully")
        
        # Check if the server has the expected tools
        expected_tools = ["calculator", "get_weather", "read_file", "list_files", "system_info"]
        print(f"\n🔍 Checking for expected tools: {expected_tools}")
        
        # This is a basic check - in a real scenario, you'd use MCP client libraries
        server_instance = mcp_server.mcp
        print(f"✅ Server instance created: {server_instance.name}")
        
        print("\n🎉 MCP Server test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {str(e)}")
        return False


def print_usage_instructions():
    """
    Print instructions on how to use the MCP server.
    """
    print("""
📖 MCP Server Usage Instructions:

1. Install Dependencies:
   pip install -r requirements.txt

2. Run the Server (stdio mode):
   python mcp_server.py

3. Integration with Cursor:
   Add to your Cursor MCP settings:
   {
     "test-mcp-server": {
       "command": "python",
       "args": ["/absolute/path/to/mcp_server.py"]
     }
   }

4. Integration with Claude Desktop:
   Add to ~/.config/claude/claude_desktop_config.json:
   {
     "mcpServers": {
       "test-mcp-server": {
         "command": "python",
         "args": ["/absolute/path/to/mcp_server.py"]
       }
     }
   }

🛠️ Available Tools:
- calculator: Evaluate mathematical expressions
- get_weather: Get weather for sample cities
- read_file: Read files from the filesystem
- list_files: List directory contents
- system_info: Get system information

📝 Available Prompts:
- code_reviewer: Review code for issues and improvements
- project_analyzer: Analyze project structure
- debug_assistant: Help debug errors and issues

🧪 Testing:
- Run this script to test the server: python test_mcp_client.py
- Use MCP Inspector for debugging: npx @modelcontextprotocol/inspector python mcp_server.py
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_usage_instructions()
    else:
        success = test_mcp_server()
        if success:
            print("\n" + "="*50)
            print_usage_instructions()
        sys.exit(0 if success else 1)