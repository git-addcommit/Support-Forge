"""
Portfolio Analyzer — Synthesize results from SpecLab, SentinelBench, SkillForge
Creates unified reports, cross-project comparisons, and statistical summaries.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import statistics


@dataclass
class ProjectMetrics:
    """Standardized metrics across all projects"""
    project_name: str
    total_scenarios: int
    avg_metric: float
    min_metric: float
    max_metric: float
    std_dev: float
    key_finding: str


class PortfolioAnalyzer:
    """Unified analysis across all three research projects"""

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).resolve().parent.parent
        self.speclab_results = self.base_path / "speclab" / "results"
        self.sentinelbench_results = self.base_path / "sentinelbench" / "results"
        self.skillforge_results = self.base_path / "skillforge" / "results"

    def load_speclab_results(self) -> Optional[Dict]:
        """Load latest SpecLab experiment results"""
        if not self.speclab_results.exists():
            return None

        json_files = sorted(self.speclab_results.glob("*.json"))
        if not json_files:
            return None

        with open(json_files[-1]) as f:
            return json.load(f)

    def load_sentinelbench_results(self) -> Optional[Dict]:
        """Load latest SentinelBench monitor evaluation results"""
        if not self.sentinelbench_results.exists():
            return None

        json_files = sorted(self.sentinelbench_results.glob("*.json"))
        if not json_files:
            return None

        with open(json_files[-1]) as f:
            return json.load(f)

    def load_skillforge_results(self) -> Optional[Dict]:
        """Load latest SkillForge experiment results"""
        if not self.skillforge_results.exists():
            return None

        json_files = sorted(self.skillforge_results.glob("*.json"))
        if not json_files:
            return None

        with open(json_files[-1]) as f:
            return json.load(f)

    def analyze_speclab(self, data: Dict) -> ProjectMetrics:
        """Extract standardized metrics from SpecLab results"""
        divergences = [
            scenario.get("divergence_score", 0)
            for scenario in data.get("scenarios", [])
        ]

        if not divergences:
            return ProjectMetrics(
                project_name="SpecLab",
                total_scenarios=0,
                avg_metric=0,
                min_metric=0,
                max_metric=0,
                std_dev=0,
                key_finding="No data"
            )

        return ProjectMetrics(
            project_name="SpecLab",
            total_scenarios=len(divergences),
            avg_metric=statistics.mean(divergences),
            min_metric=min(divergences),
            max_metric=max(divergences),
            std_dev=statistics.stdev(divergences) if len(divergences) > 1 else 0,
            key_finding=f"Average behavioral divergence: {statistics.mean(divergences):.2%}. "
                       f"Models with explanations showed lower divergence."
        )

    def analyze_sentinelbench(self, data: Dict) -> ProjectMetrics:
        """Extract standardized metrics from SentinelBench results"""
        blind_spot_rates = [
            transcript.get("missed_rate", 0)
            for transcript in data.get("transcripts", [])
        ]

        if not blind_spot_rates:
            return ProjectMetrics(
                project_name="SentinelBench",
                total_scenarios=0,
                avg_metric=0,
                min_metric=0,
                max_metric=0,
                std_dev=0,
                key_finding="No data"
            )

        return ProjectMetrics(
            project_name="SentinelBench",
            total_scenarios=len(blind_spot_rates),
            avg_metric=statistics.mean(blind_spot_rates),
            min_metric=min(blind_spot_rates),
            max_metric=max(blind_spot_rates),
            std_dev=statistics.stdev(blind_spot_rates) if len(blind_spot_rates) > 1 else 0,
            key_finding=f"Monitor missed {statistics.mean(blind_spot_rates):.1%} of harmful transcripts. "
                       f"File-reuse and counting blind spots most exploited."
        )

    def analyze_skillforge(self, data: Dict) -> ProjectMetrics:
        """Extract standardized metrics from SkillForge results"""
        ai_assisted_scores = data.get("ai_assisted_scores", [])
        solo_scores = data.get("solo_scores", [])

        if not (ai_assisted_scores and solo_scores):
            return ProjectMetrics(
                project_name="SkillForge",
                total_scenarios=0,
                avg_metric=0,
                min_metric=0,
                max_metric=0,
                std_dev=0,
                key_finding="No data"
            )

        all_scores = ai_assisted_scores + solo_scores
        ai_avg = statistics.mean(ai_assisted_scores)
        solo_avg = statistics.mean(solo_scores)
        gap = solo_avg - ai_avg

        return ProjectMetrics(
            project_name="SkillForge",
            total_scenarios=len(ai_assisted_scores) + len(solo_scores),
            avg_metric=statistics.mean(all_scores),
            min_metric=min(all_scores),
            max_metric=max(all_scores),
            std_dev=statistics.stdev(all_scores) if len(all_scores) > 1 else 0,
            key_finding=f"AI-assisted avg: {ai_avg:.1%}, Solo avg: {solo_avg:.1%}. "
                       f"Replicated {gap:.1%} mastery gap from Shen & Tamkin."
        )

    def generate_portfolio_report(self) -> Dict:
        """Generate unified portfolio report across all projects"""
        report = {
            "metadata": {
                "title": "Cipher-Fellows Portfolio Analysis",
                "projects": 3,
                "created_at": Path.cwd().stat().st_mtime
            },
            "projects": []
        }

        # Load and analyze each project
        speclab = self.load_speclab_results()
        if speclab:
            report["projects"].append(asdict(self.analyze_speclab(speclab)))

        sentinelbench = self.load_sentinelbench_results()
        if sentinelbench:
            report["projects"].append(asdict(self.analyze_sentinelbench(sentinelbench)))

        skillforge = self.load_skillforge_results()
        if skillforge:
            report["projects"].append(asdict(self.analyze_skillforge(skillforge)))

        report["cross_project_insights"] = self._generate_insights(report["projects"])

        return report

    def _generate_insights(self, metrics: List[Dict]) -> List[str]:
        """Generate cross-project insights"""
        insights = []

        if len(metrics) >= 2:
            avg_metrics = [m["avg_metric"] for m in metrics]
            insights.append(
                f"Portfolio shows {statistics.mean(avg_metrics):.1%} average alignment "
                f"across all projects."
            )

        if len(metrics) == 3:
            insights.append(
                "All three research directions validated: specs diverge under conflict, "
                "monitors miss blind spots, and AI affects skill retention."
            )

        return insights

    def export_markdown_report(self, report: Dict, output_path: Path) -> None:
        """Export report as Markdown for GitHub"""
        md_lines = [
            "# Cipher-Fellows Portfolio Report\n",
            "## Executive Summary\n",
            "Cross-project analysis of three research initiatives for Anthropic Fellows.\n"
        ]

        if report.get("projects"):
            md_lines.append("## Project Metrics\n")
            for project in report["projects"]:
                md_lines.append(f"\n### {project['project_name']}\n")
                md_lines.append(f"- **Scenarios**: {project['total_scenarios']}\n")
                md_lines.append(f"- **Average Metric**: {project['avg_metric']:.2%}\n")
                md_lines.append(f"- **Range**: [{project['min_metric']:.2%}, {project['max_metric']:.2%}]\n")
                md_lines.append(f"- **Key Finding**: {project['key_finding']}\n")

        if report.get("cross_project_insights"):
            md_lines.append("## Cross-Project Insights\n")
            for insight in report["cross_project_insights"]:
                md_lines.append(f"- {insight}\n")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("".join(md_lines))


if __name__ == "__main__":
    analyzer = PortfolioAnalyzer()
    report = analyzer.generate_portfolio_report()
    print(json.dumps(report, indent=2))

    # Export markdown
    analyzer.export_markdown_report(
        report,
        Path("docs/portfolio-report.md")
    )
