# RefG: conditional atemporal structural F1 proof

This directory is a self-contained symbolic supplement. It proves two exact
impossibility boundaries, verifies one conditional spectral construction, and
derives one deliberately narrow structural corollary. It does not read any
other repository file and does not use observational data.

Expected verdict:

`CONDITIONAL_ATEMPORAL_STRUCTURAL_F1_RELATIVE_TO_IMPORTED_PRIMITIVES`

## ქართული შეჯამება

ეს პაკეტი ამტკიცებს ოთხ ერთმანეთისგან მკაფიოდ გამიჯნულ შედეგს.

1. მკაცრად ერთმდგომარეობიანი დახურული სისტემა საკუთარ თავში ორ განსხვავებულ
   მდგომარეობას ან როლს ვერ წარმოქმნის. თუ მეორე იარლიყი, რეგისტრი ან სივრცე
   დავამატეთ, ეს უკვე ახალი შემოტანილი სტრუქტურაა.
2. ზუსტად სიმეტრიული მდგომარეობა ერთმნიშვნელოვანი და სიმეტრიის შემნახველი
   წესით სიმეტრიულ ფიქსირებულ სიმრავლეს ვერ ტოვებს. სიმეტრიის დამრღვევი ტოტის
   არჩევას სჭირდება სხვა მექანიზმი: გადახრა, შემთხვევითობა, მრავალმნიშვნელოვანი
   წესი ან არადროითი ფაქტორ-სივრცის სტრუქტურა.
3. ქვემოთ ჩამოთვლილი პრიმიტივების შემოტანის შემთხვევაში კვარტიკულ კანონს აქვს
   ერთი არანულოვანი გლობალური მინიმუმის კლასი სრულად გამოცხადებული
   `O(3)`-ეკვივალენტობის მიმართ. ამ მდგომარეობიდან კანონიკურად მიიღება
   ურთიერთორთოგონალური რანგი-1 და რანგი-2 პროექტორები.
4. ამიტომ, მხოლოდ შემოტანილი პრიმიტივების მიმართ, მიიღება არადროითი
   სტრუქტურული თვითგარჩევა. ეს არ არის ფუძის კანონის წარმოშობის, დროის,
   სივრცე-დროის, GR-ის ან დაკვირვებების მტკიცება.

### შემოტანილი და გამოუყვანელი დაშვებები

- ერთი აბსტრაქტული შიდა მატარებელი `Q`;
- მდგომარეობათა სივრცე `Sym₀(3,R)`;
- დადებითი შიდა შეკუმშვა და ტრანსპონირება;
- მატრიცული ნამრავლი და ალგებრული კვალი;
- სრულად გამოცხადებული ეკვივალენტობა `Q ~ R Q Rᵀ`, `R in O(3)`;
- `Q -> -Q` არ არის კალიბრული ეკვივალენტობა;
- კვარტიკული ფუნქციონალის ფორმა, ნიშნები და მეოთხე ხარისხზე შეწყვეტა;
- ღია არე `alpha>0`, `b>0`, `c>0`;
- დასაშვები მდგომარეობის არადროითი გლობალური მინიმუმის არჩევის წესი.

პაკეტი არც ერთ ამ დაშვებას RefG-ის უფრო ღრმა მექანიზმიდან გამოყვანილად არ
აცხადებს. მონაცემებზე მორგებული პარამეტრების რაოდენობა ზუსტად ნულია.

მნიშვნელოვანი ზღვარი: შემოტანილი კუბური წევრი და პირობა `b>0` თავად ირჩევს
მინიმუმის ორბიტის ფორმასა და ნიშნის ტოტს. მტკიცება მხოლოდ იმას ადგენს, რომ
კანონში წინასწარ არ არის ჩადებული კონკრეტული მიმართულება, პროექტორი,
ანიზოტროპული წყარო ან დაკვირვებით მორგებული მონაცემი.

### რას არ ამტკიცებს შედეგი

შედეგი არ ხურავს ფუძის კანონის წარმოშობას, ფუნქციონალის უნიკალურობას,
`N=3`-ის ფიზიკურ წარმოშობას, დროით ჩამოყალიბებას, ფიზიკურ კვანძებს,
ოპერაციულ ურთიერთობებს, მიზეზობრივ რიგს, დამოუკიდებელ ფიზიკურ რეჟიმებს,
სივრცეს, უწყვეტობას, ლორენცულ მეტრიკას, მოქმედებას, შენახვის კანონებს,
RefG-ის რეზონანსულ გარემოსთან რუკას, მასას, წნევას, ნაწილაკებს, GR/PN/PPN-ს
ან დაკვირვებით დადასტურებას.

### გაშვება

```text
python -m pip install -r "RefG/work 2/w2_09a_f1_proof/requirements.txt"
python "RefG/work 2/w2_09a_f1_proof/refg_f1_atemporal_structural_proof.py"
python -m unittest discover -s "RefG/work 2/w2_09a_f1_proof" -p "test_*.py" -v
```

ყველა ანგარიში ზუსტ სიმბოლურ ალგებრას იყენებს. ათწილადი მიახლოება და
რიცხვითი ცდომილების ზღვარი არ გამოიყენება.

---

## Scientific statement

### 1. Strict-singleton no-go

Let the complete closed state space be `X={x₀}`. If an allowed rule is an
endomorphism of `X` and neither enlarges the state space nor writes to a
prestructured external register, then every deterministic image is `{x₀}`.
The normalized `1 x 1` Markov kernel is `[1]`; every functional on `X` has one
state and one minimizer; every normalized one-dimensional quantum vector gives
the density matrix `[1]`, and every trace-preserving one-dimensional channel
leaves it unchanged. A many-valued measurement can add outcome labels, but its
conditional internal post-state remains `[1]`.

Therefore a literal closed singleton cannot contain two inequivalent internal
states or two nonempty state-generated roles. This theorem does **not** say
that one ontological carrier must have only one possible internal state.

### 2. Deterministic equivariant fixed-set no-go

Let a group `G` act on `X`, and let `F:X->X` be single-valued and equivariant:

```text
F(g x) = g F(x).
```

If `x` is fixed by every `g`, then

```text
g F(x) = F(g x) = F(x),
```

so `F(x)` is also fixed. More generally,
`Stab(x)` is a subgroup of `Stab(F(x))`. A unique minimizer of a
`G`-invariant functional is likewise fixed because its entire group orbit is
also minimizing.

The proof does not exclude perturbation-selected, stochastic, set-valued, or
boundary-selected outcomes. It also does not exclude a unique quotient class
that internally contains canonical roles without selecting a representative
orientation. The code independently enumerates complete three-state and
four-state `C₂` controls, a degenerate nonfixed minimum orbit, a set-valued
orbit, and a deliberately non-equivariant escape.

### 3. Conditional `Sym₀(3)` spectral construction

Import

```text
Q in Sym₀(3,R),                 Q ~ R Q Rᵀ  for every R in O(3),
I₂ = Tr(Q²),                    I₃ = Tr(Q³),
V(Q) = -alpha I₂/2 - b I₃/3 + c I₂²/4,
alpha>0, b>0, c>0.
```

A real symmetric matrix is orthogonally diagonalizable. Conjugation-invariant
polynomials are therefore symmetric eigenvalue polynomials. With `Tr(Q)=0`,
the invariant ring is generated by `I₂` and `I₃`. Cayley-Hamilton gives

```text
Q³ - I₂ Q/2 - (I₃/3) I = 0,    Tr(Q⁴) = I₂²/2.
```

Thus the complete nonconstant polynomial basis through degree four is
`I₂`, `I₃`, `I₂²`. This establishes completeness only inside the declared
polynomial, degree-four, `Sym₀(3)` class; it does not derive that truncation.

For real eigenvalues with zero sum,

```text
I₂³ - 6 I₃² = 2 product_{i<j}(lambda_i-lambda_j)² >= 0.
```

At fixed `r=sqrt(I₂)`, positive `b` selects the positive saturation
`I₃=r³/sqrt(6)`. The reduced potential is

```text
v(r) = -alpha r²/2 - b r³/(3 sqrt(6)) + c r⁴/4.
```

It is coercive and has one positive stationary radius. Equivalently, the
global-minimum set is the `O(3)` orbit of

```text
Q* = s* (n nᵀ - I/3),
s* = (b + sqrt(b² + 24 alpha c))/(4 c),
```

where `n` is any unit internal vector. Hence the quotient contains one
nonzero global-minimum class. The equality-locus calculation is explicit:
positive saturated `I₃`, together with the trace-free condition, factors the
characteristic polynomial with spectrum
`(2s*/3,-s*/3,-s*/3)`. The spectral theorem then makes every minimizer
orthogonally conjugate to the displayed representative.

The imported cubic term and the assumption `b>0` do select this orbit shape
and its sign branch. The narrower target-free statement is only that the law
is `O(3)`-invariant and contains no preferred representative direction,
projector, anisotropic source, or fitted datum.

At a diagonal representative define

```text
P₁ = I/3 + Q*/s*,               P₂ = I - P₁.
```

They are complementary orthogonal projectors with ranks one and two. Their
amplitude is intrinsic, `s*=3 I₃/I₂`, so no fixed basis projector is an input.
Orthogonal conjugation preserves rank and trace and therefore cannot exchange
the roles. At `Q=0`, a state-generated scalar idempotent is only `0` or `1`,
so the reference state has no corresponding nontrivial role. More explicitly,
equivariance makes a projector at `Q=0` commute with every orthogonal
transformation; coordinate reflections remove its off-diagonal entries and
permutations equalize its diagonal entries. It is therefore `z I`, and
idempotency leaves only `z=0` or `z=1`.

The five-dimensional Hessian splits into one radial normal mode, two biaxial
normal modes and two orbit modes. On the selected branch,

```text
lambda_radial = s*(4 c s* - b)/3 > 0,
lambda_biaxial = b s* > 0,
```

while the two orbit modes are exactly zero. This is quotient structural
stability, not temporal formation or dynamical persistence.

### 4. Conditional structural F1 corollary

Define structural F1 as intrinsic differentiation absent from the
undifferentiated reference and surviving the complete declared equivalence.
The witness may be several inequivalent accepted quotient classes, or one
accepted quotient class containing canonical, coexisting, nonexchangeable
roles. The construction above realizes the second witness.

The public decision is fail-closed:

```text
effective result = valid audit AND conjunction of every structural gate.
```

A valid one-gate failure returns `COMPLETE_NOT_PROMOTED`; malformed evidence or
an invalid audit returns `INVALID_AUDIT`, and neither can export promotion.

Strict falsifiers include a lower-energy state, a non-orbit nonpositive Hessian
direction, an omitted independent invariant through degree four, a complete
declared equivalence that exchanges the roles, a nontrivial state-generated
projector at `Q=0`, or a hidden representative direction, projector,
anisotropic source, or fitted-data term.

## Reproducibility and release boundary

- Tested with Python 3.10.6 and SymPy 1.13.3.
- `test_refg_f1_atemporal_structural_proof.py` uses only the standard library
  plus the pinned SymPy dependency.
- A standalone-copy test runs the proof after copying only the public script
  into a temporary empty directory.
- No software license is declared here. The author must choose the license and
  citation metadata before a tagged archival/DOI release.
