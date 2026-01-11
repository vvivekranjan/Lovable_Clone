from typing import Tuple
import pathlib
import subprocess
from langchain_core.tools import tool
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Generated projects are stored in the current working directory
# This ensures the generated_project directory is in the same location as main.py
PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"


def safe_path_for_project(path: str) -> pathlib.Path:
    """Validate that a path is within the project root to prevent directory traversal attacks."""
    p = (PROJECT_ROOT / path).resolve()
    try:
        p.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        raise ValueError(f"Attempt to write outside project root: {p}")
    return p

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root.
    
    Args:
        path: The file path relative to the project root
        content: The content to write to the file
        
    Returns:
        Confirmation message with the file path written
    """
    try:
        p = safe_path_for_project(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"File written: {p}")
        return f"WROTE: {p}"
    except Exception as e:
        logger.error(f"Error writing file {path}: {e}")
        return f"ERROR: Failed to write {path}: {str(e)}"

@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root.
    
    Args:
        path: The file path relative to the project root
        
    Returns:
        The file content, or empty string if file doesn't exist
    """
    try:
        p = safe_path_for_project(path)
        if not p.exists():
            logger.debug(f"File not found: {p}")
            return ""
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {path}: {e}")
        return f"ERROR: Failed to read {path}: {str(e)}"

@tool
def get_current_directory() -> str:
    """Returns the current working directory (project root).
    
    Returns:
        The absolute path to the project root directory
    """
    return str(PROJECT_ROOT)

@tool
def list_files(directory: str = ".") -> str:
    """List all files in the specified directory within the project root.
    
    Args:
        directory: The directory path relative to the project root (default: ".")
        
    Returns:
        A newline-separated list of file paths, or an error message
    """
    try:
        p = safe_path_for_project(directory)
        if not p.is_dir():
            return f"ERROR: {p} is not a directory"
        files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
        return "\n".join(files) if files else "No files found."
    except Exception as e:
        logger.error(f"Error listing directory {directory}: {e}")
        return f"ERROR: Failed to list {directory}: {str(e)}"

@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result.
    
    Args:
        cmd: The shell command to execute
        cwd: The working directory (relative to project root), defaults to PROJECT_ROOT
        timeout: Command timeout in seconds (default: 30)
        
    Returns:
        A tuple of (return_code, stdout, stderr)
    """
    try:
        cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
        res = subprocess.run(
            cmd,
            shell=True,
            cwd=str(cwd_dir),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        logger.info(f"Command executed: {cmd} (return code: {res.returncode})")
        return res.returncode, res.stdout, res.stderr
    except subprocess.TimeoutExpired:
        error_msg = f"Command timeout after {timeout} seconds"
        logger.error(error_msg)
        return -1, "", error_msg
    except Exception as e:
        logger.error(f"Error running command {cmd}: {e}")
        return -1, "", str(e)

def init_project_root() -> str:
    """Initialize the project root directory.
    
    Returns:
        The absolute path to the initialized project root directory
        
    Raises:
        OSError: If the directory cannot be created
    """
    try:
        PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
        logger.info(f"Project root initialized: {PROJECT_ROOT}")
        return str(PROJECT_ROOT)
    except Exception as e:
        logger.error(f"Failed to initialize project root: {e}")
        raise
