"""
MIKE AI - Advanced File Agent
Handles all file system operations with safety checks
"""
import os
import shutil
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from config.settings import AGENT_CONFIG


class FileAgent:
    """
    Advanced file operations agent.
    Capabilities: create, read, write, delete, move, copy, search, organize
    """
    
    def __init__(self):
        self.safe_mode = AGENT_CONFIG["safe_mode"]
        self.allowed_dirs = [Path(d) for d in AGENT_CONFIG["allowed_directories"]]
        self.blocked_commands = AGENT_CONFIG["blocked_commands"]
        
    def _is_safe_path(self, path: Path) -> bool:
        """Check if path is within allowed directories."""
        try:
            resolved = path.resolve()
            return any(str(resolved).startswith(str(d)) for d in self.allowed_dirs)
        except Exception:
            return False
    
    def execute(self, command: str, context: str = "") -> Dict[str, Any]:
        """Execute file operation based on natural language command."""
        cmd_lower = command.lower()
        
        try:
            # Create file/directory
            if any(kw in cmd_lower for kw in ["create", "make", "new"]):
                if "folder" in cmd_lower or "directory" in cmd_lower:
                    return self._create_directory(command)
                else:
                    return self._create_file(command)
            
            # Read file
            elif any(kw in cmd_lower for kw in ["read", "show", "display", "view", "open"]):
                return self._read_file(command)
            
            # Write to file
            elif any(kw in cmd_lower for kw in ["write", "save", "update", "edit"]):
                return self._write_file(command, context)
            
            # Delete
            elif any(kw in cmd_lower for kw in ["delete", "remove"]):
                return self._delete(command)
            
            # Move/Rename
            elif "move" in cmd_lower or "rename" in cmd_lower:
                return self._move_file(command)
            
            # Copy
            elif "copy" in cmd_lower:
                return self._copy_file(command)
            
            # List/Search files
            elif any(kw in cmd_lower for kw in ["list", "find", "search", "show files"]):
                return self._list_files(command)
            
            # Organize files
            elif "organize" in cmd_lower:
                return self._organize_files(command)
            
            # Get file info
            elif any(kw in cmd_lower for kw in ["info", "details", "stat"]):
                return self._get_file_info(command)
            
            else:
                # Default: try to list or create based on context
                return self._list_files(command)
                
        except Exception as e:
            return {"success": False, "error": str(e), "output": None}
    
    def _extract_path(self, command: str) -> Optional[Path]:
        """Extract file path from command."""
        import re
        # Look for quoted paths or common patterns
        patterns = [
            r'["\']([^"\']*?)["\']',  # Quoted strings
            r'\b(\w+\.+\w+)\b',  # Filenames with extensions
            r'\b(/[^\s]+)\b',  # Unix paths
            r'\b([A-Za-z]:\\[^\s]+)\b',  # Windows paths
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, command)
            if matches:
                path_str = matches[0]
                path = Path(path_str).expanduser()
                if self._is_safe_path(path):
                    return path
        
        # Return current directory if no path found
        return Path.cwd()
    
    def _create_file(self, command: str) -> Dict[str, Any]:
        """Create a new file."""
        import re
        
        # Extract filename
        name_match = re.search(r'["\']([^"\']+\.?\w*)["\']|(\w+\.+\w+)', command)
        if not name_match:
            # Generate default name
            filename = "new_file.txt"
        else:
            filename = name_match.group(1) or name_match.group(2)
        
        filepath = Path(filename)
        if not filepath.is_absolute():
            filepath = Path.cwd() / filepath
        
        if not self._is_safe_path(filepath):
            return {"success": False, "error": "Path not allowed", "output": None}
        
        # Extract content if provided
        content_match = re.search(r'(?:with|containing)[:\s]+(.+)$', command, re.IGNORECASE)
        content = content_match.group(1).strip() if content_match else ""
        
        # Create parent directories if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        filepath.write_text(content)
        
        return {
            "success": True,
            "output": f"Created file: {filepath}\nSize: {filepath.stat().st_size} bytes",
            "path": str(filepath),
            "action": "create_file"
        }
    
    def _create_directory(self, command: str) -> Dict[str, Any]:
        """Create a new directory."""
        import re
        
        # Try multiple patterns to extract directory name
        dirname = None
        
        # Pattern 1: "named X" or "called X"
        match = re.search(r'(?:named|called)\s+["\']?(\w+)["\']?', command, re.IGNORECASE)
        if match:
            dirname = match.group(1)
        
        # Pattern 2: mkdir X
        if not dirname:
            match = re.search(r'mkdir\s+(\w+)', command)
            if match:
                dirname = match.group(1)
        
        # Pattern 3: Quoted string
        if not dirname:
            match = re.search(r'["\']([^"\']+)["\']', command)
            if match:
                dirname = match.group(1)
        
        # Pattern 4: Last meaningful word (excluding common keywords)
        if not dirname:
            keywords = {'create', 'a', 'an', 'the', 'folder', 'directory', 'named', 'called', 'make', 'new', 'mkdir'}
            words = command.split()
            for word in reversed(words):
                clean = re.sub(r'[^\w]', '', word)
                if clean and clean.lower() not in keywords:
                    dirname = clean
                    break
        
        # Default fallback
        if not dirname:
            dirname = "new_folder"
        
        dirpath = Path(dirname)
        if not dirpath.is_absolute():
            dirpath = Path.cwd() / dirpath
        
        if not self._is_safe_path(dirpath):
            return {"success": False, "error": "Path not allowed", "output": None}
        
        dirpath.mkdir(parents=True, exist_ok=True)
        
        return {
            "success": True,
            "output": f"Created directory: {dirpath}",
            "path": str(dirpath),
            "action": "create_directory"
        }
    
    def _read_file(self, command: str) -> Dict[str, Any]:
        """Read file contents."""
        filepath = self._extract_path(command)
        
        if not filepath or not filepath.exists():
            return {"success": False, "error": f"File not found: {filepath}", "output": None}
        
        if filepath.is_dir():
            return self._list_files(f"list files in {filepath}")
        
        try:
            content = filepath.read_text()
            lines = content.split('\n')
            
            return {
                "success": True,
                "output": f"=== {filepath.name} ===\n{content}",
                "path": str(filepath),
                "lines": len(lines),
                "size": filepath.stat().st_size,
                "action": "read_file"
            }
        except UnicodeDecodeError:
            return {
                "success": True,
                "output": f"Binary file: {filepath} ({filepath.stat().st_size} bytes)",
                "action": "read_binary"
            }
    
    def _write_file(self, command: str, context: str = "") -> Dict[str, Any]:
        """Write content to file."""
        filepath = self._extract_path(command)
        
        if not filepath:
            return {"success": False, "error": "Could not determine file path", "output": None}
        
        if not self._is_safe_path(filepath):
            return {"success": False, "error": "Path not allowed", "output": None}
        
        # Extract content from command or use context
        import re
        content_match = re.search(r'(?:write|save)[:\s]+(.+?)(?:to|in|$)', command, re.IGNORECASE | re.DOTALL)
        content = content_match.group(1).strip() if content_match else context
        
        if not content:
            content = "# New file created by MIKE\n"
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        
        return {
            "success": True,
            "output": f"Written to {filepath} ({len(content)} characters)",
            "path": str(filepath),
            "action": "write_file"
        }
    
    def _delete(self, command: str) -> Dict[str, Any]:
        """Delete file or directory."""
        filepath = self._extract_path(command)
        
        if not filepath or not filepath.exists():
            return {"success": False, "error": "Path not found", "output": None}
        
        if not self._is_safe_path(filepath):
            return {"success": False, "error": "Path not allowed for deletion", "output": None}
        
        if self.safe_mode:
            # In safe mode, just report what would be deleted
            target_type = "directory" if filepath.is_dir() else "file"
            return {
                "success": True,
                "output": f"[Safe Mode] Would delete {target_type}: {filepath}\nUse --no-safe-mode to actually delete.",
                "action": "delete_dry_run"
            }
        
        if filepath.is_dir():
            shutil.rmtree(filepath)
        else:
            filepath.unlink()
        
        return {
            "success": True,
            "output": f"Deleted: {filepath}",
            "action": "delete"
        }
    
    def _move_file(self, command: str) -> Dict[str, Any]:
        """Move or rename file."""
        import re
        
        # Try to extract source and destination
        parts = re.split(r'\b(to|as)\b', command, flags=re.IGNORECASE)
        if len(parts) >= 3:
            src_name = parts[0].strip()
            dst_name = parts[2].strip()
            
            src = Path(src_name)
            dst = Path(dst_name)
            
            if not src.is_absolute():
                src = Path.cwd() / src
            if not dst.is_absolute():
                dst = Path.cwd() / dst
            
            if src.exists() and self._is_safe_path(src) and self._is_safe_path(dst):
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                
                return {
                    "success": True,
                    "output": f"Moved {src} → {dst}",
                    "action": "move"
                }
        
        return {"success": False, "error": "Could not parse move command", "output": None}
    
    def _copy_file(self, command: str) -> Dict[str, Any]:
        """Copy file."""
        import re
        
        parts = re.split(r'\b(to|as)\b', command, flags=re.IGNORECASE)
        if len(parts) >= 3:
            src_name = parts[0].strip()
            dst_name = parts[2].strip()
            
            src = Path(src_name)
            dst = Path(dst_name)
            
            if not src.is_absolute():
                src = Path.cwd() / src
            if not dst.is_absolute():
                dst = Path.cwd() / dst
            
            if src.exists() and self._is_safe_path(src) and self._is_safe_path(dst):
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    shutil.copytree(str(src), str(dst))
                else:
                    shutil.copy2(str(src), str(dst))
                
                return {
                    "success": True,
                    "output": f"Copied {src} → {dst}",
                    "action": "copy"
                }
        
        return {"success": False, "error": "Could not parse copy command", "output": None}
    
    def _list_files(self, command: str) -> Dict[str, Any]:
        """List files in directory."""
        filepath = self._extract_path(command)
        
        if not filepath:
            filepath = Path.cwd()
        
        if not filepath.exists():
            return {"success": False, "error": f"Path not found: {filepath}", "output": None}
        
        if filepath.is_file():
            return self._read_file(f"read {filepath}")
        
        # Filter by extension if specified
        import re
        ext_match = re.search(r'\.(\w+)\s*files?', command, re.IGNORECASE)
        extension = f".{ext_match.group(1)}" if ext_match else None
        
        files = []
        dirs = []
        
        try:
            for item in filepath.iterdir():
                if extension and not item.name.endswith(extension):
                    continue
                if item.is_dir():
                    dirs.append(item.name)
                else:
                    files.append(item.name)
        except PermissionError:
            return {"success": False, "error": "Permission denied", "output": None}
        
        output_lines = [f"📁 {filepath}"]
        if dirs:
            output_lines.append("\n📂 Directories:")
            output_lines.extend([f"  {d}/" for d in sorted(dirs)])
        if files:
            output_lines.append("\n📄 Files:")
            output_lines.extend([f"  {f}" for f in sorted(files)])
        
        return {
            "success": True,
            "output": "\n".join(output_lines),
            "directories": dirs,
            "files": files,
            "total": len(dirs) + len(files),
            "action": "list_files"
        }
    
    def _organize_files(self, command: str) -> Dict[str, Any]:
        """Organize files by type/extension."""
        filepath = self._extract_path(command)
        
        if not filepath or not filepath.is_dir():
            return {"success": False, "error": "Please specify a valid directory", "output": None}
        
        organized = {}
        
        for item in filepath.iterdir():
            if item.is_file():
                ext = item.suffix.lower().replace('.', '') or 'no_extension'
                if ext not in organized:
                    organized[ext] = []
                organized[ext].append(item.name)
        
        output_lines = [f"📊 Organization summary for {filepath}:"]
        for ext, files in sorted(organized.items()):
            output_lines.append(f"  • .{ext}: {len(files)} files")
        
        return {
            "success": True,
            "output": "\n".join(output_lines),
            "organization": organized,
            "action": "organize_files"
        }
    
    def _get_file_info(self, command: str) -> Dict[str, Any]:
        """Get detailed file information."""
        filepath = self._extract_path(command)
        
        if not filepath or not filepath.exists():
            return {"success": False, "error": "File not found", "output": None}
        
        stat = filepath.stat()
        
        info = {
            "name": filepath.name,
            "path": str(filepath.absolute()),
            "type": "directory" if filepath.is_dir() else "file",
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:],
        }
        
        output = (
            f"📄 Name: {info['name']}\n"
            f"📍 Path: {info['path']}\n"
            f"📊 Type: {info['type']}\n"
            f"💾 Size: {info['size']} bytes\n"
            f"🕐 Modified: {__import__('datetime').datetime.fromtimestamp(info['modified'])}\n"
            f"🔒 Permissions: {info['permissions']}"
        )
        
        return {
            "success": True,
            "output": output,
            "info": info,
            "action": "file_info"
        }
