"""W2_F1-ის პირველი იზოლირებული კანდიდატური კარიბჭე.

ეს ფაილი არ ამტკიცებს RefG-ის ფუძის თვითგარჩევას. იგი ამოწმებს მხოლოდ
უფრო ვიწრო, ზუსტად დასახელებულ ფაქტს: არსებობს თუ არა წინასწარ არჩეული
მიმართულების გარეშე ჩაწერილი, ატემპორალური და სიმეტრიული სათამაშო კანდიდატი, რომელსაც
პარამეტრების ღია არეში ნულოვანი და არანულოვანი ტოტების გარჩევა შეუძლია.

აქ q არის აბსტრაქტული შიდა რიგის პარამეტრი. იგი არ არის სივრცე, დრო,
მეტრიკა, ფუძის წნევა ან დაკვირვებადი ფიზიკური ველი. ამიტომ ამ კოდის PASS
ნიშნავს მხოლოდ ``TOY_EXACT_IDENTITY`` დონის კანდიდატურ წარმატებას;
``W2_F1_SELF_DIFFERENTIATION`` და ყველა შემდგომი ფიზიკური კარიბჭე ღია რჩება.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-RADIAL-LANDAU-v1.2-frozen"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"


CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_TOY_RADIAL_SELF_DIFFERENTIATION_001",
    "CLAIM": (
        "ორკომპონენტიან აბსტრაქტულ რიგის პარამეტრზე აგებულ, წინასწარ არჩეული "
        "მიმართულების არმქონე O(2)-სიმეტრიულ "
        "ატემპორალურ ვარიაციულ კანდიდატს a < 0 და lambda > 0 ღია არეში აქვს "
        "სტაბილური არანულოვანი ტოტი, ხოლო a > 0 საკონტროლო არეში — სტაბილური "
        "ნულოვანი ტოტი."
    ),
    "TYPE": "EXACT_IDENTITY; მტკიცებულების როლი: TOY_POSITIVE_CONTROL; არა MECHANISM_DERIVED",
    "MODEL_VERSION": (
        f"{MODEL_VERSION}; პოტენციალის, კომპონენტების რაოდენობის, წყაროს ან "
        "PASS-ლოგიკის ცვლილება ახალ ვერსიას მოითხოვს."
    ),
    "ASSUMPTIONS": [
        "q=(q1,q2) არის რეალური აბსტრაქტული შიდა რიგის პარამეტრი.",
        "lambda > 0.",
        "გატეხილ ტოტზე a < 0; ნულოვან საკონტროლო ტოტზე a > 0.",
        "მდგომარეობა მიიღება ატემპორალური ვარიაციული პირობით grad(V)=0.",
        "a-ს ნიშანი აქ დაშვებულია და ფუძის მიკროდინამიკიდან ჯერ არ არის გამოყვანილი.",
    ],
    "DOMAIN": (
        "სასრულგანზომილებიანი სტატიკური სათამაშო მოდელი; a != 0, lambda > 0. "
        "კრიტიკული წერტილი a=0 ცალკეა და ამ მტკიცებით არ იხურება."
    ),
    "CONVENTIONS": (
        "V=(a/2)(q.q)+(lambda/4)(q.q)^2; ევკლიდური შიდა ნამრავლი მხოლოდ "
        "აბსტრაქტულ შიდა კანდიდატურ სივრცეში; ფიზიკური დრო და სივრცე არ გამოიყენება."
    ),
    "FREEDOM_LEDGER": {
        "q1,q2": {
            "source": "გარედან მოცემული R^2 მდგომარეობათა სივრცე",
            "range": "R^2",
            "scope": "თითოეული ვარიაციული მდგომარეობა",
            "effective_complexity": "ორი რეალური ვარიაციული თავისუფლება; მონაცემით არ ირგება",
        },
        "a": {
            "source": "გარედან მოცემული კვადრატული კოეფიციენტი",
            "range": "გატეხილ კონტროლში a<0; ნულოვან კონტროლში a>0; a=0 გამორიცხულია",
            "scope": "ერთი უნივერსალური სკალარი თითო კანდიდატურ მოდელში",
            "effective_complexity": "ერთი რეალური პარამეტრი; მონაცემით არ ირგება",
        },
        "lambda": {
            "source": "გარედან მოცემული მეოთხე ხარისხის კოეფიციენტი",
            "range": "lambda>0",
            "scope": "ერთი უნივერსალური სკალარი თითო კანდიდატურ მოდელში",
            "effective_complexity": "ერთი დადებითი პარამეტრი; მონაცემით არ ირგება",
        },
        "h": {
            "source": "მხოლოდ წინასწარ ჩაშენებული მიმართულების უარყოფითი კონტროლი",
            "range": "რეალური h!=0",
            "scope": "საბაზო კანდიდატში აკრძალულია",
            "effective_complexity": "ერთი საკონტროლო სკალარი; საბაზო მოდელის სირთულეში არ შედის",
        },
        "r,mu,alpha,rho,theta": {
            "source": "მტკიცების ალგებრული პარამეტრიზაციები",
            "range": "r,mu,alpha>0; rho,theta რეალურია",
            "scope": "მხოლოდ ზუსტი ჩასმა და მეორე გამოყვანა",
            "effective_complexity": "ნულოვანი მოდელური თავისუფლება; ახალი ფიზიკური პარამეტრები არ არის",
        },
        "fixed_dimension_and_functional_form": {
            "source": "გარედან მოცემული სათამაშო არქიტექტურა",
            "range": "ზუსტად ორი კომპონენტი და კვარტიკული O(2)-ინვარიანტული V",
            "scope": "მხოლოდ ამ გაყინულ კანდიდატში",
            "effective_complexity": "დისკრეტული არქიტექტურული არჩევანი; ფუძიდან ჯერ არ არის გამოყვანილი",
        },
        "data_fitted_parameters": {
            "source": "N/A — მონაცემი არ გამოიყენება",
            "range": "ზუსტად 0",
            "scope": "მთელი კანდიდატი",
            "effective_complexity": "0",
        },
    },
    "DEPENDENCIES": [
        f"{PROGRAM_CONTRACT}: პროგრამული საზღვრების PASS; ფიზიკური მტკიცებები ღიაა",
        "ფუძის მიკროდინამიკიდან a<0-ის გამოყვანა არ არის დამოკიდებულებად გამოცხადებული; ამიტომ W2_F1 ღია რჩება.",
    ],
    "METHOD": (
        "SymPy-ით ზუსტი სიმბოლური დიფერენცირება, ჰესიანის ანალიზი, პირდაპირი "
        "ჩასმა, ორთოგონალური არევის ტესტი და წინასწარ ჩაშენებული წყაროს უარყოფითი კონტროლი."
    ),
    "PASS_CONDITION": [
        "საწყისი პოტენციალი შეიცავს მხოლოდ {q1,q2,a,lambda}-ს, არ შეიცავს მიმართულების წყაროს და ზუსტად O(2)-ინვარიანტულია.",
        "ზუსტი გრადიენტი და ჰესიანი ემთხვევა დამოუკიდებლად ჩაწერილ ანალიზურ ფორმებს.",
        "a>0 ტოტზე ნულოვანი მდგომარეობა დადებითად მდგრადია და რეალური არანულოვანი ტოტი არ არსებობს.",
        "a<0-ზე q=0 სტაციონარული, მაგრამ არამდგრადი ტოტია.",
        "a<0 ტოტზე არანულოვანი წრე completed-square იდენტობით გლობალური მინიმუმია, რადიალურად მდგრადია და სიმეტრიის მიმართულებით ნულოვანი მოდა აქვს.",
        "პოტენციალი ზუსტად უცვლელია ზოგადი ბრუნვისა და reflection-ისას, რომლებიც O(2)-ის ორივე კომპონენტს ფარავს.",
        "არანულოვანი ტოტი ნარჩუნდება a<0, lambda>0 ღია არეში.",
        "-h*q1 წყაროს მქონე წინასწარ ჩაშენებული მოდელი სწორად უარყოფილია როგორც სპონტანური თვითგარჩევა.",
    ],
    "FAIL_CONDITION": (
        "ნებისმიერი ზუსტი ნაშთი არანულოვანია, მდგრადობის ნიშანი მცდარია, "
        "საბაზო პოტენციალის ცხადი O(2)-ინვარიანტობა ირღვევა წყაროს გარეშე, ან "
        "წინასწარ ჩაშენებული კონტროლი შეცდომით გადის PASS-ზე. მდგომარეობის მიერ "
        "მიმართულების სპონტანური არჩევა მარცხი არ არის."
    ),
    "FALSIFIER": (
        "საწყისი პოტენციალიდან მიღებული არანულოვანი გრადიენტული/ჰესიანური ნაშთი, "
        "a<0-ზე არანულოვანი მინიმუმის არყოფნა, a>0-ზე რეალური არანულოვანი მინიმუმი, "
        "ან ორთოგონალური არევისას V-ის ცვლილება."
    ),
    "RESIDUAL": "ყველა შემოწმებული იდენტობისთვის ზუსტად 0 უნდა იყოს.",
    "ERROR_BOUND": "0 — მხოლოდ ზუსტი სიმბოლური ალგებრა; რიცხვითი მიახლოება არ გამოიყენება.",
    "VALIDITY_HEALTH": (
        "მხოლოდ სტატიკური, სასრულგანზომილებიანი ვარიაციული სათამაშო მოდელი. "
        "ჰესიანი გატეხილ ტოტზე დადებით ნახევრადგანსაზღვრულია; ნულოვანი მიმართულება "
        "O(2)-ის სიმეტრიულ ორბიტას ეკუთვნის. მიზეზობრიობა, გავრცელება და ველის "
        "ფიზიკური თავისუფლების ხარისხები აქ არ განისაზღვრება."
    ),
    "BRANCHES": {
        "a>0": "q=0 — სტაბილური ნულოვანი ტოტი",
        "a<0_unstable_origin": "q=0 — სტაციონარული, მაგრამ უარყოფითი ჰესიანით არამდგრადი ტოტი",
        "a<0_global_minima": "q.q=-a/lambda — გლობალური მინიმუმების არანულოვანი წრე, სიმეტრიის მოდულით",
        "a=0": "კრიტიკული ტოტი — ამ მტკიცების ფარგლებს გარეთ",
        "prewired_h!=0": "უარყოფილი: მიმართულება წყაროში წინასწარ არის ჩადებული",
    },
    "OBSERVABLE_MAP": (
        "ფიზიკური დაკვირვებადი: N/A — სათამაშო მოდელია. შიდა დიაგნოსტიკური რუკაა q -> s=q.q."
    ),
    "FORWARD_MODEL": "N/A — დაკვირვებით მონაცემთან კავშირი ამ კარიბჭის ფარგლებს გარეთაა.",
    "DATA_ROLE": "N/A — არც მორგების, არც ვალიდაციის და არც პროგნოზის მონაცემი არ გამოიყენება.",
    "IDENTIFIABILITY": (
        "მეთოდია ზუსტი სიმეტრიული ორბიტისა და იაკობიანის რანგის ანალიზი; ზღურბლია "
        "ზუსტი ნული. შიდა ამპლიტუდა s=-a/lambda მხოლოდ a/lambda შეფარდებას ადგენს, "
        "ამიტომ a და lambda ცალ-ცალკე დეგენერირებულია; მიმართულებაც განუზღვრელია "
        "O(2)-ის ორბიტის გამო. ფიზიკური დაკვირვებადი აქ საერთოდ არ არსებობს."
    ),
    "BENCHMARK": (
        "დადებითი კონტროლია ცნობილი a<0 Landau-ტოტი; ნულოვანი კონტროლია a>0, "
        "lambda>0; წინასწარ ჩაშენებული კონტროლია V_h=V-h*q1. შედარების მეტრიკაა "
        "ზუსტი სიმბოლური ნაშთი და ჰესიანის ნიშანი; PASS-ზღურბლია ზუსტად 0 და "
        "მკაცრი ნიშანი, რიცხვითი ტოლერანტობის გარეშე."
    ),
    "PRIMITIVE_REGISTRY": {
        "1_objects_and_state_space": "q=(q1,q2) in R^2; სხვა მდგომარეობითი ობიექტი არ არის.",
        "2_primitive_relations": "ხელით მოცემული ევკლიდური შიდა ნამრავლი და s=q.q.",
        "3_symmetry_and_equivalence": "O(2) სიმეტრია; q და Rq ერთ სიმეტრიულ ორბიტას ეკუთვნის.",
        "4_rule": "ატემპორალური ვარიაციული პირობა grad(V)=0 და ჰესიანით მდგრადობა.",
        "5_free_parameters": "a რეალურია; lambda>0; q ვარიაციულია; მონაცემით მორგება არ არის.",
        "6_initial_and_boundary_conditions": "N/A — არც ევოლუცია და არც სივრცითი საზღვარი არ გამოიყენება.",
        "7_randomness": "N/A — შემთხვევითი თესლი ან განაწილება არ გამოიყენება.",
        "8_computational_index": "N/A — q1,q2 ალგებრული კომპონენტებია და არა სივრცე/დრო.",
        "9_validity_and_limits": "სასრულგანზომილებიანი სტატიკური სათამაშო მოდელი; a!=0, lambda>0.",
        "10_imported_not_derived": (
            "R^2 მდგომარეობათა სივრცე, ევკლიდური შიდა ნამრავლი, O(2), მეოთხე ხარისხის "
            "პოტენციალი და a-ს ნიშანი გარედანაა მოცემული; არცერთი მათგანი RefG-ის ფუძიდან არ არის მიღებული."
        ),
    },
    "METRIC_ROUTE": (
        "N/A — W2_F1 ეტაპზე მეტრიკამდე არც რიგი+ოთხმოცულობის, არც K-მატრიცის და "
        "არც ჰიბრიდული გზა არ არის არჩეული."
    ),
    "CONTROL_REGISTRY": {
        "positive": "a<0-ზე ცნობილი არანულოვანი სიმეტრიული ორბიტის აღდგენა",
        "null": "a>0-ზე მხოლოდ სტაბილური q=0",
        "prewired": "V-h*q1 უნდა გამოვლინდეს და უარყოფილ იქნეს",
        "scrambled": "ზუსტი O(2) არევა ნორმასა და V-ს არ ცვლის",
        "robustness": "a<0-ის გარშემო უწყვეტი შეშფოთების ოჯახი ტოტს ინარჩუნებს",
        "second_algebraic_derivation": "ერთცვლადიანი რადიალური გამოყვანა; იგივე SymPy ძრავა, არა დამოუკიდებელი პროგრამა",
    },
    "COMPUTATIONAL_INDEX_ROLE": "N/A — გამოთვლითი ნაბიჯი, ევოლუციის ინდექსი ან ფიზიკური დრო არ არსებობს.",
    "OLD_WORK_LEDGER": (
        "N/A — ძველი RefG/work-იდან არცერთი ლემა, ფორმულა, კოეფიციენტი ან PASS არ არის შემოტანილი."
    ),
    "CLOSURE_FLAGS": {
        "W2_G1_CONVENTIONS": False,
        "toy_positive_control_exact_identity": False,
        "W2_F1_SELF_DIFFERENTIATION": False,
        "W2_F2_OPERATIONAL_RELATIONS": False,
        "W2_F3_INTERNAL_ORDER_CAUSALITY": False,
        "W2_F4_INDEPENDENT_ADDITIVE_MODES": False,
        "W2_M1_DIMENSION_CONTINUUM": False,
        "W2_M2_LORENTZIAN_METRIC": False,
        "W2_A0_EFFECTIVE_ACTION_ORIGIN": False,
        "W2_A1_ACTION_VARIATION": False,
        "W2_A2_CONSERVATION_NO_DOUBLE_COUNT": False,
        "W2_A3_DOF_HEALTH": False,
        "W2_A4_UNIVERSAL_MATTER_METRIC": False,
        "W2_E1_REDUCED_ACTION_MATCHING": False,
        "W2_E2_EXACT_EINSTEIN_BRANCH": False,
        "W2_E3_SOURCE_WORLDTUBE_MATCHING": False,
        "W2_L1_WEAK_SOURCE_PN_PPN_HANDOFF": False,
        "W2_L2_COMPACT_SOURCE_EIH_HANDOFF": False,
    },
    "CROSSCHECK": (
        "მრავალცვლადიანი ჰესიანისგან ცალკე გამოიყენება რადიალური ერთცვლადიანი "
        "ალგებრული გამოყვანა და პირდაპირი ჩასმა. ეს მეორე გამოყვანაა, მაგრამ იგივე "
        "SymPy ძრავას იყენებს და დამოუკიდებელ პროგრამულ იმპლემენტაციად არ ითვლება."
    ),
    "PROVENANCE": (
        "2026-07-21; კოდის, W2-C0 კონტრაქტისა და CODES.md-ის SHA-256 გაშვებისას "
        "იბეჭდება; გამომავალი არტეფაქტი — სტანდარტულ გამომავალში დაბეჭდილი JSON ანგარიში."
    ),
    "FILES": [
        "CODES.md",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_01_self_differentiation_candidate_gate.py",
    ],
}


def _is_zero(expr: sp.Expr) -> bool:
    """ამოწმებს ზუსტ სიმბოლურ ნულს."""

    return sp.simplify(expr) == 0


def _matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    """ამოწმებს, რომ მატრიცის ყველა კომპონენტი ზუსტად ნულია."""

    return all(_is_zero(entry) for entry in matrix)


def run_gate() -> dict[str, Any]:
    """ასრულებს W2_F1-ის სათამაშო კანდიდატის ყველა წინასწარ გაყინულ ტესტს."""

    q1, q2, a = sp.symbols("q1 q2 a", real=True)
    lam, r, mu, alpha = sp.symbols("lambda r mu alpha", positive=True)
    h = sp.symbols("h", real=True, nonzero=True)
    theta = sp.symbols("theta", real=True)

    q = sp.Matrix([q1, q2])
    s = sp.expand(q.dot(q))
    potential = a * s / 2 + lam * s**2 / 4

    gradient = sp.Matrix([sp.diff(potential, variable) for variable in q])
    hessian = sp.hessian(potential, (q1, q2))

    expected_gradient = (a + lam * s) * q
    expected_hessian = (a + lam * s) * sp.eye(2) + 2 * lam * (q * q.T)

    gradient_residual = sp.simplify(gradient - expected_gradient)
    hessian_residual = sp.simplify(hessian - expected_hessian)

    allowed_symbols = {q1, q2, a, lam}
    declared_symbol_inventory_exact = potential.free_symbols == allowed_symbols

    required_contract_fields = {
        "CLAIM_ID",
        "CLAIM",
        "TYPE",
        "MODEL_VERSION",
        "ASSUMPTIONS",
        "DOMAIN",
        "CONVENTIONS",
        "FREEDOM_LEDGER",
        "DEPENDENCIES",
        "METHOD",
        "PASS_CONDITION",
        "FAIL_CONDITION",
        "FALSIFIER",
        "RESIDUAL",
        "ERROR_BOUND",
        "VALIDITY_HEALTH",
        "BRANCHES",
        "OBSERVABLE_MAP",
        "FORWARD_MODEL",
        "DATA_ROLE",
        "IDENTIFIABILITY",
        "BENCHMARK",
        "CLOSURE_FLAGS",
        "CROSSCHECK",
        "PROVENANCE",
        "FILES",
    }
    required_primitive_entries = {
        "1_objects_and_state_space",
        "2_primitive_relations",
        "3_symmetry_and_equivalence",
        "4_rule",
        "5_free_parameters",
        "6_initial_and_boundary_conditions",
        "7_randomness",
        "8_computational_index",
        "9_validity_and_limits",
        "10_imported_not_derived",
    }
    required_controls = {
        "positive",
        "null",
        "prewired",
        "scrambled",
        "robustness",
        "second_algebraic_derivation",
    }
    conventions_gate_pass = (
        required_contract_fields.issubset(CLAIM_CONTRACT)
        and set(CLAIM_CONTRACT["PRIMITIVE_REGISTRY"]) == required_primitive_entries
        and set(CLAIM_CONTRACT["CONTROL_REGISTRY"]) == required_controls
        and CLAIM_CONTRACT["METRIC_ROUTE"].startswith("N/A")
        and CLAIM_CONTRACT["COMPUTATIONAL_INDEX_ROLE"].startswith("N/A")
        and CLAIM_CONTRACT["OLD_WORK_LEDGER"].startswith("N/A")
    )

    # წინასწარ განსაზღვრული ნულოვანი კონტროლი: a=mu^2>0.
    null_substitution = {q1: 0, q2: 0, a: mu**2}
    null_gradient = sp.simplify(gradient.subs(null_substitution))
    null_hessian = sp.simplify(hessian.subs(null_substitution))
    null_required_norm_sq = -mu**2 / lam
    null_control_pass = (
        _matrix_is_zero(null_gradient)
        and null_hessian == mu**2 * sp.eye(2)
        and null_required_norm_sq.is_negative is True
    )

    # გატეხილი ტოტის წარმომადგენელი: a=-lambda*r^2, q=(r,0).
    broken_substitution = {q1: r, q2: 0, a: -lam * r**2}
    broken_gradient = sp.simplify(gradient.subs(broken_substitution))
    broken_hessian = sp.simplify(hessian.subs(broken_substitution))
    expected_broken_hessian = sp.diag(2 * lam * r**2, 0)
    broken_energy_gap = sp.simplify(potential.subs(broken_substitution) - potential.subs({q1: 0, q2: 0}))

    completed_square = lam * (s + a / lam) ** 2 / 4 - a**2 / (4 * lam)
    completed_square_residual = sp.simplify(potential - completed_square)
    nonnegative_square_term = lam * (s + a / lam) ** 2 / 4
    completed_square_minimum_residual = sp.simplify(
        nonnegative_square_term.subs(broken_substitution)
    )

    broken_origin_substitution = {q1: 0, q2: 0, a: -mu**2}
    broken_origin_gradient = sp.simplify(gradient.subs(broken_origin_substitution))
    broken_origin_hessian = sp.simplify(hessian.subs(broken_origin_substitution))
    broken_origin_unstable = (
        _matrix_is_zero(broken_origin_gradient)
        and broken_origin_hessian == -mu**2 * sp.eye(2)
        and (-mu**2).is_negative is True
    )

    radial_vector = sp.Matrix([r, 0])
    tangent_vector = sp.Matrix([0, r])
    radial_eigen_residual = sp.simplify(
        broken_hessian * radial_vector - 2 * lam * r**2 * radial_vector
    )
    tangent_zero_mode_residual = sp.simplify(broken_hessian * tangent_vector)
    broken_branch_pass = (
        _matrix_is_zero(broken_gradient)
        and broken_hessian == expected_broken_hessian
        and broken_energy_gap == -lam * r**4 / 4
        and (2 * lam * r**2).is_positive is True
        and (-lam * r**4 / 4).is_negative is True
        and _is_zero(completed_square_residual)
        and nonnegative_square_term.is_nonnegative is True
        and _is_zero(completed_square_minimum_residual)
        and broken_origin_unstable
        and _matrix_is_zero(radial_eigen_residual)
        and _matrix_is_zero(tangent_zero_mode_residual)
    )

    # ზოგადი SO(2) ბრუნვა და reflection*rotation ფარავს O(2)-ის ორივე კომპონენტს.
    rotation = sp.Matrix(
        [
            [sp.cos(theta), -sp.sin(theta)],
            [sp.sin(theta), sp.cos(theta)],
        ]
    )
    reflection = sp.diag(1, -1)
    improper_rotation = reflection * rotation

    rotation_orthogonality_residual = (rotation.T * rotation - sp.eye(2)).applyfunc(sp.trigsimp)
    improper_orthogonality_residual = (
        improper_rotation.T * improper_rotation - sp.eye(2)
    ).applyfunc(sp.trigsimp)
    rotation_determinant_residual = sp.trigsimp(rotation.det() - 1)
    improper_determinant_residual = sp.trigsimp(improper_rotation.det() + 1)

    rotated_q = rotation * q
    reflected_rotated_q = improper_rotation * q
    rotated_s = sp.trigsimp(sp.expand(rotated_q.dot(rotated_q)))
    reflected_rotated_s = sp.trigsimp(sp.expand(reflected_rotated_q.dot(reflected_rotated_q)))
    rotated_potential = a * rotated_s / 2 + lam * rotated_s**2 / 4
    reflected_rotated_potential = (
        a * reflected_rotated_s / 2 + lam * reflected_rotated_s**2 / 4
    )
    rotation_norm_residual = sp.trigsimp(rotated_s - s)
    improper_norm_residual = sp.trigsimp(reflected_rotated_s - s)
    rotation_potential_residual = sp.trigsimp(sp.expand(rotated_potential - potential))
    improper_potential_residual = sp.trigsimp(
        sp.expand(reflected_rotated_potential - potential)
    )
    o2_invariance_pass = (
        _matrix_is_zero(rotation_orthogonality_residual)
        and _matrix_is_zero(improper_orthogonality_residual)
        and _is_zero(rotation_determinant_residual)
        and _is_zero(improper_determinant_residual)
        and _is_zero(rotation_norm_residual)
        and _is_zero(improper_norm_residual)
        and _is_zero(rotation_potential_residual)
        and _is_zero(improper_potential_residual)
    )

    # (alpha,lambda)->(a,lambda)=(-alpha,lambda) ზუსტად ფარავს ღია არეს
    # a<0, lambda>0 და აქვს არანულოვანი იაკობიანი.
    open_a = -alpha
    open_norm_sq = alpha / lam
    open_radial_eigenvalue = 2 * alpha
    open_stationarity_residual = sp.simplify(open_a + lam * open_norm_sq)
    open_parameter_map = sp.Matrix([open_a, lam])
    open_map_jacobian = open_parameter_map.jacobian((alpha, lam))
    open_map_determinant = sp.simplify(open_map_jacobian.det())
    open_region_pass = (
        open_a.is_negative is True
        and open_norm_sq.is_positive is True
        and open_radial_eigenvalue.is_positive is True
        and _is_zero(open_stationarity_residual)
        and open_map_determinant == -1
    )

    # დამოუკიდებელი ერთცვლადიანი რადიალური გადამოწმება.
    rho = sp.symbols("rho", real=True)
    radial_potential = a * rho**2 / 2 + lam * rho**4 / 4
    radial_first = sp.diff(radial_potential, rho)
    radial_second = sp.diff(radial_potential, rho, 2)
    radial_first_residual = sp.simplify(radial_first.subs({rho: r, a: -lam * r**2}))
    radial_second_residual = sp.simplify(
        radial_second.subs({rho: r, a: -lam * r**2}) - 2 * lam * r**2
    )
    radial_second_derivation_pass = _is_zero(radial_first_residual) and _is_zero(radial_second_residual)

    # წინასწარ ჩაშენებული მიმართულება. ეს მოდელი განზრახ უნდა ჩავარდეს.
    prewired_potential = potential - h * q1
    prewired_gradient = sp.Matrix(
        [sp.diff(prewired_potential, variable) for variable in q]
    )
    prewired_gradient_at_origin = sp.simplify(prewired_gradient.subs({q1: 0, q2: 0}))
    prewired_source_detected = prewired_gradient_at_origin == sp.Matrix([-h, 0])
    prewired_candidate_rejected = prewired_source_detected and h.is_nonzero is True

    exact_residuals_pass = _matrix_is_zero(gradient_residual) and _matrix_is_zero(hessian_residual)
    toy_positive_control_pass = all(
        [
            declared_symbol_inventory_exact,
            conventions_gate_pass,
            exact_residuals_pass,
            null_control_pass,
            broken_branch_pass,
            o2_invariance_pass,
            open_region_pass,
            radial_second_derivation_pass,
            prewired_candidate_rejected,
        ]
    )

    closure_flags = dict(CLAIM_CONTRACT["CLOSURE_FLAGS"])
    closure_flags["W2_G1_CONVENTIONS"] = conventions_gate_pass
    closure_flags["toy_positive_control_exact_identity"] = toy_positive_control_pass

    source_path = Path(__file__).resolve()
    program_contract_path = source_path.with_name("w2_00_foundation_to_einstein_contract.md")
    codes_path = source_path.parents[2] / "CODES.md"
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    program_contract_hash = hashlib.sha256(program_contract_path.read_bytes()).hexdigest()
    codes_hash = hashlib.sha256(codes_path.read_bytes()).hexdigest()

    return {
        "claim_id": CLAIM_CONTRACT["CLAIM_ID"],
        "model_version": MODEL_VERSION,
        "program_contract": PROGRAM_CONTRACT,
        "status": (
            "EXACT_IDENTITY_PASS__TOY_POSITIVE_CONTROL__W2_F1_OPEN"
            if toy_positive_control_pass
            else "EXACT_IDENTITY_FAIL__TOY_POSITIVE_CONTROL__W2_F1_OPEN"
        ),
        "toy_positive_control_pass": toy_positive_control_pass,
        "refg_W2_F1_closed": False,
        "scope_ceiling": "TOY_SELF_DIFFERENTIATION_CANDIDATE_ONLY",
        "reason_refg_gate_remains_open": (
            "R^2 მდგომარეობათა სივრცე, O(2), კვარტიკული ფუნქციური ფორმა და a<0-ის "
            "ნიშანი ფუძის მიკროდინამიკიდან ჯერ არ არის გამოყვანილი; q-ს ფიზიკური "
            "მნიშვნელობა და დაკვირვებადი რუკაც არ აქვს."
        ),
        "checks": {
            "complete_claim_and_primitive_registry": conventions_gate_pass,
            "declared_symbol_inventory_exact": declared_symbol_inventory_exact,
            "no_preferred_direction_O2_invariance": o2_invariance_pass,
            "exact_gradient_hessian_residuals": exact_residuals_pass,
            "null_control_a_positive": null_control_pass,
            "unstable_origin_a_negative": broken_origin_unstable,
            "broken_branch_a_negative": broken_branch_pass,
            "completed_square_global_minimum": (
                _is_zero(completed_square_residual)
                and nonnegative_square_term.is_nonnegative is True
                and _is_zero(completed_square_minimum_residual)
            ),
            "open_region_robustness": open_region_pass,
            "second_radial_algebraic_derivation": radial_second_derivation_pass,
            "prewired_direction_rejected": prewired_candidate_rejected,
        },
        "exact_residuals": {
            "gradient": str(gradient_residual),
            "hessian": str(hessian_residual),
            "completed_square": str(completed_square_residual),
            "rotation_orthogonality": str(rotation_orthogonality_residual),
            "improper_orthogonality": str(improper_orthogonality_residual),
            "rotation_norm": str(rotation_norm_residual),
            "improper_norm": str(improper_norm_residual),
            "rotation_potential": str(rotation_potential_residual),
            "improper_potential": str(improper_potential_residual),
            "open_region_stationarity": str(open_stationarity_residual),
            "radial_first": str(radial_first_residual),
            "radial_second": str(radial_second_residual),
        },
        "branch_diagnostics": {
            "null_required_norm_sq": str(null_required_norm_sq),
            "broken_hessian": str(broken_hessian),
            "broken_energy_gap": str(broken_energy_gap),
            "broken_origin_hessian": str(broken_origin_hessian),
            "open_region_a": str(open_a),
            "open_region_norm_sq": str(open_norm_sq),
            "open_region_radial_eigenvalue": str(open_radial_eigenvalue),
            "open_map_determinant": str(open_map_determinant),
            "prewired_gradient_at_origin": str(prewired_gradient_at_origin),
        },
        "closure_flags": closure_flags,
        "provenance": {
            "source_file": str(source_path.as_posix()),
            "source_sha256": source_hash,
            "program_contract_sha256": program_contract_hash,
            "codes_sha256": codes_hash,
            "sympy_version": sp.__version__,
        },
    }


def main() -> int:
    """ბეჭდავს თვითკმარ JSON ანგარიშს და მარცხისას აბრუნებს არანულოვან კოდს."""

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["toy_positive_control_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
