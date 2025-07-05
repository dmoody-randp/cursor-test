# cursor-test

A comprehensive test MCP (Model Context Protocol) server for demonstrating integration with Cursor and other MCP clients.

## What is MCP?

The Model Context Protocol (MCP) is an open-source protocol developed by Anthropic that provides a standardized way for AI assistants to access external tools and data sources. This eliminates the need for custom integrations for each AI system.

## Features

This test MCP server provides:

### 🛠️ Tools
- **calculator**: Evaluate mathematical expressions safely
- **get_weather**: Get weather information for sample cities
- **read_file**: Read files from the local filesystem
- **list_files**: List directory contents with file information
- **system_info**: Get basic system information

### 📝 Prompts
- **code_reviewer**: Review code for potential issues and improvements
- **project_analyzer**: Analyze project structure and provide insights
- **debug_assistant**: Help debug errors and issues

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test the Server

```bash
python test_mcp_client.py
```

### 3. Run the Server

```bash
python mcp_server.py
```

## Integration

### With Cursor

1. Open Cursor settings
2. Navigate to the MCP section
3. Add a new MCP server with the following configuration:

```json
{
  "test-mcp-server": {
    "command": "python",
    "args": ["/absolute/path/to/your/cursor-test/mcp_server.py"]
  }
}
```

**Note**: Replace `/absolute/path/to/your/cursor-test/` with the actual absolute path to your project directory.

### With Claude Desktop

Add to your Claude Desktop configuration file (`~/.config/claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "test-mcp-server": {
      "command": "python", 
      "args": ["/absolute/path/to/your/cursor-test/mcp_server.py"]
    }
  }
}
```

## Usage Examples

Once integrated with your MCP client, you can:

1. **Perform calculations**: Ask "What is 25 * 4 + 10?"
2. **Check weather**: Ask "What's the weather like in Tokyo?"
3. **Read files**: Ask "Can you read the contents of README.md?"
4. **List files**: Ask "What files are in the current directory?"
5. **Get system info**: Ask "What's my current Python version?"
6. **Review code**: Use the code reviewer prompt to analyze code snippets
7. **Debug issues**: Use the debug assistant prompt to troubleshoot problems

## Development

### Project Structure

```
cursor-test/
├── mcp_server.py          # Main MCP server implementation
├── test_mcp_client.py     # Test client for verification
├── requirements.txt       # Python dependencies
├── setup.py              # Package configuration
├── cursor_config.json    # Sample Cursor configuration
└── README.md            # This file
```

### Testing

To test the server functionality:

```bash
python test_mcp_client.py
```

For more detailed debugging, use the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

### Adding New Tools

To add a new tool to the server:

1. Define your tool function with the `@mcp.tool()` decorator
2. Add appropriate type hints and docstrings
3. Use Pydantic models for structured responses
4. Test your tool with the test client

Example:

```python
@mcp.tool()
def my_new_tool(
    param: str = Field(description="Parameter description")
) -> str:
    """
    Tool description that will be shown to the LLM.
    """
    return f"Processed: {param}"
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
2. **Path issues**: Use absolute paths in MCP client configurations
3. **Permission errors**: Ensure the Python script has execution permissions
4. **Port conflicts**: The server uses stdio transport, so no port conflicts should occur

### Debug Mode

Run the server with debug logging:

```bash
python mcp_server.py --debug
```

## Security Considerations

This test server includes basic safety measures:

- File reading is limited by size (default 100KB)
- Calculator uses safe evaluation (no arbitrary code execution)
- Directory listing respects hidden file settings
- System info excludes sensitive environment variables

For production use, consider additional security measures like:
- Input validation and sanitization
- Rate limiting
- Access controls
- Audit logging

## Contributing

This is a test/demonstration server. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for testing and educational purposes.

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Cursor MCP Integration](https://cursor.com/docs/mcp)
- [Claude Desktop MCP Setup](https://claude.ai/docs/mcp)
