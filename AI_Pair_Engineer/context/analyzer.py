"""
File context analyzer for AI pair programming.
"""

import os
from pathlib import Path
from typing import Optional


class ContextAnalyzer:
    """Analyze file context for AI pair programming."""
    
    def __init__(self, max_context_length: int = 8000):
        """Initialize context analyzer.
        
        Args:
            max_context_length: Maximum number of characters to include in context
        """
        self.max_context_length = max_context_length
    
    def analyze(self, code: str, cursor_line: int, cursor_col: int) -> str:
        """Analyze code context around cursor position.
        
        Args:
            code: Full code content
            cursor_line: Cursor line number (1-indexed)
            cursor_col: Cursor column number (0-indexed)
        
        Returns:
            Formatted context string for LLM
        """
        lines = code.split('\n')
        
        # Get context window
        start_line = max(0, cursor_line - 10)
        end_line = min(len(lines), cursor_line + 10)
        
        # Extract context
        context_lines = lines[start_line:end_line]
        context = '\n'.join(context_lines)
        
        # Add file metadata
        metadata = f"""
File Context:
- Total lines: {len(lines)}
- Cursor position: line {cursor_line}, column {cursor_col}
- Context window: lines {start_line + 1} to {end_line}
"""
        
        return metadata + context
    
    def get_relevant_files(self, project_path: str, target_file: str) -> list:
        """Get relevant files in project context.
        
        Args:
            project_path: Path to project root
            target_file: Target file path
        
        Returns:
            List of relevant file paths
        """
        project_path = Path(project_path)
        target_path = project_path / target_file
        
        if not target_path.exists():
            return []
        
        # Get parent directory
        parent_dir = target_path.parent
        
        # Find related files
        relevant_files = []
        
        # Add parent directory files
        for file_path in parent_dir.glob("*.py"):
            if file_path != target_path:
                relevant_files.append(str(file_path.relative_to(project_path)))
        
        # Add sibling files
        for file_path in parent_dir.glob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts', '.java']:
                relevant_files.append(str(file_path.relative_to(project_path)))
        
        # Limit to max files
        return relevant_files[:10]
    
    def extract_function_context(self, code: str, function_name: str) -> str:
        """Extract context for a specific function.
        
        Args:
            code: Full code content
            function_name: Name of function to extract
        
        Returns:
            Function context string
        """
        lines = code.split('\n')
        
        # Find function definition
        for i, line in enumerate(lines):
            if f"def {function_name}" in line or f"function {function_name}" in line:
                # Get function body
                start = i
                indent = len(line) - len(line.lstrip())
                
                # Find end of function
                end = i
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and len(lines[j]) - len(lines[j].lstrip()) <= indent:
                        end = j
                        break
                
                # Extract function
                function_lines = lines[start:end]
                return '\n'.join(function_lines)
        
        return ""
    
    def get_imports(self, code: str) -> list:
        """Extract imports from code.
        
        Args:
            code: Code content
        
        Returns:
            List of import statements
        """
        lines = code.split('\n')
        imports = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                imports.append(stripped)
        
        return imports
    
    def get_class_context(self, code: str, class_name: str) -> str:
        """Extract context for a specific class.
        
        Args:
            code: Full code content
            class_name: Name of class to extract
        
        Returns:
            Class context string
        """
        lines = code.split('\n')
        
        # Find class definition
        for i, line in enumerate(lines):
            if f"class {class_name}" in line:
                # Get class body
                start = i
                indent = len(line) - len(line.lstrip())
                
                # Find end of class
                end = i
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and len(lines[j]) - len(lines[j].lstrip()) <= indent:
                        end = j
                        break
                
                # Extract class
                class_lines = lines[start:end]
                return '\n'.join(class_lines)
        
        return ""
