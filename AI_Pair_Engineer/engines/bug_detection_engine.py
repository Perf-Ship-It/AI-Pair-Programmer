"""
Bug detection engine for AI pair programming.
"""

from typing import Optional, List, Dict
from AI_Pair_Engineer.models.llm_manager import LLMManager
from AI_Pair_Engineer.context.analyzer import ContextAnalyzer
from AI_Pair_Engineer.utils.code_formatter import CodeFormatter
from AI_Pair_Engineer.utils.prompt_templates import PromptTemplates


class BugDetectionEngine:
    """Engine for bug detection."""
    
    def __init__(
        self,
        llm_manager: Optional[LLMManager] = None,
        context_analyzer: Optional[ContextAnalyzer] = None,
        code_formatter: Optional[CodeFormatter] = None,
        prompt_templates: Optional[PromptTemplates] = None
    ):
        """Initialize bug detection engine.
        
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
        """Analyze code for potential bugs.
        
        Args:
            code: Code to analyze
        
        Returns:
            Dictionary with analysis results
        """
        # Format prompt
        prompt = self.prompt_templates.format_bug_detection_prompt(code)
        
        # Generate analysis
        response = self.llm_manager.generate(prompt)
        
        # Parse response
        return self._parse_analysis(response)
    
    def _parse_analysis(self, response: str) -> Dict:
        """Parse bug detection analysis response.
        
        Args:
            response: LLM response
        
        Returns:
            Dictionary with analysis results
        """
        # Simple parsing - in production, use structured output
        bugs = []
        warnings = []
        
        # Extract bugs
        if "bug" in response.lower() or "error" in response.lower():
            # Parse bugs from response
            lines = response.split('\n')
            for line in lines:
                if "bug" in line.lower() or "error" in line.lower():
                    bugs.append(line.strip())
        
        # Extract warnings
        if "warning" in response.lower():
            # Parse warnings from response
            lines = response.split('\n')
            for line in lines:
                if "warning" in line.lower():
                    warnings.append(line.strip())
        
        return {
            "bugs": bugs,
            "warnings": warnings,
            "response": response
        }
    
    def detect_bugs(
        self,
        code: str
    ) -> List[Dict]:
        """Detect bugs in the code.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of detected bugs
        """
        analysis = self.analyze(code)
        
        # Extract bugs
        bugs = analysis.get("bugs", [])
        
        # Format bugs
        formatted_bugs = []
        for bug in bugs:
            formatted_bugs.append({
                "description": bug,
                "severity": "high",
                "fix": "Review and fix the bug"
            })
        
        return formatted_bugs
    
    def detect_null_pointer_issues(
        self,
        code: str
    ) -> List[Dict]:
        """Detect potential null pointer exceptions.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of null pointer issues
        """
        analysis = self.analyze(code)
        
        # Extract null pointer issues
        issues = []
        for bug in analysis.get("bugs", []):
            if "null" in bug.lower() or "none" in bug.lower() or "undefined" in bug.lower():
                issues.append({
                    "description": bug,
                    "severity": "high",
                    "fix": "Add null checks"
                })
        
        return issues
    
    def detect_off_by_one_errors(
        self,
        code: str
    ) -> List[Dict]:
        """Detect potential off-by-one errors.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of off-by-one errors
        """
        analysis = self.analyze(code)
        
        # Extract off-by-one errors
        issues = []
        for bug in analysis.get("bugs", []):
            if "off-by-one" in bug.lower() or "boundary" in bug.lower() or "index" in bug.lower():
                issues.append({
                    "description": bug,
                    "severity": "medium",
                    "fix": "Review loop bounds and array indices"
                })
        
        return issues
    
    def detect_resource_leaks(
        self,
        code: str
    ) -> List[Dict]:
        """Detect potential resource leaks.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of resource leaks
        """
        analysis = self.analyze(code)
        
        # Extract resource leak issues
        issues = []
        for bug in analysis.get("bugs", []):
            if "leak" in bug.lower() or "close" in bug.lower() or "release" in bug.lower():
                issues.append({
                    "description": bug,
                    "severity": "medium",
                    "fix": "Ensure proper resource cleanup"
                })
        
        return issues
    
    def detect_race_conditions(
        self,
        code: str
    ) -> List[Dict]:
        """Detect potential race conditions.
        
        Args:
            code: Code to analyze
        
        Returns:
            List of race conditions
        """
        analysis = self.analyze(code)
        
        # Extract race condition issues
        issues = []
        for bug in analysis.get("bugs", []):
            if "race" in bug.lower() or "concurrent" in bug.lower() or "thread" in bug.lower():
                issues.append({
                    "description": bug,
                    "severity": "high",
                    "fix": "Add proper synchronization"
                })
        
        return issues
