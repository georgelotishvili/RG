# W3-37 Preregistration: Conditional Genesis Domain Consistency

**CLAIM_ID:** `W3_37_GENESIS_DOMAIN_SEPARATION`

**CLAIM:** Under the frozen branch definitions and retained candidate DAG, the
birth parameter set is disjoint from the already-activated parameter set, the
local threshold is not identically forced to follow either activated null
characteristic, and adding G -> N while retaining the base edges makes the
declared graph cyclic. These are conditional assumption-consequences only.

**TYPE:** `EXACT_CONDITIONAL_DEFINITION_AND_GRAPH_CONSISTENCY_GATE`. This gate
does not derive Genesis, causal law, globality, centerlessness, or topology.

**MODEL_VERSION:** `W3-37-v1.1-GENESIS-DOMAINS`. Version 1.1 replaces the
overstrong v1.0 causal interpretation with an assumption-consistency claim,
tests both null branches, completes the structural freedom ledger, and adds
explicit non-identity mutations. Any change to branch definitions, candidate DAG, activated
metric, claim, or flag sets requires a new version.

**ASSUMPTIONS:**

1. The process-time origin is encoded as `t=0`, `tau(0)=0`; for `t>0`,
   `tau(t)=int_0^t p(s)ds`, where `p` is positive and continuous.
2. The birth parameter set is declared `D_B={0}` and the already-activated
   parameter set is declared `D_+=(0,infinity)`. This is temporal/parameter
   bookkeeping and says nothing about a finite spatial universe.
3. The global bookkeeping field is represented as `B(t)` with no spatial
   argument. Its zero spatial derivative is a representation consequence, not
   a derivation of globality or centerlessness.
4. A local threshold in the post-origin branch is a differentiable level set
   `Phi(R(t),t)=Phi_*` with `Phi_R!=0`; `Phi_t` may vanish.
5. The supplied already-activated metric is
   `ds^2=p^2 c0^2 dt^2-(a^2/p^2)dchi^2`, with `a,p,c0>0`.
6. No PDE relation is supplied between the local threshold and either activated
   null branch.
7. The retained candidate DAG is `B -> N -> O -> G -> P`. The gate checks this
   chosen graph; it does not derive its edges.
8. Adding `G -> N` is tested while retaining every base edge. Other causal
   models are outside this gate.

**DOMAIN:** Exact parameter sets `D_B={0}` and `D_+=(0,infinity)`; positive
continuous cadence; local post-origin threshold patches with `Phi_R!=0`; the
supplied activated metric; one finite declared DAG. No pre-origin dynamics,
spatial size, physical tail domain, or observable domain is derived.

**CONVENTIONS:** `birth` here means the declared parameter origin. `global`
and `centerless` are frozen scenario words, not outputs. `tail` is the declared
node `G` in the candidate DAG. `not identically forced` permits a future PDE or
special solution to make threshold and null speeds coincide. Signature is
`(+---)`; `c0>0`, `a>0`, `p>0`.

**FREEDOM_LEDGER:** `d_eff=0` means zero data-fitted parameters, not zero
structural freedom. Frozen entries are gate inputs and remain physically
underived; open entries are uninstantiated:

- `branch_domain_choice`: source = Genesis ontology; admissible class =
  measurable ordered parameter subsets with a declared origin; scale =
  `universal`; effective complexity = set/function choice; status =
  `FROZEN_FOR_GATE__NOT_DERIVED`.
- `candidate_dependency_graph`: source = Genesis causal hypothesis; admissible
  class = directed graphs on declared event classes; scale = `universal`;
  effective complexity = discrete edge set; status =
  `FROZEN_FOR_GATE__NOT_DERIVED`.
- `activated_metric_form`: source = structural gate choice; admissible class =
  Lorentzian post-origin metric forms; scale = `universal`; effective complexity
  = one structural form; status = `FROZEN_FOR_GATE__NOT_DERIVED`.
- `background_functions`: source = foundation action; admissible class =
  positive continuous `p(t)` and positive differentiable `a(t)`; scale =
  `universal`; effective complexity = functional/infinite-dimensional; status =
  `OPEN_UNINSTANTIATED`.
- `activation_tail_field_law`: source = activation/tail action; admissible class
  = universal differentiable field equations and characteristic laws; scale =
  `universal`; effective complexity = functional/infinite-dimensional; status =
  `OPEN_UNINSTANTIATED`.
- `mode_family_response`: source = nonlinear field solutions; admissible class
  = response/profile per mode family; scale = `group`; effective complexity =
  one functional response per family; status = `OPEN_UNINSTANTIATED`.
- `local_seed_profiles`: source = nonlinear solutions; admissible class =
  finite-energy profiles and states; scale = `object`; effective complexity =
  one functional state per object; status = `OPEN_UNINSTANTIATED`.
- `future_observable_nuisance`: source = future likelihood; admissible class =
  declared finite calibration parameters; scale = `data`; effective complexity
  = `N_nuisance=0` because no data are read; status = `OPEN_UNINSTANTIATED`.

**DEPENDENCIES:** None. The gate is self-contained and imports no upstream
result or mutable manuscript.

**METHOD:** Exact SymPy FTC/chain-rule/set/metric substitutions; both null
branches; pure-Python DAG checks; robust wrong-speed and graph mutations; exact
registered top-level keysets; strict atomic JSON and SHA-256. The method checks
assumption consequences, not physical Genesis.

**PASS_CONDITION:** FTC and origin identities hold; declared birth and activated
sets are disjoint; the differentiated level-set chain rule and both activated
null branches are exact; neither null/threshold equality is an algebraic identity without another
relation; the base DAG is acyclic; adding `G -> N` while retaining it creates a
cycle; mutations and registered top-level schemas pass; every physical flag is
false; aggregate is the AND of atomic checks.

**FAIL_CONDITION:** Any declared identity fails; the two declared parameter
sets overlap; a null/threshold identity is silently inserted; the supplied DAG
checks fail; mutation/keyset checks fail; or a physical result is reported as
derived.

**FALSIFIER:** A failure invalidates this definitional/assumption-consistency
gate only. No RefG-wide or observational falsifier is supplied.

**RESIDUAL:** Exact symbolic zero or non-identity residuals, set equality, DAG
predicates, and registered top-level keysets.

**ERROR_BOUND:** Zero algebraic error. Physical, numerical, and observational
errors are N/A because no such result is produced.

**VALIDITY_HEALTH:** Algebraic health is tested exactly. Structural freedom is
large and disclosed above. Conservation, stability, thermodynamics, physical
causality, topology, and observables are N/A because the gate supplies no action,
energy law, evolution equation, or forward model.

**BRANCHES:** `DECLARED_BIRTH_PARAMETER_SET`,
`DECLARED_ALREADY_ACTIVATED_SET`, `LOCAL_THRESHOLD_CHAIN_RULE`,
`SUPPLIED_ACTIVATED_NULL`, `RETAINED_CANDIDATE_DAG`,
`ADDED_TAIL_TO_RELATION_EDGE_MUTATION`.

**OBSERVABLE_MAP:** N/A; no spectroscopic, distance, clock, temperature, or
structure map.

**FORWARD_MODEL:** N/A; no simulated physical history or likelihood.

**DATA_ROLE:** No data are read.

**IDENTIFIABILITY:** The gate identifies only consequences of supplied set,
metric, level-set, and graph definitions. It does not identify the trigger,
globality, centerlessness, causal edges, fields, energy, topology, or stable
forms.

**BENCHMARK:** N/A as a competing-model benchmark.

**CLOSURE_FLAGS:**

Exact/computational flags, all required true:

- `finite_process_time_origin_encoded_exact`
- `elapsed_process_time_FTC_exact`
- `bookkeeping_field_has_no_spatial_argument_exact`
- `local_threshold_chain_rule_exact`
- `activated_null_branches_exact`
- `birth_activated_parameter_sets_disjoint_exact`
- `candidate_DAG_acyclic_exact`
- `added_tail_to_relation_edge_creates_cycle_exact`
- `threshold_null_identity_not_forced_exact`
- `registered_top_level_keysets_exact`
- `mutation_controls_pass`
- `aggregate_identity_pass`

Physical flags, all required false:

- `genesis_action_derived`
- `global_trigger_instability_derived`
- `initial_state_derived`
- `initial_spectrum_topology_derived`
- `order_parameter_defined`
- `phase_transition_potential_derived`
- `activation_threshold_derived`
- `activation_front_eom_derived`
- `global_centerlessness_derived`
- `foundation_energy_balance_derived`
- `energy_partition_transfer_derived`
- `candidate_DAG_edges_derived`
- `tail_propagation_law_derived`
- `mode_selection_operator_derived`
- `stable_oscillon_spectrum_derived`
- `thermal_history_derived`
- `spectroscopic_forward_model_derived`
- `CMB_BBN_structure_validated`

**CROSSCHECK:** Pointwise FTC under continuity; exact level-set chain rule; both
metric null signs; exact set intersection; independent DAG traversal; robust
factor-two null-speed mutation; wrong-sign non-identity; spatial-argument
mutation; every physical-flag flip.

**PROVENANCE:** Source pins the raw preregistration SHA-256, checks actual LF
line endings, and records source/runtime hashes, UTC, and paths. JSON is strict,
finite, sorted, LF-written, and atomically replaced with an external checksum.

**FILES:** `w3_37_genesis_domain_preregistration.md`,
`w3_37_genesis_domain_gate.py`, `w3_37_result.json`, and
`w3_37_result.sha256`.
