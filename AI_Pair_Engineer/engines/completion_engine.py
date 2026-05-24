"""
Code completion engine for AI pair programming.
"""

from typing import Optional, List
from AI_Pair_Engineer.models.llm_manager import LLMManager
from AI_Pair_Engineer.context.analyzer import ContextAnalyzer
from AI_Pair_Engineer.utils.code_formatter import CodeFormatter
from AI_Pair_Engineer.utils.prompt_templates import PromptTemplates


class CodeCompletionEngine:
    """Engine for code completion suggestions."""
    
    def __init__(
        self,
        llm_manager: Optional[LLMManager] = None,
        context_analyzer: Optional[ContextAnalyzer] = None,
        code_formatter: Optional[CodeFormatter] = None,
        prompt_templates: Optional[PromptTemplates] = None
    ):
        """Initialize code completion engine.
        
        Args:
            llm_manager: LLM manager instance
            context_analyzer: Context analyzer instance
            code_formatter: Code formatter instance
            prompt_templates: Prompt templates instance
        """
        self.llm_manager = llm_manager or LLMManager()
        self.context_analyzer = context_analyzer or ContextAnalyzer()
        self.code_formatter = code_formatter or CodeFormatter()
        self.prompt_templates = prompt_templates or PromptTemplates()
    
    def complete(
        self,
        code: str,
        cursor_line: int,
        cursor_col: int,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> List[str]:
        """Generate code completion suggestions.
        
        Args:
            code: Full code content
            cursor_line: Cursor line number (1-indexed)
            cursor_col: Cursor column number (0-indexed)
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling
        
        Returns:
            List of completion suggestions
        """
        # Get context around cursor
        context = self.context_analyzer.analyze(code, cursor_line, cursor_col)
        
        # Get imports for context
        imports = self.context_analyzer.get_imports(code)
        
        # Format prompt
        prompt = self.prompt_templates.format_completion_prompt(
            context=context,
            code=code,
            cursor_line=cursor_line,
            cursor_col=cursor_col
        )
        
        # Generate completions
        completions = self.llm_manager.complete(prompt, max_tokens=max_tokens)
        
        return completions
    
    def complete_file(
        self,
        file_path: str,
        cursor_line: int,
        cursor_col: int,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> List[str]:
        """Generate code completion for a file.
        
        Args:
            file_path: Path to file (relative to project root)
            cursor_line: Cursor line number (1-indexed)
            cursor_col: Cursor column number (0-indexed)
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling
        
        Returns:
            List of completion suggestions
        """
        # Read file content
        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except FileNotFoundError:
            return ["# File not found"]
        except Exception as e:
            return [f"# Error reading file: {e}"]
        
        # Get completions
        return self.complete(code, cursor_line, cursor_col, max_tokens, temperature)
    
    def get_suggestions(
        self,
        code: str,
        cursor_line: int,
        cursor_col: int,
        max_suggestions: int = 3
    ) -> List[str]:
        """Get multiple completion suggestions.
        
        Args:
            code: Full code content
            cursor_line: Cursor line number (1-indexed)
            cursor_col: Cursor column number (0-indexed)
            max_suggestions: Maximum number of suggestions
        
        Returns:
            List of completion suggestions
        """
        completions = self.complete(code, cursor_line, cursor_col)
        
        # Limit to max suggestions
        return completions[:max_suggestions]
    
    def complete_line(
        self,
        code: str,
        cursor_line: int,
        cursor_col: int,
        max_tokens: Optional[int] = None
    ) -> str:
        """Complete the current line.
        
        Args:
            code: Full code content
            cursor_line: Cursor line number (1-indexed)
            cursor_col: Cursor column number (0-indexed)
            max_tokens: Maximum tokens to generate
        
        Returns:
            Completed line
        """
        completions = self.complete(code, cursor_line, cursor_col, max_tokens)
        
        if completions:
            # Get first suggestion
            suggestion = completions[0]
            
            # Remove any prefix that matches existing code
            current_line = code.split('\n')[cursor_line - 1]
            
            # Find where to insert completion
            insert_pos = cursor_col
            
            # Check if there's existing text after cursor
            if cursor_col < len(current_line):
                # Remove existing text after cursor
                suggestion = suggestion[len(current_line[cursor_col:]).strip():]
            
            return suggestion.strip()
        
        return ""
