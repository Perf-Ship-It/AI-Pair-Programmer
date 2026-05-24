"""
Prompt templates for AI pair programming.
"""

from typing import Optional


class PromptTemplates:
    """Manage prompt templates for different features."""
    
    def __init__(self):
        """Initialize prompt templates."""
        self.templates = {
            "completion": self._get_completion_template(),
            "refactoring": self._get_refactoring_template(),
            "bug_detection": self._get_bug_detection_template(),
            "explanation": self._get_explanation_template(),
            "documentation": self._get_documentation_template()
        }
    
    def _get_completion_template(self) -> str:
        """Get code completion prompt template."""
        return """Complete the following code:

Context:
{context}

Current code:
{code}

Cursor position: line {cursor_line}, column {cursor_col}

Please complete the code in a way that:
1. Maintains the existing coding style
2. Follows best practices
3. Handles edge cases appropriately
4. Is consistent with the surrounding code

Complete the code:
"""
    
    def _get_refactoring_template(self) -> str:
        """Get refactoring suggestion prompt template."""
        return """Analyze the following code and suggest improvements:

Code:
{code}

Please identify:
1. Code smells or anti-patterns
2. Performance issues
3. Security vulnerabilities
4. Maintainability concerns
5. Best practice violations

For each issue found, provide:
- Description of the issue
- Why it's a problem
- How to fix it
- Example of the improved code

Refactoring suggestions:
"""
    
    def _get_bug_detection_template(self) -> str:
        """Get bug detection prompt template."""
        return """Analyze the following code for potential bugs:

Code:
{code}

Please check for:
1. Null pointer exceptions
2. Off-by-one errors
3. Resource leaks
4. Race conditions
5. Type mismatches
6. Logic errors
7. Boundary condition issues

For each potential bug found, provide:
- Description of the potential issue
- Why it could cause a problem
- How to fix it
- Test case to verify the fix

Bug detection results:
"""
    
    def _get_explanation_template(self) -> str:
        """Get code explanation prompt template."""
        return """Explain the following code:

Code:
{code}

Please provide:
1. High-level overview of what the code does
2. Detailed explanation of key components
3. Explanation of important algorithms or patterns
4. Notes on performance considerations
5. Any important caveats or limitations

Explanation:
"""
    
    def _get_documentation_template(self) -> str:
        """Get documentation generation prompt template."""
        return """Generate documentation for the following code:

Code:
{code}

Please generate:
1. Module-level docstring
2. Class docstrings
3. Method docstrings
4. Parameter descriptions
5. Return value descriptions
6. Example usage
7. Notes on usage and limitations

Documentation:
"""
    
    def get_template(self, template_name: str) -> str:
        """Get a prompt template by name.
        
        Args:
            template_name: Name of the template
        
        Returns:
            Template string
        """
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        return self.templates[template_name]
    
    def format_completion_prompt(
        self,
        context: str,
        code: str,
        cursor_line: int,
        cursor_col: int
    ) -> str:
        """Format code completion prompt.
        
        Args:
            context: Code context
            code: Current code
            cursor_line: Cursor line number
            cursor_col: Cursor column number
        
        Returns:
            Formatted prompt
        """
        template = self.get_template("completion")
        return template.format(
            context=context,
            code=code,
            cursor_line=cursor_line,
            cursor_col=cursor_col
        )
    
    def format_refactoring_prompt(self, code: str) -> str:
        """Format refactoring suggestion prompt.
        
        Args:
            code: Code to analyze
        
        Returns:
            Formatted prompt
        """
        template = self.get_template("refactoring")
        return template.format(code=code)
    
    def format_bug_detection_prompt(self, code: str) -> str:
        """Format bug detection prompt.
        
        Args:
            code: Code to analyze
        
        Returns:
            Formatted prompt
        """
        template = self.get_template("bug_detection")
        return template.format(code=code)
    
    def format_explanation_prompt(self, code: str) -> str:
        """Format code explanation prompt.
        
        Args:
            code: Code to explain
        
        Returns:
            Formatted prompt
        """
        template = self.get_template("explanation")
        return template.format(code=code)
    
    def format_documentation_prompt(self, code: str) -> str:
        """Format documentation generation prompt.
        
        Args:
            code: Code to document
        
        Returns:
            Formatted prompt
        """
        template = self.get_template("documentation")
        return template.format(code=code)
