from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
RG_DIR = ROOT / "RG"
WORK_DIR = RG_DIR / "work"
INTUITIVE_FILE = RG_DIR / "Intuitive_Theory.md"
DEFAULT_REPORT = WORK_DIR / "intuition_audit_report.md"


ARTICLE_CANDIDATES = [
    ROOT / "artikle" / "GERG" / "RefG_EN.tex",
    ROOT / "artikle" / "CQG" / "RefG_EN.tex",
    ROOT / "artikle" / "CQG" / "CQG_EN.tex",
    ROOT / "artikle" / "article.tex",
    ROOT / "artikle" / "ARTICLE_EN.tex",
]


STATUS_RE = re.compile(
    r"\b(PASS[A-Z0-9_]*|FAIL[A-Z0-9_]*|OPEN[A-Z0-9_]*|"
    r"REJECTED[A-Z0-9_]*|BLOCKED[A-Z0-9_]*|CLOSED[A-Z0-9_]*|"
    r"COMPLETE[A-Z0-9_]*|SOLVED[A-Z0-9_]*)\b"
)


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    pattern: str
    message: str
    rationale: str
    allowed_context: tuple[str, ...] = ()
    scopes: tuple[str, ...] = ("work", "article", "intuition")

    def regex(self) -> re.Pattern[str]:
        return re.compile(self.pattern, re.IGNORECASE)


@dataclass
class Finding:
    severity: str
    rule_id: str
    path: Path
    line_no: int
    message: str
    snippet: str
    rationale: str


INTUITION_ANCHORS = [
    (
        "multi_channel_medium",
        "One base medium can have phase, pressure, longitudinal, transverse, "
        "rotational, topological, resonance, and memory channels. These channels "
        "may interact, but they are not identical variables.",
    ),
    (
        "operational_stretch_invisibility",
        "Base-medium internal spacing/stretch is not directly measured by rods "
        "and clocks built from the same medium. Observable gravity reads the "
        "pressure/energy deficit, phase delay, time-rate change, and matter "
        "scale response.",
    ),
    (
        "pressure_deficit_source",
        "The compact source is the pressure/energy-deficit channel H_Delta, "
        "through the projected deficit operator. A spatial determinant may be "
        "an internal label, but it is not the compact source law.",
    ),
    (
        "no_double_counting",
        "If RefG supplies the mechanism of the Einstein geometry, the same "
        "medium structure must not be counted again as extra matter on the same "
        "geometry unless the action explicitly defines that additional source.",
    ),
    (
        "article_self_containment",
        "Every strong article claim must be hand-checkable from the paper text "
        "and backed by a concrete work-file calculation.",
    ),
]


RULES = [
    Rule(
        "C_DELTA_LOCK",
        "BLOCKER",
        r"\bC[_\\]?Delta\b|\\Lambda[_\\]?Delta\b|\bLambda[_\\]?Delta\b",
        "Old Delta constraint machinery found.",
        "The current intuition separates the independent pressure-deficit "
        "channel H_Delta from spatial determinant locking.",
        ("old", "rejected", "removed", "audit", "forbid", "forbidden", "grep"),
    ),
    Rule(
        "H_EQUALS_DETERMINANT",
        "BLOCKER",
        r"H(?:[_\\]?Delta)?\s*=\s*-?\s*(?:sp\.)?(?:log|ln|\\ln)\s*\(?"
        r"(?:I[_\\]?3|\\lambda_r|lambda_r)",
        "H is tied directly to a determinant or spatial stretch.",
        "H_Delta is the pressure/energy-deficit channel. Direct determinant "
        "locking was the core intuition mismatch that caused the compact-branch "
        "dead end.",
        (
            "not a global",
            "not a global pre-variation",
            "compact repair",
            "trial",
            "rejected",
            "rejects",
            "audit",
            "no constant",
            "no solution",
            "determinant-locked",
        ),
    ),
    Rule(
        "DETERMINANT_AS_SOURCE",
        "HIGH",
        r"(?:I[_\\]?3|determinant|spatial determinant).{0,80}(?:source|law)|"
        r"(?:source|law).{0,80}(?:I[_\\]?3|determinant|spatial determinant)",
        "A determinant is being described near source-law language.",
        "The determinant can be an internal medium invariant or label. The "
        "compact active source must be H_Delta through the projected deficit "
        "operator.",
        (
            "internal",
            "label",
            "not the",
            "not a",
            "measured compact source law is carried by h_delta",
            "compact source law is the independent",
            "active source law is the projected",
            "no determinant",
            "not used",
            "no spatial determinant",
        ),
    ),
    Rule(
        "RAW_FMIN_DOUBLE_COUNT",
        "HIGH",
        r"(?:Theta[_\\]?Delta|\\Theta[_\\]?Delta).{0,120}"
        r"(?:Theta[_\\]?F|\\Theta[_\\]?F)|"
        r"raw.{0,40}F[_\\]?min.{0,80}(?:source|matter)",
        "Possible compact double counting between deficit source and raw F_min.",
        "The compact phase-normalized F_min sector is quiet on the pure-phase "
        "exterior. Raw F_min may appear only as a rejected audit or obstruction.",
        (
            "rejected",
            "audit",
            "obstruction",
            "nonzero",
            "residual",
            "phase-normalized",
        ),
    ),
    Rule(
        "DIRECT_BASE_STRETCH_MEASURE",
        "HIGH",
        r"(?:base[- ]medium|internal|spatial).{0,80}(?:stretch|spacing)"
        r".{0,80}(?:measured|observable|observed)|"
        r"(?:measured|observable|observed|directly measured).{0,80}"
        r"(?:base[- ]medium|internal|spatial).{0,80}(?:stretch|spacing)",
        "Base-medium internal stretch is written as directly measurable.",
        "The intuition file says internal base stretch/compression is not "
        "directly measured. The observable is weakened connection, pressure "
        "deficit, phase delay, time-rate change, or matter scale response.",
        (
            "not directly",
            "not a measured",
            "not measured",
            "not the directly measured",
            "is not an observable",
            "unobservable",
        ),
    ),
    Rule(
        "CHANNEL_IDENTITY",
        "HIGH",
        r"(?:phase|pressure|longitudinal|transverse|rotation|vortex|memory)"
        r".{0,80}(?:identical|same variable|same dynamical property|automatic copy|"
        r"automatic copies)",
        "Different medium channels are being identified too strongly.",
        "The one-medium picture permits interactions between channels, not "
        "pre-imposed identities between them.",
        ("not identical", "not automatic", "different", "not copies"),
    ),
    Rule(
        "CLAIM_TOO_STRONG",
        "MEDIUM",
        r"\b(fully closed|complete proof|proved everywhere|final theory|"
        r"no open issue|all sectors closed)\b",
        "Very strong closure language found.",
        "Strong claims must match the actual work-file status. Mixed PASS/OPEN "
        "ledgers must stay mixed, not become total closure claims.",
        ("not final", "without promoting", "not the final"),
    ),
    Rule(
        "DEFENSIVE_LANGUAGE",
        "MEDIUM",
        r"\b(we do not claim|should not be read as|not meant to|merely|"
        r"only a toy|speculative only|preliminary only)\b",
        "Defensive/apologetic wording found.",
        "The article style should be calm and direct: state the actual status, "
        "calculation, and limitation without apology.",
        (),
        ("article",),
    ),
    Rule(
        "BAD_TERMINOLOGY",
        "LOW",
        r"\b(non-emptiness|coefficiential|coefficientary|toy model)\b",
        "Weak or bad terminology found.",
        "Terminology must stay clean and publication-level.",
        (),
    ),
    Rule(
        "YILMAZ_REFERENCE",
        "MEDIUM",
        r"\bYilmaz\b",
        "Yilmaz reference found.",
        "Deliberate decision (2026-06-10 rebuild plan): Yilmaz IS cited, but "
        "only neutrally/historically (Papapetrou metric lineage, the Misner "
        "controversy, distinction from Yilmaz's field equations). Supportive "
        "use of Yilmaz for the compact branch is still flagged.",
        (
            "avoid", "not include", "do not cite", "rejected",
            "controversy", "bibitem", "import the ghost", "refutation",
            "cancels newton",
        ),
        ("article", "work"),
    ),
]


CLAIM_BACKING = [
    (
        "phase-normalized F_min",
        ("phase-normalized", "F_{\\rm min}", "F_min"),
        (
            "p05s_phase_normalized_fmin_action_gate.py",
            "p03d_phase_normalized_solar_global_audit.py",
            "p05t_single_action_branch_consistency_gate.py",
        ),
    ),
    (
        "single-action branch consistency",
        ("same covariant EFT action", "same action", "branch action", "H=0"),
        ("p05t_single_action_branch_consistency_gate.py",),
    ),
    (
        "H Euler source on Solar guard",
        ("S_H", "H Euler", "H-equation", "partial F_{\\rm branch}/\\partial H"),
        ("p05t_single_action_branch_consistency_gate.py",),
    ),
    (
        "independent H_Delta compact source",
        ("H_\\Delta", "H_Delta", "projected deficit"),
        ("p05g_exponential_source_eom.py", "p05i_spatial_medium_eom_gate.py"),
    ),
    (
        "no double counting",
        ("double count", "additional compact matter", "raw F"),
        ("p05q_no_double_count_reprocessing_audit.py", "p05r_variational_no_double_count_projector_gate.py"),
    ),
    (
        "NEC deficit interpretation",
        ("NEC", "null energy", "deficit"),
        ("p14_nec_deficit.py",),
    ),
    (
        "strong-field prediction",
        ("ISCO", "photon sphere", "b_c", "golden"),
        ("p05_compact.py", "p12_predictions.py"),
    ),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def classify_scope(path: Path) -> str:
    if path == INTUITIVE_FILE:
        return "intuition"
    if WORK_DIR in path.parents:
        return "work"
    return "article"


def discover_targets(include_articles: bool) -> list[Path]:
    targets: list[Path] = []
    if INTUITIVE_FILE.exists():
        targets.append(INTUITIVE_FILE)
    targets.extend(sorted(WORK_DIR.glob("p*.py")))
    if include_articles:
        targets.extend(path for path in ARTICLE_CANDIDATES if path.exists())
    return targets


def context_lines(lines: list[str], index: int, radius: int = 2) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return "\n".join(lines[start:end]).lower()


def is_allowed(rule: Rule, context: str) -> bool:
    if not rule.allowed_context:
        return False
    normalized = re.sub(r"[\"']", " ", context.lower())
    normalized = " ".join(normalized.split())
    return any(" ".join(token.lower().split()) in normalized for token in rule.allowed_context)


def scan_static(targets: Iterable[Path], show_allowed: bool) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    suppressed = 0
    compiled = [(rule, rule.regex()) for rule in RULES]
    for path in targets:
        scope = classify_scope(path)
        text = read_text(path)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            for rule, regex in compiled:
                if scope not in rule.scopes:
                    continue
                if not regex.search(line):
                    continue
                context = context_lines(lines, idx)
                if is_allowed(rule, context):
                    suppressed += 1
                    if not show_allowed:
                        continue
                findings.append(
                    Finding(
                        severity="INFO_ALLOWED" if is_allowed(rule, context) else rule.severity,
                        rule_id=rule.rule_id,
                        path=path,
                        line_no=idx + 1,
                        message=rule.message,
                        snippet=line.strip(),
                        rationale=rule.rationale,
                    )
                )
    return findings, suppressed


def collect_statuses(path: Path) -> list[str]:
    try:
        text = read_text(path)
    except OSError:
        return []
    seen: list[str] = []
    for match in STATUS_RE.finditer(text):
        value = match.group(1)
        if value not in seen:
            seen.append(value)
    return seen


def status_ledger(files: Iterable[Path]) -> list[tuple[Path, list[str], str]]:
    rows: list[tuple[Path, list[str], str]] = []
    for path in files:
        statuses = collect_statuses(path)
        if not statuses:
            rows.append((path, [], "NO_STATUS_TOKEN"))
            continue
        has_pass = any(s.startswith("PASS") for s in statuses)
        has_open = any("OPEN" in s or s.startswith("OPEN") for s in statuses)
        has_fail = any(s.startswith("FAIL") or s.startswith("BLOCKED") for s in statuses)
        has_closed = any(
            s.startswith("CLOSED") or s.startswith("COMPLETE") or s.startswith("SOLVED")
            for s in statuses
        )
        if has_fail and has_pass:
            health = "CONFLICT_PASS_FAIL"
        elif has_closed and (has_open or has_fail):
            health = "CONFLICT_CLOSED_WITH_OPEN_OR_FAIL"
        elif has_pass and has_open:
            health = "MIXED_PASS_WITH_OPEN"
        elif has_open:
            health = "OPEN"
        elif has_pass:
            health = "PASS"
        else:
            health = "STATUS_REVIEW"
        rows.append((path, statuses, health))
    return rows


def status_findings_from_ledger(
    ledger: Iterable[tuple[Path, list[str], str]]
) -> list[Finding]:
    findings: list[Finding] = []
    severity_for_health = {
        "CONFLICT_CLOSED_WITH_OPEN_OR_FAIL": "HIGH",
        "CONFLICT_PASS_FAIL": "MEDIUM",
        "MIXED_PASS_WITH_OPEN": "LOW",
        "STATUS_REVIEW": "LOW",
        "NO_STATUS_TOKEN": "LOW",
    }
    for path, statuses, health in ledger:
        severity = severity_for_health.get(health)
        if severity is None:
            continue
        snippet = ", ".join(statuses[:6]) if statuses else "none"
        findings.append(
            Finding(
                severity=severity,
                rule_id="STATUS_LEDGER_REVIEW",
                path=path,
                line_no=1,
                message=f"Work-file status ledger needs review: {health}.",
                snippet=snippet,
                rationale=(
                    "Status words are part of the theory control surface. "
                    "A file that keeps old FAIL/OPEN/CLOSED labels beside new "
                    "PASS results can mislead article-status decisions."
                ),
            )
        )
    return findings


def run_work_files(files: Iterable[Path], timeout: float) -> list[tuple[Path, int | str, list[str]]]:
    results: list[tuple[Path, int | str, list[str]]] = []
    for path in files:
        try:
            proc = subprocess.run(
                [sys.executable, str(path)],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
                timeout=timeout,
            )
            output = "\n".join([proc.stdout, proc.stderr])
            statuses = []
            for match in STATUS_RE.finditer(output):
                value = match.group(1)
                if value not in statuses:
                    statuses.append(value)
            results.append((path, proc.returncode, statuses))
        except subprocess.TimeoutExpired:
            results.append((path, "TIMEOUT", []))
    return results


def claim_backing_report(article_paths: Iterable[Path]) -> list[tuple[str, str]]:
    article_text = "\n".join(read_text(path) for path in article_paths if path.exists())
    work_files = {path.name: path for path in WORK_DIR.glob("p*.py")}
    rows: list[tuple[str, str]] = []
    for claim_name, terms, backing_names in CLAIM_BACKING:
        present = any(term in article_text for term in terms)
        if not present:
            rows.append((claim_name, "NOT_IN_ARTICLE"))
            continue
        missing = [name for name in backing_names if name not in work_files]
        if missing:
            rows.append((claim_name, "MISSING_BACKING_FILE: " + ", ".join(missing)))
            continue
        weak = []
        for name in backing_names:
            statuses = collect_statuses(work_files[name])
            if not any(s.startswith("PASS") for s in statuses):
                weak.append(name)
        if weak:
            rows.append((claim_name, "BACKING_WITHOUT_PASS: " + ", ".join(weak)))
        else:
            rows.append((claim_name, "BACKED_BY_PASS_WORK_FILES"))
    return rows


def severity_counts(findings: Iterable[Finding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in findings:
        counts[item.severity] = counts.get(item.severity, 0) + 1
    return counts


def render_report(
    findings: list[Finding],
    suppressed: int,
    ledger: list[tuple[Path, list[str], str]],
    claim_rows: list[tuple[str, str]],
    run_rows: list[tuple[Path, int | str, list[str]]] | None,
) -> str:
    counts = severity_counts(findings)
    lines: list[str] = []
    lines.append("# Intuition Consistency Audit")
    lines.append("")
    lines.append("## Summary")
    if counts:
        for severity in ["BLOCKER", "HIGH", "MEDIUM", "LOW", "INFO_ALLOWED"]:
            if severity in counts:
                lines.append(f"- {severity}: {counts[severity]}")
    else:
        lines.append("- No unresolved static findings.")
    lines.append(f"- Suppressed allowed audit mentions: {suppressed}")
    lines.append("")
    lines.append("## Intuition Anchors")
    for key, text in INTUITION_ANCHORS:
        lines.append(f"- `{key}`: {text}")
    lines.append("")
    lines.append("## Static Findings")
    if findings:
        for item in findings:
            lines.append(
                f"- **{item.severity}** `{item.rule_id}` "
                f"[{rel(item.path)}:{item.line_no}]"
            )
            lines.append(f"  - {item.message}")
            lines.append(f"  - `{item.snippet}`")
            lines.append(f"  - {item.rationale}")
    else:
        lines.append("- No unresolved static findings.")
    lines.append("")
    lines.append("## Work Status Ledger")
    for path, statuses, health in ledger:
        shown = ", ".join(statuses[:8]) if statuses else "none"
        extra = "" if len(statuses) <= 8 else f" ... (+{len(statuses) - 8})"
        lines.append(f"- `{rel(path)}`: **{health}**; statuses: {shown}{extra}")
    lines.append("")
    lines.append("## Article Claim Backing")
    if claim_rows:
        for claim, status in claim_rows:
            lines.append(f"- `{claim}`: **{status}**")
    else:
        lines.append("- No article file found for claim-backing scan.")
    if run_rows is not None:
        lines.append("")
        lines.append("## Execution Ledger")
        for path, code, statuses in run_rows:
            shown = ", ".join(statuses) if statuses else "no status in output"
            lines.append(f"- `{rel(path)}`: exit={code}; output statuses: {shown}")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit RefG work files against core intuition constraints."
    )
    parser.add_argument(
        "--no-article",
        action="store_true",
        help="Skip article claim and terminology checks.",
    )
    parser.add_argument(
        "--show-allowed",
        action="store_true",
        help="Show allowed audit-only mentions such as rejected determinant trials.",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute every p*.py work file and collect exit codes/status tokens.",
    )
    parser.add_argument(
        "--strict-status",
        action="store_true",
        help="Promote mixed PASS/FAIL/OPEN/CLOSED status ledgers to findings.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Timeout in seconds for each work file when --run is used.",
    )
    parser.add_argument(
        "--write",
        nargs="?",
        const=str(DEFAULT_REPORT),
        help="Write the Markdown report. Optional path defaults to RG/work/intuition_audit_report.md.",
    )
    parser.add_argument(
        "--fail-on",
        choices=["BLOCKER", "HIGH", "MEDIUM", "LOW"],
        default="BLOCKER",
        help="Return nonzero if findings at this severity or higher exist.",
    )
    return parser.parse_args()


def exit_code_for(findings: list[Finding], fail_on: str) -> int:
    rank = {"BLOCKER": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "INFO_ALLOWED": 0}
    threshold = rank[fail_on]
    for item in findings:
        if rank.get(item.severity, 0) >= threshold:
            return 2
    return 0


def main() -> int:
    args = parse_args()
    include_articles = not args.no_article
    targets = discover_targets(include_articles=include_articles)
    work_files = sorted(WORK_DIR.glob("p*.py"))
    article_paths = [path for path in ARTICLE_CANDIDATES if path.exists()]

    findings, suppressed = scan_static(targets, show_allowed=args.show_allowed)
    ledger = status_ledger(work_files)
    if args.strict_status:
        findings.extend(status_findings_from_ledger(ledger))
    claim_rows = [] if args.no_article else claim_backing_report(article_paths)
    run_rows = run_work_files(work_files, args.timeout) if args.run else None

    report = render_report(findings, suppressed, ledger, claim_rows, run_rows)
    print(report)

    if args.write:
        out_path = Path(args.write)
        if not out_path.is_absolute():
            out_path = ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8", newline="\n")
        print(f"Wrote report: {rel(out_path)}")

    return exit_code_for(findings, args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
