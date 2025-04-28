"""
Utility functions for AgentFleet CLI commands
"""

import os
import subprocess
import json
import click
from colorama import Fore, Style
import requests
from tabulate import tabulate

def detect_framework(repo_dir="."):
    """Detect the agent framework based on requirements or other files"""
    try:
        if os.path.exists(os.path.join(repo_dir, "requirements.txt")):
            with open(os.path.join(repo_dir, "requirements.txt")) as f:
                requirements = f.read().lower()
                if "langchain" in requirements:
                    return "LANGCHAIN"
                elif "llama-index" in requirements or "llamaindex" in requirements:
                    return "LLAMAINDEX"
                elif "langgraph" in requirements:
                    return "LANGGRAPH"
                elif "crewai" in requirements:
                    return "CREWAI"
                
        # Check for specific framework files
        if os.path.exists(os.path.join(repo_dir, "agent_graph.py")) or \
           os.path.exists(os.path.join(repo_dir, "graph.py")):
            return "LANGGRAPH"
            
        if os.path.exists(os.path.join(repo_dir, "agent_crew.py")) or \
           os.path.exists(os.path.join(repo_dir, "crew.py")):
            return "CREWAI"
            
        if any(f.endswith("_chain.py") for f in os.listdir(repo_dir) if os.path.isfile(os.path.join(repo_dir, f))):
            return "LANGCHAIN"
    except Exception as e:
        click.echo(f"{Fore.YELLOW}Warning: Error detecting framework: {str(e)}{Style.RESET_ALL}")
    
    return "CUSTOM"

def get_git_info():
    """Get git repository information"""
    info = {"repo_url": None, "commit": None}
    
    try:
        # Get remote URL
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=True
        )
        info["repo_url"] = result.stdout.strip()
        
        # Get current commit
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        info["commit"] = result.stdout.strip()
    except subprocess.CalledProcessError:
        pass  # Not a git repository or git not installed
    except Exception as e:
        click.echo(f"{Fore.YELLOW}Warning: Error getting git info: {str(e)}{Style.RESET_ALL}")
    
    return info

def make_api_request(method, endpoint, data=None, params=None, api_url=None, api_key=None):
    """Make a request to the AgentFleet API"""
    
    if not api_url:
        click.echo(f"{Fore.RED}Error: No API URL provided. Set AGENTFLEET_API_URL environment variable or use --api-url option.{Style.RESET_ALL}")
        return None
    
    url = f"{api_url.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            click.echo(f"{Fore.RED}Error: Invalid HTTP method: {method}{Style.RESET_ALL}")
            return None
        
        # Check for error responses
        if response.status_code >= 400:
            click.echo(f"{Fore.RED}API Error ({response.status_code}): {response.text}{Style.RESET_ALL}")
            return None
        
        # Return parsed JSON response if available
        if response.content:
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
        
        return True  # Success with no content
        
    except requests.exceptions.RequestException as e:
        click.echo(f"{Fore.RED}Error connecting to API: {str(e)}{Style.RESET_ALL}")
        return None

def format_table(data, headers=None):
    """Format data as a table"""
    if not data:
        return "No data available"
    
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        if not headers and data:
            headers = list(data[0].keys())
        
        rows = [[item.get(header, '') for header in headers] for item in data]
        return tabulate(rows, headers=headers, tablefmt="grid")
    
    return str(data)

def print_success(message):
    """Print a success message"""
    click.echo(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    """Print an error message"""
    click.echo(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print a warning message"""
    click.echo(f"{Fore.YELLOW}! {message}{Style.RESET_ALL}")

def print_info(message):
    """Print an info message"""
    click.echo(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")

def print_verbose(message, verbose=False):
    """Print a message only if verbose mode is enabled"""
    if verbose:
        click.echo(f"{Fore.CYAN}▶ {message}{Style.RESET_ALL}")
