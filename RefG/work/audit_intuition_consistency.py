from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
REFG_DIR = ROOT / "RefG"
WORK_DIR = REFG_DIR / "work"
INTUITIVE_FILE = ROOT / "Intuitive.md"
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
        "operational_readout",
        "The measurable world is the base medium's operational self-distinction. "
        "Rods, clocks, particles, and detectors are themselves medium modes, so "
        "pure void, internal spacing, or absolute tempo are not read directly.",
    ),
    (
        "local_omega_population_lock",
        "Stable oscillons lock to a local population tempo Omega(x). Ratios are "
        "the invariant objects; the active framework has no independent universal "
        "substrate frequency nu0 or hidden master clock.",
    ),
    (
        "bernoulli_refractive_source",
        "Mass/gravity is the external refractive readout of a Bernoulli "
        "pressure/energy deficit. The active source is the projected deficit "
        "channel, not a naked determinant, raw F_min source, or direct pressure "
        "push on matter.",
    ),
    (
        "internal_external_split",
        "Proper/internal inventory and external mass/readout are distinct. "
        "Compact objects may read as lower external active mass without implying "
        "that the internal material inventory vanished.",
    ),
    (
        "no_double_counting",
        "Node pressure, local oscillon tails, vortex/MOND transport, clock/unit "
        "readout, and ADM/bulk readout must stay in separate ledgers unless an "
        "action-level bridge explicitly combines them.",
    ),
    (
        "three_scale_pressure_ledger",
        "Compact objects, MOND/galaxies, clusters, and cosmology are read as "
        "different pressure/readout channels of one medium. MOND, Bullet, CMB/LSS, "
        "and no-particle-DM claims remain conditional until their fit gates close.",
    ),
    (
        "process_time_guard",
        "Process-time language is an internal formation-budget interpretation. "
        "It must not be inserted into primary H(z), CMB, BBN, photon-redshift, "
        "observed time-dilation, or atomic-clock channels.",
    ),
    (
        "particle_c3_candidate",
        "The active charged-lepton route is a C3/order-9 candidate-triplet. "
        "Koide structure is algebraically strong, but theta=2/9, h=2, "
        "m~nu^2, the electron scale, and radiative protection are open gates.",
    ),
    (
        "topology_gauge_candidate_map",
        "Spin, charge, color, and Standard-Model hosting are topological/geometric "
        "candidate maps. Maxwell/QED, U(1), SU(2), SU(3), fractional charge, "
        "spin-statistics, g=2, CKM/PMNS, and Born rule are not derived here.",
    ),
    (
        "alpha_open_structural_number",
        "alpha_EM is an open resonance/topological-lock hypothesis. It must not "
        "be derived from a substrate base frequency, Planck/Compton ratio, or the "
        "definition of the classical electron radius.",
    ),
]


RULES = [
    Rule(
        "OLD_INTUITIVE_FILE_NAME",
        "BLOCKER",
        r"Intuitive_Theory(?:\s*-\s*Copy)?\.md",
        "Old intuition-file name found.",
        "The active intuition source is Intuitive.md. Old intuition file "
        "names are stale references and make the audit miss the live source.",
        ("old", "legacy", "removed", "renamed", "not used", "migration"),
    ),
    Rule(
        "OLD_REFG_ROOT_DOC_PATH",
        "BLOCKER",
        r"RefG[/\\]+(?:Intuitive\.md|CODES\.md)",
        "Moved root document is still referenced inside RefG.",
        "Intuitive.md and CODES.md now live at the workspace root. RefG/... "
        "is reserved for work files and data paths.",
        ("old", "legacy", "removed", "renamed", "moved", "not used", "migration", "grep"),
    ),
    Rule(
        "OLD_RG_FOLDER_PATH",
        "BLOCKER",
        r"RG[/\\]+(?:Intuitive\.md|CODES\.md|work[/\\]+|data[/\\]+)",
        "Old RG folder path found.",
        "Work/data file references must use RefG/..., while Intuitive.md and "
        "CODES.md live at the workspace root. The conceptual theory name RG "
        "may remain unchanged.",
        ("old", "legacy", "removed", "renamed", "not used", "migration", "grep"),
    ),
    Rule(
        "C_DELTA_LOCK",
        "BLOCKER",
        r"\bC[_\\]?Delta\b|\\Lambda[_\\]?Delta\b|\bLambda[_\\]?Delta\b",
        "Old Delta constraint machinery found.",
        "The current intuition uses projected Bernoulli pressure/energy "
        "deficit as the active source channel. Old C_Delta/Lambda_Delta "
        "constraint machinery must remain historical or rejected.",
        ("old", "legacy", "rejected", "removed", "audit", "forbid", "forbidden", "grep"),
    ),
    Rule(
        "H_EQUALS_DETERMINANT",
        "BLOCKER",
        r"H(?:[_\\]?Delta)?\s*=\s*-?\s*(?:sp\.)?(?:log|ln|\\ln)\s*\(?"
        r"(?:I[_\\]?3|\\lambda_r|lambda_r)",
        "H is tied directly to a determinant or spatial stretch.",
        "The compact/refractive source is the projected Bernoulli "
        "pressure/energy-deficit channel. Direct determinant locking is not the "
        "current source law.",
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
        "compact active source must be the projected pressure/energy deficit, "
        "not a naked determinant.",
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
        "Raw F_min is not itself the compact source. The current intuition "
        "keeps local deficit, population lock, and action-level selection in "
        "separate ledgers unless a bridge is explicitly derived.",
        (
            "rejected",
            "audit",
            "obstruction",
            "nonzero",
            "residual",
            "phase-normalized",
            "not a naked",
            "not the source",
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
        "SUBSTRATE_NU0_LOCK",
        "HIGH",
        r"(?:nu[_\\]?0|\\nu[_\\]?0|substrate frequency|background frequency|"
        r"base frequency|universal numerical frequency|master clock).{0,120}"
        r"(?:lock|standard|input|required|derived|fundamental|absolute|"
        r"carrier)|(?:137|alpha|alpha[_\\]?EM).{0,120}"
        r"(?:nu[_\\]?0|\\nu[_\\]?0|substrate frequency|base frequency)",
        "Old substrate-frequency/master-clock language found.",
        "The active intuition uses local Omega(x) and population mutual lock. "
        "There is no independent universal nu0, hidden clock, or 137-from-nu0 "
        "derivation.",
        (
            "old",
            "legacy",
            "rejected",
            "removed",
            "not",
            "no ",
            "without",
            "does not",
            "not require",
            "not a required input",
            "historical",
            "metaphor",
            "firewall",
        ),
    ),
    Rule(
        "DIRECT_PRESSURE_PUSH",
        "HIGH",
        r"(?:pressure|deficit|medium).{0,80}(?:push|wind|drag|friction|"
        r"direct force)|(?:push|wind|drag|friction|direct force).{0,80}"
        r"(?:pressure|deficit|medium)",
        "Gravity is being written as a direct pressure push/wind/drag.",
        "The current language is pressure/stress source -> metric/index "
        "readout -> geodesic or refractive motion. Uniform motion has no "
        "medium drag.",
        (
            "not",
            "no ",
            "zero",
            "absence",
            "without",
            "not direct",
            "no direct",
            "not a direct",
            "not a pressure push",
            "no medium drag",
            "frictionless",
            "ram pressure",
            "gas",
            "hydro",
        ),
    ),
    Rule(
        "LOCAL_LIGHT_SPEED_CHANGED",
        "HIGH",
        r"(?:local|locally|measured|laboratory).{0,80}"
        r"(?:speed of light|c[_\\]?meas|c_meas).{0,80}"
        r"(?:changes|varies|slows|decreases|is reduced)|"
        r"(?:speed of light|c[_\\]?meas|c_meas).{0,80}"
        r"(?:changes|varies|slows|decreases|is reduced).{0,80}"
        r"(?:local|locally|measured|laboratory)",
        "Locally measured light speed is being changed.",
        "Only coordinate/readout light speed changes. Local dimensionless "
        "measurements self-calibrate with rods and clocks.",
        ("not", "no ", "unchanged", "invariant", "does not", "cannot"),
    ),
    Rule(
        "PROPER_INVENTORY_VANISHES",
        "HIGH",
        r"(?:proper|internal|interior|material|matter).{0,80}"
        r"(?:inventory|mass|matter|material).{0,80}"
        r"(?:vanishes|disappears|is destroyed|is erased|goes to zero|"
        r"ceases to exist)|(?:mass|matter).{0,80}"
        r"(?:vanishes|disappears|is destroyed|is erased).{0,80}"
        r"(?:compact|black hole|merger|interior)",
        "Internal/proper inventory is being erased.",
        "Compact deficit language changes external active/readout mass; it "
        "must not claim that internal material inventory simply disappears.",
        ("not", "no ", "does not", "without", "not saying", "not mean"),
    ),
    Rule(
        "PROCESS_TIME_PRIMARY_BRANCH_MIX",
        "HIGH",
        r"(?:C\(z\)|process[- ]time|process time).{0,140}"
        r"(?:H\(z\)|CMB|BBN|photon redshift|atomic clocks?|"
        r"observed time dilation|primary metric|primary FLRW)|"
        r"(?:H\(z\)|CMB|BBN|photon redshift|atomic clocks?|"
        r"observed time dilation|primary metric|primary FLRW).{0,140}"
        r"(?:C\(z\)|process[- ]time|process time)",
        "Process-time language is mixed into a primary metric/clock channel.",
        "Process time is allowed only as an intrinsic formation-budget "
        "interpretation. It must not be inserted into H(z), CMB, BBN, photon "
        "redshift, observed time dilation, or atomic clocks.",
        (
            "not",
            "no ",
            "must not",
            "blocked",
            "separate",
            "does not enter",
            "do not insert",
            "not added",
            "not be inserted",
            "outside the primary",
            "outside primary",
            "separate from",
            "separation",
            "restriction",
            "provide bounds",
            "bounds on",
            "bookkeeping",
            "field-space",
            "postulate",
            "არ უნდა",
            "არ არის",
            "არ შედის",
            "არ დაემატოს",
            "დამხმარე",
        ),
    ),
    Rule(
        "TIRED_LIGHT",
        "HIGH",
        r"\btired[- ]light\b|light.{0,40}(?:gets tired|loses energy by tired)",
        "Tired-light language found.",
        "The active cosmology keeps FLRW/redshift compatibility. Internal "
        "pressure/tempo relaxation is not tired light.",
        ("not", "no ", "rejected", "blocked", "not tired", "would become", "double-count"),
    ),
    Rule(
        "RAW_PSI2_COSMIC_MAP",
        "HIGH",
        r"(?:rho|density|matter|cosmic web|large[- ]scale).{0,80}"
        r"(?:=|is|as|mapped to).{0,40}(?:\|psi\|\^2|\\psi\^2|raw amplitude)|"
        r"(?:\|psi\|\^2|\\psi\^2|raw amplitude).{0,80}"
        r"(?:matter|density|cosmic web|large[- ]scale)",
        "Cosmic matter is mapped to raw amplitude instead of node/pressure readout.",
        "The Chladni analogy must be node/pressure/gradient readout, not raw "
        "|psi|^2 amplitude mapping.",
        ("not", "no ", "instead", "avoid", "blocked", "not raw", "not mapped"),
    ),
    Rule(
        "C3_GENERATION_OVERCLAIM",
        "HIGH",
        r"(?:C3|order[- ]9|Koide|theta\s*=\s*2/9|m\s*(?:~|\\propto|propto)"
        r"\s*nu\^?2).{0,140}(?:complete|final|derived|proved|generation "
        r"theorem|PDG[- ]precision|electron mass derived|radiative protection "
        r"closed)",
        "C3/Koide charged-lepton candidate is being overclaimed.",
        "The C3/order-9 route is active and strong, but theta=2/9, h=2, "
        "m~nu^2, electron scale, pole masses, and radiative protection remain "
        "open or conditional gates.",
        (
            "not",
            "no ",
            "candidate",
            "open",
            "conditional",
            "not complete",
            "not final",
            "not derived",
            "not a generation theorem",
            "fail",
            "fails",
            "misses",
            "residual",
        ),
    ),
    Rule(
        "GAUGE_SM_OVERCLAIM",
        "HIGH",
        r"(?:Maxwell|QED|U\(1\)|SU\(2\)|SU\(3\)|QCD|Standard Model|"
        r"fractional charge|spin[- ]statistics|g\s*=\s*2|CKM|PMNS|"
        r"Born rule).{0,140}(?:derived|proved|closed|complete|final|solved)",
        "Gauge/SM/quantum candidate map is being promoted to a derivation.",
        "The new intuition treats these as hosting/candidate maps until the "
        "relevant action-level, QFT, and empirical gates are closed.",
        (
            "not",
            "no ",
            "candidate",
            "open",
            "requires",
            "not derived",
            "not closed",
            "not complete",
            "still open",
            "do_not_claim",
            "do not claim",
            "blacklist",
            "forbid",
            "forbidden",
            "legacy mathieu",
            "overclaim blacklist",
        ),
    ),
    Rule(
        "ALPHA_DERIVATION_OVERCLAIM",
        "HIGH",
        r"(?:alpha[_\\]?EM|\\alpha[_\\]?EM|fine[- ]structure|1/137|137\b)"
        r".{0,140}"
        r"(?:derived|proved|closed|comes from|is predicted by|from substrate "
        r"frequency|from base frequency|Planck.*Compton|Compton.*Planck|"
        r"classical electron radius)",
        "alpha_EM/137 is being overclaimed.",
        "alpha_EM is an open structural number. It is not derived from a base "
        "frequency, Planck/Compton ratio, or the definitional classical electron "
        "radius identity.",
        (
            "not",
            "no ",
            "open",
            "not derived",
            "does not",
            "fails",
            "definition",
            "definitional",
            "stress-test",
            "do_not_claim",
            "do not claim",
            "legacy mathieu",
            "overclaim blacklist",
        ),
    ),
    Rule(
        "OBSERVATIONAL_PASS_OVERCLAIM",
        "HIGH",
        r"(?:SPARC|RAR|Bullet|cluster|CMB|LSS|BAO|Planck|LVK|LIGO|EHT|"
        r"Solar[- ]System|2PN|GW catalog).{0,140}"
        r"(?:pass|passed|proved|solved|closed|confirmed|validated|likelihood "
        r"complete|posterior)",
        "A phenomenology/observational gate may be overclaimed.",
        "Empirical pass starts only at the relevant fit, likelihood, posterior, "
        "or benchmark gate. Algebraic or candidate bridges do not count as "
        "observational passes.",
        (
            "not",
            "no ",
            "requires",
            "open",
            "conditional",
            "benchmark",
            "not completed",
            "not a proof",
            "not observational",
            "separate gate",
            "blocked",
            "toy",
            "toy_pass",
            "toy_fail",
            "scan",
            "comparison",
            "benchmark",
            "same-input",
            "same_input",
            "linear_same_input",
            "not_article_ready",
            "not article ready",
            "particle/quantum predictions before",
            "requires",
            "require",
        ),
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
        r"\b(non-emptiness|coefficiential|coefficientary)\b",
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
        "one-medium many-channel foundation",
        (
            "one base medium",
            "one medium",
            "many channels",
            "phase channel",
            "pressure channel",
        ),
        ("p01_core.py",),
    ),
    (
        "local Omega population lock",
        (
            "Omega",
            "\\Omega",
            "population lock",
            "mutual lock",
            "no master clock",
            "substrate frequency",
        ),
        (
            "p10_oscillons.py",
            "p11c_population_lock_ledger.py",
            "p11h_fmin_population_first_set_gate.py",
            "p17_unified_spectral_formula.py",
        ),
    ),
    (
        "Bernoulli/refractive gravity chain",
        (
            "Bernoulli",
            "pressure deficit",
            "refractive",
            "n_eff",
            "h_eff",
            "factor 2",
        ),
        (
            "p10_oscillons.py",
            "p13_refractive_force.py",
            "p15h_metric_readout_filters_gate.py",
        ),
    ),
    (
        "internal/external compact readout split",
        (
            "proper inventory",
            "external readout",
            "mass deficit",
            "finite core",
            "horizonless",
        ),
        (
            "p15e_internal_external_readout_split_gate.py",
            "p15h_metric_readout_filters_gate.py",
            "p16j_geodesic_completeness_regular_object.py",
        ),
    ),
    (
        "projected compact deficit source",
        ("H_\\Delta", "H_Delta", "projected deficit", "naked determinant", "F_min"),
        (
            "p05g_exponential_source_eom.py",
            "p05i_spatial_medium_eom_gate.py",
            "p05q_no_double_count_reprocessing_audit.py",
            "p05r_variational_no_double_count_projector_gate.py",
        ),
    ),
    (
        "MOND/vortex/coherence bridge",
        ("MOND", "BTFR", "vortex", "coherence", "SPARC", "RAR"),
        ("p07_mond.py", "p13_refractive_force.py"),
    ),
    (
        "cluster/Bullet three-channel pressure ledger",
        ("Bullet", "cluster", "cosmic-node", "tail retention", "merger memory"),
        ("p09_bullet.py", "p17_unified_spectral_formula.py"),
    ),
    (
        "FLRW/process-time/CMB separation",
        ("process time", "C(z)", "FLRW", "CMB", "BBN", "redshift"),
        (
            "p02_cosmo.py",
            "p02b_process_time_ledger.py",
            "p02c_dynamic_phase_clock.py",
            "p08_cmb.py",
        ),
    ),
    (
        "charged-lepton C3/Koide candidate",
        ("C3", "Koide", "theta=2/9", "order-9", "m\\propto\\nu^2"),
        (
            "p11_particles.py",
            "p11b_c3_triplet_inversion.py",
            "p11d_koide_structure_reduction.py",
            "p11i_mass_bridge_radiative_residual_gate.py",
        ),
    ),
    (
        "topological/gauge candidate map",
        (
            "spin",
            "charge",
            "color",
            "Maxwell",
            "QED",
            "SU(3)",
            "Standard Model",
        ),
        ("p11_particles.py", "p17_unified_spectral_formula.py"),
    ),
    (
        "unified micro-macro spectral skeleton",
        ("unified spectral", "Chladni", "node pressure", "cosmic web", "Kronecker"),
        ("p17_unified_spectral_formula.py",),
    ),
    (
        "prediction/status discipline",
        ("prediction", "observational pass", "article-ready", "claim gate"),
        (
            "p12_predictions.py",
            "p17_unified_spectral_formula.py",
        ),
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


def context_lines(lines: list[str], index: int, radius: int = 5) -> str:
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
    lines.append(f"- Active intuition source: `{rel(INTUITIVE_FILE)}`")
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
        help="Write the Markdown report. Optional path defaults to RefG/work/intuition_audit_report.md.",
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


def configure_output_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass


def main() -> int:
    configure_output_encoding()
    args = parse_args()
    include_articles = not args.no_article
    targets = discover_targets(include_articles=include_articles)
    work_files = sorted(WORK_DIR.glob("p*.py"))
    article_paths = [path for path in ARTICLE_CANDIDATES if path.exists()]

    findings, suppressed = scan_static(targets, show_allowed=args.show_allowed)
    if not INTUITIVE_FILE.exists():
        findings.append(
            Finding(
                severity="BLOCKER",
                rule_id="INTUITIVE_FILE_MISSING",
                path=INTUITIVE_FILE,
                line_no=1,
                message="Active intuition file is missing.",
                snippet=str(INTUITIVE_FILE),
                rationale="The audit must scan Intuitive.md; otherwise it can "
                "silently compare work files against stale assumptions.",
            )
        )
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
