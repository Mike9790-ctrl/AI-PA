"""
MIKE AI - Trading & Investment Agent
Handles trading operations for Gold, Forex, Crypto, Stocks with technical analysis and automated strategies
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import random
import math

class TradingAgent:
    """Agent for trading and investment operations across multiple asset classes"""
    
    def __init__(self, config_path: str = None):
        self.name = "Trading Agent"
        self.config_path = config_path or "config/trading_config.json"
        self.portfolio = {}
        self.active_trades = []
        self.trade_history = []
        self.watchlist = []
        self.load_config()
    
    def load_config(self):
        """Load trading configuration"""
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.broker_api = config.get('broker_api', {})
                self.risk_profile = config.get('risk_profile', 'moderate')
                self.default_capital = config.get('default_capital', 10000)
        else:
            self.broker_api = {}
            self.risk_profile = 'moderate'
            self.default_capital = 10000
    
    def save_config(self):
        """Save trading configuration"""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config = {
            'broker_api': self.broker_api,
            'risk_profile': self.risk_profile,
            'default_capital': self.default_capital,
            'last_updated': datetime.now().isoformat()
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def setup_broker(self, broker: str, api_key: str, api_secret: str = None, 
                     account_id: str = None) -> Dict:
        """Setup broker connection for trading"""
        supported_brokers = ['metatrader', 'binance', 'coinbase', 'interactive_brokers', 
                            'td_ameritrade', 'oanda', 'xm', 'ic_markets']
        
        if broker.lower() not in [b.lower() for b in supported_brokers]:
            return {
                'success': False,
                'error': f'Unsupported broker. Supported: {", ".join(supported_brokers)}'
            }
        
        self.broker_api[broker.lower()] = {
            'api_key': api_key,
            'api_secret': api_secret,
            'account_id': account_id,
            'connected_at': datetime.now().isoformat(),
            'status': 'configured'
        }
        
        self.save_config()
        
        return {
            'success': True,
            'message': f'{broker} broker configured successfully',
            'broker': broker,
            'note': 'Mock mode: Enable with real API credentials for actual trading'
        }
    
    def get_market_data(self, symbol: str, timeframe: str = '1h', 
                        periods: int = 100) -> Dict:
        """
        Get market data for a symbol
        Supports: XAUUSD (Gold), EURUSD, GBPUSD, BTCUSD, ETHUSD, stocks
        """
        print(f"[TRADING] Fetching {timeframe} data for {symbol}...")
        
        # Generate realistic mock price data
        base_prices = {
            'XAUUSD': 2030,  # Gold
            'EURUSD': 1.0850,
            'GBPUSD': 1.2650,
            'BTCUSD': 43000,
            'ETHUSD': 2300,
            'AAPL': 185,
            'TSLA': 245,
            'GOOGL': 140,
            'MSFT': 375,
            'SPY': 475
        }
        
        base_price = base_prices.get(symbol.upper(), 100)
        
        # Generate candlestick data
        candles = []
        current_price = base_price * (1 + random.uniform(-0.02, 0.02))
        
        for i in range(periods):
            volatility = base_price * 0.002  # 0.2% volatility
            
            open_price = current_price
            close_price = open_price * (1 + random.uniform(-0.005, 0.005))
            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.003))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.003))
            
            candles.append({
                'timestamp': (datetime.now() - timedelta(hours=periods-i)).isoformat(),
                'open': round(open_price, 4),
                'high': round(high_price, 4),
                'low': round(low_price, 4),
                'close': round(close_price, 4),
                'volume': random.randint(1000, 100000)
            })
            
            current_price = close_price
        
        # Calculate technical indicators
        indicators = self._calculate_indicators(candles)
        
        return {
            'success': True,
            'symbol': symbol.upper(),
            'timeframe': timeframe,
            'current_price': round(current_price, 4),
            'candles': candles[-20:],  # Last 20 candles
            'indicators': indicators,
            'market_status': 'open',
            'last_updated': datetime.now().isoformat()
        }
    
    def _calculate_indicators(self, candles: List[Dict]) -> Dict:
        """Calculate technical indicators from candle data"""
        if len(candles) < 20:
            return {}
        
        closes = [c['close'] for c in candles]
        highs = [c['high'] for c in candles]
        lows = [c['low'] for c in candles]
        
        # Simple Moving Averages
        sma_20 = sum(closes[-20:]) / 20
        sma_50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else sma_20
        
        # RSI (14-period)
        gains = []
        losses = []
        for i in range(1, min(15, len(closes))):
            change = closes[-i] - closes[-i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / len(gains) if gains else 0
        avg_loss = sum(losses) / len(losses) if losses else 1
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = sum(closes[-12:]) / 12 if len(closes) >= 12 else closes[-1]
        ema_26 = sum(closes[-26:]) / 26 if len(closes) >= 26 else closes[-1]
        macd_line = ema_12 - ema_26
        signal_line = macd_line * 0.9  # Simplified
        macd_histogram = macd_line - signal_line
        
        # Bollinger Bands
        std_dev = math.sqrt(sum((x - sma_20)**2 for x in closes[-20:]) / 20)
        upper_band = sma_20 + (2 * std_dev)
        lower_band = sma_20 - (2 * std_dev)
        
        # Support/Resistance
        support = min(lows[-20:])
        resistance = max(highs[-20:])
        
        return {
            'sma_20': round(sma_20, 4),
            'sma_50': round(sma_50, 4),
            'rsi_14': round(rsi, 2),
            'macd': {
                'line': round(macd_line, 4),
                'signal': round(signal_line, 4),
                'histogram': round(macd_histogram, 4)
            },
            'bollinger_bands': {
                'upper': round(upper_band, 4),
                'middle': round(sma_20, 4),
                'lower': round(lower_band, 4)
            },
            'support_resistance': {
                'support': round(support, 4),
                'resistance': round(resistance, 4)
            },
            'trend': 'bullish' if closes[-1] > sma_20 else 'bearish',
            'signal': self._generate_signal(rsi, macd_line, closes[-1], sma_20)
        }
    
    def _generate_signal(self, rsi: float, macd: float, price: float, sma: float) -> str:
        """Generate trading signal based on indicators"""
        signals = []
        
        # RSI signals
        if rsi < 30:
            signals.append('oversold')
        elif rsi > 70:
            signals.append('overbought')
        
        # MACD signals
        if macd > 0:
            signals.append('macd_bullish')
        else:
            signals.append('macd_bearish')
        
        # Price vs SMA
        if price > sma:
            signals.append('above_sma')
        else:
            signals.append('below_sma')
        
        # Combined signal
        bullish_count = sum(1 for s in signals if 'bullish' in s or 'oversold' in s or 'above_sma' in s)
        bearish_count = sum(1 for s in signals if 'bearish' in s or 'overbought' in s or 'below_sma' in s)
        
        if bullish_count > bearish_count + 1:
            return 'BUY'
        elif bearish_count > bullish_count + 1:
            return 'SELL'
        else:
            return 'HOLD'
    
    def execute_trade(self, symbol: str, action: str, quantity: float,
                      order_type: str = 'market', stop_loss: float = None,
                      take_profit: float = None, leverage: int = 1) -> Dict:
        """
        Execute a trade (Buy/Sell)
        action: 'buy' or 'sell'
        order_type: 'market', 'limit', 'stop'
        """
        print(f"[TRADING] Executing {action.upper()} order for {symbol}")
        print(f"  Quantity: {quantity}")
        print(f"  Type: {order_type}")
        print(f"  Leverage: {leverage}x")
        
        # Get current price
        market_data = self.get_market_data(symbol)
        current_price = market_data['current_price']
        
        # Calculate position value
        position_value = quantity * current_price * leverage
        
        # Risk check
        if position_value > self.default_capital * 0.2:  # Max 20% per trade
            return {
                'success': False,
                'error': 'Position size exceeds risk limit (max 20% of capital)',
                'position_value': position_value,
                'max_allowed': self.default_capital * 0.2
            }
        
        # Create trade
        trade = {
            'id': f'trade_{random.randint(100000, 999999)}',
            'symbol': symbol.upper(),
            'action': action.lower(),
            'quantity': quantity,
            'entry_price': current_price,
            'order_type': order_type,
            'leverage': leverage,
            'position_value': position_value,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'opened_at': datetime.now().isoformat(),
            'status': 'open',
            'pnl': 0,
            'pnl_percent': 0
        }
        
        # Add stop loss and take profit if not set
        if not stop_loss and not take_profit:
            if action.lower() == 'buy':
                trade['stop_loss'] = current_price * 0.98  # 2% SL
                trade['take_profit'] = current_price * 1.04  # 4% TP
            else:
                trade['stop_loss'] = current_price * 1.02
                trade['take_profit'] = current_price * 0.96
        
        self.active_trades.append(trade)
        self.trade_history.append({**trade, 'status': 'executed'})
        
        return {
            'success': True,
            'message': f'{action.upper()} order executed for {symbol}',
            'trade': trade,
            'trade_id': trade['id'],
            'execution_price': current_price,
            'note': 'Mock mode: Enable with real broker API for actual trading'
        }
    
    def close_trade(self, trade_id: str) -> Dict:
        """Close an active trade"""
        trade = next((t for t in self.active_trades if t['id'] == trade_id), None)
        
        if not trade:
            return {'success': False, 'error': 'Trade not found'}
        
        # Get current price
        market_data = self.get_market_data(trade['symbol'])
        current_price = market_data['current_price']
        
        # Calculate PnL
        if trade['action'] == 'buy':
            pnl = (current_price - trade['entry_price']) * trade['quantity'] * trade['leverage']
        else:
            pnl = (trade['entry_price'] - current_price) * trade['quantity'] * trade['leverage']
        
        pnl_percent = (pnl / trade['position_value']) * 100
        
        # Update trade
        trade['status'] = 'closed'
        trade['close_price'] = current_price
        trade['close_time'] = datetime.now().isoformat()
        trade['pnl'] = pnl
        trade['pnl_percent'] = pnl_percent
        
        # Remove from active trades
        self.active_trades = [t for t in self.active_trades if t['id'] != trade_id]
        
        return {
            'success': True,
            'message': f'Trade closed with {"profit" if pnl > 0 else "loss"} of ${pnl:.2f}',
            'trade_id': trade_id,
            'pnl': pnl,
            'pnl_percent': f'{pnl_percent:.2f}%',
            'close_price': current_price
        }
    
    def get_portfolio(self) -> Dict:
        """Get current portfolio status"""
        total_equity = self.default_capital
        unrealized_pnl = 0
        
        positions = []
        for trade in self.active_trades:
            market_data = self.get_market_data(trade['symbol'])
            current_price = market_data['current_price']
            
            if trade['action'] == 'buy':
                pnl = (current_price - trade['entry_price']) * trade['quantity'] * trade['leverage']
            else:
                pnl = (trade['entry_price'] - current_price) * trade['quantity'] * trade['leverage']
            
            unrealized_pnl += pnl
            
            positions.append({
                'symbol': trade['symbol'],
                'action': trade['action'],
                'quantity': trade['quantity'],
                'entry_price': trade['entry_price'],
                'current_price': current_price,
                'pnl': pnl,
                'pnl_percent': (pnl / trade['position_value']) * 100,
                'leverage': trade['leverage']
            })
        
        return {
            'success': True,
            'account_balance': self.default_capital,
            'unrealized_pnl': unrealized_pnl,
            'total_equity': self.default_capital + unrealized_pnl,
            'active_positions': len(positions),
            'positions': positions,
            'equity_curve': self._generate_equity_curve(),
            'risk_metrics': {
                'total_exposure': sum(p['quantity'] * p['current_price'] for p in positions),
                'largest_position': max([p['quantity'] * p['current_price'] for p in positions], default=0),
                'drawdown': f'{random.uniform(0, 15):.1f}%'
            }
        }
    
    def _generate_equity_curve(self) -> List[Dict]:
        """Generate mock equity curve data"""
        equity = self.default_capital
        curve = []
        
        for i in range(30):
            equity *= (1 + random.uniform(-0.03, 0.04))
            curve.append({
                'date': (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d'),
                'equity': round(equity, 2)
            })
        
        return curve
    
    def trading_strategy(self, strategy: str, symbol: str, 
                         parameters: Dict = None) -> Dict:
        """
        Deploy automated trading strategies
        Strategies: scalping, day_trading, swing_trading, grid, martingale
        """
        print(f"[TRADING] Deploying {strategy} strategy on {symbol}...")
        
        strategies = {
            'scalping': {
                'description': 'Quick trades targeting small profits',
                'timeframe': '1m-5m',
                'typical_hold': 'Minutes',
                'risk_per_trade': '0.5-1%',
                'parameters': {
                    'take_profit': '5-10 pips',
                    'stop_loss': '3-5 pips',
                    'max_trades_per_day': 20
                }
            },
            'day_trading': {
                'description': 'Open and close positions within same day',
                'timeframe': '15m-1h',
                'typical_hold': 'Hours',
                'risk_per_trade': '1-2%',
                'parameters': {
                    'take_profit': '20-50 pips',
                    'stop_loss': '10-20 pips',
                    'max_trades_per_day': 5
                }
            },
            'swing_trading': {
                'description': 'Capture medium-term price swings',
                'timeframe': '4h-Daily',
                'typical_hold': 'Days to weeks',
                'risk_per_trade': '2-3%',
                'parameters': {
                    'take_profit': '100-300 pips',
                    'stop_loss': '50-100 pips',
                    'max_open_positions': 3
                }
            },
            'grid': {
                'description': 'Place buy/sell orders at fixed intervals',
                'timeframe': 'Any',
                'typical_hold': 'Variable',
                'risk_per_trade': 'Varies',
                'parameters': {
                    'grid_spacing': '10-20 pips',
                    'grid_levels': 10,
                    'lot_multiplier': 1.0
                }
            },
            'breakout': {
                'description': 'Trade when price breaks key levels',
                'timeframe': '1h-4h',
                'typical_hold': 'Hours to days',
                'risk_per_trade': '1-2%',
                'parameters': {
                    'entry': 'On breakout confirmation',
                    'stop_loss': 'Below/above breakout level',
                    'take_profit': 'Measured move'
                }
            }
        }
        
        if strategy.lower() not in strategies:
            return {
                'success': False,
                'error': f'Unknown strategy. Available: {", ".join(strategies.keys())}'
            }
        
        selected_strategy = strategies[strategy.lower()]
        
        # Add symbol-specific recommendations
        if 'XAU' in symbol.upper():  # Gold
            selected_strategy['asset_notes'] = 'Gold has higher volatility, adjust position sizes accordingly'
            selected_strategy['best_sessions'] = 'London & New York overlap'
        elif 'BTC' in symbol.upper() or 'ETH' in symbol.upper():
            selected_strategy['asset_notes'] = 'Crypto trades 24/7, watch for weekend volatility'
            selected_strategy['best_sessions'] = 'Any time, higher volume during US hours'
        
        return {
            'success': True,
            'strategy': strategy,
            'symbol': symbol,
            'configuration': selected_strategy,
            'deployment_status': 'ready',
            'next_steps': [
                'Review strategy parameters',
                'Set risk limits',
                'Start with demo/paper trading',
                'Monitor first few trades manually'
            ],
            'warning': 'Always test strategies in demo mode before live trading'
        }
    
    def market_analysis(self, symbol: str) -> Dict:
        """Comprehensive market analysis for a symbol"""
        print(f"[TRADING] Analyzing {symbol}...")
        
        market_data = self.get_market_data(symbol)
        indicators = market_data['indicators']
        
        # Fundamental factors (mock)
        fundamentals = {
            'XAUUSD': {
                'drivers': ['USD strength', 'Interest rates', 'Geopolitical tension', 'Inflation data'],
                'sentiment': random.choice(['Bullish', 'Bearish', 'Neutral']),
                'key_events': ['FOMC meeting', 'NFP report', 'CPI data']
            },
            'EURUSD': {
                'drivers': ['ECB policy', 'Fed policy', 'Economic data', 'Risk sentiment'],
                'sentiment': random.choice(['Bullish', 'Bearish', 'Neutral']),
                'key_events': ['ECB decision', 'US jobs data', 'Eurozone PMI']
            },
            'BTCUSD': {
                'drivers': ['Institutional adoption', 'Regulatory news', 'Market sentiment', 'Halving cycle'],
                'sentiment': random.choice(['Bullish', 'Bearish', 'Neutral']),
                'key_events': ['ETF decisions', 'Major exchange news', 'Macro trends']
            }
        }
        
        asset_fundamentals = fundamentals.get(symbol.upper(), {
            'drivers': ['Market sentiment', 'Technical levels', 'Volume'],
            'sentiment': 'Neutral',
            'key_events': ['Economic calendar events']
        })
        
        return {
            'success': True,
            'symbol': symbol.upper(),
            'technical_analysis': {
                'current_price': market_data['current_price'],
                'trend': indicators.get('trend', 'neutral'),
                'signal': indicators.get('signal', 'HOLD'),
                'rsi': indicators.get('rsi_14', {}).get('rsi_14', 50),
                'support_resistance': indicators.get('support_resistance', {}),
                'key_levels': [
                    indicators.get('bollinger_bands', {}).get('upper', 0),
                    indicators.get('sma_20', 0),
                    indicators.get('bollinger_bands', {}).get('lower', 0)
                ]
            },
            'fundamental_analysis': asset_fundamentals,
            'recommendation': self._generate_recommendation(indicators, asset_fundamentals),
            'confidence': f'{random.randint(60, 90)}%',
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_recommendation(self, technical: Dict, fundamental: Dict) -> str:
        """Generate overall trading recommendation"""
        tech_signal = technical.get('signal', 'HOLD')
        fund_sentiment = fundamental.get('sentiment', 'Neutral')
        
        if tech_signal == 'BUY' and fund_sentiment == 'Bullish':
            return 'STRONG BUY - Technical and fundamental alignment'
        elif tech_signal == 'BUY':
            return 'BUY - Technical signal, monitor fundamentals'
        elif tech_signal == 'SELL' and fund_sentiment == 'Bearish':
            return 'STRONG SELL - Technical and fundamental alignment'
        elif tech_signal == 'SELL':
            return 'SELL - Technical signal, monitor fundamentals'
        else:
            return 'HOLD/NEUTRAL - Wait for clearer signals'
    
    def execute_capability(self) -> Dict:
        """Return agent capabilities"""
        return {
            'agent_name': self.name,
            'capabilities': [
                'market_data_feed',
                'technical_analysis',
                'execute_trades',
                'portfolio_management',
                'automated_strategies',
                'risk_management',
                'market_analysis'
            ],
            'supported_assets': {
                'forex': ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'],
                'commodities': ['XAUUSD (Gold)', 'XAGUSD (Silver)', 'WTI (Oil)', 'BRENT'],
                'crypto': ['BTCUSD', 'ETHUSD', 'BNBUSD', 'SOLUSD'],
                'stocks': ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN', 'SPY'],
                'indices': ['US30', 'NAS100', 'SPX500', 'GER30']
            },
            'features': {
                'technical_indicators': 'RSI, MACD, Moving Averages, Bollinger Bands, Support/Resistance',
                'order_types': 'Market, Limit, Stop, Stop-Loss, Take-Profit',
                'strategies': 'Scalping, Day Trading, Swing Trading, Grid, Breakout',
                'risk_management': 'Position sizing, Max drawdown limits, Exposure monitoring',
                'analysis': 'Real-time market analysis with buy/sell signals'
            },
            'disclaimer': 'Trading involves significant risk. This is for educational purposes. Always do your own research.'
        }


if __name__ == "__main__":
    # Test the Trading agent
    agent = TradingAgent()
    print("=== MIKE AI Trading Agent ===\n")
    print(json.dumps(agent.execute_capability(), indent=2))
    
    # Example: Get market data for Gold
    # gold_data = agent.get_market_data('XAUUSD')
    # print(json.dumps(gold_data, indent=2))
    
    # Example: Execute a trade
    # trade = agent.execute_trade('XAUUSD', 'buy', 0.1, stop_loss=2000, take_profit=2080)
    # print(json.dumps(trade, indent=2))
