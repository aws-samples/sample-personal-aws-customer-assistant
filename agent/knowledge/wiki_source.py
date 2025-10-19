"""WikiKnowledgeSource - File I/O operations for GitHub wiki repository."""

from pathlib import Path
from typing import List

import git


class WikiKnowledgeSource:
    """Provides file I/O operations for GitHub wiki repository.
    
    Handles cloning/updating GitHub wiki repository and provides
    file access operations. No search logic - only data access.
    """
    
    def __init__(self, repo_url: str, local_path: Path) -> None:
        """Initialize WikiKnowledgeSource.
        
        Args:
            repo_url: GitHub wiki repository URL
            local_path: Local directory to clone/store wiki
        """
        self.repo_url = repo_url
        self.local_path = Path(local_path)
    
    def clone_or_update(self) -> None:
        """Clone repository if not exists, otherwise pull latest changes."""
        if self.local_path.exists() and (self.local_path / ".git").exists():
            # Repository exists, pull latest changes
            repo = git.Repo(self.local_path)
            repo.remotes.origin.pull()
        else:
            # Clone repository
            self.local_path.mkdir(parents=True, exist_ok=True)
            git.Repo.clone_from(self.repo_url, self.local_path)
    
    def load_file(self, path: Path) -> str:
        """Load file contents by path.
        
        Args:
            path: Path to file relative to wiki root or absolute path
            
        Returns:
            File contents as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if path.is_absolute():
            file_path = path
        else:
            file_path = self.local_path / path
            
        return file_path.read_text(encoding='utf-8')
    
    def list_files(self) -> List[Path]:
        """List all files in the wiki repository.
        
        Returns:
            List of file paths relative to wiki root
        """
        if not self.local_path.exists():
            return []
            
        files = []
        for file_path in self.local_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                # Return path relative to wiki root
                relative_path = file_path.relative_to(self.local_path)
                files.append(relative_path)
        
        return files
