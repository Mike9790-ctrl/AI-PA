# 🤖 MIKE AI - Advanced Multimodal Agentic Assistant

**Your Personal AI That Does Everything** - Local, Private, Powerful

---

## 🚀 What MIKE Can Do

### 💬 **Communication Agent** - Send Messages Everywhere
- **Telegram** - Bot & User API support
- **KakaoTalk** - Korean messaging platform
- **WhatsApp** - Business API integration  
- **Email** - SMTP email sending
- **Discord** - Bot integration
- **Contact Management** - Save and manage contacts per platform

```python
# Setup Telegram
mike.setup_platform('telegram', bot_token='YOUR_TOKEN')

# Send message
mike.send_message('telegram', '@username', 'Hello from MIKE!')
```

### 📺 **YouTube Agent** - Run Your Channel Automatically
- **Video Upload** - Auto-upload with SEO optimization
- **Analytics** - Views, watch time, subscribers, revenue
- **Comment Management** - Auto-reply, delete, pin, heart
- **SEO Optimization** - AI-generated tags, titles, descriptions
- **Content Scheduling** - Plan your upload calendar
- **Monetization Tracking** - Revenue insights

```python
# Upload video
mike.upload_video('video.mp4', 'My Tutorial', tags=['AI', 'Python'])

# Get analytics
analytics = mike.get_analytics()

# Auto-reply to comments
mike.manage_comments('reply', comment_id='cmt_123', reply_text='Thanks!')
```

### 💼 **Business Agent** - Create Side Hustles & Earn Money
- **Idea Generation** - 50+ personalized side hustle ideas
- **Business Plans** - Complete plans with financial projections
- **Income Tracking** - Track revenue/expenses per project
- **Financial Reports** - Profit/loss statements
- **Growth Strategies** - Scaling advice

**Categories:**
- 🖥️ Tech (Web dev, AI services, Consulting)
- 🎨 Creative (Content, YouTube, Courses)
- 🛎️ Service (VA, Social media, Tutoring)
- 🌐 Online (Affiliate, Dropshipping, Print-on-demand)
- 📈 Investment (Stocks, Crypto, REITs)

```python
# Generate ideas based on your skills
mike.setup_profile(skills=['Python', 'Writing'], budget=1000, hours=15)
ideas = mike.generate_ideas(count=10)

# Create business plan
plan = mike.create_business_plan('AI Chatbot Services')

# Track income
mike.track_income('Consulting', 500, category='revenue')
```

### 📊 **Trading Agent** - Trade Gold, Forex, Crypto, Stocks
- **Market Data** - Real-time prices & candlestick charts
- **Technical Analysis** - RSI, MACD, Moving Averages, Bollinger Bands
- **Execute Trades** - Buy/Sell with stop-loss & take-profit
- **Portfolio Management** - Track positions & PnL
- **Automated Strategies** - Scalping, Day Trading, Swing, Grid
- **Market Analysis** - Buy/Sell signals with confidence scores

**Supported Assets:**
- 🥇 **Commodities**: Gold (XAUUSD), Silver, Oil
- 💱 **Forex**: EURUSD, GBPUSD, USDJPY, etc.
- ₿ **Crypto**: BTC, ETH, BNB, SOL
- 📈 **Stocks**: AAPL, TSLA, GOOGL, MSFT
- 📊 **Indices**: US30, NAS100, SPX500

```python
# Get gold analysis
analysis = mike.market_analysis('XAUUSD')

# Execute trade
mike.execute_trade('XAUUSD', 'buy', 0.1, stop_loss=2000, take_profit=2080)

# Deploy strategy
mike.trading_strategy('swing_trading', 'BTCUSD')

# Check portfolio
portfolio = mike.get_portfolio()
```

### 📁 **File Agent** - Manage Files & Folders
- Create, read, write, organize files
- Smart directory navigation
- Batch operations

### 💻 **Code Agent** - Programming Assistant
- Generate code in any language
- Debug & refactor
- Explain code
- Best practices

### 🔧 **System Agent** - Monitor Your Computer
- CPU, Memory, Disk usage
- Process management
- System health checks

### 🌐 **Web Agent** - Internet Research
- Search the web
- Fetch content
- Summarize articles

---

## 🎯 Quick Start

### Installation

```bash
# Navigate to MIKE AI folder
cd ~/jarvis_ai

# Install dependencies
pip install -r requirements.txt

# Run MIKE
python main.py
```

### Usage Examples

**Interactive Mode:**
```bash
python main.py
```

**Single Command:**
```bash
python main.py -t "Send a Telegram message to @john saying hello"
python main.py -t "Upload my video tutorial to YouTube"
python main.py -t "Generate 5 side hustle ideas for a Python developer"
python main.py -t "Analyze gold price and give me a trading signal"
python main.py -t "Create a business plan for AI consulting"
```

**Demo Mode:**
```bash
python main.py --demo
```

---

## 🧠 Independent Brain Architecture

MIKE uses an **Advanced Agent Orchestrator** with:

1. **Task Decomposition** - Breaks complex tasks into steps
2. **Multi-Agent Coordination** - Routes tasks to specialized agents
3. **Self-Reflection** - Reviews and corrects its own work
4. **Planning Engine** - Creates execution plans
5. **Confidence Scoring** - Rates output reliability
6. **Memory & Context** - Remembers conversation history

---

## 🔒 Privacy & Security

- ✅ **100% Local** - Runs on your machine
- ✅ **No Cloud Dependencies** - Your data stays private
- ✅ **Safe Mode** - Confirms dangerous operations
- ✅ **Configurable Permissions** - Control what MIKE can access

---

## 📋 Full Agent List

| Agent | Purpose | Status |
|-------|---------|--------|
| Communication | Messaging (Telegram, Kakao, WhatsApp, Email, Discord) | ✅ Active |
| YouTube | Channel management & automation | ✅ Active |
| Business | Side hustles & income tracking | ✅ Active |
| Trading | Gold, Forex, Crypto, Stocks | ✅ Active |
| File | File/folder operations | ✅ Active |
| Code | Programming assistance | ✅ Active |
| System | System monitoring | ✅ Active |
| Web | Internet research | ✅ Active |
| Image | Image generation/processing | ⚙️ Optional |
| Voice | Voice interaction | ⚙️ Optional |
| Scheduler | Task scheduling | ⚙️ Optional |
| Database | Data management | ⚙️ Optional |

---

## ⚙️ Configuration

Edit `config/settings.py` to customize:

```python
# Enable/disable agents
AGENT_CONFIG = {
    "enable_communication_agent": True,
    "enable_youtube_agent": True,
    "enable_business_agent": True,
    "enable_trading_agent": True,
    # ... more agents
}

# Use real LLM models (requires Ollama)
LLM_CONFIG = {
    "mock_mode": False,  # Set to False for real AI
    "model_name": "qwen-coder:latest",
}
```

---

## 🛠️ API Setup (For Real Operations)

### Telegram
1. Create bot via @BotFather
2. Get bot token
3. `mike.setup_platform('telegram', bot_token='YOUR_TOKEN')`

### YouTube
1. Go to Google Cloud Console
2. Enable YouTube Data API
3. Create API key
4. `mike.setup_channel(api_key='YOUR_KEY')`

### Trading
1. Choose broker (MetaTrader, Binance, etc.)
2. Get API credentials
3. `mike.setup_broker('binance', api_key='KEY', api_secret='SECRET')`

### Email
1. Get SMTP credentials from provider
2. `mike.setup_platform('email', smtp_server='smtp.gmail.com', email_address='you@gmail.com', password='APP_PASSWORD')`

---

## ⚠️ Important Disclaimers

- **Trading**: High risk of loss. For educational purposes only. Not financial advice.
- **Business**: Success not guaranteed. Requires effort and execution.
- **YouTube**: Results vary. Algorithm changes affect performance.
- **Messaging**: Respect platform ToS and anti-spam policies.

---

## 📞 Support & Community

- Documentation: See `/docs` folder
- Examples: Check `/examples` directory
- Issues: Report bugs on GitHub

---

## 🎉 Example Commands to Try

```
"Send a message to my team on Telegram about the meeting"
"Upload my latest tutorial to YouTube with optimized tags"
"Give me 10 side hustle ideas I can start with $500"
"Analyze Bitcoin and tell me if I should buy or sell"
"Create a full business plan for a dropshipping store"
"Track my $1200 income from freelancing this week"
"What's the current gold price and technical analysis?"
"Set up automated swing trading for Ethereum"
"Reply to all unanswered YouTube comments"
"Show me my trading portfolio performance"
```

---

**Built with ❤️ for Mike Johnson**
*Your AI Partner for Productivity, Business & Trading*
