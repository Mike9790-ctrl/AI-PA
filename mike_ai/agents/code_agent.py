"""
MIKE AI - Advanced Code Agent
Code generation, analysis, debugging, and refactoring
"""
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from config.settings import AGENT_CONFIG
from core.llm_engine import get_llm_engine


class CodeAgent:
    """
    Advanced code operations agent.
    Capabilities: generate, analyze, debug, refactor, explain code
    """
    
    def __init__(self):
        self.llm = get_llm_engine()
        self.supported_languages = ["python", "javascript", "java", "cpp", "c", "go", "rust", "typescript"]
        
    def execute(self, command: str, context: str = "") -> Dict[str, Any]:
        """Execute code operation based on natural language command."""
        cmd_lower = command.lower()
        
        try:
            # Generate code
            if any(kw in cmd_lower for kw in ["generate", "create", "write", "make", "implement"]):
                return self._generate_code(command)
            
            # Explain code
            elif any(kw in cmd_lower for kw in ["explain", "describe", "what does", "understand"]):
                return self._explain_code(command, context)
            
            # Debug code
            elif any(kw in cmd_lower for kw in ["debug", "fix", "error", "bug", "issue"]):
                return self._debug_code(command, context)
            
            # Refactor code
            elif any(kw in cmd_lower for kw in ["refactor", "optimize", "improve", "clean up"]):
                return self._refactor_code(command, context)
            
            # Review code
            elif any(kw in cmd_lower for kw in ["review", "analyze", "check", "audit"]):
                return self._review_code(command, context)
            
            # Convert between languages
            elif any(kw in cmd_lower for kw in ["convert", "translate", "port"]):
                return self._convert_code(command, context)
            
            # Write tests
            elif any(kw in cmd_lower for kw in ["test", "unit test", "pytest", "spec"]):
                return self._write_tests(command, context)
            
            # Documentation
            elif any(kw in cmd_lower for kw in ["document", "docstring", "comment", "readme"]):
                return self._add_documentation(command, context)
            
            else:
                # Default to code generation
                return self._generate_code(command)
                
        except Exception as e:
            return {"success": False, "error": str(e), "output": None}
    
    def _generate_code(self, command: str) -> Dict[str, Any]:
        """Generate code based on description."""
        # Detect target language
        language = self._detect_language(command)
        
        system_prompt = f"""You are an expert {language} developer. Generate clean, well-documented, production-ready code.
Include:
- Clear function/class names
- Type hints (if applicable)
- Docstrings
- Error handling
- Example usage

Return ONLY the code, no explanations outside comments."""

        response = self.llm.process(command, system_prompt)
        
        # Extract code block from response
        code = self._extract_code(response.get("response", ""))
        
        return {
            "success": True,
            "output": f"```{language}\n{code}\n```",
            "code": code,
            "language": language,
            "action": "generate_code"
        }
    
    def _explain_code(self, command: str, context: str = "") -> Dict[str, Any]:
        """Explain what code does."""
        code = self._extract_code_from_context(context) or self._extract_code(command)
        
        if not code:
            return {"success": False, "error": "No code found to explain", "output": None}
        
        system_prompt = """Explain this code clearly:
1. What it does overall
2. Key components and their purposes
3. How data flows through it
4. Any potential issues or improvements

Use simple language suitable for a junior developer."""

        prompt = f"Explain this code:\n\n```{code}```"
        response = self.llm.process(prompt, system_prompt)
        
        return {
            "success": True,
            "output": response.get("response", ""),
            "code": code,
            "explanation": response.get("response", ""),
            "action": "explain_code"
        }
    
    def _debug_code(self, command: str, context: str = "") -> Dict[str, Any]:
        """Find and fix bugs in code."""
        code = self._extract_code_from_context(context) or self._extract_code(command)
        
        if not code:
            return {"success": False, "error": "No code found to debug", "output": None}
        
        system_prompt = """Debug this code:
1. Identify all bugs and issues
2. Explain what's wrong
3. Provide the corrected code
4. Explain the fixes

Be thorough and check for:
- Syntax errors
- Logic errors
- Edge cases
- Performance issues
- Security vulnerabilities"""

        prompt = f"Debug this code:\n\n```{code}```"
        response = self.llm.process(prompt, system_prompt)
        
        fixed_code = self._extract_code(response.get("response", ""))
        
        return {
            "success": True,
            "output": response.get("response", ""),
            "original_code": code,
            "fixed_code": fixed_code,
            "action": "debug_code"
        }
    
    def _refactor_code(self, command: str, context: str = "") -> Dict[str, Any]:
        """Refactor and improve code quality."""
        code = self._extract_code_from_context(context) or self._extract_code(command)
        
        if not code:
            return {"success": False, "error": "No code found to refactor", "output": None}
        
        system_prompt = """Refactor this code to improve:
- Readability
- Maintainability
- Performance
- Adherence to best practices
- DRY principles
- Single responsibility

Provide the refactored code with explanations of changes."""

        prompt = f"Refactor this code:\n\n```{code}```"
        response = self.llm.process(prompt, system_prompt)
        
        refactored = self._extract_code(response.get("response", ""))
        
        return {
            "success": True,
            "output": response.get("response", ""),
            "original_code": code,
            "refactored_code": refactored,
            "action": "refactor_code"
        }
    
    def _review_code(self, command: str, context: str = "") -> Dict[str, Any]:
        """Perform code review."""
        code = self._extract_code_from_context(context) or self._extract_code(command)
        
        if not code:
            return {"success": False, "error": "No code found to review", "output": None}
        
        system_prompt = """Perform a thorough code review. Evaluate:
✓ Code correctness
✓ Error handling
✓ Edge cases
✓ Performance
✓ Security
✓ Readability
✓ Best practices
✓ Testability

Provide specific suggestions for improvement."""

        prompt = f"Review this code:\n\n```{code}```"
        response = self.llm.process(prompt, system_prompt)
        
        return {
            "success": True,
            "output": response.get("response", ""),
            "code": code,
            "review": response.get("response", ""),
            "action": "review_code"
        }
    
    def _convert_code(self, command: str, context: str = "") -> Dict[str, Any]:
        """Convert code between languages."""
        code = self._extract_code_from_context(context) or self._extract_code(command)
        
        # Detect source and target languages
        lang_match = re.search(r'(?:from|in)\s+(\w+)\s+(?:to|into)\s+(\w+)', command, re.IGNORECASE)
        if lang_match:
            source_lang = lang_match.group(1)
            target_lang = lang_match.group(2)
        else:
            source_lang = self._detect_language(code)
            target_lang = "python"  # Default target
        
        if not code:
            return {"success": False, "error": "No code found to convert", "output": None}
        
        system_prompt = f"""Convert this {source_lang} code to {target_lang}.
Maintain the same functionality and logic.
Write idiomatic {target_lang} code following its conventions.
Include appropriate error handling and documentation."""

        prompt = f"Convert from {source_lang} to {target_lang}:\n\n```{code}```"
        response = self.llm.process(prompt, system_prompt)
        
        converted = self._extract_code(response.get("response", ""))
        
        return {
            "success": True,
            "output": f"```{target_lang}\n{converted}\n```",
            "source_language": source_lang,
            "target_language": target_lang,
            "original_code": code,
            "converted_code": converted,
            "action": "convert_code"
        }
    
    def _write_tests(self, command: str, context: str = "") -> Dict[str, Any]:
        """Write unit tests for code."""
        code = self._extract_code_from_context(context) or self._extract_code(command)
        
        if not code:
            return {"success": False, "error": "No code found to test", "output": None}
        
        language = self._detect_language(code)
        test_framework = self._get_test_framework(language)
        
        system_prompt = f"""Write comprehensive unit tests using {test_framework}.
Include:
- Happy path tests
- Edge case tests
- Error condition tests
- Mock external dependencies

Aim for >80% code coverage."""

        prompt = f"Write tests for this {language} code:\n\n```{code}```"
        response = self.llm.process(prompt, system_prompt)
        
        tests = self._extract_code(response.get("response", ""))
        
        return {
            "success": True,
            "output": f"```{language}\n{tests}\n```",
            "test_framework": test_framework,
            "tests": tests,
            "action": "write_tests"
        }
    
    def _add_documentation(self, command: str, context: str = "") -> Dict[str, Any]:
        """Add documentation to code."""
        code = self._extract_code_from_context(context) or self._extract_code(command)
        
        if not code:
            return {"success": False, "error": "No code found to document", "output": None}
        
        language = self._detect_language(code)
        
        system_prompt = f"""Add comprehensive documentation to this {language} code:
- Module-level docstrings
- Function/method docstrings with parameters and returns
- Inline comments for complex logic
- Type hints where applicable

Follow the language's documentation conventions."""

        prompt = f"Document this code:\n\n```{code}```"
        response = self.llm.process(prompt, system_prompt)
        
        documented = self._extract_code(response.get("response", ""))
        
        return {
            "success": True,
            "output": f"```{language}\n{documented}\n```",
            "language": language,
            "documented_code": documented,
            "action": "add_documentation"
        }
    
    def _detect_language(self, text: str) -> str:
        """Detect programming language from text."""
        text_lower = text.lower()
        
        for lang in self.supported_languages:
            if lang in text_lower:
                return lang
        
        # Heuristics
        if "def " in text and ":" in text:
            return "python"
        if "function " in text or "const " in text or "let " in text:
            return "javascript"
        if "public class" in text or "public static void main" in text:
            return "java"
        if "#include" in text or "int main(" in text:
            return "cpp"
        
        return "python"  # Default
    
    def _get_test_framework(self, language: str) -> str:
        """Get appropriate test framework for language."""
        frameworks = {
            "python": "pytest",
            "javascript": "Jest",
            "typescript": "Jest",
            "java": "JUnit 5",
            "cpp": "Google Test",
            "go": "testing package",
            "rust": "built-in test framework",
        }
        return frameworks.get(language, "appropriate testing framework")
    
    def _extract_code(self, text: str) -> str:
        """Extract code from markdown code blocks."""
        # Try to extract from code blocks
        pattern = r'```(?:\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, return text as-is (might be pure code)
        return text.strip()
    
    def _extract_code_from_context(self, context: str) -> Optional[str]:
        """Try to extract code from context string."""
        if not context:
            return None
        
        # Check if context looks like code
        if any(marker in context for marker in ["def ", "function", "class ", "import ", "from ", "public ", "private "]):
            return context
        
        return self._extract_code(context)
