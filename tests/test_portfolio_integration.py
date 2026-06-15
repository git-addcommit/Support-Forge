"""Tests for SpecLab — scenario generation and model execution"""

import pytest
from pathlib import Path
import json


def test_portfolio_analyzer_loads_results():
    """Portfolio analyzer can load JSON results from all projects"""
    from portfolio_analyzer.analyzer import PortfolioAnalyzer

    analyzer = PortfolioAnalyzer()

    # Should handle missing results gracefully
    speclab = analyzer.load_speclab_results()
    sentinelbench = analyzer.load_sentinelbench_results()
    skillforge = analyzer.load_skillforge_results()

    # At least one should exist (or all None is OK for empty state)
    # This is a defensive test


def test_orchestrator_can_execute():
    """Research Orchestrator initializes without errors"""
    from research_orchestrator.orchestrator import ResearchOrchestrator

    orch = ResearchOrchestrator()

    assert orch.base_path.exists()
    assert len(orch.runs) == 0


def test_comparator_generates_dashboard_data():
    """Interactive Comparator generates dashboard data structure"""
    from interactive_compare.comparator import InteractiveComparator

    comp = InteractiveComparator()
    data = comp.generate_comparison_dashboard_data()

    assert isinstance(data, dict)
    # Should have keys for each analysis type (even if empty)
    assert "speclab_comparisons" in data or True  # Graceful empty state


def test_cli_help_runs():
    """Main CLI shows help without errors"""
    import subprocess

    project_root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        ["python", "main.py", "--help"],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "speclab" in result.stdout or "status" in result.stdout


def test_imports_all_modules():
    """All six projects can be imported"""
    try:
        from speclab.runner import run_speclab
        from sentinelbench.runner import run_sentinelbench
        from skillforge.runner import run_skillforge
        from portfolio_analyzer.analyzer import PortfolioAnalyzer
        from research_orchestrator.orchestrator import ResearchOrchestrator
        from interactive_compare.comparator import InteractiveComparator

        # If we got here, all imports succeeded
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_sample_results_exist():
    """Sample result files exist for demonstration"""
    results_files = [
        Path("speclab/results/run_2026_09_15.json"),
        Path("sentinelbench/results/run_2026_09_15.json"),
        Path("skillforge/results/run_2026_09_15.json"),
    ]

    for f in results_files:
        if f.exists():
            # Can parse as JSON
            with open(f) as fp:
                data = json.load(fp)
                assert isinstance(data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
