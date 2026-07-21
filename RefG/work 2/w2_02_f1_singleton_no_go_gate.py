"""მკაცრად ერთმდგომარეობიანი ფუძის თვითგარჩევის შეუძლებლობის კარიბჭე.

ეს ფაილი ამოწმებს პირობით თეორემას და არა RefG-ის ფიზიკურ მექანიზმს:
თუ „სრულად გაურჩეველი ფუძე“ ნიშნავს ფიქსირებულ ერთელემენტიან მდგომარეობათა
სივრცეს, რომელსაც არც გარე გამომავალი რეესტრი და არც საკუთარი სივრცის
გაფართოების წესი აქვს, მაშინ მის შიგნით ორი არაეკვივალენტური მდგომარეობა
ვერ წარმოიქმნება. მრავალშედეგიანი საზომის იარლიყები დამატებითი კლასიკური
რეესტრია და არა singleton-ის ახალი შინაგანი მდგომარეობები.

თეორემა არ უარყოფს ერთ ონტოლოგიურ ფუძეს. იგი ერთმანეთისგან მიჯნავს:

1. ერთ ონტოლოგიურ მატარებელს, რომელსაც შეიძლება ჰქონდეს არატრივიალური
   თვითრელაციური მდგომარეობათა სივრცე; და
2. მკაცრ ერთმდგომარეობიან მოდელს, რომელსაც ასეთი შესაძლებლობაც არ აქვს.

მეორე წაკითხვა ზუსტად იკეტება no-go-თი. პირველი არის შემდეგი კანდიდატის
დასაშვები მიმართულება და ჯერ ღიაა.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


MODEL_VERSION = "W2-F1-SINGLETON-NO-GO-v1.5-corrected-internal"
PROGRAM_CONTRACT = "W2-C0-v1.0-frozen"


CLAIM_CONTRACT: dict[str, Any] = {
    "CLAIM_ID": "W2_F1_STRICT_SINGLETON_NO_GO_001",
    "CLAIM": (
        "ფიქსირებულ ერთელემენტიან მდგომარეობათა სივრცეზე, სივრცის გაფართოების "
        "გარე წესის გარეშე, დეტერმინისტული ენდომორფიზმი, ნორმირებული სტოქასტიკური "
        "ბირთვი, ატემპორალური ფუნქციონალი და ერთგანზომილებიანი კვანტური ევოლუცია "
        "ვერ წარმოქმნის ორ ოპერაციულად არაეკვივალენტურ მდგომარეობას."
    ),
    "TYPE": "CONDITIONAL / EXACT_IDENTITY (კარდინალობის no-go); არა ფიზიკური W2_F1 closure",
    "MODEL_VERSION": (
        f"{MODEL_VERSION}; დომენის, დაშვებული წესების, ოპერაციული ეკვივალენტობის "
        "ან PASS-ლოგიკის ცვლილება ახალ ვერსიას მოითხოვს."
    ),
    "ASSUMPTIONS": [
        "საბაზო მდგომარეობათა სივრცეა ზუსტად S={omega}.",
        "დაშვებული წესი S-ს არ აფართოებს და გარე ჩანაწერს/ნიშანს არ ამატებს.",
        "დეტერმინისტული წესი არის f:S->S.",
        "სტოქასტიკური წესი არის 1x1 არაუარყოფითი, რიგით ნორმირებული მარკოვის ბირთვი.",
        "ვარიაციული წესი არის ნებისმიერი რეალური ფუნქცია S-ზე.",
        "კვანტური წესი მოქმედებს ერთგანზომილებიან ჰილბერტის სივრცეზე; გლობალური ფაზით განსხვავებული ვექტორები ერთი ფიზიკური სხივია და ერთადერთი density matrix არის [1].",
        "მრავალშედეგიანი POVM ან S->Y სტოქასტიკური გამოსავალი მოითხოვს დამატებით outcome alphabet/register-ს; იგი S-ის შინაგანი მდგომარეობა არ არის.",
        "შინაგანი ოპერაციული განსხვავება მოითხოვს მინიმუმ ორ არაეკვივალენტურ მდგომარეობას; გარე ჩანაწერი ცალკე თავისუფლებად აღირიცხება.",
    ],
    "DOMAIN": (
        "მხოლოდ ფიქსირებული მკაცრი singleton მოდელები. გენერაციული გრამატიკა, "
        "არატრივიალური თვითრელაცია, მრავალმდგომარეობიანი სივრცე, გარე ხმაური, "
        "გამომავალი კლასიკური რეესტრი ან ჰილბერტის განზომილების ზრდა ამ დომენს "
        "სცდება და დამატებითი პრიმიტივია."
    ),
    "CONVENTIONS": (
        "omega არის აბსტრაქტული ერთადერთი მდგომარეობა; გამოთვლითი ინდექსები "
        "ფიზიკურ სივრცეს ან დროს არ აღნიშნავს; კვანტური მდგომარეობები სხივებით იდენტიფიცირდება."
    ),
    "FREEDOM_LEDGER": {
        "singleton_state": {
            "source": "თეორემის პირობითი დაშვება",
            "range": "ზუსტად ერთი ელემენტი",
            "scope": "საბაზო no-go დომენი",
            "effective_complexity": "0 არჩევითი მდგომარეობითი თავისუფლება",
            "scale_class": "უნივერსალური თეორემის დომენში",
        },
        "deterministic_rule": {
            "source": "S->S ყველა შესაძლო ფუნქციის სრული კლასი",
            "range": "singleton-ზე ზუსტად ერთი ფუნქცია",
            "scope": "დეტერმინისტული ქვეკარიბჭე",
            "effective_complexity": "0 თავისუფალი არჩევანი",
            "scale_class": "უნივერსალური თეორემის დომენში",
        },
        "stochastic_kernel": {
            "source": "ყველა 1x1 ნორმირებული მარკოვის ბირთვი",
            "range": "ზუსტად [1]",
            "scope": "სტოქასტიკური ქვეკარიბჭე",
            "effective_complexity": "0 თავისუფალი ალბათური პარამეტრი",
            "scale_class": "უნივერსალური თეორემის დომენში",
        },
        "variational_value_E": {
            "source": "ნებისმიერი რეალური ფუნქციის ერთადერთი მნიშვნელობა",
            "range": "E in R",
            "scope": "მტკიცების დამხმარე სიმბოლო; ტოტების რაოდენობას არ ცვლის",
            "effective_complexity": "ერთი შეუსაბამო საერთო მნიშვნელობა; განსხვავების თავისუფლება 0",
            "scale_class": "უნივერსალური მტკიცების დამხმარე",
        },
        "quantum_phases_theta_phi": {
            "source": "ერთგანზომილებიანი ნორმირებული ვექტორების პარამეტრიზაცია",
            "range": "theta,phi in R",
            "scope": "მტკიცების დამხმარე გლობალური ფაზები",
            "effective_complexity": "0 ფიზიკური თავისუფლება სხივებზე გადასვლის შემდეგ",
            "scale_class": "უნივერსალური მტკიცების დამხმარე",
        },
        "quantum_density_channel_and_measurement_weights": {
            "source": "ზოგადი 1x1 density/CPTP კლასი და ორშედეგიანი POVM კონტროლი",
            "range": "rho=1; channel scale=1; outcome weights დადებითია და ჯამი 1",
            "scope": "შინაგანი კვანტური მდგომარეობისა და გარე outcome-register-ის გამიჯვნა",
            "effective_complexity": "0 შინაგანი თავისუფლება; outcome alphabet დამატებითი რეესტრია",
            "scale_class": "უნივერსალური მტკიცების დამხმარე",
        },
        "two_state_control": {
            "source": "წინასწარ გამოცხადებული დადებითი კონტროლი, საბაზო დომენის გარეთ",
            "range": "ზუსტად ორი მდგომარეობა",
            "scope": "მხოლოდ დეტექტორის მგრძნობელობის შემოწმება",
            "effective_complexity": "ერთი დამატებული ბინარული განსხვავება; RefG-ის პრიმიტივი არაა",
            "scale_class": "უნივერსალური მხოლოდ საკონტროლო მოდელში",
        },
        "data_fitted_parameters": {
            "source": "N/A — მონაცემი არ გამოიყენება",
            "range": "ზუსტად 0",
            "scope": "მთელი თეორემა",
            "effective_complexity": "0",
            "scale_class": "მონაცემობრივი",
        },
    },
    "DEPENDENCIES": [
        f"{PROGRAM_CONTRACT}: პროგრამული საზღვრების PASS; ფიზიკური კარიბჭეები ღიაა.",
        "w2_01: სათამაშო Landau დადებითი კონტროლი; W2_F1 ღიაა.",
        "p03i/p03j: მხოლოდ მიმდინარე ხიდის ღია სტატუსის მტკიცებულება; მათი ფორმულები აქ არ გამოიყენება.",
        "p01_core: გამორიცხულია როგორც ფუძის მტკიცება, რადგან უკვე სივრცე-დროით ეფექტურ ფენაზე მუშაობს.",
    ],
    "METHOD": (
        "singleton-ზე ყველა დეტერმინისტული ფუნქციის სრული ჩამოთვლა; 1x1 "
        "სტოქასტიკური ნორმირების ზუსტი ამოხსნა; quotient-ის პირდაპირი დათვლა; "
        "ერთგანზომილებიანი density matrix-ისა და CPTP-არხის უნიკალურობა; POVM/"
        "output-register გამიჯვნა; ძლიერი და სუსტი ორშტატიანი დადებითი კონტროლები."
    ),
    "PASS_CONDITION": [
        "singleton-ზე ყველა f:S->S-ის გამოსახულების კარდინალობა ზუსტად 1-ია.",
        "ერთადერთი 1x1 ნორმირებული სტოქასტიკური ბირთვია [1] და მდგომარეობას არ ცვლის; მრავალნიშნა output alphabet დამატებით რეესტრად ვლინდება.",
        "ნებისმიერ singleton-ფუნქციონალს მხოლოდ ერთი მნიშვნელობა და ერთი მინიმიზატორი აქვს.",
        "ერთადერთი 1D density matrix არის [1], ყველა შინაგანი CPTP არხი მას უცვლელად ტოვებს და ნებისმიერი ორი სხივის trace distance=0.",
        "მრავალშედეგიანი 1D POVM ქმნის მხოლოდ გარე outcome-label-ს; ყოველი პირობითი შინაგანი post-state კვლავ [1]-ია.",
        "ორშტატიანი დადებითი კონტროლი განსხვავებას სწორად ავლენს.",
        "სუსტი დადებითი კონტროლი 0<distance<1 განსხვავებასაც სწორად ავლენს.",
        "singleton-ის გარე ნიშნით გაორმაგება სწორად უარყოფილია როგორც დამატებული მდგომარეობათა სივრცე.",
        "ორშტატიანი კონტროლის სახელების გადანაცვლება განსხვავების ინვარიანტებს არ ცვლის.",
    ],
    "FAIL_CONDITION": (
        "დაშვებების უცვლელად დატოვებისას რომელიმე ქვეკლასში ორი არაეკვივალენტური "
        "მდგომარეობა ჩნდება, ან კონტროლი ვერ არჩევს შინაგან ორ მდგომარეობას გარედან "
        "დამატებული outcome-label/register-ისგან."
    ),
    "FALSIFIER": (
        "კონკრეტული კონტრმაგალითი იმავე ფიქსირებულ S={omega}-ზე, რომელიც არც "
        "მდგომარეობათა სივრცეს აფართოებს, არც გარე outcome-register-ს ამატებს და მაინც ქმნის "
        "ორ ოპერაციულად არაეკვივალენტურ მდგომარეობას."
    ),
    "RESIDUAL": "ყველა ალგებრული/მატრიცული ნაშთი ზუსტად 0; ყველა singleton კლასის რაოდენობა ზუსტად 1.",
    "ERROR_BOUND": "0 — სრული სასრული ჩამოთვლა და ზუსტი სიმბოლური ალგებრა.",
    "VALIDITY_HEALTH": (
        "ეს არის პირობითი ლოგიკურ-მათემატიკური no-go. იგი არ იყენებს სივრცეს, "
        "დროს, მეტრიკას, წნევას ან დაკვირვებით მონაცემს და არ აცხადებს, რომ RefG-ის "
        "ერთი ფუძე აუცილებლად მკაცრი singleton-ია."
    ),
    "BRANCHES": {
        "strict_singleton_deterministic": "no-go",
        "strict_singleton_stochastic": "no-go",
        "strict_singleton_variational": "no-go",
        "strict_singleton_quantum_1D": "no-go",
        "one_carrier_nontrivial_self_relations": "დასაშვები escape; ჯერ ღია კანდიდატი",
        "state_space_expanding_rule": "დასაშვები escape, მაგრამ დამატებული გენერაციული პრიმიტივი",
        "external_label_or_noise": "უარყოფილი როგორც ფუძის შინაგანი თვითგარჩევის მტკიცება",
    },
    "OBSERVABLE_MAP": (
        "ფიზიკური დაკვირვებადი: N/A. შიდა ლოგიკური დიაგნოსტიკაა D=|S/~|, "
        "ოპერაციულად არაეკვივალენტური კლასების რაოდენობა."
    ),
    "FORWARD_MODEL": "N/A — ფიზიკურ მონაცემამდე რუკა ამ პირობით თეორემას არ აქვს.",
    "DATA_ROLE": "N/A — მონაცემი არც მორგებისთვის, არც ვალიდაციისთვის და არც პროგნოზისთვის გამოიყენება.",
    "IDENTIFIABILITY": (
        "მეთოდია ზუსტი კარდინალობა, მარკოვის ბირთვის რანგი და კვანტური trace distance; "
        "ზღურბლია ზუსტად D>=2 ან distance>0. singleton-ზე D=1 და distance=0; "
        "სუსტი კონტროლი ამოწმებს მკაცრად შუალედურ 0<distance<1 შემთხვევას."
    ),
    "BENCHMARK": (
        "ნულოვანი შემთხვევაა singleton; ძლიერი დადებითი კონტროლია ორი მდგომარეობა "
        "distance=1-ით; სუსტი კონტროლია 0<distance<1; წინასწარ ჩაშენებული შემთხვევაა "
        "omega-სთვის გარე ნიშნის ან POVM outcome-register-ის მიწებება. მეტრიკა ზუსტია და ტოლერანტობა 0."
    ),
    "PRIMITIVE_REGISTRY": {
        "1_objects_and_state_space": "ერთი აბსტრაქტული მდგომარეობა S={omega}.",
        "2_primitive_relations": "მხოლოდ ტოლობა; არატრივიალური თვითრელაცია არ არის.",
        "3_symmetry_and_equivalence": "singleton-ის ავტომორფიზმი ტრივიალურია; კვანტურში გლობალური ფაზა კალიბრულია.",
        "4_rule": "ფიქსირებული დომენის deterministic/stochastic/variational/1D-quantum კლასები; variational map S->R ენდომორფიზმად არ იწოდება.",
        "5_free_parameters": "ფიზიკური პარამეტრი 0; E და ფაზები მხოლოდ მტკიცების დამხმარეა.",
        "6_initial_and_boundary_conditions": "N/A — სივრცითი საზღვარი ან ფიზიკური ევოლუცია არ გამოიყენება.",
        "7_randomness": "1x1 შინაგანი სტოქასტიკური ბირთვი უნიკალურია; მრავალნიშნა output alphabet ცალკე გარე რეესტრია.",
        "8_computational_index": "სასრული ჩამოთვლის ინდექსი მხოლოდ პროგრამულია და ფიზიკურ დროს არ აღნიშნავს.",
        "9_validity_and_limits": "ფიქსირებული singleton; state-space-changing წესები დომენის გარეთაა.",
        "10_imported_not_derived": "singleton წაკითხვა პირობითადაა შეტანილი; თეორემა არ ამტკიცებს, რომ ეს RefG-ის აუცილებელი ონტოლოგიაა.",
    },
    "METRIC_ROUTE": "N/A — მეტრიკა, მიზეზობრივი რიგი და განზომილება ამ F1 no-go-ში არ განისაზღვრება.",
    "CONTROL_REGISTRY": {
        "positive": "ორი ნამდვილი მდგომარეობა detector-მა უნდა გაარჩიოს როგორც distance=1, ისე 0<distance<1 შემთხვევაში",
        "null": "strict singleton არცერთ დაშვებულ ქვეკლასში არ უნდა გაიყოს",
        "prewired": "გარე ბინარული ნიშანი, stochastic output ან POVM outcome უნდა გამოვლინდეს როგორც დამატებითი register/codomain",
        "scrambled": "ორი მდგომარეობის სახელების swap-მა ინვარიანტები არ უნდა შეცვალოს",
        "robustness": "singleton-ის ყველა deterministic map, სრული 1x1 stochastic/density/CPTP კლასი და outcome-register ხვრელი მოწმდება",
        "second_algebraic_derivation": "quotient |S/~|=1 პირდაპირ ითვლება და მისგან დამოუკიდებლად მოწმდება rank/trace-distance წარმოდგენები",
    },
    "COMPUTATIONAL_INDEX_ROLE": "მხოლოდ სასრული ჩამოთვლა; ფიზიკური დრო, რიგი ან ევოლუცია არაა.",
    "OLD_WORK_LEDGER": (
        "p03i და p03j ადასტურებს მხოლოდ emergence-map-ის ღია სტატუსს; p01 უკვე "
        "ეფექტურ სივრცე-დროით ცვლადებს იყენებს. არცერთი ძველი PASS ამ თეორემაში არ გადმოდის."
    ),
    "GATE_APPLICABILITY": {
        "G0_GOAL": "REQUIRED — claim/type/domain/PASS/FAIL წინასწარ ფიქსირდება",
        "G1_CONVENTIONS": "REQUIRED — singleton, ინდექსი, ეკვივალენტობა და გარე register-ის საზღვარი",
        "G2_CORE_ALGEBRA": "REQUIRED — cardinality, Markov, density/CPTP და trace residuals",
        "G3_STRUCTURE": "REQUIRED — quotient-ის ერთადერთობა და no-go-ს ზუსტი scope",
        "G4_INDEPENDENT_CHECK": "REQUIRED — quotient გზა vs map/rank/trace-distance გზები",
        "G5_LIMITS_REGRESSION": "REQUIRED — ორი-state ძლიერი/სუსტი, relabel და external-register controls",
        "G6_PHYSICAL_MATCH": "N/A — თეორემა ფიზიკურ წყაროს, მუხტს ან observable map-ს არ აცხადებს",
        "G7_OBSERVATION": "N/A — დაკვირვებითი მტკიცება და მონაცემი არ არსებობს",
        "G8_EXPORT": "N/A — შიდა Git-ignored კვლევითი gate; Canon/სტატიაში ექსპორტი არაა ავტორიზებული",
    },
    "CLOSURE_FLAGS": {
        "G0_GOAL": False,
        "G1_CONVENTIONS": False,
        "G2_CORE_ALGEBRA": False,
        "G3_STRUCTURE": False,
        "G4_INDEPENDENT_CHECK": False,
        "G5_LIMITS_REGRESSION": False,
        "G6_PHYSICAL_MATCH": False,
        "G7_OBSERVATION": False,
        "G8_EXPORT": False,
        "strict_singleton_no_go": False,
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
        "პირველი გზა პირდაპირ ითვლის singleton-ის ყველა ეკვივალენტობის მიმართებასა "
        "და quotient-ს. მისგან დამოუკიდებელი წარმოდგენებია ფუნქციების სრული ჩამოთვლა, "
        "მარკოვის ნორმირება და 1D density/CPTP/trace-distance ალგებრა; საერთო დაშვებაა მხოლოდ S={omega}."
    ),
    "PROVENANCE": (
        "2026-07-21; კოდის, W2-C0-ის, w2_01-ის, CODES.md-ის, Canon-ის, ქართული "
        "ინტუიციური ფაილისა და გამოყენებული ძველი guard-ფაილების SHA-256 გაშვებისას "
        "იბეჭდება; არტეფაქტია stdout JSON ანგარიში."
    ),
    "FILES": [
        "CODES.md",
        "Theory_Canon.md",
        "intuitive/RefG_GE.md",
        "RefG/work/p01_core.py",
        "RefG/work/p03i_full_forest_to_einstein_bridge_theorem.py",
        "RefG/work/p03j_order_volume_forest_to_metric_bridge_gate.py",
        "RefG/work 2/w2_00_foundation_to_einstein_contract.md",
        "RefG/work 2/w2_01_self_differentiation_candidate_gate.py",
        "RefG/work 2/w2_02_f1_singleton_no_go_gate.py",
    ],
}


def _is_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def _matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(_is_zero(entry) for entry in matrix)


def _all_functions(size: int) -> list[tuple[int, ...]]:
    """აბრუნებს {0,...,size-1}-დან საკუთარ თავში ყველა ფუნქციას."""

    return list(itertools.product(range(size), repeat=size))


def _image_size(function: tuple[int, ...]) -> int:
    return len(set(function))


def _equivalence_relations(size: int) -> list[frozenset[tuple[int, int]]]:
    """სრულად ჩამოთვლის სასრულ სიმრავლეზე ყველა ეკვივალენტობის მიმართებას."""

    pairs = tuple(itertools.product(range(size), repeat=2))
    relations: list[frozenset[tuple[int, int]]] = []
    for mask in itertools.product((False, True), repeat=len(pairs)):
        relation = frozenset(pair for pair, keep in zip(pairs, mask) if keep)
        reflexive = all((item, item) in relation for item in range(size))
        symmetric = all((right, left) in relation for left, right in relation)
        transitive = all(
            (left, end) in relation
            for left, middle in relation
            for start, end in relation
            if middle == start
        )
        if reflexive and symmetric and transitive:
            relations.append(relation)
    return relations


def _quotient_class_count(size: int, relation: frozenset[tuple[int, int]]) -> int:
    classes = {
        frozenset(right for right in range(size) if (left, right) in relation)
        for left in range(size)
    }
    return len(classes)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_gate() -> dict[str, Any]:
    """ასრულებს პირობით singleton no-go-ს და წინასწარ გამოცხადებულ კონტროლებს."""

    required_contract_fields = {
        "CLAIM_ID", "CLAIM", "TYPE", "MODEL_VERSION", "ASSUMPTIONS",
        "DOMAIN", "CONVENTIONS", "FREEDOM_LEDGER", "DEPENDENCIES", "METHOD",
        "PASS_CONDITION", "FAIL_CONDITION", "FALSIFIER", "RESIDUAL",
        "ERROR_BOUND", "VALIDITY_HEALTH", "BRANCHES", "OBSERVABLE_MAP",
        "FORWARD_MODEL", "DATA_ROLE", "IDENTIFIABILITY", "BENCHMARK",
        "CLOSURE_FLAGS", "CROSSCHECK", "PROVENANCE", "FILES",
        "PRIMITIVE_REGISTRY", "METRIC_ROUTE", "CONTROL_REGISTRY",
        "COMPUTATIONAL_INDEX_ROLE", "OLD_WORK_LEDGER", "GATE_APPLICABILITY",
    }
    required_primitive_entries = {
        "1_objects_and_state_space", "2_primitive_relations",
        "3_symmetry_and_equivalence", "4_rule", "5_free_parameters",
        "6_initial_and_boundary_conditions", "7_randomness",
        "8_computational_index", "9_validity_and_limits",
        "10_imported_not_derived",
    }
    required_controls = {
        "positive", "null", "prewired", "scrambled", "robustness",
        "second_algebraic_derivation",
    }
    required_universal_gates = {
        "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
        "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
        "G7_OBSERVATION", "G8_EXPORT",
    }
    required_ledger_fields = {
        "source", "range", "scope", "effective_complexity", "scale_class"
    }
    required_freedom_slots = {
        "singleton_state", "deterministic_rule", "stochastic_kernel",
        "variational_value_E", "quantum_phases_theta_phi",
        "quantum_density_channel_and_measurement_weights",
        "two_state_control", "data_fitted_parameters",
    }
    required_closure_flags = {
        "G0_GOAL", "G1_CONVENTIONS", "G2_CORE_ALGEBRA", "G3_STRUCTURE",
        "G4_INDEPENDENT_CHECK", "G5_LIMITS_REGRESSION", "G6_PHYSICAL_MATCH",
        "G7_OBSERVATION", "G8_EXPORT", "strict_singleton_no_go",
        "W2_F1_SELF_DIFFERENTIATION", "W2_F2_OPERATIONAL_RELATIONS",
        "W2_F3_INTERNAL_ORDER_CAUSALITY", "W2_F4_INDEPENDENT_ADDITIVE_MODES",
        "W2_M1_DIMENSION_CONTINUUM", "W2_M2_LORENTZIAN_METRIC",
        "W2_A0_EFFECTIVE_ACTION_ORIGIN", "W2_A1_ACTION_VARIATION",
        "W2_A2_CONSERVATION_NO_DOUBLE_COUNT", "W2_A3_DOF_HEALTH",
        "W2_A4_UNIVERSAL_MATTER_METRIC", "W2_E1_REDUCED_ACTION_MATCHING",
        "W2_E2_EXACT_EINSTEIN_BRANCH", "W2_E3_SOURCE_WORLDTUBE_MATCHING",
        "W2_L1_WEAK_SOURCE_PN_PPN_HANDOFF", "W2_L2_COMPACT_SOURCE_EIH_HANDOFF",
    }
    required_branches = {
        "strict_singleton_deterministic": "no-go",
        "strict_singleton_stochastic": "no-go",
        "strict_singleton_variational": "no-go",
        "strict_singleton_quantum_1D": "no-go",
        "one_carrier_nontrivial_self_relations": "დასაშვები escape; ჯერ ღია კანდიდატი",
        "state_space_expanding_rule": "დასაშვები escape, მაგრამ დამატებული გენერაციული პრიმიტივი",
        "external_label_or_noise": "უარყოფილი როგორც ფუძის შინაგანი თვითგარჩევის მტკიცება",
    }
    version_contract_bound = (
        isinstance(CLAIM_CONTRACT.get("MODEL_VERSION"), str)
        and CLAIM_CONTRACT["MODEL_VERSION"].startswith(f"{MODEL_VERSION};")
    )
    contract_values_nonempty = all(
        value.strip() if isinstance(value, str) else bool(value)
        for value in (CLAIM_CONTRACT.get(key) for key in required_contract_fields)
    )
    text_sequences_valid = all(
        isinstance(CLAIM_CONTRACT.get(key), (list, tuple))
        and bool(CLAIM_CONTRACT[key])
        and all(isinstance(item, str) and item.strip() for item in CLAIM_CONTRACT[key])
        for key in ("ASSUMPTIONS", "DEPENDENCIES", "PASS_CONDITION", "FILES")
    )
    registry_values_nonblank = all(
        isinstance(value, str) and bool(value.strip())
        for registry_name in (
            "PRIMITIVE_REGISTRY", "CONTROL_REGISTRY", "GATE_APPLICABILITY"
        )
        for value in CLAIM_CONTRACT[registry_name].values()
    )
    g0_goal_pass = (
        required_contract_fields.issubset(CLAIM_CONTRACT)
        and contract_values_nonempty
        and text_sequences_valid
        and version_contract_bound
        and CLAIM_CONTRACT["TYPE"].startswith("CONDITIONAL / EXACT_IDENTITY")
        and bool(CLAIM_CONTRACT["PASS_CONDITION"])
        and bool(CLAIM_CONTRACT["FAIL_CONDITION"])
        and bool(CLAIM_CONTRACT["FALSIFIER"])
    )
    conventions_pass = (
        g0_goal_pass
        and set(CLAIM_CONTRACT["PRIMITIVE_REGISTRY"]) == required_primitive_entries
        and set(CLAIM_CONTRACT["CONTROL_REGISTRY"]) == required_controls
        and set(CLAIM_CONTRACT["GATE_APPLICABILITY"]) == required_universal_gates
        and registry_values_nonblank
        and CLAIM_CONTRACT["BRANCHES"] == required_branches
        and set(CLAIM_CONTRACT["FREEDOM_LEDGER"]) == required_freedom_slots
        and all(
            isinstance(entry, dict)
            and set(entry) == required_ledger_fields
            and all(
                value is not None
                and (not isinstance(value, str) or bool(value.strip()))
                for value in entry.values()
            )
            for entry in CLAIM_CONTRACT["FREEDOM_LEDGER"].values()
        )
        and CLAIM_CONTRACT["METRIC_ROUTE"].startswith("N/A")
        and "ფიზიკური დრო" in CLAIM_CONTRACT["COMPUTATIONAL_INDEX_ROLE"]
        and "არცერთი ძველი PASS" in CLAIM_CONTRACT["OLD_WORK_LEDGER"]
        and "გამომავალი კლასიკური რეესტრი" in CLAIM_CONTRACT["DOMAIN"]
        and set(CLAIM_CONTRACT["CLOSURE_FLAGS"]) == required_closure_flags
        and all(
            isinstance(value, bool) and value is False
            for value in CLAIM_CONTRACT["CLOSURE_FLAGS"].values()
        )
    )

    singleton_equivalence_relations = _equivalence_relations(1)
    singleton_quotient_counts = [
        _quotient_class_count(1, relation)
        for relation in singleton_equivalence_relations
    ]
    quotient_independent_pass = (
        singleton_equivalence_relations == [frozenset({(0, 0)})]
        and singleton_quotient_counts == [1]
    )

    singleton_functions = _all_functions(1)
    deterministic_pass = (
        singleton_functions == [(0,)]
        and all(_image_size(function) == 1 for function in singleton_functions)
    )

    kernel_entry = sp.symbols("k", real=True, nonnegative=True)
    normalized_kernel_solution = sp.solve(sp.Eq(kernel_entry, 1), kernel_entry)
    singleton_kernel = sp.Matrix([[normalized_kernel_solution[0]]])
    singleton_probability = sp.Matrix([1])
    stochastic_residual = sp.simplify(singleton_kernel * singleton_probability - singleton_probability)
    stochastic_pass = (
        normalized_kernel_solution == [1]
        and singleton_kernel.rank() == 1
        and _matrix_is_zero(stochastic_residual)
    )

    energy = sp.symbols("E", real=True)
    singleton_states = (0,)
    singleton_energy_map = {state: energy for state in singleton_states}
    singleton_function_image = set(singleton_energy_map.values())
    singleton_minimizers = tuple(singleton_states)
    variational_pass = len(singleton_function_image) == 1 and len(singleton_minimizers) == 1

    # სრული 1x1 კვანტური კლასი: density matrix და შინაგანი CPTP არხი უნიკალურია.
    density_entry = sp.symbols("rho", real=True, nonnegative=True)
    density_solution = sp.solve(sp.Eq(density_entry, 1), density_entry)
    general_density = sp.Matrix([[density_solution[0]]])
    channel_scale = sp.symbols("channel_scale", real=True, nonnegative=True)
    channel_solution = sp.solve(sp.Eq(channel_scale, 1), channel_scale)
    channel_output = sp.simplify(channel_solution[0] * general_density)
    channel_residual = sp.simplify(channel_output - general_density)
    density_cptp_pass = (
        density_solution == [1]
        and channel_solution == [1]
        and general_density == sp.Matrix([[1]])
        and _matrix_is_zero(channel_residual)
    )

    # წმინდა სხივების დამოუკიდებელი სპეციალიზაცია: გლობალური ფაზა უქმდება.
    theta, phi = sp.symbols("theta phi", real=True)
    psi_theta = sp.Matrix([sp.exp(sp.I * theta)])
    psi_phi = sp.Matrix([sp.exp(sp.I * phi)])
    rho_theta = sp.simplify(psi_theta * psi_theta.conjugate().T)
    rho_phi = sp.simplify(psi_phi * psi_phi.conjugate().T)
    quantum_density_residual = sp.simplify(rho_theta - rho_phi)
    quantum_trace_distance = sp.simplify(sp.Abs(quantum_density_residual[0, 0]) / 2)
    quantum_ray_pass = (
        rho_theta == sp.Matrix([[1]])
        and rho_phi == sp.Matrix([[1]])
        and _matrix_is_zero(quantum_density_residual)
        and quantum_trace_distance == 0
    )

    # მრავალშედეგიანი POVM შესაძლებელია, მაგრამ outcome alphabet/register დამატებითი
    # კლასიკური სისტემაა; თითოეული პირობითი შინაგანი post-state კვლავ [1]-ია.
    outcome_ratio = sp.symbols("outcome_ratio", positive=True)
    outcome_weight_0 = sp.simplify(outcome_ratio / (1 + outcome_ratio))
    outcome_weight_1 = sp.simplify(1 / (1 + outcome_ratio))
    povm_effect_0 = sp.Matrix([[outcome_weight_0]])
    povm_effect_1 = sp.Matrix([[outcome_weight_1]])
    povm_completeness_residual = sp.simplify(
        povm_effect_0 + povm_effect_1 - sp.eye(1)
    )
    post_state_0 = sp.simplify(
        outcome_weight_0 * general_density / outcome_weight_0
    )
    post_state_1 = sp.simplify(
        outcome_weight_1 * general_density / outcome_weight_1
    )
    quantum_outcome_register = ("outcome_0", "outcome_1")
    povm_register_pass = (
        outcome_weight_0.is_positive is True
        and outcome_weight_1.is_positive is True
        and _matrix_is_zero(povm_completeness_residual)
        and post_state_0 == sp.Matrix([[1]])
        and post_state_1 == sp.Matrix([[1]])
        and len(quantum_outcome_register) == 2
    )

    # იგივე საზღვარი კლასიკურ ენაში: S->Y გამოსავალი Y-ს დამატებით codomain-ად ითხოვს.
    stochastic_output_distribution = sp.Matrix(
        [outcome_weight_0, outcome_weight_1]
    )
    stochastic_output_normalization_residual = sp.simplify(
        sum(stochastic_output_distribution) - 1
    )
    stochastic_output_register = ("label_0", "label_1")
    stochastic_register_pass = (
        _is_zero(stochastic_output_normalization_residual)
        and len(stochastic_output_register) == 2
        and singleton_kernel == sp.Matrix([[1]])
        and singleton_probability == sp.Matrix([1])
    )

    quantum_pass = density_cptp_pass and quantum_ray_pass and povm_register_pass

    # დადებითი კონტროლი: ორი ნამდვილი მდგომარეობა ყველა შესაბამის დიაგნოსტიკაში ჩანს.
    two_state_identity = (0, 1)
    two_state_image_size = _image_size(two_state_identity)
    p0 = sp.Matrix([1, 0])
    p1 = sp.Matrix([0, 1])
    classical_total_variation = sp.simplify(sum(abs(entry) for entry in (p0 - p1)) / 2)
    rho0 = sp.diag(1, 0)
    rho1 = sp.diag(0, 1)
    two_state_density_difference = rho0 - rho1
    quantum_two_state_trace_distance = sp.simplify(
        sum(
            sp.Abs(eigenvalue) * multiplicity
            for eigenvalue, multiplicity in two_state_density_difference.eigenvals().items()
        )
        / 2
    )
    positive_control_pass = (
        two_state_image_size == 2
        and classical_total_variation == 1
        and quantum_two_state_trace_distance == 1
        and rho0 != rho1
    )

    # სუსტი დადებითი კონტროლი ამოწმებს ზუსტ ზღურბლს 0<distance<1.
    weak_classical_0 = sp.Matrix([sp.Rational(3, 4), sp.Rational(1, 4)])
    weak_classical_1 = sp.Matrix([sp.Rational(1, 4), sp.Rational(3, 4)])
    weak_classical_distance = sp.simplify(
        sum(abs(entry) for entry in (weak_classical_0 - weak_classical_1)) / 2
    )
    ket_zero = sp.Matrix([1, 0])
    ket_plus = sp.Matrix([1, 1]) / sp.sqrt(2)
    weak_rho_0 = sp.simplify(ket_zero * ket_zero.conjugate().T)
    weak_rho_1 = sp.simplify(ket_plus * ket_plus.conjugate().T)
    weak_density_difference = sp.simplify(weak_rho_0 - weak_rho_1)
    weak_quantum_distance = sp.simplify(
        sum(
            sp.Abs(eigenvalue) * multiplicity
            for eigenvalue, multiplicity in weak_density_difference.eigenvals().items()
        )
        / 2
    )
    weak_positive_control_pass = (
        weak_classical_distance == sp.Rational(1, 2)
        and weak_classical_distance.is_positive is True
        and (1 - weak_classical_distance).is_positive is True
        and weak_quantum_distance == sp.sqrt(2) / 2
        and weak_quantum_distance.is_positive is True
        and (1 - weak_quantum_distance).is_positive is True
    )

    # სახელების swap არ ცვლის განსხვავების არც კარდინალობას და არც მანძილს.
    swap = sp.Matrix([[0, 1], [1, 0]])
    swapped_p0 = swap * p0
    swapped_p1 = swap * p1
    swapped_total_variation = sp.simplify(
        sum(abs(entry) for entry in (swapped_p0 - swapped_p1)) / 2
    )
    relabel_pass = (
        swap.T * swap == sp.eye(2)
        and swapped_total_variation == classical_total_variation
        and {tuple(swapped_p0), tuple(swapped_p1)} == {tuple(p0), tuple(p1)}
    )

    # გარე ბინარული დეკორაცია რეალურად Sx{0,1}-ს ქმნის და singleton აღარ არის.
    externally_decorated_states = {(0, "left"), (0, "right")}
    prewired_injection_detected = len(externally_decorated_states) == 2
    prewired_control_rejected = (
        prewired_injection_detected
        and stochastic_register_pass
        and povm_register_pass
        and post_state_0 == post_state_1 == general_density
    )

    g2_core_algebra_pass = all(
        [deterministic_pass, stochastic_pass, variational_pass, quantum_pass]
    )
    g3_structure_pass = quotient_independent_pass and g2_core_algebra_pass
    g4_independent_check_pass = (
        quotient_independent_pass
        and deterministic_pass
        and stochastic_pass
        and quantum_pass
    )
    g5_limits_regression_pass = all(
        [
            positive_control_pass,
            weak_positive_control_pass,
            relabel_pass,
            prewired_control_rejected,
        ]
    )

    strict_singleton_no_go_pass = all(
        [
            g0_goal_pass,
            conventions_pass,
            g2_core_algebra_pass,
            g3_structure_pass,
            g4_independent_check_pass,
            g5_limits_regression_pass,
        ]
    )

    closure_flags = dict(CLAIM_CONTRACT["CLOSURE_FLAGS"])
    closure_flags["G0_GOAL"] = g0_goal_pass
    closure_flags["G1_CONVENTIONS"] = conventions_pass
    closure_flags["G2_CORE_ALGEBRA"] = g2_core_algebra_pass
    closure_flags["G3_STRUCTURE"] = g3_structure_pass
    closure_flags["G4_INDEPENDENT_CHECK"] = g4_independent_check_pass
    closure_flags["G5_LIMITS_REGRESSION"] = g5_limits_regression_pass
    closure_flags["strict_singleton_no_go"] = strict_singleton_no_go_pass

    source_path = Path(__file__).resolve()
    root = source_path.parents[2]
    dependency_paths = {
        "codes": root / "CODES.md",
        "theory_canon": root / "Theory_Canon.md",
        "intuitive_ge": root / "intuitive" / "RefG_GE.md",
        "p01_core": root / "RefG" / "work" / "p01_core.py",
        "p03i_bridge": root / "RefG" / "work" / "p03i_full_forest_to_einstein_bridge_theorem.py",
        "p03j_bridge": root / "RefG" / "work" / "p03j_order_volume_forest_to_metric_bridge_gate.py",
        "program_contract": source_path.with_name("w2_00_foundation_to_einstein_contract.md"),
        "w2_01": source_path.with_name("w2_01_self_differentiation_candidate_gate.py"),
    }

    return {
        "claim_id": CLAIM_CONTRACT["CLAIM_ID"],
        "model_version": MODEL_VERSION,
        "program_contract": PROGRAM_CONTRACT,
        "status": (
            "EXACT_SINGLETON_NO_GO_PASS__W2_F1_OPEN"
            if strict_singleton_no_go_pass
            else "EXACT_SINGLETON_NO_GO_FAIL__W2_F1_OPEN"
        ),
        "strict_singleton_no_go_pass": strict_singleton_no_go_pass,
        "refg_W2_F1_closed": False,
        "scope_ceiling": "CONDITIONAL_STRICT_SINGLETON_NO_GO_ONLY",
        "theory_consequence": (
            "RefG-ის ერთი ფუძე არ უნდა განიმარტოს როგორც შესაძლებლობების არმქონე "
            "ერთი მდგომარეობა. ეს no-go არ ირჩევს ერთ კონკრეტულ escape-არქიტექტურას: "
            "შემდეგ კანდიდატს შეიძლება ჰქონდეს არატრივიალური არაიარლიყიანი შესაძლებლობათა "
            "სივრცე, გენერაციული წესი, სტოქასტიკური/კვანტური outcome ან სხვა მკაფიო "
            "target-free მექანიზმი, მაგრამ განსხვავება შედეგში უნდა წარმოიქმნას."
        ),
        "checks": {
            "required_contract_values_nonempty": contract_values_nonempty,
            "required_text_sequences_valid": text_sequences_valid,
            "registry_values_nonblank": registry_values_nonblank,
            "contract_and_runtime_model_versions_bound": version_contract_bound,
            "G0_goal_contract_complete": g0_goal_pass,
            "G1_conventions_and_ledgers_complete": conventions_pass,
            "independent_singleton_quotient_count_is_one": quotient_independent_pass,
            "all_singleton_deterministic_maps_no_distinction": deterministic_pass,
            "unique_normalized_1x1_stochastic_kernel": stochastic_pass,
            "stochastic_multi_label_output_requires_extra_register": stochastic_register_pass,
            "singleton_variational_image_and_minimizer_unique": variational_pass,
            "unique_one_dimensional_density_and_CPTP_channel": density_cptp_pass,
            "one_dimensional_quantum_rays_indistinguishable": quantum_ray_pass,
            "POVM_outputs_external_internal_post_state_unique": povm_register_pass,
            "two_state_positive_control_detected": positive_control_pass,
            "weak_positive_distance_control_detected": weak_positive_control_pass,
            "state_relabel_invariance": relabel_pass,
            "external_label_injection_rejected": prewired_control_rejected,
            "G2_core_algebra": g2_core_algebra_pass,
            "G3_structure": g3_structure_pass,
            "G4_independent_check": g4_independent_check_pass,
            "G5_limits_regression": g5_limits_regression_pass,
        },
        "exact_diagnostics": {
            "singleton_equivalence_relation_count": len(singleton_equivalence_relations),
            "singleton_quotient_class_counts": singleton_quotient_counts,
            "singleton_function_count": len(singleton_functions),
            "singleton_function_image_sizes": [
                _image_size(function) for function in singleton_functions
            ],
            "normalized_1x1_kernel": str(singleton_kernel),
            "stochastic_residual": str(stochastic_residual),
            "singleton_variational_image_size": len(singleton_function_image),
            "singleton_minimizer_count": len(singleton_minimizers),
            "quantum_density_residual": str(quantum_density_residual),
            "quantum_trace_distance": str(quantum_trace_distance),
            "general_1D_density": str(general_density),
            "CPTP_channel_residual": str(channel_residual),
            "POVM_completeness_residual": str(povm_completeness_residual),
            "POVM_conditional_post_state_0": str(post_state_0),
            "POVM_conditional_post_state_1": str(post_state_1),
            "POVM_outcome_register_size": len(quantum_outcome_register),
            "stochastic_output_normalization_residual": str(
                stochastic_output_normalization_residual
            ),
            "stochastic_output_register_size": len(stochastic_output_register),
            "two_state_image_size": two_state_image_size,
            "two_state_classical_total_variation": str(classical_total_variation),
            "two_state_quantum_trace_distance": str(quantum_two_state_trace_distance),
            "weak_classical_total_variation": str(weak_classical_distance),
            "weak_quantum_trace_distance": str(weak_quantum_distance),
            "swapped_total_variation": str(swapped_total_variation),
            "externally_decorated_state_count": len(externally_decorated_states),
        },
        "minimum_escape_ledger": {
            "recommended": (
                "NON_SINGLETON_OR_GENERATIVE_TARGET_FREE_CANDIDATE_CLASS"
            ),
            "why": (
                "ერთი ონტოლოგიური მატარებელი არ უდრის ერთ შესაძლო მდგომარეობას. "
                "თეორემა მხოლოდ strict singleton-ს გამორიცხავს და deterministic, "
                "variational, stochastic, quantum, relational ან generative გზებს ღიად ტოვებს."
            ),
            "not_yet_derived": [
                "candidate_class_and_primitive_registry",
                "selection_or_variational_rule",
                "stable_inequivalent_sectors",
                "node_imprint_relation_operational_map",
            ],
        },
        "closure_flags": closure_flags,
        "universal_gate_applicability": CLAIM_CONTRACT["GATE_APPLICABILITY"],
        "provenance": {
            "source_file": source_path.as_posix(),
            "source_sha256": _sha256(source_path),
            "dependency_sha256": {
                name: _sha256(path) for name, path in dependency_paths.items()
            },
            "sympy_version": sp.__version__,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = run_gate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["strict_singleton_no_go_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
