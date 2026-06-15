# cipher-fellows

**AI safety research toolkit** — three empirical tools built as a portfolio for the Anthropic Fellows Program (ML Systems & Performance / AI Safety streams).

## Projects

### 1. SpecLab — Value-Conflict Stress Tester
Tests whether LLMs behave consistently when two legitimate values (honesty, helpfulness, safety, autonomy) conflict with each other. Measures behavioral divergence across models as a signal of spec ambiguity.

**Hypothesis:** Models receiving value explanations in their system prompt will show lower behavioral divergence on tradeoff scenarios than models given only rules.

**Inspired by:** Zhang et al. (2026) — *Stress-Testing Model Specs Reveals Character Differences among Language Models*

```bash
python main.py speclab --models llama3 qwen2 --demo
```

---

### 2. SentinelBench — Monitor Blind Spot Detector
Runs synthetic agent transcripts through Claude-as-monitor and measures which categories of harmful actions get missed. Focuses on 3 of the 11 SLEIGHT-Bench blind spot categories: file reuse, counting errors, and model priors.

**Hypothesis:** Claude-as-monitor will fail to flag harmful transcripts exploiting counting and file_reuse blind spots significantly more often than transcripts with overt harmful actions.

**Inspired by:** SLEIGHT-Bench — *Anthropic Fellows Program research output (2026)*

```bash
python main.py sentinelbench --demo
```

---

### 3. SkillForge — AI-Assisted Learning Experiment
Measures skill retention (quiz scores) after completing Python tasks with vs without AI assistance. Designed to partially replicate the Shen & Tamkin (2026) RCT methodology at small scale.

**Hypothesis:** AI-assisted participants will score lower on conceptual quiz questions than solo participants, replicating the 17% mastery gap reported in Shen & Tamkin (2026).

**Inspired by:** Shen & Tamkin (2026) — *How AI Impacts Skill Formation*

```bash
python main.py skillforge --demo
```

---

## Quick start

```bash
# Clone and set up
git clone https://github.com/YOUR_USERNAME/cipher-fellows
cd cipher-fellows
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Check environment
python main.py status

# Run a demo of all three tools
python main.py speclab --demo
python main.py sentinelbench --demo
python main.py skillforge --demo
```

## Claude usage

This project uses Claude (`claude-sonnet-4-6`) in three ways:
1. **SpecLab:** Claude analyzes behavioral divergence across model responses and identifies which value each model prioritized.
2. **SentinelBench:** Claude acts as the safety monitor, rating transcript suspiciousness 0–100.
3. **SkillForge:** Claude provides Socratic tutoring during AI-assisted task sessions.

All prompts are version-controlled in the `prompts/` directory. See `CLAUDE_USAGE.md` for full transparency on how Claude was used during development.

## Results

Key results will appear in `RESULTS.md` as experiments run. Each tool saves JSON output to its `results/` directory.

## Structure

```
cipher-fellows/
├── main.py                    # Unified CLI entry point
├── speclab/
│   ├── runner.py              # Scenario generator + model runner
│   └── results/               # JSON experiment outputs
├── sentinelbench/
│   ├── runner.py              # Transcript analyzer + monitor
│   └── results/
├── skillforge/
│   ├── runner.py              # Experiment + quiz + analysis
│   └── results/
├── shared/
│   └── status.py              # Environment checker
├── prompts/                   # All Claude prompts, version-controlled
├── notebooks/                 # Jupyter analysis notebooks
├── docs/                      # GitHub Pages output
└── requirements.txt
```

## Currently working on

- [ ] Running SpecLab across 3 models (llama3, qwen2, mistral) — 50 scenarios each
- [ ] Expanding SentinelBench to cover all 11 SLEIGHT-Bench categories
- [ ] Statistical analysis notebook comparing AI-assisted vs solo quiz scores
- [ ] Blog post writeup of preliminary findings

## References

- Zhang, J., Sleight, H., Peng, A., Schulman, J., & Durmus, E. (2026). Stress-Testing Model Specs Reveals Character Differences among Language Models.
- Shen, J. H. & Tamkin, A. (2026). How AI Impacts Skill Formation. arXiv:2601.20245.
- SLEIGHT-Bench (2026). Anthropic Fellows Program Research Output.
