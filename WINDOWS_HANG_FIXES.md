# Windows Hang Issue - Fixes Applied

## Summary of Changes

Based on analysis of the infinite loop/hang issue with `proxyman unset` on Windows, several potential causes were identified and fixed:

## Root Cause Analysis

The hang was likely caused by one or more of these issues:

1. **System Settings Refresh Hang**: The `SendMessageW` API call to refresh system proxy settings could hang indefinitely
2. **Input Handling Issues**: Windows-specific problems with input() function in different shells
3. **Signal Handling Problems**: Inadequate signal handling preventing Ctrl+C from working

## Fixes Applied

### 1. Fixed System Settings Refresh (`targets.py`)

**Problem**: The `_refresh_system_settings()` method used `SendMessageW` which could hang.

**Solution**: Replaced with `SendMessageTimeoutW` with a 5-second timeout:

```python
def _refresh_system_settings(self) -> None:
    """Refresh system settings with timeout protection."""
    try:
        if platform.system() != "Windows":
            return

        import ctypes
        user32 = ctypes.windll.user32
        SMTO_ABORTIFHUNG = 0x0002
        timeout_ms = 5000  # 5 second timeout

        result = user32.SendMessageTimeoutW(
            0xFFFF,  # HWND_BROADCAST
            0x1A,    # WM_SETTINGCHANGE
            0, "Environment",
            SMTO_ABORTIFHUNG,
            timeout_ms,
            None
        )
    except Exception:
        pass  # Ignore errors
```

### 2. Enhanced Signal Handling (`utils.py`)

**Problem**: Signal handling wasn't robust enough for Windows.

**Solution**:

- Added `SIGBREAK` handling for Windows
- Used `os._exit(0)` instead of `sys.exit(0)` for forced termination
- Added exception handling for signal setup

```python
def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        print_colored("\n\nOperation interrupted by user", get_colors()['yellow'])
        os._exit(0)  # Force exit

    try:
        signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)
        if hasattr(signal, 'SIGBREAK'):  # Windows
            signal.signal(signal.SIGBREAK, signal_handler)
    except Exception:
        pass
```

### 3. Improved Input Handling (`utils.py`)

**Problem**: Input functions could hang or not handle interrupts properly.

**Solution**:

- Added `sys.stdout.flush()` before input calls
- Used `os._exit(1)` for forced termination on KeyboardInterrupt
- Added better error handling for input failures

```python
def get_user_input(prompt: str, default: str = None, password: bool = False) -> str:
    try:
        if password:
            import getpass
            result = getpass.getpass(display_prompt)
        else:
            sys.stdout.flush()  # Ensure prompt is visible
            result = input(display_prompt).strip()

        return result if result else (default or '')
    except KeyboardInterrupt:
        print_colored("\n\nOperation cancelled by user", get_colors()['yellow'])
        os._exit(1)  # Force exit
    # ... additional error handling
```

## Testing

Created test scripts to validate the fixes:

1. **`test_windows_hang.py`**: Comprehensive test with timeout detection
2. **`simple_test.py`**: Basic signal handling test
3. **`debug_unset.py`**: Step-by-step debugging of unset command

## Files Modified

- `src/targets.py`: Fixed system settings refresh timeout
- `src/utils.py`: Enhanced signal handling and input functions
- Added test scripts for validation

## Expected Results

After these changes:

1. **No more infinite loops**: System calls have timeouts
2. **Ctrl+C works properly**: Enhanced signal handling with forced exit
3. **Better error recovery**: Input functions handle failures gracefully
4. **Cross-platform compatibility**: All fixes include platform checks

## How to Test

1. Run `python test_windows_hang.py` on Windows
2. Test `proxyman unset` command
3. Verify Ctrl+C works during input prompts
4. Check that operations complete within reasonable time

## Commit Message

```
fix(windows): resolve infinite loop and Ctrl+C issues in unset command

- Replace SendMessageW with SendMessageTimeoutW to prevent hangs
- Enhance signal handling with SIGBREAK support and forced exit
- Improve input handling with better error recovery
- Add comprehensive Windows hang detection tests

Fixes: Windows infinite loop/hang in proxyman unset command
Fixes: Ctrl+C not working on Windows/PowerShell
```
