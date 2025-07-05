from setuptools import setup, find_packages

setup(
    name="test-mcp-server",
    version="0.1.0",
    description="A comprehensive test MCP server for demonstration purposes",
    author="Test Author",
    author_email="test@example.com",
    packages=find_packages(),
    install_requires=[
        "fastmcp>=0.1.0",
        "pydantic>=2.0.0",
        "httpx>=0.25.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "test-mcp-server=mcp_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)