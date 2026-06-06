"""
MIKE AI - Advanced Multimodal Agentic Personal Assistant
Main Entry Point with Rich CLI Interface and Voice Activation
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.table import Table
    from rich.live import Live
    from rich.spinner import Spinner
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Installing rich for beautiful CLI...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.table import Table
    from rich.live import Live
    from rich.spinner import Spinner
    from rich.text import Text

# Voice activation imports
import time
import threading
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

from core.llm_engine import get_llm_engine
from core.agent_orchestrator import get_orchestrator


def print_banner(console: Console):
    """Print MIKE ASCII art banner."""
    banner = """
╒═══════════════════════════════════════════════════════════════════╕
│     ███╗   ███████╗ ██████╗ ███╗   ███╗██╗████████╗               │
│     ████╗ ██╔══╝██╔═══██╗████╗ ████║██║╚══██╔══╝               │
│     ██╔██╔█████╗  ██████╔╝██╔████╔██║██║   ██║                  │
│     ██║╚██╔██╔══╝  ██╔═══██╗██║╚██╔╝██║██║   ██║                  │
│     ╚█████╔███████╗██║   ██║██║ ╚═╝ ██║██║   ██║                  │
│      ╚═══╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝                  │
│                                                                   │
│          Advanced Multimodal Agentic AI Assistant          │
╘═══════════════════════════════════════════════════════════════════╛
    """
    console.print(Panel(banner, style="bold cyan"))


def print_capabilities(console: Console, orchestrator):
    """Display system capabilities."""
    status = orchestrator.get_status()
    
    table = Table(title="🚀 MIKE Capabilities", show_header=True, header_style="bold magenta")
    table.add_column("Feature", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="white")
    
    # Agents
    agents = status["available_agents"]
    table.add_row("🤖 Active Agents", "✔ Online", ", ".join(agents))
    
    # LLM Engine
    llm = get_llm_engine()
    caps = llm.get_capabilities()
    mode = "Mock (Demo)" if caps["mock_mode"] else "Real Models"
    table.add_row("🧠 LLM Engine", mode, f"{len(caps['available_models'])} model types")
    
    # Features
    table.add_row("📋 Task Planning", "✔ Enabled", f"Max {status['config']['max_steps']} steps")
    table.add_row("🔄 Self-Correction", "✔ Enabled" if status['config']['self_correction_enabled'] else "✗ Disabled", "")
    table.add_row("💭 Reflection", "✔ Enabled" if status['config']['reflection_enabled'] else "✗ Disabled", "")
    
    console.print(table)
    console.print()


def voice_activation_mode(console: Console, orchestrator):
    """Run voice activation mode with 'Hey Mike' wake word."""
    if not SPEECH_AVAILABLE:
        console.print("[red]Speech recognition not available. Install with: pip install speechrecognition pyaudio[/]")
        return
    
    print_banner(console)
    console.print(Panel("[bold green]🎤 Voice Activation Mode[/]\n"
                       "Say 'Hey Mike' to activate, then give your command.\n"
                       "Say 'exit' or 'quit' to stop.", 
                       title="🗣️ MIKE Listening", border_style="cyan"))
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Adjust for ambient noise
    console.print("[yellow]Calibrating for ambient noise... (please wait 2 seconds)[/]")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    console.print("[green]✓ Calibration complete. Say 'Hey Mike' to start![/]")
    
    while True:
        try:
            # Listen for wake word
            console.print("\n[bold cyan]👂 Listening for 'Hey Mike'...[/]")
            
            with microphone as source:
                audio = recognizer.listen(source, phrase_time_limit=5)
            
            try:
                # Recognize speech
                text = recognizer.recognize_google(audio).lower()
                console.print(f"[dim]Heard: {text}[/]")
                
                # Check for wake word
                if "hey mike" in text or "hi mike" in text or "mike" in text:
                    console.print("[bold green]✓ Activated![/]")
                    
                    # Extract command after wake word
                    command = text.replace("hey mike", "").replace("hi mike", "").replace("mike", "").strip()
                    
                    if not command:
                        # Listen for full command
                        console.print("[bold cyan]👂 What can I do for you?[/]")
                        with microphone as source:
                            audio = recognizer.listen(source, phrase_time_limit=10)
                        command = recognizer.recognize_google(audio)
                    
                    if command.lower() in ['exit', 'quit', 'stop listening']:
                        console.print(Panel("Goodbye! Have a great day!", style="green"))
                        break
                    
                    # Process command
                    with console.status("[bold blue]🧠 Thinking...", spinner="dots"):
                        result = orchestrator.execute_plan(command)
                    
                    # Display and speak result
                    if result.get("final_response"):
                        response_text = result["final_response"]
                        console.print(Panel(
                            Markdown(response_text),
                            title="🤖 MIKE",
                            border_style="green"
                        ))
                        
                        # Optional: Text-to-speech response
                        try:
                            from gtts import gTTS
                            from playsound import playsound
                            tts = gTTS(text=response_text, lang='en')
                            tts.save("temp_response.mp3")
                            playsound("temp_response.mp3")
                            import os
                            os.remove("temp_response.mp3")
                        except Exception as e:
                            pass  # TTS is optional
                
                elif command.lower() in ['exit', 'quit']:
                    console.print(Panel("Goodbye! Have a great day!", style="green"))
                    break
                    
            except sr.UnknownValueError:
                console.print("[dim]Could not understand audio[/]")
            except sr.RequestError as e:
                console.print(f"[red]Speech service error: {e}[/]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/]")


def interactive_mode(console: Console, orchestrator):
    """Run interactive chat mode."""
    print_banner(console)
    print_capabilities(console, orchestrator)
    
    console.print(Panel("[bold green]Welcome! I'm MIKE, your AI assistant.[/]\n"
                       "Type 'help' for commands, 'exit' to quit.\n"
                       "Try: 'Create a Python script that calculates Fibonacci'\n"
                       "[yellow]💡 Tip: Use --voice flag for 'Hey Mike' voice activation![/]", 
                       title="💬 Interactive Mode", border_style="blue"))
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if not user_input.strip():
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print(Panel("Goodbye! Have a great day!", style="green"))
                break
            
            if user_input.lower() == 'help':
                help_text = """
**Available Commands:**
- `exit` - Quit the application
- `clear` - Clear conversation history  
- `status` - Show system status
- `capabilities` - Show available features
- `demo` - Run demo tasks
- `voice` - Switch to voice mode

**Example Tasks:**
- "Create a file called test.py with a hello world program"
- "Show me my system information"
- "Search for Python best practices"
- "Write a function to sort a list"
- "What's the weather in London?"
- "List all files in current directory"
- "Send a message on Telegram to John saying hello"
- "Check my YouTube channel stats"
- "Analyze gold price trends"
                """
                console.print(Markdown(help_text))
                continue
            
            if user_input.lower() == 'voice':
                console.print("[yellow]Switching to voice mode...[/]")
                voice_activation_mode(console, orchestrator)
                continue
            
            if user_input.lower() == 'clear':
                orchestrator.reset()
                get_llm_engine().clear_history()
                console.print("[green]Conversation cleared![/]")
                continue
            
            if user_input.lower() == 'status':
                status = orchestrator.get_status()
                console.print(status)
                continue
            
            if user_input.lower() == 'demo':
                run_demo(console, orchestrator)
                continue
            
            # Process with spinner
            with console.status("[bold blue]Thinking...", spinner="dots"):
                result = orchestrator.execute_plan(user_input)
            
            # Display result
            if result.get("final_response"):
                console.print(Panel(
                    Markdown(result["final_response"]),
                    title="🤖 MIKE",
                    border_style="green"
                ))
            
            # Show execution details if multi-step
            if len(result.get("plan", [])) > 1:
                console.print("\n[bold]Execution Plan:[/]")
                for task in result["plan"]:
                    status_emoji = "✔" if task.get("id") in [r["task_id"] for r in result["results"] if r["status"] == "completed"] else "✘"
                    console.print(f"  {status_emoji} {task['description']}")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/]")


def run_demo(console: Console, orchestrator):
    """Run demonstration tasks."""
    demo_tasks = [
        "Show system information",
        "List files in current directory",
        "Create a file called demo.txt with Hello from MIKE",
    ]
    
    console.print(Panel("[bold]Running Demo Tasks[/]", border_style="yellow"))
    
    for i, task in enumerate(demo_tasks, 1):
        console.print(f"\n[cyan]Task {i}/{len(demo_tasks)}: {task}[/]")
        
        with console.status("[bold blue]Executing...", spinner="dots"):
            result = orchestrator.execute_plan(task)
        
        if result.get("final_response"):
            console.print(f"[green]{result['final_response']}[/]")


def single_task_mode(console: Console, orchestrator, task: str, auto_confirm: bool = False):
    """Execute a single task and exit."""
    with console.status("[bold blue]Processing...", spinner="dots"):
        result = orchestrator.execute_plan(task)
    
    if result.get("final_response"):
        console.print(Panel(
            Markdown(result["final_response"]),
            title="🤖 Result",
            border_style="green"
        ))
    
    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MIKE AI - Advanced Multimodal Agentic Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                     # Interactive mode
  python main.py -t "Show system info"  # Single task
  python main.py --demo              # Run demo tasks
  python main.py -a -t "Create file"    # Auto-confirm mode
  python main.py --voice             # Voice activation mode ('Hey Mike')
        """
    )
    
    parser.add_argument("-t", "--task", type=str, help="Single task to execute")
    parser.add_argument("-a", "--auto-confirm", action="store_true", help="Skip confirmation prompts")
    parser.add_argument("--demo", action="store_true", help="Run demo tasks")
    parser.add_argument("--voice", action="store_true", help="Enable voice mode with 'Hey Mike' wake word")
    
    args = parser.parse_args()
    
    # Initialize console
    console = Console()
    
    # Initialize orchestrator
    orchestrator = get_orchestrator()
    
    try:
        if args.task:
            # Single task mode
            single_task_mode(console, orchestrator, args.task, args.auto_confirm)
        elif args.demo:
            # Demo mode
            print_banner(console)
            run_demo(console, orchestrator)
        elif args.voice:
            # Voice activation mode
            voice_activation_mode(console, orchestrator)
        else:
            # Interactive mode
            interactive_mode(console, orchestrator)
            
    except Exception as e:
        console.print(f"[red]Fatal error: {str(e)}[/]")
        sys.exit(1)


if __name__ == "__main__":
    main()
