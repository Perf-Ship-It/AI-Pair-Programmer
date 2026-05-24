"""
Refactoring engine for AI pair programming.
"""

from typing import Optional, List, Dict
from AI_Pair_Engineer.models.llm_manager import LLMManager
from AI_Pair_Engineer.context.analyzer import ContextAnalyzer
from AI_Pair_Engineer.utils.code_formatter import CodeFormatter
from AI_Pair_Engineer.utils.prompt_templates import PromptTemplates


class RefactoringEngine:
    """Engine for refactoring suggestions."""
    
    def __init__(
        self,
        llm_manager: Optional[LLMManager] = None,
        context_analyzer: Optional[ContextAnalyzer] = None,
        code_formatter: Optional[CodeFormatter] = None,
        prompt_templates: Optional[PromptTemplates] = None
    ):
        """Initialize refactoring engine.
        
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
    
    def analyze(self, code: str) -> Dict:
        """Analyze code for refactoring opportunities.
        
        Args:
            code: Code to analyze
        
        Returns:
            Dictionary with analysis results
        """
        # Format prompt
        prompt = self.prompt_templates.format_refactoring_prompt(code)
        
        # Generate analysis
        response = self.llm_manager.generate(prompt)
        
        # Parse response
        return self._parse_analysis(response)
    
    def _parse_analysis(self, response: str) -> Dict:
        """Parse refactoring analysis response.
        
        Args:
            response: LLM response
        
        Returns:
            Dictionary with analysis results
        """
        # Simple parsing - in production, use structured output
        issues = []
        suggestions = []
        
        # Extract issues
        if "issue" in response.lower() or "problem" in response.lower():
            # Parse issues from response
            lines = response.split('\n')
            for line in lines:
                if "issue" in line.lower() or "problem" in line.lower():
                    issues.append(line.strip())
        
        # Extract suggestions
        if "suggestion" in response.lower() or "improvement" in response.lower():
            # Parse suggestions from response
            lines = response.split('\n')
            for line in lines:
                if "suggestion" in line.lower() or "improvement" in line.lower():
                    suggestions.append(line.strip())
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "response": response
        }
    
    def suggest_refactorings(
        self,
        code: str,
        max_suggestions: int = 5
    ) -> List[Dict]:
        """Get refactoring suggestions.
        
        Args:
            code: Code to analyze
            max_suggestions: Maximum number of suggestions
        
        Returns:
            List of refactoring suggestions
        """
        analysis = self.analyze(code)
        
        # Extract suggestions
        suggestions = analysis.get("suggestions", [])
        
        # Limit to max suggestions
        return suggestions[:max_suggestions]
    
    def get_code_smells(
        self,
        code: str
    ) -> List[Dict]:
        """Identify code smells in the code.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of code smells
        """
        analysis = self.analyze(code)
        
        # Extract issues as code smells
        smells = []
        for issue in analysis.get("issues", []):
            smells.append({
                "description": issue,
                "severity": "medium",
                "fix": "Review and refactor"
            })
        
        return smells
    
    def get_performance_issues(
        self,
        code: str
    ) -> List[Dict]:
        """Identify performance issues in the code.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of performance issues
        """
        analysis = self.analyze(code)
        
        # Extract performance-related issues
        issues = []
        for issue in analysis.get("issues", []):
            if "performance" in issue.lower() or "slow" in issue.lower() or "inefficient" in issue.lower():
                issues.append({
                    "description": issue,
                    "severity": "high",
                    "fix": "Optimize algorithm or data structure"
                })
        
        return issues
    
    def get_security_issues(
        self,
        code: str
    ) -> List[Dict]:
        """Identify security issues in the code.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of security issues
        """
        analysis = self.analyze(code)
        
        # Extract security-related issues
        issues = []
        for issue in analysis.get("issues", []):
            if "security" in issue.lower() or "vulnerability" in issue.lower() or "unsafe" in issue.lower():
                issues.append({
                    "description": issue,
                    "severity": "critical",
                    "fix": "Fix security vulnerability"
                })
        
        return issues
