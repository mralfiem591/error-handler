# Error Reporter

The **Error Reporter** is a Python-based tool designed to capture, report, and manage application errors. It provides a seamless way to log errors, collect system information, and report issues directly to a GitHub repository.

## Features

- Encrypts sensitive GitHub tokens for secure usage.
- Automatically collects system, environment, and traceback details.
- Reports issues to a configured GitHub repository.
- Saves error reports locally if GitHub reporting fails.
- Includes a standalone mode for manual issue reporting.

## Setup

Follow these steps to set up the Error Reporter:

1. Clone or download this repository.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the setup script to configure the tool:

   ```bash
   python setup.py
   ```

   During setup, you will be prompted to:
   - Enter your GitHub token.
   - Specify the GitHub repository (format: `username/repo`).
   - Provide the application name.

4. The setup script will:
   - Generate an encryption key (`key.key`).
   - Encrypt your GitHub token.
   - Create a configuration file (`errorconfig.json`).

## Usage

### Automatic Error Reporting

Integrate the `handle_exception` function from `main.py` into your application to automatically capture and report exceptions. For example:

```python
try:
    # Your application code here
    pass
except Exception as e:
    handle_exception(e)
```

### Standalone Mode

Run the tool in standalone mode to manually report issues:

```bash
python main.py
```

If standalone mode is enabled in the configuration, you can provide a title and description for the issue, which will be reported to the configured GitHub repository.

## Configuration

The `errorconfig.json` file contains the following settings:

- `app_name`: The name of your application.
- `app_version`: The version of your application.
- `error_screen_text`: The message displayed to users when an error occurs.
- `enable_standalone`: Enables or disables standalone mode.
- `github_repo`: The GitHub repository for reporting issues.
- `github_token`: The encrypted GitHub token.
- `ui_colors`: Customizable colors for the error screen.

## Local Error Reports

If the tool fails to report an issue to GitHub, it will save the error report locally as a JSON file in the current directory.

## Dependencies

- `cryptography`: For encrypting and decrypting the GitHub token.
- `requests`: For interacting with the GitHub API.
- `rich`: For creating a user-friendly console interface.
- `pkg_resources`: For retrieving installed Python packages.

Install these dependencies using:

```bash
pip install cryptography requests rich
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the tool.

## Contact

For questions or support, please contact the project maintainer.
