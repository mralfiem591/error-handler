import os
import json
import traceback
import requests
import platform
import socket
import sys
from rich.console import Console
from rich.prompt import Prompt
from datetime import datetime
from cryptography.fernet import Fernet
import random
import pkg_resources

console = Console()

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "errorconfig.json")
KEY_PATH = os.path.join(os.path.dirname(__file__), "key.key")

# Decrypt the token at runtime
if os.path.exists(KEY_PATH) and os.path.exists(CONFIG_PATH):
    with open(KEY_PATH, "rb") as key_file:
        key = key_file.read()
    cipher = Fernet(key)
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    try:
        decrypted_token = cipher.decrypt(config["github_token"].encode()).decode()
    except Exception as e:
        console.print("[red]Error: Failed to decrypt the GitHub token.[/red]")
        exit(1)
else:
    console.print("[red]Error: Configuration file or key file not found![/red]")
    exit(1)

CONFIG = config

# GitHub API token and repository
GITHUB_TOKEN = decrypted_token
GITHUB_REPO = CONFIG.get("github_repo")

if not GITHUB_TOKEN or not GITHUB_REPO:
    console.print("[red]Error: GitHub token or repository is not configured in 'errorconfig.json'.[/red]")
    exit(1)

def report_issue(title, body):
    """Report an issue to the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"title": title, "body": body}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            console.print("[green]Issue reported successfully![/green]")
        else:
            console.print(f"[red]Failed to report issue: {response.status_code}[/red]")
            console.print(response.json())
            save_report_locally(title, body)
    except requests.RequestException as e:
        console.print(f"[red]Failed to connect to GitHub: {e}[/red]")
        save_report_locally(title, body)

def save_report_locally(title, body):
    """Save the error report locally as a JSON file."""
    report = {
        "title": title,
        "body": body,
        "timestamp": datetime.now().isoformat()
    }
    file_name = f"error_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(file_name, "w") as f:
        json.dump(report, f, indent=4)
    console.print(f"[yellow]Error report saved locally as '{file_name}'.[/yellow]")

def collect_error_data(exception=None):
    """Collect error data, including traceback, system info, and user notes."""
    os_data = {
        "os_name": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.architecture()[0],
        "python_version": platform.python_version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

    network_info = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname())
    }

    env_vars = {key: os.environ[key] for key in ["PATH", "PYTHONPATH"] if key in os.environ}
    for key in env_vars:
        if len(env_vars[key]) > 300:
            env_vars[key] = env_vars[key][:300] + "... (truncated)"

    # Use pkg_resources to get installed packages
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

    error_data = {
        "app_name": CONFIG["app_name"],
        "app_version": CONFIG.get("app_version", "Unknown"),
        "timestamp": datetime.now().isoformat(),
        "command_line_args": sys.argv,
        "environment_variables": env_vars,
        "installed_packages": installed_packages,
        "network_info": network_info,
        "traceback": traceback.format_exc() if exception else None,
        "user_notes": None,
        "os_data": os_data
    }
    return error_data

def display_error_screen(exception=None):
    """Display the error screen and collect user input."""
    console.print(f"[{CONFIG['ui_colors']['title']}]Error in {CONFIG['app_name']}[/]")
    console.print(f"[{CONFIG['ui_colors']['text']}]")
    console.print(CONFIG["error_screen_text"])

    if exception:
        console.print(f"[{CONFIG['ui_colors']['text']}]Traceback:[/]")
        console.print(traceback.format_exc())

    user_notes = Prompt.ask(f"[{CONFIG['ui_colors']['input']}]Add any additional details (optional)[/]")
    return user_notes

def handle_exception(exception):
    """Handle an exception and report it."""
    error_data = collect_error_data(exception)
    error_data["user_notes"] = display_error_screen(exception)

    # Extract a concise title from the traceback
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb_summary = traceback.extract_tb(exc_tb)[-1]  # Get the last traceback entry
    if exc_type is not None:
        error_title = f"{exc_type.__name__}: {exc_value} at {tb_summary.filename}, line {tb_summary.lineno}"
    else:
        error_title = "UnknownError: An unknown error occurred. Refer to the full Traceback."

    # Format the issue body
    os_info = error_data["os_data"]
    possible_messages = [
        "Oh no! Something went wrong!",
        "Oops! An error occurred.",
        "Uh-oh! We hit a snag.",
        "Yikes! An error happened.",
        "Something broke! We're on it.",
        "Whoops! That didn’t go as planned.",
        "Oh dear! An unexpected error occurred.",
        "Drat! Something went wrong.",
        "Snap! We encountered an issue.",
        "Oh snap! An error occurred.",
        "Hmmm... Something isn’t right.",
        "Oh no! We’ve run into a problem.",
        "Oopsie! Something went wrong.",
        "Oh crumbs! An error occurred.",
        "Oh fiddlesticks! Something broke.",
        "Oh bother! We hit a snag.",
        "Oh no! The app encountered an issue.",
        "Oops! Looks like something crashed.",
        "Oh no! Something unexpected happened.",
        "Oh dear! We encountered a hiccup.",
        "Yikes! That wasn’t supposed to happen.",
        "Oh no! Something’s not working as expected.",
        "Oops! We ran into a technical issue.",
        "Oh no! The app tripped over something.",
        "Whoops! Something went sideways.",
        "Oh no! We’ve encountered a glitch.",
        "Oops! Something didn’t go as planned.",
        "Oh no! We’ve hit a roadblock.",
        "Oops! Something went off the rails.",
        "Oh no! We’ve encountered turbulence.",
        "Oops! Something’s gone awry.",
        "Oh no! We’ve hit a bump in the road.",
        "Oops! Something’s not quite right.",
        "Oh no! We’ve run into a snag.",
        "Oops! Something’s acting up.",
        "Oh no! We’ve encountered a hiccup in the system.",
        "Oops! Something’s misbehaving.",
        "Oh no! We’ve hit a technical snag.",
        "Oops! Something’s gone haywire.",
        "Oh no! We’ve encountered a gremlin in the system."
    ]
    random_message = random.choice(possible_messages)
    summary = f"""
# Summary

Error type: {error_title}
Error message: {exc_value}
File: {tb_summary.filename}
Line: {tb_summary.lineno}
"""
    issue_body = f"""
{random_message}
Not to fear, we have reported the error!

{summary}

# Error Details

App Name: {error_data['app_name']}
App Version: {error_data['app_version']}
Timestamp: {error_data['timestamp']}
Command-Line Arguments: {error_data['command_line_args']}
Environment Variables (300 Char Limit):
{json.dumps(error_data['environment_variables'], indent=4)}
Installed Packages:
{json.dumps(error_data['installed_packages'], indent=4)}
Network Information:
- Hostname: {error_data['network_info']['hostname']}
- IP Address: {error_data['network_info']['ip_address']}
OS Information:
- OS: {os_info['os_name']} {os_info['os_release']} (Version: {os_info['os_version']})
- Architecture: {os_info['architecture']}
- Machine: {os_info['machine']}
- Processor: {os_info['processor']}
- Python Version: {os_info['python_version']}

Traceback:
```
Captured by the error reporter:

-- TRACEBACK START --

{error_data['traceback']}

-- TRACEBACK END --
```

User Notes:
{error_data['user_notes']}

Thank you for helping us improve our app!
### CAPTURED BY ERROR REPORTER
    """

    # Report the issue
    report_issue(error_title, issue_body)

# Standalone mode
def standalone_mode():
    """Run the bug reporter as a standalone app."""
    console.print(f"[{CONFIG['ui_colors']['title']}]Welcome to {CONFIG['app_name']} Bug Reporter[/]")
    console.print(f"[{CONFIG['ui_colors']['text']}]Please describe the issue you encountered.[/]")

    title = Prompt.ask(f"[{CONFIG['ui_colors']['input']}]Issue Title[/]")
    description = Prompt.ask(f"[{CONFIG['ui_colors']['input']}]Issue Description[/]")

    # Report the issue
    report_issue(title, description)

if __name__ == "__main__":
    console.clear()
    if CONFIG["enable_standalone"]:
        standalone_mode()
    else:
        console.print("[red]Standalone mode is disabled in the configuration.[/red]")
        console.print("[yellow]Developer note: If you want standalone mode, [bold]enable it in errorconfig.json[/bold][/yellow]")
        console.print("[yellow]Exiting...[/yellow]")
        exit(1)