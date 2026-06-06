"""
MIKE AI - Advanced Web Agent
Web search, content fetching, and data extraction
"""
import json
from typing import Dict, Any, List, Optional
from urllib.parse import quote_plus

from config.settings import WEB_CONFIG


class WebAgent:
    """
    Advanced web operations agent.
    Capabilities: search, fetch URLs, extract content, get news/weather
    """
    
    def __init__(self):
        self.search_engine = WEB_CONFIG["search_engine"]
        self.max_results = WEB_CONFIG["max_results"]
        self.timeout = WEB_CONFIG["timeout"]
        self.user_agent = WEB_CONFIG["user_agent"]
        
    def execute(self, command: str, context: str = "") -> Dict[str, Any]:
        """Execute web operation based on natural language command."""
        cmd_lower = command.lower()
        
        try:
            # Search the web
            if any(kw in cmd_lower for kw in ["search", "find", "look up", "google"]):
                return self._search_web(command)
            
            # Fetch URL content
            elif any(kw in cmd_lower for kw in ["fetch", "get url", "open link", "visit"]):
                return self._fetch_url(command)
            
            # Get weather
            elif "weather" in cmd_lower:
                return self._get_weather(command)
            
            # Get news
            elif "news" in cmd_lower:
                return self._get_news(command)
            
            # Wikipedia lookup
            elif "wikipedia" in cmd_lower or "wiki" in cmd_lower:
                return self._wikipedia_search(command)
            
            # Stock/crypto prices
            elif any(kw in cmd_lower for kw in ["stock", "price", "crypto", "bitcoin"]):
                return self._get_price(command)
            
            else:
                # Default to search
                return self._search_web(command)
                
        except Exception as e:
            return {"success": False, "error": str(e), "output": None}
    
    def _search_web(self, command: str) -> Dict[str, Any]:
        """Search the web using DuckDuckGo (no API key needed)."""
        import re
        
        # Extract search query
        patterns = [
            r'(?:search|find|look up|google)\s+(?:for\s+)?(.+)',
            r'(.+)'  # Fallback: use entire command
        ]
        
        query = command
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                break
        
        # Use DuckDuckGo HTML interface for scraping
        results = []
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            headers = {"User-Agent": self.user_agent}
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            result_elements = soup.find_all('div', class_='result__body', limit=self.max_results)
            
            for elem in result_elements:
                title_elem = elem.find('a', class_='result__a')
                snippet_elem = elem.find('a', class_='result__snippet')
                
                if title_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": title_elem.get('href'),
                        "snippet": snippet_elem.get_text(strip=True) if snippet_elem else ""
                    })
                    
        except ImportError:
            # Fallback without beautifulsoup
            results = [{
                "title": f"Search result for: {query}",
                "url": f"https://duckduckgo.com/?q={quote_plus(query)}",
                "snippet": "Install beautifulsoup4 for detailed results"
            }]
        except Exception as e:
            results = [{
                "title": "Search unavailable",
                "url": f"https://duckduckgo.com/?q={quote_plus(query)}",
                "snippet": f"Visit the link directly. Error: {str(e)}"
            }]
        
        output_lines = [f"🔍 Search results for: '{query}'\n"]
        for i, r in enumerate(results, 1):
            output_lines.append(f"{i}. {r['title']}")
            output_lines.append(f"   {r['url']}")
            if r['snippet']:
                output_lines.append(f"   {r['snippet'][:150]}...")
            output_lines.append("")
        
        return {
            "success": True,
            "output": "\n".join(output_lines),
            "query": query,
            "results": results,
            "count": len(results),
            "action": "web_search"
        }
    
    def _fetch_url(self, command: str) -> Dict[str, Any]:
        """Fetch content from a URL."""
        import re
        
        # Extract URL
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        matches = re.findall(url_pattern, command)
        
        if not matches:
            return {"success": False, "error": "No URL found in command", "output": None}
        
        url = matches[0]
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "No title"
            
            # Remove scripts and styles
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            text = soup.get_text(separator='\n', strip=True)[:3000]
            
            output = f"📄 Title: {title_text}\n\n{text}"
            
            return {
                "success": True,
                "output": output,
                "url": url,
                "title": title_text,
                "content_length": len(text),
                "action": "fetch_url"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch URL: {str(e)}",
                "output": None
            }
    
    def _get_weather(self, command: str) -> Dict[str, Any]:
        """Get weather information (mock or from wttr.in)."""
        import re
        
        # Extract location
        loc_match = re.search(r'(?:in|for)\s+([A-Za-z\s,]+)', command)
        location = loc_match.group(1).strip() if loc_match else "London"
        
        try:
            import requests
            
            # Use wttr.in (free, no API key)
            url = f"https://wttr.in/{quote_plus(location)}?format=j1"
            response = requests.get(url, timeout=self.timeout)
            data = response.json()
            
            current = data['current_condition'][0]
            
            weather_info = {
                "location": location,
                "temperature": f"{current.get('temp_C', 'N/A')}°C ({current.get('temp_F', 'N/A')}°F)",
                "condition": current.get('weatherDesc', [{}])[0].get('value', 'Unknown'),
                "humidity": f"{current.get('humidity', 'N/A')}%",
                "wind": f"{current.get('windspeedKmph', 'N/A')} km/h",
            }
            
            output = (
                f"🌤️ Weather in {weather_info['location']}:\n"
                f"Temperature: {weather_info['temperature']}\n"
                f"Condition: {weather_info['condition']}\n"
                f"Humidity: {weather_info['humidity']}\n"
                f"Wind: {weather_info['wind']}"
            )
            
            return {
                "success": True,
                "output": output,
                "weather": weather_info,
                "action": "get_weather"
            }
            
        except Exception as e:
            return {
                "success": True,
                "output": f"Weather data unavailable. Try again later.\nError: {str(e)}",
                "action": "weather_error"
            }
    
    def _get_news(self, command: str) -> Dict[str, Any]:
        """Get latest news headlines."""
        # Mock news headlines (can be extended with real APIs)
        headlines = [
            "Tech Giants Announce New AI Initiatives",
            "Global Markets Show Strong Growth",
            "Breakthrough in Renewable Energy Research",
            "Space Exploration Mission Reaches New Milestone",
            "Healthcare Innovation Improves Patient Outcomes"
        ]
        
        output = "📰 Latest Headlines:\n\n" + "\n".join([f"• {h}" for h in headlines])
        
        return {
            "success": True,
            "output": output,
            "headlines": headlines,
            "action": "get_news"
        }
    
    def _wikipedia_search(self, command: str) -> Dict[str, Any]:
        """Search Wikipedia."""
        import re
        
        # Extract search term
        patterns = [
            r'(?:wikipedia|wiki)\s+(?:for|about)?\s*(.+)',
            r'(.+)'
        ]
        
        query = command
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                query = match.group(1).strip().replace("wikipedia", "").replace("wiki", "").strip()
                break
        
        try:
            import requests
            
            # Wikipedia API
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                summary = {
                    "title": data.get('title', query),
                    "extract": data.get('extract', 'No summary available'),
                    "url": data.get('content_urls', {}).get('desktop', {}).get('page', '')
                }
                
                output = (
                    f"📚 {summary['title']}\n\n"
                    f"{summary['extract'][:500]}...\n\n"
                    f"Read more: {summary['url']}"
                )
                
                return {
                    "success": True,
                    "output": output,
                    "summary": summary,
                    "action": "wikipedia_search"
                }
            else:
                raise Exception("Page not found")
                
        except Exception as e:
            return {
                "success": True,
                "output": f"Wikipedia search failed. Try: https://en.wikipedia.org/wiki/{quote_plus(query)}",
                "action": "wikipedia_error"
            }
    
    def _get_price(self, command: str) -> Dict[str, Any]:
        """Get stock or crypto prices (mock data)."""
        import re
        
        # Extract symbol
        symbol_match = re.search(r'\b([A-Z]{2,6})\b', command.upper())
        symbol = symbol_match.group(1) if symbol_match else "BTC"
        
        # Mock prices (would use real API in production)
        mock_prices = {
            "BTC": {"price": 67842.50, "change": "+2.3%"},
            "ETH": {"price": 3456.78, "change": "+1.8%"},
            "AAPL": {"price": 189.45, "change": "-0.5%"},
            "GOOGL": {"price": 141.23, "change": "+0.9%"},
            "TSLA": {"price": 245.67, "change": "+3.2%"},
        }
        
        price_data = mock_prices.get(symbol, {"price": "N/A", "change": "N/A"})
        
        output = (
            f"💰 {symbol} Price:\n"
            f"Price: ${price_data['price']}\n"
            f"Change: {price_data['change']}"
        )
        
        return {
            "success": True,
            "output": output,
            "symbol": symbol,
            "price": price_data,
            "action": "get_price"
        }
