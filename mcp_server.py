#!/usr/bin/env python3
"""
Test MCP Server
A comprehensive MCP server demonstrating tools, resources, and prompts.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize the MCP server
mcp = FastMCP("test-mcp-server")

# Sample data for demonstration
SAMPLE_DATA = {
    "cities": {
        "new_york": {"temp": 72, "condition": "sunny", "humidity": 65},
        "london": {"temp": 60, "condition": "rainy", "humidity": 80},
        "tokyo": {"temp": 75, "condition": "cloudy", "humidity": 70},
    }
}

class WeatherResponse(BaseModel):
    """Weather information for a city."""
    city: str = Field(description="The city name")
    temperature: int = Field(description="Temperature in Fahrenheit")
    condition: str = Field(description="Weather condition")
    humidity: int = Field(description="Humidity percentage")

class CalculationResult(BaseModel):
    """Result of a mathematical calculation."""
    expression: str = Field(description="The mathematical expression")
    result: float = Field(description="The calculated result")

class FileInfo(BaseModel):
    """Information about a file."""
    path: str = Field(description="File path")
    size: int = Field(description="File size in bytes")
    exists: bool = Field(description="Whether the file exists")
    content: Optional[str] = Field(description="File content if readable")

# Tools
@mcp.tool()
def calculator(
    expression: str = Field(description="Mathematical expression to evaluate (e.g., '2 + 3 * 4')")
) -> CalculationResult:
    """
    Evaluate a mathematical expression safely.
    Supports basic arithmetic operations: +, -, *, /, **, (), and common functions.
    """
    try:
        # Simple safety check - only allow basic math operations
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression.replace("**", "^").replace("^", "**")):
            raise ValueError("Expression contains invalid characters")
        
        result = eval(expression)
        return CalculationResult(expression=expression, result=float(result))
    except Exception as e:
        raise ValueError(f"Invalid mathematical expression: {str(e)}")

@mcp.tool()
def get_weather(
    city: str = Field(description="Name of the city (e.g., 'new_york', 'london', 'tokyo')")
) -> WeatherResponse:
    """
    Get current weather information for a city.
    Available cities: new_york, london, tokyo
    """
    city_key = city.lower().replace(" ", "_")
    
    if city_key not in SAMPLE_DATA["cities"]:
        available_cities = ", ".join(SAMPLE_DATA["cities"].keys())
        raise ValueError(f"City '{city}' not found. Available cities: {available_cities}")
    
    weather_data = SAMPLE_DATA["cities"][city_key]
    return WeatherResponse(
        city=city,
        temperature=weather_data["temp"],
        condition=weather_data["condition"],
        humidity=weather_data["humidity"]
    )

@mcp.tool()
def read_file(
    file_path: str = Field(description="Path to the file to read"),
    max_size_kb: int = Field(default=100, description="Maximum file size to read in KB")
) -> FileInfo:
    """
    Read a file from the local filesystem.
    Returns file information and content if the file is readable and under the size limit.
    """
    path = Path(file_path)
    
    if not path.exists():
        return FileInfo(path=file_path, size=0, exists=False, content=None)
    
    try:
        size = path.stat().st_size
        max_size_bytes = max_size_kb * 1024
        
        if size > max_size_bytes:
            return FileInfo(
                path=file_path,
                size=size,
                exists=True,
                content=f"File too large ({size} bytes). Maximum allowed: {max_size_bytes} bytes."
            )
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return FileInfo(path=file_path, size=size, exists=True, content=content)
    
    except Exception as e:
        return FileInfo(
            path=file_path,
            size=path.stat().st_size if path.exists() else 0,
            exists=True,
            content=f"Error reading file: {str(e)}"
        )

@mcp.tool()
def list_files(
    directory: str = Field(default=".", description="Directory to list files from"),
    include_hidden: bool = Field(default=False, description="Include hidden files")
) -> List[Dict[str, Any]]:
    """
    List files in a directory with their basic information.
    """
    try:
        path = Path(directory)
        if not path.exists():
            raise ValueError(f"Directory '{directory}' does not exist")
        
        if not path.is_dir():
            raise ValueError(f"'{directory}' is not a directory")
        
        files = []
        for item in path.iterdir():
            if not include_hidden and item.name.startswith('.'):
                continue
                
            try:
                stat = item.stat()
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except Exception as e:
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "unknown",
                    "size": 0,
                    "error": str(e)
                })
        
        return files
    
    except Exception as e:
        raise ValueError(f"Error listing directory: {str(e)}")

@mcp.tool()
def system_info() -> Dict[str, Any]:
    """
    Get basic system information.
    """
    return {
        "platform": sys.platform,
        "python_version": sys.version,
        "current_directory": os.getcwd(),
        "environment_variables": dict(os.environ),
        "timestamp": datetime.now().isoformat()
    }

# Prompts
@mcp.prompt()
def code_reviewer(
    code: str = Field(description="The code to review"),
    language: str = Field(default="python", description="Programming language of the code")
) -> str:
    """
    Review code for potential issues, best practices, and improvements.
    """
    return f"""
Please review the following {language} code for:
1. Potential bugs or errors
2. Code quality and best practices
3. Performance considerations
4. Security issues
5. Readability and maintainability
6. Suggested improvements

Code to review:
```{language}
{code}
```

Please provide a detailed analysis with specific recommendations.
"""

@mcp.prompt()
def project_analyzer(
    project_description: str = Field(description="Description of the project to analyze")
) -> str:
    """
    Analyze a project and provide insights about its structure and potential improvements.
    """
    return f"""
Please analyze the following project:

Project Description: {project_description}

Use the available tools to:
1. Explore the project structure using list_files
2. Read key files like README.md, package.json, requirements.txt using read_file
3. Analyze the codebase structure and dependencies
4. Identify potential areas for improvement
5. Suggest best practices for the project type

Provide a comprehensive analysis covering:
- Project structure and organization
- Dependencies and their versions
- Code quality observations
- Security considerations
- Performance optimization opportunities
- Documentation quality
- Testing coverage (if applicable)
- Deployment considerations

Please be thorough and provide actionable recommendations.
"""

@mcp.prompt()
def debug_assistant(
    error_message: str = Field(description="The error message or issue description"),
    context: str = Field(default="", description="Additional context about when the error occurs")
) -> str:
    """
    Help debug an issue by analyzing the error and providing solutions.
    """
    return f"""
Please help debug the following issue:

Error/Issue: {error_message}

Context: {context}

Please:
1. Analyze the error message to identify the root cause
2. Provide step-by-step troubleshooting instructions
3. Suggest multiple potential solutions
4. Recommend preventive measures to avoid similar issues
5. If relevant, use the available tools to:
   - Check file system issues with read_file and list_files
   - Verify system information with system_info
   - Perform calculations if needed with calculator

Please provide a comprehensive debugging guide with clear explanations.
"""

# Main execution
if __name__ == "__main__":
    # Run the MCP server
    mcp.run()