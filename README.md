# 🛡️ Sentinel: Local-First Cognitive Firewall

> **"Your AI Bodyguard against the Dark Forest of the Internet."**

Sentinel is an open-source, privacy-first AI agent that runs entirely on your local machine. It acts as a middleware between you and digital threats, analyzing clipboard content, emails, and messages for social engineering attacks, urgency traps, and deepfake patterns.

**Status:** 🟢 Active Prototype

## ⚡ Why Sentinel?

- **100% Privacy:** No data leaves your device. Powered by [Ollama](https://ollama.com).
- **OS-Agnostic:** Works on Windows, Mac, and Linux via Clipboard monitoring.
- **Zero Latency:** Uses quantized local models (Mistral/Phi-3) for sub-second analysis.

## 🚀 Quick Start

### Prerequisites
1. Install [Ollama](https://ollama.com).
2. Pull a lightweight model: `ollama run mistral`

### Installation
```bash
git clone [https://github.com/YOUR_USERNAME/sentinel-ai.git](https://github.com/YOUR_USERNAME/sentinel-ai.git)
cd sentinel-ai
pip install -r requirements.txt
