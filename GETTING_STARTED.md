# 🚀 Getting Started — 5 Minutes to Running

## Step 1: Install (1 minute)

```bash
cd cfui
pip install -r requirements.txt
```

## Step 2: Configure (2 minutes)

```bash
cp .env.example .env
```

Then edit `.env` and add at least ONE of these:
- `GROQ_API_KEY=` (free, fast) — Get from https://console.groq.com
- `ANTHROPIC_API_KEY=` (Claude) — Get from https://console.anthropic.com
- Or just use Ollama (free, local, no API key)

## Step 3: Run (1 minute)

**Option A — Web UI (Recommended)**
```bash
python app.py
```
Then open http://localhost:7860 in your browser

**Option B — Desktop UI**
```bash
python desktop_app.py
```

## Step 4: Test (1 minute)

1. Select a model from dropdown
2. Type a message in the chat box
3. Click "Send"
4. Wait for response (1-5 seconds depending on model)

---

## 🔥 Quick Features

### Chat Tab
- Pick any model
- Edit system prompt
- Full conversation history
- Metrics tracked

### Copilot Tab
- AI assistant for coding questions
- Research methodology help
- Portfolio advice
- Unlimited conversations

### Tools Tab
- 🧮 Calculator (safe math)
- 🔍 Web Search (mock)
- 📄 File Reader (sandboxed)

### SpecLab Tab
- Test value conflicts
- Compare model behavior
- Export results as JSON

### SentinelBench Tab
- Evaluate a monitor on synthetic transcripts
- See suspiciousness scores and blind spot categories
- Use it to demonstrate safety-monitor style evaluation

### Status Tab
- Check API configuration
- View session metrics
- See provider status

---

## ⚡ No API Key? Use Ollama (Free & Local)

```bash
# 1. Install Ollama from ollama.ai
# 2. Start server
ollama serve

# 3. Pull a model (in another terminal)
ollama pull llama2

# 4. In app, select ollama/llama2
# 5. Chat works offline!
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named gradio" | `pip install -r requirements.txt` |
| "GROQ_API_KEY not set" | Edit .env with your Groq key |
| "Ollama not running" | Run `ollama serve` in another terminal |
| "Port 7860 in use" | Close other Gradio apps or edit app.py |
| "Can't import timer" | Make sure you're in cfui/ directory |

---

## 📊 Pro Tips

1. **First time?** Start with `ollama/llama2` (local, no API key)
2. **Fast responses?** Use `groq/llama3-70b` (free, 1-2 sec)
3. **Best quality?** Use `anthropic/claude-sonnet` (needs API key)
4. **Multiple models?** Run tests to benchmark them

---

## 🎯 Next: Explore Features

After basic chat works:
- [ ] Try Copilot tab (ask it Python questions)
- [ ] Run Calculator tool with "sqrt(16)"
- [ ] Try SpecLab with 2 different models
- [ ] Check Status tab for metrics
- [ ] Add your own API key for better models

---

## 🔗 Resources

- **Gradio** — https://www.gradio.app
- **Groq** — https://console.groq.com
- **Anthropic** — https://console.anthropic.com
- **Ollama** — https://ollama.ai
- **NIM** — https://docs.nvidia.com/nim

---

**That's it! You're ready to start researching.** 🚀
