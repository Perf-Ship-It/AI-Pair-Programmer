"""
Project structure parser for AI pair programming.
"""

import os
from pathlib import Path
from typing import Optional


class ProjectStructureParser:
    """Parse and analyze project structure."""
    
    def __init__(self):
        """Initialize project structure parser."""
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp'
        }
    
    def parse_project(self, project_path: str) -> dict:
        """Parse project structure.
        
        Args:
            project_path: Path to project root
        
        Returns:
            Dictionary with project structure information
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            return {"error": f"Project path does not exist: {project_path}"}
        
        # Get all files
        files = {}
        for file_path in project_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                relative_path = file_path.relative_to(project_path)
                files[str(relative_path)] = {
                    "language": self.supported_extensions.get(file_path.suffix, "unknown"),
                    "size": file_path.stat().st_size
                }
        
        # Get directories
        directories = [str(d.relative_to(project_path)) for d in project_path.rglob("*") if d.is_dir()]
        
        return {
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_size": sum(f["size"] for f in files.values())
        }
    
    def get_file_info(self, file_path: str) -> dict:
        """Get information about a specific file.
        
        Args:
            file_path: Path to file (relative to project root)
        
        Returns:
            Dictionary with file information
        """
        project_path = Path(file_path)
        
        if not project_path.exists():
            return {"error": f"File does not exist: {file_path}"}
        
        return {
            "path": str(project_path),
            "language": self.supported_extensions.get(project_path.suffix, "unknown"),
            "size": project_path.stat().st_size,
            "modified": project_path.stat().st_mtime
        }
    
    def find_related_files(self, target_file: str, project_path: str) -> list:
        """Find files related to target file.
        
        Args:
            target_file: Target file path (relative to project root)
            project_path: Path to project root
        
        Returns:
            List of related file paths
        """
        project_path = Path(project_path)
        target_path = project_path / target_file
        
        if not target_path.exists():
            return []
        
        # Get parent directory
        parent_dir = target_path.parent
        
        # Find related files
        related_files = []
        
        # Add parent directory files
        for file_path in parent_dir.glob("*.py"):
            if str(file_path.relative_to(project_path)) != target_file:
                related_files.append(str(file_path.relative_to(project_path)))
        
        # Add sibling files
        for file_path in parent_dir.glob("*"):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                related_files.append(str(file_path.relative_to(project_path)))
        
        # Limit to max files
        return related_files[:10]
    
    def get_file_dependencies(self, file_path: str, project_path: str) -> list:
        """Get dependencies for a file.
        
        Args:
            file_path: File path (relative to project root)
            project_path: Path to project root
        
        Returns:
            List of dependency file paths
        """
        project_path = Path(project_path)
        file_path = project_path / file_path
        
        if not file_path.exists():
            return []
        
        # Read file content
        try:
            content = file_path.read_text()
        except:
            return []
        
        # Extract imports
        dependencies = []
        
        # Python imports
        if file_path.suffix == '.py':
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    # Extract module name
                    if 'import ' in line:
                        module = line.split('import ')[1].split()[0]
                        dependencies.append(module)
                    elif 'from ' in line:
                        module = line.split('from ')[1].split('.')[0]
                        dependencies.append(module)
        
        return dependencies
