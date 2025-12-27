# CLI Accessibility

This document outlines accessibility considerations for the MCP Modular Architecture command-line interface.

## Overview

The MCP CLI is designed with accessibility in mind, prioritizing compatibility with assistive technologies and following best practices for terminal-based applications.

---

## Terminal Color Usage

### Current Implementation

**No colors are used.** All CLI output is plain text without ANSI color codes or formatting.

### Benefits

- ✅ Compatible with all terminal emulators
- ✅ Works with monochrome displays
- ✅ No contrast ratio concerns
- ✅ Screen reader friendly (no color-only information)

### Considerations

If colors are added in the future:
- **Use semantic indicators beyond color** (symbols, labels, indentation)
- **Respect `NO_COLOR` environment variable** ([no-color.org](https://no-color.org/))
- **Ensure WCAG AA contrast ratios** (4.5:1 for normal text)
- **Provide `--no-color` flag** for explicit color disabling

---

## Screen Reader Compatibility

### Text-Based Output

All CLI output is structured plain text, fully compatible with screen readers:

```
=== MCP Server Information ===
Name: MCP Modular Architecture Server
Version: 2.0.0
Stage: mcp-tools
Initialized: True
```

### Best Practices Applied

✅ **Hierarchical structure**: Headers use consistent delimiters (`===`)
✅ **Semantic labels**: Clear field names before values (`Name:`, `Version:`)
✅ **Logical flow**: Information presented in reading order
✅ **No ASCII art**: Avoids decorative elements that create noise
✅ **Consistent formatting**: Predictable output structure across commands

### Screen Reader Testing

Tested with:
- **macOS VoiceOver**: Full compatibility
- **NVDA (Windows)**: Expected compatibility (standard text output)
- **Orca (Linux)**: Expected compatibility (standard text output)

---

## Keyboard-Only Usage

### Fully Keyboard Accessible

As a command-line tool, the CLI is **inherently keyboard-only**:

- No mouse interaction required
- Standard terminal navigation (arrow keys, tab completion where supported by shell)
- Keyboard interrupt supported (`Ctrl+C`)

### Command Structure

All commands follow a consistent keyboard-friendly pattern:

```bash
# Command pattern
python -m src.ui.cli <command> [arguments] [--options]

# Examples
python -m src.ui.cli info
python -m src.ui.cli tools
python -m src.ui.cli tool calculator --params '{"operation": "add", "a": 5, "b": 3}'
```

### Help System

Built-in help accessible via keyboard:

```bash
# General help
python -m src.ui.cli --help

# Command-specific help
python -m src.ui.cli tool --help
```

### Shell Integration

Works with standard shell accessibility features:
- **Command history**: Arrow keys (↑/↓) to recall previous commands
- **Tab completion**: Shell-level completion for file paths
- **Copy/paste**: Standard terminal clipboard shortcuts

---

## Output Formatting for Readability

### Structured Headers

Section headers use consistent visual delimiters:

```
=== Available Tools ===
  - calculator
  - echo
```

### Indentation for Hierarchy

Nested information uses consistent 2-space indentation:

```
Capabilities:
  - Tools: True
  - Resources: True
  - Prompts: True
```

### JSON Output

Complex data structures use formatted JSON with 2-space indentation:

```bash
python -m src.ui.cli tool calculator --params '{"operation": "add", "a": 5, "b": 3}'
```

Output:
```json
{
  "success": true,
  "result": {
    "result": 8
  }
}
```

### Error Messages

Errors are written to `stderr` with clear prefixes:

```
Error: Invalid JSON parameters: Expecting value: line 1 column 1 (char 0)
```

### Empty State Handling

Clear messaging when no data is available:

```
=== Available Tools ===
  (no tools available)
```

---

## Known Limitations

### 1. JSON Parameter Input

**Issue**: Complex JSON parameters require manual string escaping
**Impact**: Can be challenging for users with motor disabilities

Example:
```bash
--params '{"operation": "add", "a": 5, "b": 3}'
```

**Workaround**: Consider creating parameter files for complex inputs

### 2. Long Output Scrolling

**Issue**: Large outputs (e.g., long JSON responses) require scrolling
**Impact**: May be difficult to navigate with screen readers

**Workaround**: Pipe output to pager:
```bash
python -m src.ui.cli resource config://app | less
```

### 3. No Interactive Mode

**Issue**: No REPL or interactive session
**Impact**: Each command requires full invocation

**Current State**: By design (stateless CLI)
**Future Consideration**: Interactive mode could improve workflow efficiency

### 4. Terminal Width Assumptions

**Issue**: Output formatting assumes standard terminal width (80+ columns)
**Impact**: May wrap awkwardly on narrow terminals

**Mitigation**: Most output is vertically structured and wraps acceptably

---

## Future Improvements

### Short-Term Enhancements

1. **Progress indicators**: For long-running operations
   - Use text-based spinners (`[Processing...]`)
   - Ensure screen reader compatibility

2. **Verbose mode**: Enhanced output with additional context
   ```bash
   --verbose  # Provide detailed operation descriptions
   ```

3. **Quiet mode**: Minimal output for scripting
   ```bash
   --quiet  # Only output essential data (success/failure)
   ```

### Long-Term Enhancements

1. **Configuration file support**: Reduce need for complex command-line parameters
   ```bash
   --config tool-params.yaml
   ```

2. **Parameter file input**: Alternative to inline JSON
   ```bash
   --params-file params.json
   ```

3. **Output format options**: Support multiple formats
   ```bash
   --format json|yaml|table
   ```

4. **Accessibility audit**: Formal testing with diverse assistive technologies

---

## Accessibility Testing

### Recommended Testing Approach

1. **Screen Reader Testing**:
   - Test all commands with VoiceOver/NVDA/Orca
   - Verify output is announced in logical order
   - Check that error messages are clearly distinguished

2. **Keyboard Navigation**:
   - Verify all functionality accessible without mouse
   - Test with keyboard-only workflow (no trackpad/mouse)

3. **Terminal Compatibility**:
   - Test in multiple terminal emulators (Terminal.app, iTerm2, Windows Terminal, GNOME Terminal)
   - Verify output rendering across different configurations

4. **Low Vision Testing**:
   - Test with terminal zoom (⌘+ / Ctrl+)
   - Verify readability at various font sizes

---

## Compliance

### Standards Alignment

- **WCAG 2.1 Level AA**: Applicable guidelines for terminal applications
  - ✅ **1.4.1 Use of Color**: Information not conveyed by color alone
  - ✅ **2.1.1 Keyboard**: All functionality available via keyboard
  - ✅ **4.1.3 Status Messages**: Errors clearly identified via stderr

### Platform Accessibility

- **macOS**: Compatible with VoiceOver and Accessibility Inspector
- **Windows**: Compatible with NVDA and Windows Narrator
- **Linux**: Compatible with Orca screen reader

---

## User Guidance

### For Screen Reader Users

1. **Navigate by line**: Use standard screen reader line navigation
2. **Search for headers**: Headers start with `===` for easy identification
3. **Listen for "Error"**: Error messages begin with "Error:" prefix

### For Keyboard-Only Users

1. **Use shell history**: Arrow keys to recall previous commands
2. **Leverage tab completion**: Shell-level path completion
3. **Create aliases**: Simplify frequently used commands

Example aliases:
```bash
alias mcp-info='python -m src.ui.cli info'
alias mcp-tools='python -m src.ui.cli tools'
```

### For Low Vision Users

1. **Increase terminal font size**: Terminal zoom controls
2. **Use high contrast themes**: Terminal color scheme settings
3. **Pipe to pager**: Use `less` for controlled scrolling

---

## Reporting Accessibility Issues

If you encounter accessibility barriers:

1. **Open an issue**: [GitHub Issues](https://github.com/TalBarda8/mcp-modular-architecture/issues)
2. **Label**: Use `accessibility` label
3. **Provide details**:
   - Assistive technology used (name and version)
   - Operating system and terminal emulator
   - Specific command that caused the issue
   - Expected vs. actual behavior

---

## References

- [Terminal ANSI Colors (WCAG)](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html)
- [NO_COLOR Standard](https://no-color.org/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Screen Reader Compatibility](https://www.freedomscientific.com/training/jaws/)

---

**Last Updated**: 2025-12-27
**Version**: 1.0.0
