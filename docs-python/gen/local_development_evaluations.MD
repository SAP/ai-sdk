# Local Development Guide for Evaluations

This guide provides step-by-step instructions for developing and testing the Evaluations SDK locally.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment tool (venv or conda)

## Setup Steps

### 1. Create and Activate Virtual Environment

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n gen-ai-hub python=3.10
conda activate gen-ai-hub
```

### 2. Install Dependencies

Install all required dependencies from the root directory:
```bash
pip install -r requirements.txt
```

### 3. Install SDK in Editable Mode

To ensure SDK changes are immediately reflected without reinstalling:
```bash
pip install -e .
```

> **Note**: Run this command every time you make changes to the SDK code. The `-e` flag installs the package in "editable" mode, linking to your local source code.

## Testing Local Changes

### 4. Test with Client Script

For quick testing, you can hardcode credentials and create a test client:

1. Open `gen_ai_hub/evaluations/client.py`
2. Add your test code in the `if __name__ == "__main__":` section
3. Run from the root directory:
   ```bash
   python gen_ai_hub/evaluations/client.py
   ```

### 5. Run Integration Tests

To run integration tests with proper environment setup:

```bash
# Set up environment variables
source integration_tests/evaluations/set_env.sh

# Run single execution flow test
pytest integration_tests/evaluations/test_single_execution_flow.py -v

# Run multiple execution flow test
pytest integration_tests/evaluations/test_multiple_execution_flow.py -v

# Run all integration tests
pytest integration_tests/evaluations/ -v
```

## Building Distribution Files

### 6. Create Wheel File for Testing

To create a distributable `.whl` file for testing in notebooks or other environments:

1. **Install build tools** (if not already installed):
   ```bash
   pip install build
   ```

2. **Build the distribution**:
   ```bash
   python -m build
   ```

   This creates two files in the `dist/` folder:
   - `*.tar.gz` (source distribution)
   - `*.whl` (wheel distribution)

3. **Use the wheel file**:
   ```bash
   pip install dist/generative_ai_hub_sdk-*.whl
   ```

### 7. Change SDK Version

To release a custom version (e.g., changing from 5.7.x to a different version):

1. Update version in `setup.py` or `pyproject.toml`
2. Update version in `gen_ai_hub/__init__.py`
3. Update version in any other relevant files
4. Rebuild the distribution:
   ```bash
   python -m build
   ```

## Development Workflow Summary

```bash
# 1. Make code changes
vim gen_ai_hub/evaluations/client.py

# 2. Reinstall in editable mode
pip install -e .

# 3. Test your changes
python gen_ai_hub/evaluations/client.py
# OR
pytest integration_tests/evaluations/

# 4. Build distribution (optional)
python -m build
```

## Troubleshooting

### Changes Not Reflected
- Make sure you ran `pip install -e .` after making changes
- Restart your Python interpreter/kernel

### Import Errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using the correct virtual environment

### Integration Test Failures
- Ensure environment variables are set (source `set_env.sh`)
- Verify your AI Core credentials have the necessary permissions
- Check that the base URL includes the `/v2` suffix

## Additional Resources

- [Integration Tests README](integration_tests/evaluations/README.md)
- [SDK Documentation](docs/SDK%20doc.md)