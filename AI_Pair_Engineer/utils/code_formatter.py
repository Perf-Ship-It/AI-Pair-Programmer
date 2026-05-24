"""
Code formatting utilities for AI pair programming.
"""

import re


class CodeFormatter:
    """Format and style code."""
    
    def __init__(self):
        """Initialize code formatter."""
        self.languages = {
            "python": "python",
            "javascript": "javascript",
            "typescript": "typescript",
            "java": "java",
            "go": "go",
            "rust": "rust",
            "c": "c",
            "cpp": "cpp"
        }
    
    def format_code(self, code: str, language: str) -> str:
        """Format code according to language-specific rules.
        
        Args:
            code: Code to format
            language: Programming language
        
        Returns:
            Formatted code
        """
        if language not in self.languages:
            return code
        
        # Python formatting
        if language == "python":
            return self._format_python(code)
        
        # JavaScript/TypeScript formatting
        elif language in ["javascript", "typescript"]:
            return self._format_javascript(code)
        
        # Java formatting
        elif language == "java":
            return self._format_java(code)
        
        # Go formatting
        elif language == "go":
            return self._format_go(code)
        
        # Rust formatting
        elif language == "rust":
            return self._format_rust(code)
        
        # C formatting
        elif language == "c":
            return self._format_c(code)
        
        # C++ formatting
        elif language == "cpp":
            return self._format_cpp(code)
        
        return code
    
    def _format_python(self, code: str) -> str:
        """Format Python code."""
        # Use black-style formatting
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Add proper indentation
            if line.startswith('def ') or line.startswith('class '):
                # Function or class definition
                indent = len(line) - len(line.lstrip())
                formatted_lines.append(' ' * indent + line)
            elif line.strip() and not line.startswith('#'):
                # Regular code line
                formatted_lines.append(line)
            else:
                # Comment or empty line
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_javascript(self, code: str) -> str:
        """Format JavaScript code."""
        # Use Prettier-style formatting
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Add proper indentation
            if line.startswith('function ') or line.startswith('const ') or line.startswith('let ') or line.startswith('var '):
                indent = len(line) - len(line.lstrip())
                formatted_lines.append(' ' * indent + line)
            elif line.strip() and not line.startswith('//'):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_java(self, code: str) -> str:
        """Format Java code."""
        # Use Checkstyle-style formatting
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Add proper indentation
            if line.startswith('public ') or line.startswith('private ') or line.startswith('protected '):
                indent = len(line) - len(line.lstrip())
                formatted_lines.append(' ' * indent + line)
            elif line.strip() and not line.startswith('//'):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_go(self, code: str) -> str:
        """Format Go code."""
        # Use Go fmt-style formatting
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Add proper indentation
            if line.startswith('func ') or line.startswith('type '):
                indent = len(line) - len(line.lstrip())
                formatted_lines.append(' ' * indent + line)
            elif line.strip() and not line.startswith('//'):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_rust(self, code: str) -> str:
        """Format Rust code."""
        # Use rustfmt-style formatting
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Add proper indentation
            if line.startswith('fn ') or line.startswith('struct ') or line.startswith('impl '):
                indent = len(line) - len(line.lstrip())
                formatted_lines.append(' ' * indent + line)
            elif line.strip() and not line.startswith('//'):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_c(self, code: str) -> str:
        """Format C code."""
        # Use clang-format-style formatting
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Add proper indentation
            if line.startswith('int ') or line.startswith('void ') or line.startswith('char '):
                indent = len(line) - len(line.lstrip())
                formatted_lines.append(' ' * indent + line)
            elif line.strip() and not line.startswith('//'):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_cpp(self, code: str) -> str:
        """Format C++ code."""
        # Use clang-format-style formatting
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Add proper indentation
            if line.startswith('int ') or line.startswith('void ') or line.startswith('class '):
                indent = len(line) - len(line.lstrip())
                formatted_lines.append(' ' * indent + line)
            elif line.strip() and not line.startswith('//'):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def detect_language(self, code: str) -> str:
        """Detect programming language from code.
        
        Args:
            code: Code content
        
        Returns:
            Detected language name
        """
        # Check for language-specific keywords
        if 'def ' in code or 'class ' in code or 'import ' in code:
            return "python"
        elif 'function ' in code or 'const ' in code or 'import ' in code:
            return "javascript"
        elif 'fn ' in code or 'struct ' in code:
            return "rust"
        elif 'public ' in code or 'private ' in code:
            return "java"
        elif 'func ' in code:
            return "go"
        elif 'int main' in code or '#include' in code:
            return "c"
        elif '#include' in code or 'extern "C"' in code:
            return "cpp"
        
        return "python"  # Default
