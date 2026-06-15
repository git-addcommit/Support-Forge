```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║           cipher-fellows UI — QUICK REFERENCE CARD                   ║
║                                                                       ║
║              Save this. Refer during implementation.                  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 🎯 THE MISSION

Build a **portfolio-grade Gradio research dashboard** that demonstrates observability,
safe tool integration, and testing discipline for Anthropic Fellows application.

---

## 📂 KEY FILES & THEIR ROLE

### Code (Wire into app.py)
```
cfui/timer.py           → Session tracking, per-model metrics, cost projection
cfui/tools.py           → Calculator, Web Search, File Reader (3 safe tools)
cfui/models.json        → Model registry (Ollama, Groq, Anthropic, Gemini)
```

### Tests (Run with pytest)
```
cfui/tests/test_timer.py  → 20+ tests for timer module
cfui/tests/test_tools.py  → 15+ tests for tool functions
```

### Docs (Read in order)
```
COPILOT.md              → What to build (detailed roadmap)
IMPLEMENTATION_GUIDE.md → How to build it (step-by-step)
SPRINT2_SUMMARY.md      → Why it matters (portfolio impact)
DELIVERABLES_CHECKLIST  → What's been done (verification)
```

### Sample Data (For testing)
```
cfui/samples/README.md        → Documentation
cfui/samples/example.py       → Python code sample
cfui/samples/sample_data.json → JSON data sample
```

### DevOps (Automate & deploy)
```
.github/workflows/test.yml    → CI/CD pipeline (GitHub Actions)
Dockerfile                     → Container deployment
```

---

## ⚡ THE IMPLEMENTATION (3 Phases)

### PHASE 1: Timer Integration (1 hour)
- [ ] Wrap `call_model()` with timing in app.py
- [ ] Call `log_usage(model, latency)` after each API response
- [ ] Test: Send a chat message → timer records it

### PHASE 2: Dynamic UI (2 hours)
- [ ] Load models from `models.json` → Create dropdown
- [ ] Add metrics panel (gr.Markdown) showing timer output
- [ ] Add tool buttons (Calculator, Search, File Reader)

### PHASE 3: Testing & Ship (1.5 hours)
- [ ] Run `pytest tests/ -v` → All 35+ tests pass
- [ ] Push to GitHub → GitHub Actions runs CI
- [ ] Verify badge shows ✅

---

## 🛡️ SECURITY PATTERNS (Copy These)

### Safe Math Evaluation
```python
safe_dict = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'log': math.log,
    # ... only safe functions
}
result = eval(expr, {"__builtins__": {}}, safe_dict)
```
✅ No __import__, no open(), no exec()

### Sandboxed File Access
```python
target = Path(file_path).resolve()
sandbox = Path("samples").resolve()
target.relative_to(sandbox)  # Raises ValueError if outside
```
✅ No path traversal attacks

### AST Validation
```python
tree = ast.parse(expression)
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        raise ValueError("Imports not allowed")
```
✅ Block dangerous patterns before eval

---

## 📊 TESTING COMMAND REFERENCE

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_timer.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run one test class
pytest tests/test_timer.py::TestSessionLifecycle -v

# Run one test method
pytest tests/test_timer.py::TestSessionLifecycle::test_start_session_initializes -v

# Show detailed output
pytest tests/ -vv -s
```

---

## 🚀 DEPLOYMENT QUICK COMMANDS

```bash
# Local development
python cfui/app.py
# → Open http://localhost:7860

# Docker
docker build -t cipher-fellows-ui .
docker run -p 7860:7860 cipher-fellows-ui

# GitHub (create repo)
git init
git add .
git commit -m "feat: Add timer, tools, and test suite"
git remote add origin https://github.com/USERNAME/cipher-fellows.git
git push -u origin main
```

---

## ✅ VERIFICATION STEPS

Before pushing:

```bash
# 1. Check imports
python -c "from cfui.timer import *; print('✅ Timer imports OK')"
python -c "from cfui.tools import *; print('✅ Tools imports OK')"

# 2. Run app
python cfui/app.py &
# → Should start on http://localhost:7860
# → Send a message
# → Timer should update

# 3. Run tests
cd cfui && pytest tests/ -v
# → All 35+ tests should pass

# 4. Check coverage
pytest tests/ --cov=. --cov-report=term-missing
# → Should show 80%+ coverage

# 5. Lint (optional)
pylint cfui/app.py cfui/timer.py cfui/tools.py

# 6. Ready to push
git add .
git commit -m "feat: Timer UI, dynamic models, tool buttons"
git push
```

---

## 🎬 PORTFOLIO TALKING POINTS

When discussing with Anthropic:

✅ **Observability:** "I track per-model latency & cost because constraints matter."

✅ **Safety:** "AST validation, sandboxing, security-first design."

✅ **Testing:** "35+ tests, GitHub Actions CI, 80%+ coverage."

✅ **Extension:** "Configuration-driven—easy to add new models, tools, agents."

✅ **Research:** "Built on Zhang et al. (spec stress-testing) & SLEIGHT-Bench."

---

## 🚨 GOTCHAS & FIXES

| Problem | Solution |
|---------|----------|
| Tests fail to import | Run `cd cfui` before `pytest tests/` |
| Dropdown empty | Check `models.json` exists & valid JSON |
| Timer doesn't update | Make sure `log_usage()` called after API response |
| GitHub Actions fails | Verify `requirements.txt` has all deps |
| File reader fails | Check `samples/` directory exists |

---

## 📞 DOCUMENTATION REFERENCE

- **timer.py** — 450 lines, well-commented, copy-paste ready
- **tools.py** — 350 lines, examples of safe eval & sandboxing
- **COPILOT.md** — 400+ lines, detailed roadmap & TODOs
- **IMPLEMENTATION_GUIDE.md** — Step-by-step with code snippets
- **Tests** — 35+ tests showing expected behavior

**Everything is documented. No ambiguity. Just execute.**

---

## 🎯 SUCCESS CRITERIA

After this sprint, you should have:

✅ `app.py` integrates `timer.py`
✅ Dynamic model dropdown (from `models.json`)
✅ Timer metrics panel in UI
✅ Three tool buttons working
✅ 35+ tests passing
✅ GitHub repo with passing CI badge
✅ Clean commit history ready for review

**Narrative ready for Anthropic application interview.**

---

## 🏁 YOU'RE READY

Everything is:
- ✅ Designed
- ✅ Documented
- ✅ Coded
- ✅ Tested

**No more planning. Time to execute.**

**Start:** Open `IMPLEMENTATION_GUIDE.md` and follow Steps 1-10.

**Finish:** Push to GitHub and watch CI pass.

**Impact:** You've built a portfolio piece that demonstrates production-grade thinking.

---

**Good luck. You've got this. 🚀**

*Quick Reference v1 • 2026-06-12*
