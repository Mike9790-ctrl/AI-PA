"""
MIKE AI - System Agent
System monitoring, process management, and diagnostics
"""
import os
import platform
from typing import Dict, Any, List

from config.settings import SYSTEM_CONFIG


class SystemAgent:
    """
    Advanced system operations agent.
    Capabilities: monitor resources, list processes, get system info, cleanup
    """
    
    def __init__(self):
        self.monitor_interval = SYSTEM_CONFIG["monitor_interval"]
        self.alert_thresholds = SYSTEM_CONFIG["alert_thresholds"]
        
    def execute(self, command: str, context: str = "") -> Dict[str, Any]:
        """Execute system operation based on natural language command."""
        cmd_lower = command.lower()
        
        try:
            # System information
            if any(kw in cmd_lower for kw in ["system info", "system information", "specs", "specifications"]):
                return self._get_system_info()
            
            # CPU monitoring
            elif any(kw in cmd_lower for kw in ["cpu", "processor"]):
                return self._get_cpu_info()
            
            # Memory monitoring
            elif any(kw in cmd_lower for kw in ["memory", "ram"]):
                return self._get_memory_info()
            
            # Disk usage
            elif any(kw in cmd_lower for kw in ["disk", "storage", "drive"]):
                return self._get_disk_info()
            
            # Process list
            elif any(kw in cmd_lower for kw in ["process", "running", "tasks"]):
                return self._list_processes(command)
            
            # Network info
            elif any(kw in cmd_lower for kw in ["network", "ip", "internet"]):
                return self._get_network_info()
            
            # Cleanup
            elif "cleanup" in cmd_lower or "clean" in cmd_lower:
                return self._cleanup_system()
            
            # General health check
            elif any(kw in cmd_lower for kw in ["health", "status", "check"]):
                return self._health_check()
            
            else:
                # Default to system info
                return self._get_system_info()
                
        except Exception as e:
            return {"success": False, "error": str(e), "output": None}
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "username": os.getenv("USERNAME") or os.getenv("USER") or "Unknown",
        }
        
        output = (
            f"💻 System Information\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"OS: {info['os']} ({info['os_version']})\n"
            f"Architecture: {info['architecture']}\n"
            f"Processor: {info['processor']}\n"
            f"Python: {info['python_version']}\n"
            f"Hostname: {info['hostname']}\n"
            f"User: {info['username']}"
        )
        
        return {
            "success": True,
            "output": output,
            "info": info,
            "action": "system_info"
        }
    
    def _get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information and usage."""
        cpu_info = {
            "processor": platform.processor() or "Unknown",
            "cores": os.cpu_count() or 1,
        }
        
        # Try to get real-time CPU usage
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_info["usage"] = f"{cpu_percent}%"
            cpu_info["per_core"] = psutil.cpu_percent(interval=1, percpu=True)
        except ImportError:
            cpu_info["usage"] = "N/A (install psutil)"
        
        output = (
            f"🖥️ CPU Information\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Processor: {cpu_info['processor']}\n"
            f"Cores: {cpu_info['cores']}\n"
            f"Usage: {cpu_info['usage']}"
        )
        
        if "per_core" in cpu_info:
            output += "\nPer-core usage: " + ", ".join([f"{c}%" for c in cpu_info["per_core"]])
        
        return {
            "success": True,
            "output": output,
            "info": cpu_info,
            "action": "cpu_info"
        }
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information."""
        mem_info = {}
        
        try:
            import psutil
            mem = psutil.virtual_memory()
            
            mem_info = {
                "total": f"{mem.total / (1024**3):.2f} GB",
                "available": f"{mem.available / (1024**3):.2f} GB",
                "used": f"{mem.used / (1024**3):.2f} GB",
                "percent": f"{mem.percent}%",
            }
            
            # Check threshold
            alert = mem.percent > self.alert_thresholds["memory_percent"]
            if alert:
                mem_info["alert"] = "⚠️ High memory usage!"
            
        except ImportError:
            mem_info = {"status": "N/A (install psutil)"}
        
        output = (
            f"🧠 Memory Information\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Total: {mem_info.get('total', 'N/A')}\n"
            f"Available: {mem_info.get('available', 'N/A')}\n"
            f"Used: {mem_info.get('used', 'N/A')}\n"
            f"Usage: {mem_info.get('percent', 'N/A')}"
        )
        
        if "alert" in mem_info:
            output += f"\n{mem_info['alert']}"
        
        return {
            "success": True,
            "output": output,
            "info": mem_info,
            "action": "memory_info"
        }
    
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk usage information."""
        disk_info = []
        
        try:
            import psutil
            
            partitions = psutil.disk_partitions()
            for partition in partitions[:5]:  # Limit to first 5
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "total": f"{usage.total / (1024**3):.2f} GB",
                        "used": f"{usage.used / (1024**3):.2f} GB",
                        "free": f"{usage.free / (1024**3):.2f} GB",
                        "percent": f"{usage.percent}%",
                    })
                except PermissionError:
                    pass
                    
        except ImportError:
            disk_info = [{"status": "N/A (install psutil)"}]
        
        output_lines = ["💾 Disk Usage\n━━━━━━━━━━━━━━━━━━━━━━"]
        for disk in disk_info:
            if "status" in disk:
                output_lines.append(disk["status"])
            else:
                output_lines.append(
                    f"\n{disk['mountpoint']} ({disk['device']}):\n"
                    f"  Total: {disk['total']}\n"
                    f"  Used: {disk['used']} ({disk['percent']})\n"
                    f"  Free: {disk['free']}"
                )
        
        return {
            "success": True,
            "output": "\n".join(output_lines),
            "disks": disk_info,
            "action": "disk_info"
        }
    
    def _list_processes(self, command: str) -> Dict[str, Any]:
        """List running processes."""
        processes = []
        
        try:
            import psutil
            
            limit = 20  # Show top 20 processes
            filter_term = ""
            
            # Check for filter term
            import re
            filter_match = re.search(r'(?:for|named|called)\s+(\w+)', command, re.IGNORECASE)
            if filter_match:
                filter_term = filter_match.group(1).lower()
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    if filter_term and filter_term not in pinfo['name'].lower():
                        continue
                    
                    processes.append(pinfo)
                    
                    if len(processes) >= limit:
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by memory usage
            processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
            
        except ImportError:
            return {
                "success": True,
                "output": "Install psutil to view processes",
                "action": "process_list_unavailable"
            }
        
        output_lines = ["🔄 Top Processes (by memory)\n━━━━━━━━━━━━━━━━━━━━━━"]
        for i, proc in enumerate(processes, 1):
            output_lines.append(
                f"{i}. {proc['name'][:30]:<30} PID: {proc['pid']:<6} "
                f"Mem: {proc.get('memory_percent', 0):.1f}%"
            )
        
        return {
            "success": True,
            "output": "\n".join(output_lines),
            "processes": processes,
            "count": len(processes),
            "action": "list_processes"
        }
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network information."""
        net_info = {}
        
        try:
            import socket
            import psutil
            
            # Get hostname and IP
            hostname = socket.gethostname()
            try:
                ip = socket.gethostbyname(hostname)
            except:
                ip = "127.0.0.1"
            
            net_info["hostname"] = hostname
            net_info["ip"] = ip
            
            # Network interfaces
            interfaces = psutil.net_if_stats()
            net_info["interfaces"] = list(interfaces.keys())
            
            # Network I/O
            net_io = psutil.net_io_counters()
            net_info["bytes_sent"] = f"{net_io.bytes_sent / (1024**2):.2f} MB"
            net_info["bytes_recv"] = f"{net_io.bytes_recv / (1024**2):.2f} MB"
            
        except ImportError:
            net_info = {"status": "N/A (install psutil)"}
        except Exception as e:
            net_info = {"error": str(e)}
        
        output = (
            f"🌐 Network Information\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Hostname: {net_info.get('hostname', 'N/A')}\n"
            f"IP Address: {net_info.get('ip', 'N/A')}\n"
            f"Interfaces: {', '.join(net_info.get('interfaces', []))}\n"
            f"Data Sent: {net_info.get('bytes_sent', 'N/A')}\n"
            f"Data Received: {net_info.get('bytes_recv', 'N/A')}"
        )
        
        return {
            "success": True,
            "output": output,
            "info": net_info,
            "action": "network_info"
        }
    
    def _cleanup_system(self) -> Dict[str, Any]:
        """Perform system cleanup (safe operations only)."""
        cleaned = []
        freed_space = 0
        
        # Clean temp directories
        temp_dirs = [
            os.path.join(os.getcwd(), "__pycache__"),
            os.path.join(os.getcwd(), ".pytest_cache"),
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    import shutil
                    count = sum(len(files) for _, _, files in os.walk(temp_dir))
                    shutil.rmtree(temp_dir)
                    cleaned.append(f"Removed: {temp_dir} ({count} files)")
                except Exception as e:
                    cleaned.append(f"Failed to clean {temp_dir}: {str(e)}")
        
        output = (
            f"🧹 System Cleanup\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Actions performed:\n" +
            "\n".join([f"  • {c}" for c in cleaned]) +
            f"\n\nEstimated space freed: {freed_space} bytes"
        )
        
        return {
            "success": True,
            "output": output,
            "cleaned": cleaned,
            "action": "cleanup"
        }
    
    def _health_check(self) -> Dict[str, Any]:
        """Perform comprehensive system health check."""
        checks = []
        alerts = []
        
        # CPU check
        try:
            import psutil
            cpu_usage = psutil.cpu_percent(interval=0.5)
            status = "✓" if cpu_usage < self.alert_thresholds["cpu_percent"] else "⚠️"
            checks.append(f"{status} CPU: {cpu_usage}%")
            if cpu_usage >= self.alert_thresholds["cpu_percent"]:
                alerts.append("High CPU usage detected")
        except:
            checks.append("? CPU: Unable to check")
        
        # Memory check
        try:
            import psutil
            mem = psutil.virtual_memory()
            status = "✓" if mem.percent < self.alert_thresholds["memory_percent"] else "⚠️"
            checks.append(f"{status} Memory: {mem.percent}%")
            if mem.percent >= self.alert_thresholds["memory_percent"]:
                alerts.append("High memory usage detected")
        except:
            checks.append("? Memory: Unable to check")
        
        # Disk check
        try:
            import psutil
            disk = psutil.disk_usage('/')
            status = "✓" if disk.percent < self.alert_thresholds["disk_percent"] else "⚠️"
            checks.append(f"{status} Disk: {disk.percent}%")
            if disk.percent >= self.alert_thresholds["disk_percent"]:
                alerts.append("Low disk space warning")
        except:
            checks.append("? Disk: Unable to check")
        
        overall_status = "✓ All systems healthy" if not alerts else f"⚠️ {len(alerts)} alert(s)"
        
        output = (
            f"🏥 System Health Check\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {overall_status}\n\n" +
            "\n".join(checks)
        )
        
        if alerts:
            output += "\n\nAlerts:\n" + "\n".join([f"  • {a}" for a in alerts])
        
        return {
            "success": True,
            "output": output,
            "checks": checks,
            "alerts": alerts,
            "healthy": len(alerts) == 0,
            "action": "health_check"
        }
