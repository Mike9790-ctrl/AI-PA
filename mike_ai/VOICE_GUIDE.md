# 🎤 MIKE AI - Voice Activation Guide

## 🗣️ How to Use "Hey Mike" Wake Word

### Quick Start

**1. Launch Voice Mode:**
```bash
cd ~/jarvis_ai
python main.py --voice
```

**2. Wait for Calibration:**
- MIKE will calibrate for 2 seconds to ambient noise
- You'll see: "✓ Calibration complete. Say 'Hey Mike' to start!"

**3. Activate with Wake Word:**
Say clearly: **"Hey Mike"** or **"Hi Mike"** or just **"Mike"**

**4. Give Your Command:**
After activation, say your command:
- "Hey Mike... create a file called test.txt"
- "Hey Mike... what's the weather?"
- "Hey Mike... show system information"

**5. Exit Voice Mode:**
Say: **"exit"**, **"quit"**, or **"stop listening"**

---

## 📋 Alternative: Use Voice in Interactive Mode

1. Start normal mode: `python main.py`
2. Type: `voice` to switch to voice mode
3. Or type commands directly with keyboard

---

## 🔧 Installation Requirements for Voice

### Windows (Git Bash/PowerShell):
```bash
cd ~/jarvis_ai
pip install -r requirements.txt
```

**If you get PyAudio errors:**
```bash
# Download precompiled PyAudio from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install: pip install PyAudio‑X.X‑cp3XX‑...whl
```

### Linux/Mac:
```bash
sudo apt-get install python3-pyaudio  # Linux
brew install portaudio                # Mac
pip install -r requirements.txt
```

---

## 💡 Tips for Best Voice Recognition

1. **Speak Clearly**: Enunciate "Hey Mike" clearly
2. **Reduce Noise**: Minimize background noise
3. **Microphone Check**: Ensure mic is working and selected
4. **Internet Required**: Google speech recognition needs internet
5. **Pause After Wake Word**: Wait for "✓ Activated!" before continuing

---

## 🎯 Example Voice Commands

| Category | Say This |
|----------|----------|
| Files | "Hey Mike... create a folder called projects" |
| System | "Hey Mike... show me my CPU usage" |
| Code | "Hey Mike... write a Python function to add two numbers" |
| Web | "Hey Mike... search for AI tutorials" |
| Messages | "Hey Mike... send a Telegram message to John saying hello" |
| Trading | "Hey Mike... analyze gold price trends" |
| YouTube | "Hey Mike... check my channel stats" |

---

## 🐛 Troubleshooting

**"Speech recognition not available"**
→ Install: `pip install speechrecognition pyaudio`

**"Could not understand audio"**
→ Speak louder/clearer, check microphone connection

**"RequestError"**
→ Check internet connection (Google API requires online)

**No TTS (Text-to-Speech)**
→ Optional feature. Install: `pip install gtts playsound`

---

## ⌨️ Keyboard Shortcuts (Interactive Mode)

- `Ctrl+C`: Interrupt current operation
- `voice`: Switch to voice mode
- `help`: Show all commands
- `exit`: Quit application

---

## 🚀 Full Command List

```bash
# Interactive mode (keyboard)
python main.py

# Voice activation mode ("Hey Mike")
python main.py --voice

# Single task
python main.py -t "create a file called hello.txt"

# Demo mode
python main.py --demo

# Auto-confirm (skip prompts)
python main.py -a -t "delete temp files"
```

---

**🎉 You're ready to talk to MIKE!**

Just say: **"Hey Mike"** and start giving commands!
