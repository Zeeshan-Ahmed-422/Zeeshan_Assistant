"""
File Manager
Handles file operations like creating folders, organizing files, etc.
"""
import os
import shutil
from datetime import datetime
from pathlib import Path
from utils.logger import logger

class FileManager:
    """Manage file operations"""
    
    def __init__(self):
        """Initialize file manager"""
        self.home_dir = Path.home()
        self.downloads_dir = self.home_dir / "Downloads"
        self.documents_dir = self.home_dir / "Documents"
        logger.info("File manager initialized")
    
    def create_folder(self, folder_name, location=None):
        """
        Create a new folder
        
        Args:
            folder_name: Name of folder to create
            location: Location path (default: Documents)
            
        Returns:
            bool: True if successful
        """
        try:
            if location is None:
                location = self.documents_dir
            else:
                location = Path(location)
            
            # Create folder path
            folder_path = location / folder_name
            
            # Create folder
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created folder: {folder_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return False
    
    def create_project_folder(self, project_name=None):
        """
        Create a project folder with date
        
        Args:
            project_name: Name of project (default: uses date)
            
        Returns:
            bool: True if successful
        """
        try:
            if project_name is None:
                project_name = datetime.now().strftime("Project_%Y%m%d")
            else:
                # Add date to project name
                date_str = datetime.now().strftime("%Y%m%d")
                project_name = f"{project_name}_{date_str}"
            
            # Create in Documents
            project_path = self.documents_dir / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create subfolders
            (project_path / "src").mkdir(exist_ok=True)
            (project_path / "docs").mkdir(exist_ok=True)
            (project_path / "data").mkdir(exist_ok=True)
            
            logger.info(f"Created project folder: {project_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating project folder: {e}")
            return False
    
    def clean_downloads(self):
        """
        Organize files in Downloads folder
        
        Returns:
            dict: Statistics of cleaned files
        """
        try:
            if not self.downloads_dir.exists():
                logger.warning("Downloads folder not found")
                return None
            
            stats = {
                "images": 0,
                "documents": 0,
                "videos": 0,
                "archives": 0,
                "others": 0
            }
            
            # File type mappings
            file_types = {
                "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
                "documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx"],
                "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
                "archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
            }
            
            # Create category folders
            for category in file_types.keys():
                category_path = self.downloads_dir / category.capitalize()
                category_path.mkdir(exist_ok=True)
            
            # Organize files
            for item in self.downloads_dir.iterdir():
                if item.is_file():
                    extension = item.suffix.lower()
                    moved = False
                    
                    # Check each category
                    for category, extensions in file_types.items():
                        if extension in extensions:
                            dest_path = self.downloads_dir / category.capitalize() / item.name
                            
                            # Move file if not already in category folder
                            if not str(item.parent).endswith(category.capitalize()):
                                try:
                                    shutil.move(str(item), str(dest_path))
                                    stats[category] += 1
                                    moved = True
                                    break
                                except Exception as e:
                                    logger.error(f"Error moving {item.name}: {e}")
                    
                    if not moved and extension:
                        # Move to Others
                        others_path = self.downloads_dir / "Others"
                        others_path.mkdir(exist_ok=True)
                        try:
                            dest_path = others_path / item.name
                            if not str(item.parent).endswith("Others"):
                                shutil.move(str(item), str(dest_path))
                                stats["others"] += 1
                        except Exception as e:
                            logger.error(f"Error moving {item.name}: {e}")
            
            logger.info(f"Downloads cleaned: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error cleaning downloads: {e}")
            return None
    
    def delete_temp_files(self):
        """
        Delete temporary files
        
        Returns:
            int: Number of files deleted
        """
        try:
            temp_extensions = [".tmp", ".temp", ".cache"]
            deleted_count = 0
            
            # Check Downloads
            for item in self.downloads_dir.iterdir():
                if item.is_file() and item.suffix.lower() in temp_extensions:
                    try:
                        item.unlink()
                        deleted_count += 1
                    except Exception as e:
                        logger.error(f"Error deleting {item.name}: {e}")
            
            logger.info(f"Deleted {deleted_count} temporary files")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error deleting temp files: {e}")
            return 0

# Global file manager instance
file_manager = FileManager()