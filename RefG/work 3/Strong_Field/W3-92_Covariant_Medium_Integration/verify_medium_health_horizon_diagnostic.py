"""Internal W92 health/horizon diagnostic. Stdout only; no repository writes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import sys
sys.dont_write_bytecode = True
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ARTICLE = ROOT / 'RefG_ka.md'
CONTRACT = HERE / 'medium_health_horizon_diagnostic.md'
EXPECTED_SHA = '2571f9fbde25cd9e5258e5bb2c78797380123bf32621e4eaf068ce97c1b4c927'
# Stage 15 audited only the introductory redshift and reciprocal-feedback
# paragraphs. Original GE pin was e137f60644a18c9631b441508a00b193db62c01af166af4fcfa665298925355d.
# The equations exercised by Stages 8, 10 and 11 remain unchanged.
INTUITIVE_GE_SHA = '89ce964c671e2d35645f2955f441c7d405de3f83337787132c93cd823e106a2c'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def simp(x):
    return s.factor(s.cancel(s.simplify(x)))


def fmin(y, b):
    i1 = s.trace(b)
    i2 = (i1*i1 - s.trace(b*b))/2
    i3 = b.det()
    return -8*y + y*y + 8*i1 + i1*i1 - 16*i2 + 16*i3 + 2*y*i1


def ricci_scalar(g, xx):
    """Direct article-convention curvature, independent of the ADM reduction."""
    n = len(xx)
    inv = g.inv()
    ch = [[[simp(sum(inv[a,l]*(s.diff(g[l,b], xx[c])
                    + s.diff(g[l,c], xx[b]) - s.diff(g[b,c], xx[l]))
                    for l in range(n))/2)
            for c in range(n)] for b in range(n)] for a in range(n)]
    ric = s.Matrix(n,n,lambda a,b: simp(sum(
        s.diff(ch[c][a][b],xx[c]) - s.diff(ch[c][a][c],xx[b])
        + sum(ch[c][a][b]*ch[d][c][d] - ch[d][a][c]*ch[c][b][d]
              for d in range(n)) for c in range(n))))
    return simp(s.trace(inv*ric))



def completion_checks(check, condition):
    """Stage 2: finite candidate sequence, no fitted response functions."""
    P,x = s.symbols('P x', positive=True)  # M_Pl^2 and k^2
    C,K,U = s.symbols('C K U', real=True, nonzero=True)
    n,b,z,E,h,zd,ed = s.symbols('n b z E h zd ed', real=True)
    G = P*(-3*zd**2-2*x*zd*b+2*x*zd*ed+x*z*z+2*x*n*z)
    Q = n+3*z-x*E-2*h
    lag = G+4*C*Q**2+P*x*h*h+K*x*b*b/2-2*U*x*x*E*E/3
    aux = s.hessian(lag,(n,b,h))
    check('completion_auxiliary_determinant',aux.det(),16*C*K*P*x*x,
          'completion_scalar')
    sol = s.solve([s.diff(lag,q) for q in (n,b,h)],(n,b,h),dict=True)[0]
    expected = {n:x*E-7*z-P*x*z/(4*C),b:2*P*zd/K,h:-2*z}
    for q in (n,b,h):
        check('completion_auxiliary_%s' % q,sol[q],expected[q],
              'completion_scalar')
        check('completion_auxiliary_residual_%s' % q,
              s.diff(lag,q).subs(sol),group='completion_scalar')
    reduced = simp(lag.subs(sol))
    kinetic = (-3*P-2*P*P*x/K)*zd**2+2*P*x*zd*ed
    potential = -(9*P*x+P*P*x*x/(4*C))*z*z+2*P*x*x*z*E-2*U*x*x*E*E/3
    check('completion_full_reduced_action',reduced,kinetic+potential,
          'completion_scalar')
    kmat = s.hessian(reduced,(zd,ed))
    check('completion_kinetic_determinant',kmat.det(),-4*P*P*x*x,
          'completion_scalar')
    condition('completion_scalar_kinetic_indefinite',
              simp(kmat.det()).is_negative,
              'real symmetric 2x2 nondegenerate kinetic matrix has opposite signs',
              'completion_scalar')

    # Independent vector and tensor normalizations, entire action positive TT.
    V,q,qd,tt,ttd = s.symbols('V q qd tt ttd',real=True)
    lv = P*x*V*V/4+K*(qd-V)**2/2-U*x*q*q/2
    vsol = s.solve(s.diff(lv,V),V)[0]
    check('completion_vector_shift',vsol,2*K*qd/(P*x+2*K),
          'completion_vector_tensor')
    keff = K*P*x/(P*x+2*K)
    lvr = simp(lv.subs(V,vsol))
    check('completion_vector_reduced',lvr,keff*qd*qd/2-U*x*q*q/2,
          'completion_vector_tensor')
    check('completion_vector_frequency',U*x/keff,(U/K)*x+2*U/P,
          'completion_vector_tensor')
    ltt = P*(ttd*ttd-x*tt*tt)/8-U*tt*tt/4
    check('completion_tensor_frequency',
          -s.diff(ltt,tt,2)/s.diff(ltt,ttd,2),x+2*U/P,
          'completion_vector_tensor')
    kp,up = s.symbols('kp up',positive=True)
    condition('completion_vector_tensor_positive_domain',
              keff.subs(K,kp).is_positive and (x+2*up/P).is_positive
              and ((up/kp)*x+2*up/P).is_positive,
              'K>0,U>0; no full scalar health or observational claim',
              'completion_vector_tensor')
    check('completion_U_zero_TT_massless', (x+2*U/P).subs(U,0), x,
          'completion_vector_tensor')

    # Full shear value and first derivative vanish at Bhat=I.
    a1,a2,a3,a4,a5,a6 = s.symbols('a1:7',real=True)
    B = s.Matrix([[a1,a4,a5],[a4,a2,a6],[a5,a6,a3]])
    shear = s.trace(B*B)-s.trace(B)**2/3
    vacuum = {a1:1,a2:1,a3:1,a4:0,a5:0,a6:0}
    check('completion_shear_exterior_value',shear.subs(vacuum),
          group='completion_exterior')
    for a in (a1,a2,a3,a4,a5,a6):
        check('completion_shear_exterior_first_%s' % a,
              s.diff(shear,a).subs(vacuum),group='completion_exterior')
    u1,u2,u3,yhat = s.symbols('u1 u2 u3 yhat',real=True)
    normZ = (u1*u1+u2*u2+u3*u3)/yhat
    silent = {u1:0,u2:0,u3:0,yhat:1}
    check('normalized_Z_exterior_value',normZ.subs(silent),
          group='completion_exterior')
    for a in (u1,u2,u3,yhat):
        check('normalized_Z_exterior_first_%s' % a,
              s.diff(normZ,a).subs(silent),group='completion_exterior')

    # One finite general-Hessian fallback: all-k lapse-constraint condition.
    a,b0,d,ss = s.symbols('a b0 d ss',real=True)
    iso = a*(n+h)**2+2*b0*(n+h)*(ss+3*h)+d*(ss+3*h)**2+P*x*h*h
    den = P*x+a+6*b0+9*d
    hsol = s.solve(s.diff(iso,h),h)[0]
    iso_red = simp(iso.subs(h,hsol))
    coeff_n2 = simp(s.diff(iso_red,n,2)/2)
    expect_coeff = (a*P*x+9*(a*d-b0*b0))/den
    check('general_Hessian_effective_lapse_square',coeff_n2,expect_coeff,
          'completion_fallback')
    num = s.expand(a*P*x+9*(a*d-b0*b0))
    conditions = s.Poly(num,x).all_coeffs()
    allk = s.solve(conditions,(a,b0),dict=True)
    condition('general_Hessian_all_k_degeneracy',
              allk == [{a:0,b0:0}],
              str(allk)+'; only on regular den != 0 branches',
              'completion_fallback')
    check('general_Hessian_maps_Fmin',coeff_n2.subs({a:4*C,b0:-4*C,d:4*C}),
          4*C*P*x/(P*x+16*C), 'completion_fallback')
    check('cross_term_recreates_lapse_square',coeff_n2.subs(a,0),
          -9*b0*b0/(P*x+6*b0+9*d),'completion_fallback')
    lf = G+d*(x*E-3*z+3*h)**2+P*x*h*h+K*x*b*b/2-2*U*x*x*E*E/3
    check('trace_only_lapse_constraint',s.diff(lf,n),2*P*x*z,
          'completion_fallback')
    constrained = lf.subs({z:0,zd:0})
    fsol = s.solve([s.diff(constrained,q) for q in (b,h)],(b,h),dict=True)[0]
    lr = simp(constrained.subs(fsol))
    expected_lr = x*x*(d*P*x/(P*x+9*d)-2*U/3)*E*E
    check('trace_only_reduced_action',lr,expected_lr,'completion_fallback')
    check('trace_only_scalar_kinetic_zero',s.diff(lr,ed,2),
          group='completion_fallback')

    # Exact nonlinear constraint witness for the C=d=0 constant-Z fallback.
    N = s.symbols('N',positive=True)
    sx,sy,sz = s.symbols('sx sy sz',real=True)
    shift2 = sx*sx+sy*sy+sz*sz
    coordinates = (N,sx,sy,sz)
    Vbad = (K*shift2/2-U*shift2**2/6)/N**3
    hbad = s.hessian(Vbad,coordinates)
    bad_det = simp(hbad.subs({sy:0,sz:0}).det())
    expected_bad = -K*sx*sx*(3*K+2*U*sx*sx)*(3*K-2*U*sx*sx)**2/(9*N**14)
    check('constant_Z_nonlinear_auxiliary_determinant',bad_det,expected_bad,
          'completion_nonlinear')
    check('constant_Z_rank_change_leading',s.diff(bad_det,sx,2).subs(sx,0)/2,
          -3*K**4/N**14,'completion_nonlinear')
    condition('constant_Z_zero_shift_rank_three',
              hbad.subs({sx:0,sy:0,sz:0}).rank()==3,
              'K!=0,N>0','completion_nonlinear')
    witness={N:1,K:3,U:1,sx:s.Rational(1,2),sy:0,sz:0}
    condition('constant_Z_nonzero_shift_rank_four',
              hbad.subs(witness).rank()==4 and
              (1-shift2/N**2).subs(witness)>0,
              'N=1,K=3,U=1,shift=(1/2,0,0),B>0',
              'completion_nonlinear')

    # Third trial: unit-clock normalization, a different nonlinear action.
    Vnormalized = K*shift2/(2*N)-U*shift2**2/(6*N**3)
    hnormalized = s.hessian(Vnormalized,coordinates)
    radial = s.Matrix(coordinates)
    check('normalized_Z_exact_Euler_homogeneity',
          sum(v*s.diff(Vnormalized,v) for v in coordinates),Vnormalized,
          'completion_normalized')
    for i,entry in enumerate(hnormalized*radial):
        check('normalized_Z_Hessian_null_%d' % i,entry,
              group='completion_normalized')
    check('normalized_Z_auxiliary_determinant',
          hnormalized.subs({sy:0,sz:0}).det(),group='completion_normalized')
    condition('normalized_Z_rank_three_control',
              hnormalized.subs(witness).rank()==3,
              'local admissible example; rank can drop on other surfaces',
              'completion_normalized')
    lam = s.symbols('lam',positive=True)
    check('normalized_Z_all_orders_scaling',
          Vnormalized.subs({v:lam*v for v in coordinates},simultaneous=True),
          lam*Vnormalized,'completion_normalized')
    eps = s.symbols('eps',real=True)
    qnorm = {N:1+eps*n,sx:eps*sx,sy:eps*sy,sz:eps*sz}
    delta_quad = s.series((Vnormalized-Vbad).subs(qnorm,simultaneous=True),
                         eps,0,3).removeO()
    check('normalized_Z_same_quadratic_action',delta_quad,
          group='completion_normalized')
    beta = s.symbols('beta',real=True)
    vratio = K*beta*beta/2-U*beta**4/6
    check('normalized_ratio_radial_Hessian',s.diff(vratio,beta,2),
          K-2*U*beta*beta,'completion_normalized')

    # Strong-field warning: retained H-gradient makes local lapse elimination
    # different from global Euler homogeneity. This is a sector test only.
    g,k,N0,nh,amp = s.symbols('g k N0 nh amp',real=True,nonzero=True)
    block = P*(N0*k*k*amp*amp+2*g*k*nh*amp)/2
    blockdet=s.hessian(block,(nh,amp)).det()
    check('gradient_lapse_H_block_determinant',blockdet,-P*P*g*g*k*k,
          'completion_gradient_warning')
    amp_sol=s.solve(s.diff(block,amp),amp)[0]
    check('gradient_H_elimination_generates_lapse_square',
          block.subs(amp,amp_sol),-P*g*g*nh*nh/(2*N0),
          'completion_gradient_warning')
    check('homogeneous_H_limit_restores_missing_term',
          (block.subs(amp,amp_sol)).subs(g,0),
          group='completion_gradient_warning')

    condition('reject_positive_scalar_kinetic_claim',
              simp(kmat.det()-4*P*P*x*x)!=0,
              'The actual determinant is strictly negative.',
              'completion_negative_control')
    condition('reject_normalization_as_cosmetic_change',
              simp(Vbad-Vnormalized)!=0,
              'Constant Z and Z/Yhat differ nonlinearly.',
              'completion_negative_control')
    condition('reject_local_constraint_from_homogeneity_alone',
              simp(-P*g*g/(2*N0))!=0,
              'The nonzero-gradient H block generates a lapse square.',
              'completion_negative_control')


def radial_exterior_checks(check, condition):
    """Stage 3: exact constrained spherical quadratic dynamics of F_3."""
    r,m,P,K,U = s.symbols('r m P K U', positive=True)
    eps = s.symbols('eps',real=True)
    alpha,sigma,h,nu,beta = [s.Function(v)(r)
                            for v in ('alpha','sigma','h','nu','beta')]
    u,v = [s.Function(w)(r) for w in ('alpha_dot','sigma_dot')]
    H0 = m/r
    g = s.diff(H0,r)
    J = 1/r+g
    j = 1/r+2*g
    A = P*r*r*s.exp(4*H0)
    ke = K*s.exp(2*H0)/(2*P)
    den = g*g+ke
    L = s.exp(H0+eps*alpha)
    R = r*s.exp(H0+eps*sigma)
    N = s.exp(-H0+eps*nu)
    H = H0+eps*h
    shift = eps*beta
    dr = lambda expr: s.diff(expr,r)
    quad = lambda expr: simp(s.diff(expr,eps,2).subs(eps,0)/2)

    # Derive the spatial-curvature formula directly, not from the target answer.
    theta,phi = s.symbols('theta phi',real=True)
    Lg,Rg = s.Function('L')(r),s.Function('R')(r)
    qmetric = s.diag(Lg**2,Rg**2,Rg**2*s.sin(theta)**2)
    R3general = 2/Rg**2*(1-dr(Rg)**2/Lg**2-2*Rg*dr(dr(Rg))/Lg**2
                        +2*Rg*dr(Rg)*dr(Lg)/Lg**3)
    check('radial_spatial_curvature_direct',
          ricci_scalar(qmetric,(r,theta,phi)),R3general,'radial_conventions')
    R3 = 2/R**2*(1-dr(R)**2/L**2-2*R*dr(dr(R))/L**2
                 +2*R*dr(R)*dr(L)/L**3)
    # Static lapse EL/P, multiplied by N. At zero extrinsic curvature,
    # the kinetic density contributes no linear lapse/H constraint.
    lapse_expr = N*(L*R*R*R3/2+R*R*dr(H)**2/L)
    Hflux = N*R*R*dr(H)/L
    check('radial_exterior_lapse_background',lapse_expr.subs(eps,0),
          group='radial_auxiliary')
    check('radial_exterior_H_flux_background',Hflux.subs(eps,0),-m,
          'radial_auxiliary')
    T = dr(dr(sigma))+(3/r+2*g)*dr(sigma)-J*dr(alpha)-(alpha-sigma)/r**2
    lapse_linear = simp(s.diff(lapse_expr,eps).subs(eps,0))
    flux_linear = simp(s.diff(Hflux,eps).subs(eps,0))
    check('radial_full_linear_lapse',lapse_linear,2*r*r*(g*dr(h)-T),
          'radial_auxiliary')
    check('radial_full_linear_H_flux',flux_linear,
          r*r*(dr(h)+g*(nu+2*sigma-alpha)),'radial_auxiliary')
    check('radial_H_EL_from_flux',dr(flux_linear),
          dr(r*r*(dr(h)+g*(nu+2*sigma-alpha))),'radial_auxiliary')

    # Derive F_3's quadratic terms from the spherical invariants.
    br = s.exp(2*H)*(1/L**2-shift**2/N**2)
    bt = s.exp(2*H)*r*r/R**2
    SB = s.Rational(2,3)*(br-bt)**2
    lmix = K*N*L*R*R*s.exp(2*H)*shift**2/(2*N**2)
    lshear = -U*N*L*R*R*SB/4
    check('radial_normalized_mixed_quadratic',quad(lmix),
          K*r*r*s.exp(6*H0)*beta**2/2,'radial_conventions')
    check('radial_shear_quadratic',quad(lshear),
          -2*U*r*r*s.exp(2*H0)*(alpha-sigma)**2/3,'radial_conventions')
    for variable in (h,nu,beta):
        check('radial_shear_no_auxiliary_%s' % variable.func,
              s.diff(quad(lshear),variable),group='radial_conventions')
    check('radial_projected_H_auxiliary_block',
          quad(P*N*R*R*dr(H)**2/L).subs({alpha:0,sigma:0,nu:nu}),
          # Exponential lapse also has a quadratic background contribution.
          # It cancels with EH on shell; remove it explicitly below.
          P*(r*r*dr(h)**2-2*m*nu*dr(h)+m*m*nu**2/(2*r*r)),
          'radial_auxiliary')
    static_total = P*lapse_expr
    pure_aux = quad(static_total).subs({alpha:0,sigma:0}).doit()
    check('radial_complete_lapse_H_auxiliary_block',pure_aux,
          P*(r*r*dr(h)**2-2*m*nu*dr(h)),'radial_auxiliary')

    # Exact extrinsic-curvature kinetic density. All radial derivatives of
    # background and shift are retained; beta carries no time derivative.
    kr = u-g*beta-dr(beta)
    kt = v-J*beta
    raw = -A*(2*kr*kt+kt*kt)+A*ke*beta*beta
    source = J*u-dr(v)-j*v
    ibp = -A*(2*u*v+v*v)+2*A*beta*source+A*den*beta*beta
    boundary_shift = 2*A*beta*v-A*J*beta*beta
    check('radial_background_derivative_A',dr(A),2*j*A,'radial_kinetic')
    check('radial_background_derivative_J',dr(J)+J*J,g*g,'radial_kinetic')
    check('radial_shift_integration_by_parts',raw-ibp,dr(boundary_shift),
          'radial_kinetic')
    beta_sol = -source/den
    shift_el = s.diff(raw,beta)-dr(s.diff(raw,dr(beta)))
    check('radial_shift_EL_direct',shift_el,2*A*(source+den*beta),
          'radial_kinetic')
    check('radial_shift_back_substitution',shift_el.subs(beta,beta_sol).doit(),
          group='radial_kinetic')
    reduced = simp(ibp.subs(beta,beta_sol))
    expected_red = -A*(2*u*v+v*v+source*source/den)
    check('radial_shift_reduced_kinetic',reduced,expected_red,'radial_kinetic')
    chi_dot = u-dr(v)/J-(j/J-den/J**2)*v
    diagonal = -A*J**2*chi_dot**2/den+A*ke*v*v/J**2
    check('radial_complete_kinetic_squares',expected_red-diagonal,
          -dr(A*v*v/J),'radial_kinetic')
    w1,w2 = s.symbols('chi_dot sigma_dot',real=True)
    diag_local = -A*J**2*w1*w1/den+A*ke*w2*w2/J**2
    det = simp(s.hessian(diag_local,(w1,w2)).det())
    check('radial_diagonal_kinetic_determinant',det,-4*A*A*ke/den,
          'radial_kinetic')
    condition('radial_diagonal_kinetic_indefinite',det.is_negative,
              'P,K,m>0 and r>m; the field map is invertible for J!=0',
              'radial_kinetic')

    # Compact-support initial data satisfy all auxiliary equations.
    h_witness = (r-m)*alpha/m
    nu_witness = alpha-dr(h_witness)/g
    witness = {sigma:0,h:h_witness,nu:nu_witness}
    check('radial_compact_witness_lapse',
          lapse_linear.subs(witness,simultaneous=True).doit(),
          group='radial_witness')
    check('radial_compact_witness_H_flux',
          flux_linear.subs(witness,simultaneous=True).doit(),
          group='radial_witness')
    check('radial_compact_witness_shift',beta_sol.subs(v,0).doit(),
          -J*u/den,'radial_witness')
    witness_kinetic = simp(expected_red.subs(v,0).doit())
    check('radial_compact_witness_kinetic',witness_kinetic,-A*J*J*u*u/den,
          'radial_witness')
    rho = s.symbols('rho',positive=True)
    witness_coeff = simp((-A*J*J/den).subs(r,m+rho))
    condition('radial_compact_witness_strict_negative',witness_coeff.is_negative,
              'r=m+rho, rho>0; smooth nonzero alpha_dot has negative integral',
              'radial_witness')
    ad = s.symbols('ad',real=True)
    energy_lag = -A*J*J*ad*ad/den
    check('radial_witness_Hamiltonian_kinetic',
          ad*s.diff(energy_lag,ad)-energy_lag,energy_lag,'radial_witness')
    check('radial_m_zero_lapse_loses_H',
          s.diff(lapse_linear,dr(h)).subs(m,0),group='radial_limits')
    condition('radial_m_zero_witness_is_singular',
              s.denom(s.factor(h_witness)).has(m),
              'Flat vacuum constraint rank differs; do not continue by dividing by m.',
              'radial_limits')
    check('radial_shear_cannot_change_kinetic',s.diff(expected_red,U),
          group='radial_limits')
    condition('reject_radial_positive_square_sign',
              simp((-A*J*J/den)-(A*J*J/den))!=0,
              'An inserted positive kinetic sign fails the reduced action.',
              'radial_negative_control')
    condition('reject_radial_frozen_H_constraint',
              simp(lapse_linear.subs({sigma:0,h:0}).doit())!=0,
              'Freezing h=0 imposes an extra metric restriction absent in F_3.',
              'radial_negative_control')


def two_H_operator_checks(check, condition):
    """Stage 4: two constant coefficients, fixed complete exterior fields."""
    P,m = s.symbols('P m',positive=True)
    a,b = s.symbols('a b',real=True)
    x,y,z = s.symbols('x y z',real=True)
    xx = (x,y,z)
    rr = s.sqrt(x*x+y*y+z*z)
    H0 = m/rr
    Hval = s.symbols('Hval',real=True)
    hv = s.Matrix(s.symbols('H0c H1c H2c H3c',real=True))
    labels = s.Matrix(4,3,lambda i,j:s.Symbol('phi_%d_%d' % (i,j),real=True))
    inv = s.diag(s.exp(2*H0),*([-s.exp(-2*H0)]*3))
    volume = s.exp(2*H0)
    hbg = s.Matrix([0]+[s.diff(H0,q) for q in xx])
    labelbg = s.Matrix([[0,0,0],[1,0,0],[0,1,0],[0,0,1]])
    substitution = {Hval:H0,**dict(zip(hv,hbg))}
    substitution.update({labels[i,j]:labelbg[i,j] for i in range(4) for j in range(3)})
    W = labels.T*inv*hv
    density_E = P*b*volume*s.exp(2*Hval)*(W.dot(W))
    current_H = s.Matrix([s.diff(density_E,q) for q in hv])
    current_H_bg = current_H.subs(substitution).applyfunc(simp)
    H_explicit = s.diff(density_E,Hval).subs(substitution)
    H_EL = simp(H_explicit-sum(s.diff(current_H_bg[i+1],xx[i])
                              for i in range(3)))
    check('two_ops_exterior_H_EL_density',H_EL,2*P*b*m*m/rr**4,
          'two_ops_exterior')
    label_residuals = []
    for j in range(3):
        # Vary independent label gradients before imposing phi=x.
        generic = s.Matrix([s.diff(density_E,labels[i,j]) for i in range(4)])
        expected_generic = 2*P*b*volume*s.exp(2*Hval)*W[j]*inv*hv
        check('two_ops_label_current_generic_%d' % j,
              sum(q*q for q in (generic-expected_generic).applyfunc(simp)),
              group='two_ops_exterior')
        current = generic.subs(substitution).applyfunc(simp)
        for i in range(3):
            check('two_ops_label_current_bg_%d_%d' % (i,j),current[i+1],
                  2*P*b*hbg[i+1]*hbg[j+1],'two_ops_exterior')
        residual = simp(-sum(s.diff(current[i+1],xx[i]) for i in range(3)))
        label_residuals.append(residual)
        check('two_ops_label_EL_%d' % j,residual,
              4*P*b*m*m*xx[j]/rr**6,'two_ops_exterior')
    check('two_ops_label_residual_norm',
          sum(q*q for q in label_residuals),16*P*P*b*b*m**4/rr**10,
          'two_ops_exterior')
    condition('two_ops_exterior_necessary_b_zero',
              s.solve(s.Eq(2*P*b*m*m,0),b)==[0],
              'm>0,r>0: H EL or the nonzero label-current vector forces b=0.',
              'two_ops_exterior')

    # At D_H=0 the operator and all first variations vanish, not only its value.
    dH = s.symbols('dH',real=True)
    density_D = P*a*dH*dH
    check('two_ops_D_static_value',density_D.subs(dH,0),
          group='two_ops_exterior')
    check('two_ops_D_static_first_variation',
          s.diff(density_D,dH).subs(dH,0),group='two_ops_exterior')
    check('two_ops_D_exterior_unit_clock',s.exp(H0)*hbg[0],
          group='two_ops_exterior')

    # Direct full quadratic expansion about the flat silent background.
    # H_mu starts at order eps, so metric/clock/label corrections enter cubically.
    eps = s.symbols('eps',real=True)
    ht,hx,hy,hz,hh = s.symbols('ht hx hy hz hh',real=True)
    q0 = s.Matrix([ht,hx,hy,hz])
    qeps = eps*q0
    eta = s.diag(1,-1,-1,-1)
    # Independent perturbation witnesses in all participating sectors.
    gg = s.diag(*s.symbols('g00 g11 g22 g33',real=True))
    uc = s.Matrix(s.symbols('u0:4',real=True))
    lc = s.Matrix(4,3,lambda i,j:s.Symbol('l%d%d' % (i,j),real=True))
    qinv = eta+eps*gg
    u = s.Matrix([1,0,0,0])+eps*uc
    lab = labelbg+eps*lc
    volpert = s.symbols('volpert',real=True)
    projected = (u*u.T-qinv)
    D = (u.T*qeps)[0]
    Evec = s.exp(eps*hh)*lab.T*qinv*qeps
    density = (1+eps*volpert)*P*((qeps.T*projected*qeps)[0]+a*D*D+b*Evec.dot(Evec))
    flat = simp(s.diff(density,eps,2).subs(eps,0)/2)
    grad2 = hx*hx+hy*hy+hz*hz
    check('two_ops_flat_H_quadratic',flat,P*(a*ht*ht+(1+b)*grad2),
          'two_ops_flat')
    # The underlying F3 normalized-Z/shear block has no H quadratic mixing
    # (verified in the earlier scalar and invariant reductions).
    check('two_ops_flat_H_canonical_momentum',s.diff(flat,ht),2*P*a*ht,
          'two_ops_flat')
    energy = simp(ht*s.diff(flat,ht)-flat)
    check('two_ops_flat_H_energy',energy,P*(a*ht*ht-(1+b)*grad2),
          'two_ops_flat')
    k = s.symbols('k',positive=True)
    w2 = -(1+b)*k*k/a
    check('two_ops_flat_dispersion_identity',a*w2+(1+b)*k*k,
          group='two_ops_flat')
    ap = s.symbols('ap',positive=True)
    condition('two_ops_b_zero_positive_a_gradient_instability',
              w2.subs({a:ap,b:0}).is_negative,
              'a>0,b=0: omega^2=-k^2/a<0 for every k>0.',
              'two_ops_cases')
    condition('two_ops_b_zero_negative_a_ghost',
              s.diff(flat,ht,2).subs({a:-ap,b:0}).is_negative,
              'a<0: the decoupled physical H kinetic coefficient is negative.',
              'two_ops_cases')
    check('two_ops_zero_a_b_returns_F3',
          (flat-P*grad2).subs({a:0,b:0}),group='two_ops_cases')
    check('two_ops_b_minus_one_zero_spatial_energy',
          s.diff(energy,hx,2).subs(b,-1),group='two_ops_cases')
    condition('two_ops_b_minus_one_changes_exterior',
              simp(H_EL.subs(b,-1))!=0,
              'The marginal zero-spatial-energy coefficient cannot preserve the exterior.',
              'two_ops_cases')
    check('two_ops_m_zero_obstruction_vanishes',H_EL.subs(m,0),
          group='two_ops_cases')
    condition('two_ops_positive_kinetic_spatial_control',
              s.diff(flat,ht,2).subs({a:1,b:-2})>0
              and s.diff(energy,hx,2).subs({a:1,b:-2})>0,
              'a=1,b=-2 passes only the flat H sign test, not the exterior.',
              'two_ops_negative_control')
    condition('reject_two_ops_healthy_exterior_control',
              simp(H_EL.subs(b,-2))!=0,
              'The flat positive-energy control fails an actual exterior EL equation.',
              'two_ops_negative_control')
    condition('reject_two_ops_wrong_spatial_sign',
              simp(flat-P*(a*ht*ht-(1+b)*grad2))!=0,
              'Flipping the spatial sign without varying the action fails.',
              'two_ops_negative_control')
    condition('reject_two_ops_a_cancels_label_source',
              all(s.diff(q,a)==0 for q in label_residuals)
              and simp(sum(q*q for q in label_residuals))!=0,
              'D_H contains no labels; a cannot cancel the b-dependent source.',
              'two_ops_negative_control')


def released_exterior_checks(check, condition):
    """Stage 5: same operators, no prescribed exterior or inserted H source."""
    P,K,U,a,x = s.symbols('P K U a x', positive=True)
    b = s.symbols('b', real=True)
    n,B,z,E,h,zd,ed,hd = s.symbols('n B z E h zd ed hd', real=True)
    bd,nd,zdd,edd,hdd = s.symbols('bd nd zdd edd hdd', real=True)
    G = P*(-3*zd**2-2*x*zd*B+2*x*zd*ed+x*z*z+2*x*n*z)
    Lh = P*(a*hd*hd+(1+b)*x*h*h)
    lag = G+K*x*B*B/2-2*U*x*x*E*E/3+Lh
    dmap = {n:nd,B:bd,z:zd,E:ed,h:hd,zd:zdd,ed:edd,hd:hdd}
    velocity = {z:zd,E:ed,h:hd}
    def dt(expr):
        return sum(s.diff(expr,q)*v for q,v in dmap.items())
    def el(q):
        return simp(s.diff(lag,q)-dt(s.diff(lag,velocity[q]))
                    if q in velocity else s.diff(lag,q))
    check('released_vacuum_lapse_constraint',el(n),2*P*x*z,
          'released_flat_scalar')
    check('released_vacuum_shift_constraint',el(B),x*(K*B-2*P*zd),
          'released_flat_scalar')
    check('released_vacuum_label_constraint',el(E),
          -4*U*x*x*E/3-2*P*x*zdd,'released_flat_scalar')
    vac = {n:0,B:0,z:0,E:0,nd:0,bd:0,zd:0,ed:0,zdd:0,edd:0}
    for q in (n,B,z,E):
        check('released_all_metric_scalar_EL_%s' % q,el(q).subs(vac),
              group='released_flat_scalar')
    check('released_physical_scalar_action',lag.subs(vac),Lh,
          'released_flat_scalar')
    check('released_physical_H_equation',el(h),
          2*P*((1+b)*x*h-a*hdd),'released_flat_scalar')
    pi = s.symbols('pi', real=True)
    energy = simp((pi*hd-Lh).subs(hd,pi/(2*P*a)))
    check('released_H_canonical_energy',energy,
          pi*pi/(4*P*a)-P*(1+b)*x*h*h,'released_flat_scalar')
    v2 = s.symbols('v2', positive=True)
    # Parametrizes the entire strict region a>0,b<-1 without sampling it.
    healthy = {b:-1-a*v2}
    condition('released_H_strict_positive_quadratic_energy',
              s.diff(energy,pi,2).is_positive and
              s.diff(energy,h,2).subs(healthy).is_positive,
              'a>0, b=-1-a*v2, v2>0, P>0, k^2=x>0',
              'released_flat_scalar')
    check('released_H_frequency',(-(1+b)*x/a).subs(healthy),v2*x,
          'released_flat_scalar')

    V,q,qd,T,Td = s.symbols('V q qd T Td', real=True)
    lv = P*x*V*V/4+K*(qd-V)**2/2-U*x*q*q/2
    Vsol = s.solve(s.diff(lv,V),V)[0]
    keff = K*P*x/(P*x+2*K)
    check('released_vector_shift',Vsol,2*K*qd/(P*x+2*K),
          'released_flat_vector_tensor')
    check('released_vector_action',lv.subs(V,Vsol),
          keff*qd*qd/2-U*x*q*q/2,'released_flat_vector_tensor')
    tt = P*(Td*Td-x*T*T)/8-U*T*T/4
    wt = -s.diff(tt,T,2)/s.diff(tt,Td,2)
    check('released_TT_frequency',wt,x+2*U/P,'released_flat_vector_tensor')
    check('released_vector_frequency',U*x/keff,(U/K)*x+2*U/P,
          'released_flat_vector_tensor')
    condition('released_vector_TT_positive_energy',
              keff.is_positive and s.diff(tt,Td,2).is_positive and
              (-s.diff(tt,T,2)).is_positive and (U*x).is_positive,
              'two transverse-vector and two TT modes, P,K,U,k>0',
              'released_flat_vector_tensor')
    check('released_TT_mass_gap',wt-x,2*U/P,'released_flat_vector_tensor')
    cV,cH = s.symbols('cV cH', positive=True)
    check('released_vector_characteristic_speed',
          (U/K).subs(U,K*cV*cV),cV*cV,'released_flat_vector_tensor')
    check('released_H_characteristic_speed',
          (-(1+b)/a).subs(b,-1-a*cH*cH),cH*cH,
          'released_flat_vector_tensor')

    rho,m,eps = s.symbols('rho m eps', real=True)
    N = s.symbols('N', positive=True)
    check('released_positive_mass_rest_action',-m*s.sqrt(N*N),-m*N,
          'released_source')
    check('released_static_matter_linear_source',
          s.diff(-rho*(1+eps*n),eps).subs(eps,0),-rho*n,
          'released_source')
    static = simp(lag.subs({zd:0,ed:0,hd:0})-rho*n)
    sol = s.solve([s.diff(static,q) for q in (n,B,z,E,h)],
                  (n,B,z,E,h),dict=True)[0]
    expected = {z:rho/(2*P*x),n:-rho/(2*P*x),B:0,E:0,h:0}
    for q in (n,B,z,E,h):
        check('released_sourced_solution_%s' % q,sol[q],expected[q],
              'released_source')
        check('released_sourced_residual_%s' % q,
              s.diff(static,q).subs(sol),group='released_source')
    check('released_static_potential_slip',sol[n]+sol[z],
          group='released_source')
    check('released_Newtonian_Poisson',-x*sol[n],rho/(2*P),
          'released_source')
    GN = s.symbols('GN', positive=True)
    check('released_Newton_constant_normalization',
          (1/(2*P)).subs(P,1/(8*s.pi*GN)),4*s.pi*GN,'released_source')
    check('released_H_direct_source_absent',s.diff(static,h,rho),
          group='released_source')
    r = s.symbols('r', positive=True)
    c0,c1 = s.symbols('c0 c1', real=True)
    harmonic = c0+c1/r
    check('released_radial_H_harmonic',(s.diff(r*r*s.diff(harmonic,r),r)),
          group='released_source')
    check('released_H_central_pole_coefficient',
          s.limit(r*harmonic,r,0,dir='+'),c1,'released_source')
    check('released_H_asymptotic_constant',s.limit(harmonic,r,s.oo),c0,
          'released_source')

    # First variations at the entire isotropic valley, before metric selection.
    entries = s.symbols('B1:7', real=True)
    B1,B2,B3,B4,B5,B6 = entries
    Bh = s.Matrix([[B1,B4,B5],[B4,B2,B6],[B5,B6,B3]])
    shear = s.trace(Bh*Bh)-s.trace(Bh)**2/3
    lam = s.symbols('lam', positive=True)
    valley = {B1:lam,B2:lam,B3:lam,B4:0,B5:0,B6:0}
    check('released_isotropic_valley_value',shear.subs(valley),
          group='released_silent_GR')
    for v in entries:
        check('released_isotropic_valley_first_%s' % v,
              s.diff(shear,v).subs(valley),group='released_silent_GR')
    eta = s.symbols('eta', real=True)
    check('released_shear_H_derivative',
          s.diff(shear.subs({v:s.exp(2*eta)*v for v in entries},
                           simultaneous=True),eta).subs(eta,0),
          4*shear,'released_silent_GR')
    yhat = s.symbols('yhat', positive=True)
    C1,C2,C3,dh,ex,ey,ez,hx,hy,hz = s.symbols(
        'C1 C2 C3 dh ex ey ez hx hy hz', real=True)
    small = (C1,C2,C3,dh,ex,ey,ez,hx,hy,hz)
    rest = K*(C1*C1+C2*C2+C3*C3)/(2*yhat) + P*(
        a*dh*dh+b*(ex*ex+ey*ey+ez*ez)+hx*hx+hy*hy+hz*hz)
    zero = dict.fromkeys(small,0)
    check('released_other_medium_value',rest.subs(zero),
          group='released_silent_GR')
    condition('released_other_medium_all_first_variations',
              all(s.diff(rest,v).subs(zero)==0 for v in (*small,yhat)),
              'C_A=dH=0; coefficient variations multiply quadratic zeros',
              'released_silent_GR')

    # Exact isotropic Schwarzschild exterior, r>m/2, and its readout.
    mp = s.symbols('mp', positive=True)
    lapse = (1-mp/(2*r))/(1+mp/(2*r))
    L = (1+mp/(2*r))**2
    R = r*L
    check('released_Schwarzschild_lapse_identity',lapse*lapse,1-2*mp/R,
          'released_silent_GR')
    check('released_Schwarzschild_radial_identity',
          L*L/s.diff(R,r)**2,1/(1-2*mp/R),'released_silent_GR')
    radius = s.symbols('radius',positive=True)
    f = 1-2*mp/radius
    check('released_Schwarzschild_vacuum_radial',
          (1-f-radius*s.diff(f,radius))/radius**2,group='released_silent_GR')
    check('released_Schwarzschild_vacuum_angular',
          s.diff(f,radius,2)/2+s.diff(f,radius)/radius,
          group='released_silent_GR')
    check('released_clock_ruler_linear_agreement',
          s.series(lapse-1/L,mp,0,2).removeO(),group='released_readout')
    check('released_clock_ruler_exact_difference',lapse-1/L,
          -mp*mp/(4*r*r*(1+mp/(2*r))**2),'released_readout')
    check('released_coordinate_light_speed_linear',
          s.series(lapse/L,mp,0,2).removeO(),1-2*mp/r,'released_readout')
    check('released_static_metric_beta',
          s.series(lapse*lapse,mp,0,3).removeO(),
          1-2*mp/r+2*mp*mp/(r*r),'released_readout')

    condition('reject_released_inserted_H_deficit',
              simp(s.diff(static,h).subs({h:rho/(2*P*x)}))!=0,
              'H=-n at linear order violates the unsourced H equation for rho!=0',
              'released_negative_control')
    condition('reject_released_exact_common_scale',
              simp(lapse-1/L)!=0,
              'clock and coordinate ruler agree only to leading order here',
              'released_negative_control')
    condition('reject_released_massless_TT_inheritance',simp(wt-x)!=0,
              'U>0 produces 2U/P; old massless-TT result is not inherited',
              'released_negative_control')
    condition('reject_released_wrong_Newtonian_sign',
              simp(-x*(-sol[n])-rho/(2*P))!=0,
              'repulsive sign fails the positive-mass source equation',
              'released_negative_control')


def volume_source_checks(check, condition):
    """Stage 6: one allowed bulk invariant; include zero-gradient boundary."""
    P,K,U,V,a,x = s.symbols('P K U V a x',positive=True)
    sigma = s.symbols('sigma',nonnegative=True)
    n,B,z,E,h,zd,ed,hd = s.symbols('n B z E h zd ed hd',real=True)
    nd,bd,zdd,edd,hdd = s.symbols('nd bd zdd edd hdd',real=True)
    eps,rho = s.symbols('eps rho',real=True)
    T = 2*U+V
    C = 6*U*V/T
    strain = x*E-3*z+3*h
    Bh = s.diag(1+2*eps*(h-z),1+2*eps*(h-z),
                1+2*eps*(h-z+x*E))
    check('volume_trace_linear',s.diff(s.trace(Bh),eps),2*strain,
          'volume_invariant')
    check('volume_quadratic_from_full_invariant',
          s.expand(-V*(s.trace(Bh)-3)**2/12).coeff(eps,2),
          -V*strain**2/3,'volume_invariant')
    tr = s.symbols('tr',real=True)
    op = -V*(tr-3)**2/12
    check('volume_silent_value',op.subs(tr,3),group='volume_invariant')
    check('volume_silent_first',s.diff(op,tr).subs(tr,3),
          group='volume_invariant')

    G = P*(-3*zd**2-2*x*zd*B+2*x*zd*ed+x*z*z+2*x*n*z)
    lag = G+K*x*B*B/2-2*U*x*x*E*E/3 \
        +P*(a*hd*hd-sigma*x*h*h)-V*strain**2/3
    dmap = {n:nd,B:bd,z:zd,E:ed,h:hd,zd:zdd,ed:edd,hd:hdd}
    velocity = {z:zd,E:ed,h:hd}
    def dt(expr):
        return sum(s.diff(expr,q)*v for q,v in dmap.items())
    def el(q):
        return simp(s.diff(lag,q)-dt(s.diff(lag,velocity[q]))
                    if q in velocity else s.diff(lag,q))
    check('volume_lapse_constraint',el(n),2*P*x*z,'volume_scalar')
    check('volume_shift_constraint',el(B),x*(K*B-2*P*zd),'volume_scalar')
    constraints = {z:0,zd:0,zdd:0,B:0,bd:0}
    Esol = s.solve(el(E).subs(constraints),E)[0]
    check('volume_auxiliary_strain',Esol,-3*V*h/(x*T),'volume_scalar')
    Eddsol = -3*V*hdd/(x*T)
    nsol = s.solve(el(z).subs(constraints).subs({E:Esol,edd:Eddsol}),n)[0]
    check('volume_lapse_reconstruction',nsol,Eddsol-C*h/(P*x),
          'volume_scalar')
    reconstruction = {**constraints,E:Esol,ed:-3*V*hd/(x*T),
                      edd:Eddsol,n:nsol}
    for q in (n,B,z,E):
        check('volume_all_auxiliary_EL_%s' % q,
              el(q).subs(reconstruction,simultaneous=True),group='volume_scalar')
    reduced = simp(lag.subs(reconstruction,simultaneous=True))
    target = P*a*hd*hd-(P*sigma*x+C)*h*h
    check('volume_reduced_physical_H_action',reduced,target,'volume_scalar')
    check('volume_reconstructed_H_equation',
          el(h).subs(reconstruction,simultaneous=True),
          -2*(P*a*hdd+(P*sigma*x+C)*h),'volume_scalar')
    pi = s.symbols('pi',real=True)
    energy = simp((pi*hd-reduced).subs(hd,pi/(2*P*a)))
    check('volume_H_Hamiltonian',energy,
          pi*pi/(4*P*a)+(P*sigma*x+C)*h*h,'volume_scalar')
    condition('volume_all_sigma_nonnegative_energy',
              s.diff(energy,pi,2).is_positive and
              s.diff(energy,h,2).is_positive,
              'P,K,U,V,a>0, sigma>=0, x=k^2>0','volume_scalar')
    check('volume_H_frequency',-s.diff(reduced,h,2)/s.diff(reduced,hd,2),
          sigma*x/a+C/(P*a),'volume_scalar')
    check('volume_zero_speed_positive_mass',
          energy.subs(sigma,0),pi*pi/(4*P*a)+C*h*h,'volume_scalar')
    check('volume_zero_characteristic_speed',
          s.diff(sigma*x/a+C/(P*a),x).subs(sigma,0),group='volume_scalar')
    # A pure tensor or transverse-vector has zero linear material trace.
    check('volume_transverse_quadratic_unchanged',
          (-V*strain**2/3).subs({z:0,E:0,h:0}),group='volume_scalar')

    static = simp(lag.subs({zd:0,ed:0,hd:0})-rho*n)
    Estatic = s.solve(s.diff(static,E),E)[0]
    check('volume_static_strain_elimination',Estatic,
          3*V*(z-h)/(x*T),'volume_source')
    check('volume_static_reduced_source_action',static.subs(E,Estatic),
          P*x*z*z+2*P*x*n*z+K*x*B*B/2
          -P*sigma*x*h*h-C*(h-z)**2-rho*n,'volume_source')
    sol = s.solve([s.diff(static,q) for q in (n,B,z,E,h)],
                  (n,B,z,E,h),dict=True)[0]
    zz = rho/(2*P*x)
    hh = C*zz/(P*sigma*x+C)
    expected = {z:zz,h:hh,n:-zz+sigma*hh,B:0,
                E:3*V*(zz-hh)/(x*T)}
    for q in (n,B,z,E,h):
        check('volume_sourced_solution_%s' % q,sol[q],expected[q],
              'volume_source')
        check('volume_sourced_residual_%s' % q,
              s.diff(static,q).subs(sol),group='volume_source')
    check('volume_metric_mediated_H_source',s.diff(sol[h],rho),
          C/(2*P*x*(P*sigma*x+C)),'volume_source')
    check('volume_no_added_direct_matter_H_term',s.diff(-rho*n,h),
          group='volume_source')
    check('volume_material_strain_relation',sol[E],P*sigma*sol[h]/(2*U),
          'volume_source')
    check('volume_static_metric_slip',sol[n]+sol[z],sigma*sol[h],
          'volume_source')

    for q,value in {z:zz,h:zz,n:-zz,E:0,B:0}.items():
        check('volume_zero_sigma_matching_%s' % q,sol[q].subs(sigma,0),
              value,'volume_matching')
    check('volume_matched_Newtonian_normalization',
          (-x*sol[n]).subs(sigma,0),rho/(2*P),'volume_matching')
    check('volume_matched_W51_deficit_Poisson',
          (-x*sol[h]).subs(sigma,0),-rho/(2*P),'volume_matching')
    clock = 1+eps*sol[n]
    # For a Fourier mode along z, a direction cosine d probes E_,zz=-xE.
    d = s.symbols('d',real=True)
    ruler = 1-eps*sol[z]+eps*x*sol[E]*d*d
    p = 1-eps*sol[h]
    check('volume_matched_clock_readout',(clock-p).subs(sigma,0),
          group='volume_matching')
    check('volume_matched_all_direction_rulers',(ruler-p).subs(sigma,0),
          group='volume_matching')
    check('volume_matched_coordinate_light_speed',
          s.series((clock*ruler).subs(sigma,0),eps,0,2).removeO(),
          1-2*eps*zz,'volume_matching')
    ratio = simp((sol[n]+sol[z])/sol[h])
    check('volume_matching_selects_sigma',ratio,sigma,'volume_matching')
    condition('volume_unique_common_scale_coefficient',
              s.solve(ratio,sigma)==[0],
              'nonzero source, finite P,U,V,a>0,k>0; b=-1',
              'volume_matching')

    sp = s.symbols('sp',positive=True)
    check('volume_long_wavelength_H_ratio',
          s.limit((sol[h]/sol[z]).subs(sigma,sp),x,0,dir='+'),1,
          'volume_limits')
    check('volume_far_clock_coupling_ratio',
          s.limit((-sol[n]/sol[z]).subs(sigma,sp),x,0,dir='+'),1-sp,
          'volume_limits')
    check('volume_short_wavelength_H_ratio',
          s.limit((sol[h]/sol[z]).subs(sigma,sp),x,s.oo),0,'volume_limits')
    check('volume_no_bulk_recovers_unsourced_H',
          s.limit(sol[h].subs(sigma,sp),V,0,dir='+'),0,'volume_limits')
    check('volume_zero_shear_restoring_energy',s.limit(C,U,0,dir='+'),0,
          'volume_limits')
    auxdet = s.hessian(static,(E,h)).det()
    check('volume_static_auxiliary_determinant_at_matching',
          auxdet.subs(sigma,0),8*U*V*x*x,'volume_limits')
    check('volume_zero_shear_matching_rank_loss',
          auxdet.subs({sigma:0,U:0}),group='volume_limits')

    # Point-source Green kernel only diagnoses the weak equations at r>0.
    r,ell,G0,m = s.symbols('r ell G0 m',positive=True)
    zpoint = G0*m/r
    hpoint = zpoint*(1-s.exp(-ell*r))
    def lap(f):
        return simp(s.diff(r*r*s.diff(f,r),r)/(r*r))
    check('volume_point_source_response_away_from_origin',
          -lap(hpoint)+ell*ell*hpoint,ell*ell*zpoint,'volume_limits')
    check('volume_point_H_finite_value',s.limit(hpoint,r,0,dir='+'),
          G0*m*ell,'volume_limits')
    check('volume_point_H_nonzero_central_slope',
          s.limit(s.diff(hpoint,r),r,0,dir='+'),-G0*m*ell*ell/2,
          'volume_limits')
    check('volume_point_metric_pole_persists',
          s.limit(r*(-zpoint+sp*hpoint),r,0,dir='+'),-G0*m,
          'volume_limits')

    condition('reject_volume_strict_sigma_common_scale',
              simp((sol[n]+sol[z]).subs(sigma,sp))!=0,
              'sigma>0 sources H but changes the static metric potential ratio',
              'volume_negative_control')
    condition('reject_volume_zero_speed_zero_energy',
              s.diff(energy.subs(sigma,0),h,2).is_positive,
              'zero spatial speed leaves finite positive volume restoring energy',
              'volume_negative_control')
    condition('reject_volume_preimposed_H_profile',
              simp(s.diff(static,h).subs({h:z,E:0,sigma:sp}))!=0,
              'h=z,E=0 violates H EL in the strict sigma>0 branch',
              'volume_negative_control')
    condition('reject_volume_complete_exponential_exterior',
              op.subs(tr,3)==0 and s.diff(op,tr).subs(tr,3)==0,
              'silent volume term cannot cancel the Stage4 b=-1 label residual',
              'volume_negative_control')
    condition('reject_volume_finite_H_as_regular_centre',
              s.limit(s.diff(hpoint,r),r,0,dir='+')!=0,
              'finite point-source H is not even a smooth spherical central profile',
              'volume_negative_control')


def nonuniform_volume_checks(check, condition):
    """Stage 7: own regular weak source, then a physical transverse pair."""
    P,K,U,V,a = s.symbols('P K U V a',positive=True)
    r,m,g,lr,lt = s.symbols('r m g lr lt',positive=True)
    eps = s.symbols('eps',real=True)
    F = -U*(lr-lt)**2/6-V*(lr+2*lt-3)**2/12
    Dr = s.diff(F,lr)
    Dt = s.diff(F,lt)/2  # two equal tangential eigenvalues
    N,A,R,H,hp = s.symbols('N A R H hp',real=True)
    br,bt = s.exp(2*H)/A**2,s.exp(2*H)*r*r/R**2
    repl = {lr:br,lt:bt}
    Lmed = N*A*R*R*(F.subs(repl)+P*hp*hp/A**2*(1-br))
    checks = {
        N:(A*R*R,(F+P*g*g*(1-lr))),
        A:(N*R*R,F-2*lr*Dr+P*g*g*(-1+3*lr)),
        R:(N*A*R,2*F-4*lt*Dt+2*P*g*g*(1-lr)),
        H:(N*A*R*R,2*lr*Dr+4*lt*Dt-2*P*lr*g*g),
    }
    for q,(factor,target) in checks.items():
        check('nonuniform_exact_medium_variation_%s' % q,s.diff(Lmed,q),
              factor*target.subs({**repl,g:hp/A}),
              'nonuniform_background')
    check('nonuniform_H_derivative_current',s.diff(Lmed,hp),
          2*P*N*R*R*hp*(1-br)/A,'nonuniform_background')
    dr,dt = s.symbols('dr dt',real=True)
    weak = {lr:1+eps*eps*dr,lt:1+eps*eps*dt,g:eps*g}
    def c2(expr):
        return simp(s.diff(expr.subs(weak,simultaneous=True),eps,2).subs(eps,0)/2)
    t,d = dr+2*dt,dr-dt
    Dr2,Dt2 = c2(Dr),c2(Dt)
    check('nonuniform_radial_prestress',Dr2,-U*d/3-V*t/6,
          'nonuniform_background')
    check('nonuniform_tangential_prestress',Dt2,U*d/6-V*t/6,
          'nonuniform_background')
    Hel2 = c2(2*lr*Dr+4*lt*Dt-2*P*lr*g*g)
    check('nonuniform_H_source_strain_equation',Hel2,-V*t-2*P*g*g,
          'nonuniform_background')
    check('nonuniform_H_derivative_current_starts_cubic',
          c2(g*(1-lr)),group='nonuniform_background')
    jr,jt = 2*Dr2-2*P*g*g,2*Dt2
    check('nonuniform_label_current_trace',jr+2*jt,Hel2,
          'nonuniform_background')
    J = s.symbols('J',real=True)
    check('nonuniform_conserved_label_current',
          s.diff(J/r**3,r)+3*(J/r**3)/r,group='nonuniform_background')
    check('nonuniform_central_current_pole',
          s.limit(r**3*(J/r**3),r,0,dir='+'),J,'nonuniform_background')
    sol = s.solve([Hel2,jr],(dr,dt),dict=True)[0]
    er = -2*P*g*g*(1/V+2/U)/3
    et = 2*P*g*g*(1/U-1/V)/3
    check('nonuniform_regular_source_radial_strain',sol[dr],er,
          'nonuniform_background')
    check('nonuniform_regular_source_tangential_strain',sol[dt],et,
          'nonuniform_background')
    check('nonuniform_regular_source_radial_prestress',Dr2.subs(sol),P*g*g,
          'nonuniform_background')
    check('nonuniform_regular_source_tangential_prestress',Dt2.subs(sol),
          group='nonuniform_background')
    for q,(_,expr) in checks.items():
        check('nonuniform_medium_field_residual_%s' % q,c2(expr).subs(sol),
              group='nonuniform_background')

    # Derived exterior in material coordinates: Schwarzschild plus a derived
    # radial-coordinate displacement, not the old exponential ansatz.
    iso = r-eps*eps*P*m*m/(4*U*r**3)
    Ns = (1-eps*m/(2*iso))/(1+eps*m/(2*iso))
    As = (1+eps*m/(2*iso))**2*s.diff(iso,r)
    Bs = iso*(1+eps*m/(2*iso))**2/r
    n2 = s.Integer(0)
    a2 = -m*m/(4*r*r)+3*P*m*m/(4*U*r**4)
    b2 = -m*m/(4*r*r)-P*m*m/(4*U*r**4)
    h2 = -m*m/(4*r*r)+P*m*m*(1/U-4/V)/(12*r**4)
    for name,expr,linear,quadratic in (
        ('N',Ns,-m/r,n2),('A',As,m/r,a2),('B',Bs,m/r,b2)):
        check('nonuniform_own_metric_linear_'+name,
              s.diff(s.log(expr),eps).subs(eps,0),linear,'nonuniform_exterior')
        check('nonuniform_own_metric_quadratic_'+name,
              s.diff(s.log(expr),eps,2).subs(eps,0)/2,quadratic,
              'nonuniform_exterior')
    check('nonuniform_own_H_radial_strain',2*(h2-a2),
          er.subs(g,m/r**2),'nonuniform_exterior')
    check('nonuniform_own_H_tangential_strain',2*(h2-b2),
          et.subs(g,m/r**2),'nonuniform_exterior')

    # Direct invariant expansion of the tangential-wave/radial-displacement
    # principal block. Field VALUES are frozen; derivative perturbations vary.
    hd,hz,pd,pz,tauz = s.symbols('hd hz pd pz tauz',real=True)
    inv = s.diag(1,-1,-1,-1)
    clock = s.Matrix([1,0,0,eps*tauz])
    Y = (clock.T*inv*clock)[0]
    u = inv*clock/s.sqrt(Y)
    Hgrad = s.Matrix([eps*hd,g,0,eps*hz])
    labels = s.Matrix([[eps*pd,s.sqrt(lr),0,eps*pz],
                       [0,0,s.sqrt(lt),0],[0,0,0,s.sqrt(lt)]])
    Bh = -labels*inv*labels.T
    mixed = labels*u
    D = (Hgrad.T*u)[0]
    Evec = labels*inv*Hgrad
    gamma = (u*u.T-inv)
    shear = s.trace(Bh*Bh)-s.trace(Bh)**2/3
    Linv = K*(mixed.T*mixed)[0]/2-U*shear/4 \
        -V*(s.trace(Bh)-3)**2/12 \
        +P*((Hgrad.T*gamma*Hgrad)[0]+a*D*D-(Evec.T*Evec)[0])
    principal = simp(s.diff(Linv,eps,2).subs(eps,0)/2)
    target = (K-2*Dr)*pd*pd/2-(U*lt-2*Dr)*pz*pz/2 \
        +P*a*hd*hd-P*(lt-1)*hz*hz \
        +2*P*s.sqrt(lr)*g*(hd*pd-hz*pz)+K*lt*tauz*tauz/2
    check('nonuniform_direct_invariant_principal',principal,target,
          'nonuniform_principal')
    for velocity in (hd,pd):
        check('nonuniform_clock_decouples_'+str(velocity),
              s.diff(principal,tauz,velocity),group='nonuniform_principal')
    check('nonuniform_clock_separate_spatial_constraint',
          s.diff(principal,tauz),K*lt*tauz,'nonuniform_principal')
    M = s.hessian(principal,(pd,hd))
    S = -s.hessian(principal,(pz,hz))
    sourceweak = {lr:1+eps*eps*er,lt:1+eps*eps*et,g:eps*g}
    # er/et above use the unscaled gradient amplitude; substitutions simultaneous.
    Mw = M.subs(sourceweak,simultaneous=True)
    Sw = S.subs(sourceweak,simultaneous=True)
    detM2 = simp(s.diff(Mw.det(),eps,2).subs(eps,0)/2)
    detS2 = simp(s.diff(Sw.det(),eps,2).subs(eps,0)/2)
    check('nonuniform_physical_kinetic_determinant_leading',detM2,
          -4*P*P*(a+1)*g*g,'nonuniform_principal')
    check('nonuniform_physical_spatial_determinant_leading',detS2,
          -4*P*P*g*g*(2+U/V)/3,'nonuniform_principal')
    condition('nonuniform_weak_kinetic_positive_by_continuity',
              Mw[0,0].subs(eps,0).is_positive and
              Mw.det().subs(eps,0).is_positive,
              'finite positive coefficients; sufficiently small source amplitude',
              'nonuniform_principal')
    condition('nonuniform_negative_spatial_determinant_all_positive_coefficients',
              detS2.is_negative,
              'g!=0; negative first nonzero weak coefficient dominates higher orders',
              'nonuniform_principal')
    speed2 = simp(detS2/(2*P*a*U))
    check('nonuniform_negative_characteristic_leading',speed2,
          -2*P*g*g*(2/U+1/V)/(3*a),'nonuniform_principal')

    # Direct ADM invariant check of the physical radial-shift coupling.
    sv,kv = s.symbols('sv kv',real=True)
    invv = s.Matrix([[1,-eps*sv,0,0],
                     [-eps*sv,eps*eps*sv*sv-1,0,0],
                     [0,0,-1,0],[0,0,0,-1]])
    uv = invv*s.Matrix([1,0,0,0])  # N=1, Phi=t; Y=1 exactly
    hg = s.Matrix([eps*hd,g,0,0])
    pg = s.Matrix([[eps*pd,s.sqrt(lr),0,0],
                   [0,0,s.sqrt(lt),0],[0,0,0,s.sqrt(lt)]])
    bv = -pg*invv*pg.T
    cv = pg*uv
    ev = pg*invv*hg
    dv = (uv.T*hg)[0]
    Lvelocity = K*(cv.T*cv)[0]/2 \
        -U*(s.trace(bv*bv)-s.trace(bv)**2/3)/4 \
        -V*(s.trace(bv)-3)**2/12 \
        +P*((hg.T*(uv*uv.T-invv)*hg)[0]+a*dv*dv-(ev.T*ev)[0]) \
        +P*kv*kv*eps*eps*sv*sv/4
    rel = s.Matrix([pd-s.sqrt(lr)*sv,hd-g*sv])
    check('nonuniform_direct_ADM_shift_coupling',
          s.diff(Lvelocity,eps,2).subs(eps,0)/2,
          (rel.T*M*rel)[0]/2+P*kv*kv*sv*sv/4,
          'nonuniform_constraints')

    # Actual vector-shift Schur complement; both physical kinetic modes remain.
    A0,B0,C0,d1,d2,Q = s.symbols('A0 B0 C0 d1 d2 Q',real=True)
    M0 = s.Matrix([[A0,B0],[B0,C0]])
    vec = s.Matrix([d1,d2])
    den = Q+(vec.T*M0*vec)[0]  # Q=P k^2/2 >0
    Meff = M0-(M0*vec)*(vec.T*M0)/den
    vp,vh,shift = s.symbols('vp vh shift',real=True)
    velocities = s.Matrix([vp,vh])
    relative = velocities-vec*shift
    Lshift = (relative.T*M0*relative)[0]/2+Q*shift*shift/2
    shift_sol = s.solve(s.diff(Lshift,shift),shift)[0]
    check('nonuniform_vector_shift_equation_solution',shift_sol,
          (vec.T*M0*velocities)[0]/den,'nonuniform_constraints')
    check('nonuniform_vector_shift_reduced_action',Lshift.subs(shift,shift_sol),
          (velocities.T*Meff*velocities)[0]/2,'nonuniform_constraints')
    check('nonuniform_shift_reduced_determinant',Meff.det(),
          M0.det()*Q/den,'nonuniform_constraints')
    for i in range(2):
        for j in range(2):
            check('nonuniform_shift_high_k_limit_%s_%s' % (i,j),
                  s.limit(Meff[i,j],Q,s.oo),M0[i,j],
                  'nonuniform_constraints')
    check('nonuniform_flat_pair_restored',detS2.subs(g,0),
          group='nonuniform_controls')
    check('nonuniform_equal_moduli_still_unstable',detS2.subs(V,U),
          -4*P*P*g*g,'nonuniform_controls')
    condition('reject_nonuniform_fixed_H_only_verdict',
              simp(et.subs(V,U))==0 and detS2.subs(V,U).is_negative,
              'at U=V the fixed-H tangential stiffness vanishes but mixing is unstable',
              'nonuniform_controls')
    condition('reject_nonuniform_positive_characteristic_control',
              simp(speed2-2*P*g*g*(2/U+1/V)/(3*a))!=0,
              'reversing the physical characteristic sign is detected',
              'nonuniform_controls')


def main():
    rows = []

    def check(name, actual, expected=0, group='algebra'):
        residual = simp(actual-expected)
        rows.append(dict(name=name, group=group, passed=(residual == 0),
                         residual=str(residual)))

    def condition(name, value, certificate, group):
        rows.append(dict(name=name, group=group, passed=bool(value),
                         certificate=certificate))

    condition('article_hash', sha(ARTICLE) == EXPECTED_SHA,
              sha(ARTICLE), 'provenance')
    eps, dy = s.symbols('eps dy', real=True)
    a,b,c,d,e,f = s.symbols('a b c d e f', real=True)
    db = s.Matrix([[a,d,e],[d,b,f],[e,f,c]])
    polynomial = fmin(1+dy, s.eye(3)+db)
    factorized = (dy+s.trace(db))**2 + 16*db.det()
    check('full_Fmin_factorization', polynomial, factorized)
    hessian = s.hessian(polynomial, (dy,a,b,c,d,e,f))
    origin = dict.fromkeys((dy,a,b,c,d,e,f), 0)
    condition('silent_Hessian_rank_one', hessian.subs(origin).rank() == 1,
              str(hessian.subs(origin)), 'algebra')
    for j, variable in enumerate((dy,a,b,c,d,e,f)):
        check('silent_first_derivative_%s' % j,
              s.diff(polynomial,variable).subs(origin))
    check('quadratic_Fmin', s.expand(polynomial.subs(
        {v: eps*v for v in (dy,a,b,c,d,e,f)}, simultaneous=True)).coeff(eps,2),
        (dy+a+b+c)**2)

    # Calibrate the original article's EH sign before combining it with matter.
    t,x,y,zcoord = s.symbols('t x y z', real=True)
    wave = s.Function('q')(t)
    g = s.diag(1,-s.exp(wave),-s.exp(-wave),-1)
    curvature = ricci_scalar(g, (t,x,y,zcoord))
    check('article_TT_curvature_sign', curvature, -s.diff(wave,t)**2/2,
          'conventions')

    # Complete scalar quadratic action in unitary gauge; lapse/shift retained.
    M,k = s.symbols('M k', positive=True)
    C = s.symbols('C', real=True, nonzero=True)
    n,bshift,zeta,E,h = s.symbols('n bshift zeta E h', real=True)
    zd,ed,bd,nd,hd,zdd,edd = s.symbols('zd ed bd nd hd zdd edd', real=True)
    Q = n + 3*zeta - k*k*E - 2*h
    delta_yhat = -2*n-2*h
    delta_trace_bhat = -6*zeta+2*k*k*E+6*h
    check('normalized_scalar_invariants', delta_yhat+delta_trace_bhat, -2*Q,
          'scalar')
    # G has positive TT convention. The original article EH contribution is -G.
    G = M*M*(-3*zd*zd-2*k*k*zd*bshift+2*k*k*zd*ed
             +k*k*zeta*zeta+2*k*k*n*zeta)
    lag = -G - 4*C*Q*Q - M*M*k*k*h*h
    derivative_map = {n:nd,bshift:bd,zeta:zd,E:ed,h:hd,zd:zdd,ed:edd}
    def dt(expr):
        return sum(s.diff(expr,u)*v for u,v in derivative_map.items())
    velocities = {zeta:zd,E:ed}
    def el(q):
        return simp(s.diff(lag,q)-dt(s.diff(lag,velocities[q]))
                    if q in velocities else s.diff(lag,q))
    check('scalar_shift_constraint', el(bshift), 2*M*M*k*k*zd, 'scalar')
    check('scalar_label_constraint', el(E),
          8*C*k*k*Q+2*M*M*k*k*zdd, 'scalar')
    check('scalar_lapse_constraint', el(n), -2*M*M*k*k*zeta-8*C*Q, 'scalar')
    check('scalar_H_constraint', el(h), 16*C*Q-2*M*M*k*k*h, 'scalar')
    solutions = s.solve([el(n), el(E).subs(zdd,0), el(h)],
                        (n,zeta,h), dict=True)
    expected = {n:k*k*E, zeta:0, h:0}
    condition('unique_algebraic_scalar_constraints',
              len(solutions)==1 and all(simp(solutions[0][v]-q)==0
                                       for v,q in expected.items()),
              str(solutions), 'scalar')
    constraints = {**expected,zd:0,zdd:0,hd:0,nd:k*k*ed,
                   bd:edd-k*k*E}
    for q in (n,bshift,zeta,E,h):
        check('scalar_remaining_EL_%s' % q,
              el(q).subs(constraints, simultaneous=True), group='scalar')
    check('scalar_reduced_action_zero',
          lag.subs(constraints, simultaneous=True), group='scalar')

    # Independent vector constraint: changing shear stiffness does not add inertia.
    p,Ev,S,Ev_d,mu = s.symbols('p Ev S Ev_d mu', real=True)
    Lvec = -M*M*k*k*(Ev_d-S)**2/4 - mu*k*k*(p-Ev)**2/2
    Ssol = s.solve(s.diff(Lvec,S),S)[0]
    check('vector_shift_solution', Ssol, Ev_d, 'vector')
    check('vector_reduced_general_shear', Lvec.subs(S,Ssol),
          -mu*k*k*(p-Ev)**2/2, 'vector')
    check('vector_Fmin_reduced_zero', Lvec.subs({S:Ev_d,mu:0}), group='vector')

    # Nonlinear transverse witness, within B>0 for sufficiently small |v|<1.
    slope,v = s.symbols('slope v', real=True)
    gradients = s.Matrix([[1,0,slope],[0,1,0],[0,0,1]])
    vel = s.Matrix([v,0,0])
    B = gradients*gradients.T-vel*vel.T
    Fshear = simp(fmin(s.Integer(1),B))
    check('nonlinear_shear_Fmin', Fshear, (slope*slope-v*v)**2, 'nonlinear')
    check('nonlinear_shear_B_determinant', B.det(), 1-v*v, 'nonlinear')
    check('nonlinear_shear_velocity_Hessian', s.diff(-C*Fshear,v,2),
          4*C*(slope*slope-3*v*v), 'nonlinear')
    check('nonlinear_shear_quadratic_zero',
          s.expand(Fshear.subs({slope:eps*slope,v:eps*v})).coeff(eps,2),
          group='nonlinear')
    condition('nonlinear_interaction_not_identically_zero', Fshear != 0,
              str(Fshear), 'nonlinear')

    # Kinematic horizon gate in regular ingoing EF coordinates.
    ff,alpha,R,V,qR,qp = s.symbols('ff alpha R V qR qp', real=True)
    inv_ef = s.Matrix([[0,-1],[-1,-ff]])
    static_covector = s.Matrix([0,qp])
    static_radial = -(static_covector.T*inv_ef*static_covector)[0]
    check('static_horizon_radial_B', static_radial, ff*qp*qp, 'horizon')
    check('static_horizon_rank_loss', static_radial.subs(ff,0), group='horizon')
    clock = s.Matrix([1,-1])
    labels = s.Matrix([alpha,1])
    Y = (clock.T*inv_ef*clock)[0]
    Bradial = -(labels.T*inv_ef*labels)[0]
    check('flowing_horizon_Y', Y, 2-ff, 'horizon')
    check('flowing_horizon_Bradial', Bradial, ff+2*alpha, 'horizon')
    check('flowing_horizon_Btangential', (R+alpha*V)**2/R**2,
          (1+alpha*V/R)**2, 'horizon')
    witness = {ff:0, alpha:1, R:1, V:0}
    tangential = (R+alpha*V)**2/R**2
    condition('explicit_regular_horizon_domain_control',
              all(expr.subs(witness)>0 for expr in (Y,Bradial,tangential)),
              'ff=0, alpha=1, R=1, V=0 gives Y=2, B=diag(2,1,1)',
              'horizon')

    # Future amendment location only; not added to the selected action.
    dPhi = s.Matrix([1,0,0,0])
    inv_shift = s.Matrix([[1,-S,0,0],[-S,S*S-1,0,0],
                         [0,0,-1,0],[0,0,0,-1]])
    dlabel = s.Matrix([v,1,0,0])
    mixed = (dPhi.T*inv_shift*dlabel)[0]
    check('mixed_clock_label_invariant', mixed, v-S, 'amendment')
    check('mixed_transverse_quadratic', mixed*mixed, (v-S)**2, 'amendment')
    check('mixed_silent_value', (mixed*mixed).subs({v:0,S:0}), group='amendment')
    for variable in (v,S):
        check('mixed_silent_first_%s' % variable,
              s.diff(mixed*mixed,variable).subs({v:0,S:0}), group='amendment')
    aa,bb = s.symbols('aa bb', nonzero=True, real=True)
    modified_vector = aa*S*S+bb*(v-S)**2
    new_shift = s.solve(s.diff(modified_vector,S),S)[0]
    check('mixed_can_survive_shift_reduction', modified_vector.subs(S,new_shift),
          aa*bb*v*v/(aa+bb), 'amendment')
    # aa+bb=0 is a different constrained branch and is not divided through.
    condition('mixed_reduction_denominator_retained',
              s.denom(s.factor(new_shift)) == aa+bb,
              'requires aa+bb != 0; signs and full scalar health unselected',
              'amendment')

    # Negative controls use changed expressions against the same validators.
    condition('reject_inserted_vector_inertia',
              simp(Lvec.subs({S:Ev_d,mu:0})-v*v) != 0,
              'An inserted kinetic term fails the original reduced identity.',
              'negative_control')
    condition('reject_static_horizon_positive_rank',
              simp(static_radial.subs(ff,0)-1) != 0,
              'A positive static radial eigenvalue fails at ff=0.',
              'negative_control')
    condition('reject_shear_wrong_time_sign',
              simp(Fshear-(slope*slope+v*v)**2) != 0,
              'The changed nonlinear time sign is detected.',
              'negative_control')
    condition('reject_inconsistent_EH_sign',
              simp(curvature-s.diff(wave,t)**2/2) != 0,
              'Only an overall action sign reversal preserves relative signs.',
              'negative_control')

    completion_checks(check, condition)
    radial_exterior_checks(check, condition)
    two_H_operator_checks(check, condition)
    released_exterior_checks(check, condition)
    volume_source_checks(check, condition)
    nonuniform_volume_checks(check, condition)
    groups = {g: all(row['passed'] for row in rows if row['group']==g)
              for g in sorted({row['group'] for row in rows})}
    passed = all(row['passed'] for row in rows)
    basis = all(groups[g] for g in ('provenance','conventions','algebra'))
    completion_basis = basis and groups['completion_exterior']
    radial_auxiliary_ok = completion_basis and groups['completion_normalized'] \
        and groups['radial_conventions'] and groups['radial_auxiliary']
    radial_ghost = radial_auxiliary_ok and all(groups[g] for g in
        ('radial_kinetic','radial_witness','radial_limits','radial_negative_control'))
    two_ops_basis = completion_basis and groups['completion_normalized'] \
        and groups['completion_fallback'] and groups['radial_conventions']
    two_ops_exterior = two_ops_basis and groups['two_ops_exterior']
    two_ops_flat = two_ops_basis and groups['two_ops_flat']
    two_ops_excluded = two_ops_exterior and two_ops_flat and radial_ghost \
        and groups['two_ops_cases'] and groups['two_ops_negative_control']
    released_basis = basis and groups['completion_normalized'] \
        and groups['two_ops_flat'] and groups['released_negative_control']
    released_flat = released_basis and groups['released_flat_scalar'] \
        and groups['released_flat_vector_tensor']
    released_source = released_flat and groups['released_source']
    released_GR = released_source and groups['released_silent_GR'] \
        and groups['released_readout']
    volume_basis = released_basis and groups['released_source'] \
        and groups['completion_vector_tensor'] and groups['volume_invariant']
    volume_energy = volume_basis and groups['volume_scalar']
    volume_source = volume_energy and groups['volume_source']
    volume_match = volume_source and groups['volume_matching'] \
        and groups['volume_limits'] and groups['volume_negative_control'] \
        and groups['two_ops_exterior']
    nonuniform_basis = volume_match and groups['nonuniform_background'] \
        and groups['nonuniform_exterior'] and groups['released_silent_GR']
    nonuniform_instability = nonuniform_basis and groups['nonuniform_principal'] \
        and groups['nonuniform_constraints'] and groups['nonuniform_controls']
    out = dict(
        status='EXACT_DIAGNOSTIC_VERIFIED' if passed else 'VERIFICATION_FAILED',
        python=platform.python_version(), sympy=s.__version__,
        article_sha256=sha(ARTICLE), contract_sha256=sha(CONTRACT),
        verifier_sha256=sha(Path(__file__)),
        check_count=len(rows), groups=groups, checks=rows,
        closure_flags=dict(
            Fmin_constrained_quadratic_degeneracy_verified=all(
                groups[g] for g in ('provenance','conventions','scalar','vector','nonlinear')),
            static_label_horizon_obstruction_verified=basis and groups['horizon'],
            flowing_labels_kinematically_admissible=basis and groups['horizon'],
            amendment_location_only_identified=basis and groups['amendment'],
            direct_completion_quadratic_scalar_ghost_verified=completion_basis
                and groups['scalar'] and groups['completion_scalar'],
            constant_Z_fallback_lapse_rank_change_verified=completion_basis
                and groups['completion_fallback'] and groups['completion_nonlinear'],
            normalized_clock_primary_degeneracy_verified=completion_basis
                and groups['completion_normalized'],
            nonzero_gradient_H_constraint_warning_verified=completion_basis
                and groups['completion_normalized'] and groups['completion_gradient_warning'],
            F3_radial_auxiliary_reduction_verified=radial_auxiliary_ok,
            F3_exterior_quadratic_ghost_verified=radial_ghost,
            F3_rejected_on_exterior_branch=radial_ghost,
            two_H_operators_exterior_b_zero_verified=two_ops_exterior,
            two_H_operators_flat_H_energy_verified=two_ops_flat,
            two_H_operators_no_healthy_fixed_exterior_pair=two_ops_excluded,
            released_exterior_flat_physical_quadratic_energy_verified=released_flat,
            released_exterior_leading_Newtonian_source_verified=released_source,
            released_exterior_linear_H_source_absence_verified=released_source,
            released_exterior_exact_static_silent_GR_branch_verified=released_GR,
            released_exterior_intended_H_pressure_bridge_derived=False,
            released_exterior_full_PPN_inherited=False,
            volume_response_flat_quadratic_energy_verified=volume_energy,
            volume_metric_mediated_H_source_verified=volume_source,
            volume_b_minus_one_leading_common_scale_verified=volume_match,
            volume_old_exact_exponential_exterior_excluded=volume_match,
            volume_bulk_coefficient_microscopically_derived=False,
            volume_full_W51_static_1PN_inherited=False,
            volume_own_second_order_weak_background_verified=nonuniform_basis,
            volume_regular_source_transverse_gradient_instability=nonuniform_instability,
            volume_regular_source_continuum_health_gate_failed=nonuniform_instability,
            volume_instability_below_physical_EFT_cutoff_proved=False,
            active_healthy_strong_field_candidate_selected=False,
            nonlinear_constraint_closure_proved=False,
            full_coupled_health_proved=False,
            nonlinear_ghost_proved=False,
            full_RefG_no_go_proved=False,
            new_response_selected=volume_match,
            official_theory_response_promoted=False,
            action_derived_regular_interior=False,
            singularity_free_black_hole=False,
            formation_and_stability_proved=False,
            observational_pass=False),
        decision=('On the candidate own regular weak sourced branch, the '
                  'coupled H/transverse-label sector has positive kinetic '
                  'energy but a negative squared principal characteristic. '
                  'The leading spatial determinant is negative for all finite '
                  'positive P,K,U,V,a with nonzero gradient. This branch fails '
                  'the two-derivative continuum health gate; no physical EFT '
                  'cutoff or observational instability has been established.'
                  if nonuniform_instability and passed
                  else 'Verification incomplete or failed.'))
    print(json.dumps(out,indent=2,ensure_ascii=True))
    return 0 if passed else 1


def scale_feedback_main():
    '''Stage 8 only: fixed supported shell, new static extension, stdout only.'''
    import mpmath as mp
    mp.mp.dps = 70
    rows = []

    def exact(name, actual, expected=0):
        residual = simp(actual-expected)
        rows.append(dict(name=name, passed=bool(residual == 0),
                         residual=str(residual)))

    def test(name, value, evidence):
        rows.append(dict(name=name, passed=bool(value), evidence=str(evidence)))

    dependencies = {
        'intuitive/RefG_GE.md': INTUITIVE_GE_SHA,
        'RefG/work 3/Lagrangian_Formulation/Weak_Field_Closure/'
        'w3_51_weak_field_closure_contract.md':
            '86bc2ed86cddee36bec5e46fdfa407701107290c783bfa81ba1440b96becc7cf',
        'RefG/work 3/Strong_Field/W3-79_Collective_Current_Backreaction/'
        'w3_79_collective_current_backreaction_contract.md':
            '7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa',
    }
    observed = {path: sha(ROOT/path) for path in dependencies}
    for path, expected in dependencies.items():
        test('source_hash:'+path, observed[path] == expected, observed[path])

    u,B,k,c,G,R,m0,r,rhob = s.symbols(
        'u B k c G R m0 r rhob', positive=True)
    v = s.symbols('v', real=True)
    p = s.exp(-u)
    lag_pp = -m0*p*s.sqrt(1-v*v/p**4)  # c=1
    exact('rest_Killing_energy', (v*s.diff(lag_pp,v)-lag_pp).subs(v,0), m0*p)
    exact('coordinate_inertia', s.diff(lag_pp,v,2).subs(v,0), m0/p**3)
    rho,P1,P2,P3 = s.symbols('rho P1 P2 P3', real=True)
    metric = [-p*p,p**(-2),p**(-2),p**(-2)]
    Tupper = [rho/p**2,P1*p**2,P2*p**2,P3*p**2]
    restricted_variation = p**(-2)*sum(
        tij*s.diff(gij,u) for tij,gij in zip(Tupper,metric))/2
    exact('restricted_Hilbert_variation', restricted_variation,
          (rho+P1+P2+P3)/p**2)
    exact('rest_dust_source', restricted_variation.subs(
        {rho:p**3*rhob,P1:0,P2:0,P3:0}), p*rhob)

    # Vary the radial bulk integrand before applying a shell ansatz.
    uf = s.Function('u')(r)
    rb = s.Function('rho_b')(r)
    radial = c**4*r*r*s.diff(uf,r)**2/(2*G) + 4*s.pi*r*r*rb*c*c*s.exp(-uf)
    euler = s.diff(radial,uf)-s.diff(s.diff(radial,s.diff(uf,r)),r)
    target = s.diff(uf,r,2)+2*s.diff(uf,r)/r+4*s.pi*G*rb*s.exp(-uf)/c**2
    exact('varied_nonlinear_Poisson', euler, -c**4*r*r*target/G)
    # Shell jump: R^2 u_out_prime=-u_s R, zero interior derivative.
    exact('shell_flux_balance', (-u*R+G*B*p/c**2).subs(
        B,u*s.exp(u)*R*c**2/G), 0)
    exterior = u*R/r
    exact('vacuum_Laplace', s.diff(exterior,r,2)+2*s.diff(exterior,r)/r)
    field_energy_mass = s.integrate(
        c*c*r*r*s.diff(exterior,r)**2/(2*G), (r,R,s.oo))
    exact('independent_field_energy', field_energy_mass, c*c*R*u*u/(2*G))

    energy = u*u/(2*k)+B*p  # E_stat/c^2, no additional rest-mass copy
    force = s.diff(energy,u)
    on = {B:u*s.exp(u)/k}
    exact('shell_energy_stationary', force.subs(on))
    exact('shell_positive_Hessian', s.diff(energy,u,2).subs(on), (1+u)/k)
    test('strict_static_minimum', ((1+u)/k).is_positive, '(1+u)/k>0')
    du = -s.diff(force,B)/s.diff(force,u)  # implicit derivative through E_uu
    du = simp(du.subs(on))
    exact('implicit_common_response', du, k*p/(1+u))
    dp = s.diff(p,u)*du
    exact('every_constituent_response', dp, -k*p*p/(1+u))
    mass = B*p
    dmass = (s.diff(mass,B)+s.diff(mass,u)*du).subs(on)
    exact('whole_ensemble_derivative', dmass, p/(1+u))
    exact('missing_old_ensemble_term', (B*dp).subs(on), -u*p/(1+u))
    d2mass = s.diff(simp(dmass),u)*du
    exact('source_concavity', d2mass, -k*p*p*(u+2)/(1+u)**3)
    denergy = s.diff(energy,B)+s.diff(energy,u)*du
    exact('full_energy_envelope', denergy.subs(on), p)
    exact('energy_concavity', s.diff(p,u)*du, -k*p*p/(1+u))
    exact('on_shell_energy', energy.subs(on), (u+u*u/2)/k)
    test('individual_decreases', dp.is_negative, str(dp))
    test('total_source_increases', simp(dmass).is_positive, str(dmass))
    test('source_increment_decreases', simp(d2mass).is_negative, str(d2mass))
    # Parametrization u>0 proves unboundedness; do not infer it from a scan.
    test('unbounded_population', s.limit(u*s.exp(u)/k,u,s.oo) == s.oo,
         'B=u exp(u)/k is increasing and unbounded')
    test('unbounded_Gauss_charge', s.limit(u/k,u,s.oo) == s.oo, 'M_G=u/k')
    test('unbounded_trial_energy', s.limit((u+u*u/2)/k,u,s.oo) == s.oo,
         'E/c^2=(u+u^2/2)/k')
    test('zero_slope_not_cap', s.limit(p/(1+u),u,s.oo) == 0, 'positive slope -> 0')
    test('finite_positive_clock', p.is_positive, 'exp(-u)>0 at finite u')

    mg = s.symbols('M_G', positive=True)
    Uext = G*mg/(c*c*r)
    spatial_factor = s.exp(2*Uext)
    adm_surface = -c*c*r*r*s.diff(spatial_factor,r)/(2*G)
    exact('geometric_ADM_surface_limit', s.limit(adm_surface,r,s.oo), mg)
    exact('energy_ADM_gap', energy.subs(on)-u/k, u*u/(2*k))
    test('positive_energy_ADM_gap', (u*u/(2*k)).is_positive, 'nonzero source')
    exact('outgoing_radial_null_speed',
          s.sqrt(s.exp(-2*Uext)/s.exp(2*Uext)), s.exp(-2*Uext))
    areal = r*s.exp(Uext)
    extremum = G*mg/c**2
    exact('areal_extremum', s.diff(areal,r).subs(r,extremum))
    exact('areal_extremum_has_nonzero_lapse',
          s.exp(-Uext).subs(r,extremum), s.exp(-1))

    # Negative controls use the same equilibrium/envelope/source identities.
    test('reject_frozen_source', simp(force.subs(u,k*B)) != 0,
         str(simp(force.subs(u,k*B))))
    test('reject_double_p_source', simp((u-k*B*p*p).subs(on)) != 0,
         str(simp((u-k*B*p*p).subs(on))))
    test('reject_omit_field_energy', simp(dmass-p) != 0, str(simp(dmass-p)))
    test('reject_update_last_only', simp(p-dmass) != 0, str(simp(p-dmass)))
    test('reject_second_rest_mass', simp(denergy.subs(on)+1-p) != 0, '1')

    def direct_root(q):
        lo,hi = mp.mpf(0),mp.log1p(q)
        for _ in range(320):
            mid = (lo+hi)/2
            if mid-q*mp.exp(-mid) > 0:
                hi = mid
            else:
                lo = mid
        return (lo+hi)/2

    def direct_energy(q):
        z = direct_root(q)
        return z*z/2+q*mp.exp(-z)

    numerical = []
    for qtext in ('0.001','0.1','1','10','100','1000000'):
        q = mp.mpf(qtext)
        z = direct_root(q)
        reference = mp.lambertw(q)
        pp = mp.exp(-z)
        es = direct_energy(q)
        errs = [abs(z-reference), abs(z-q*pp), abs(es-z-z*z/2)]
        test('numerical_root_energy:'+qtext, max(errs) < mp.mpf('1e-55'),
             [mp.nstr(e,12) for e in errs])
        differences = {}
        for label, fun, expected in (
            ('energy', direct_energy, pp),
            ('Gauss', direct_root, pp/(1+z))):
            errors = []
            for rel in ('1e-4','5e-5'):
                step = q*mp.mpf(rel)
                derivative = (fun(q+step)-fun(q-step))/(2*step)
                errors.append(abs(derivative-expected)/abs(expected))
            test('finite_difference:'+label+':'+qtext,
                 max(errors) < mp.mpf('1e-7') and
                 (max(errors) < mp.mpf('1e-40') or errors[1]/errors[0] < mp.mpf('0.3')),
                 [mp.nstr(e,12) for e in errors])
            differences[label] = [mp.nstr(e,12) for e in errors]
        numerical.append(dict(q=qtext, u=mp.nstr(z,16), p=mp.nstr(pp,16),
                              k_MG=mp.nstr(z,16), k_E_over_c2=mp.nstr(es,16),
                              dMG_dB=mp.nstr(pp/(1+z),16),
                              derivative_relative_errors=differences))

    passed = all(row['passed'] for row in rows)
    print(json.dumps(dict(
        status='CONDITIONAL_STATIC_FEEDBACK_VERIFIED' if passed else 'VERIFICATION_FAILED',
        scope='New fixed-source static extension of W51; Stage 7 is a different action',
        python=platform.python_version(), sympy=s.__version__, mpmath=mp.__version__,
        source_sha256=observed, contract_sha256=sha(CONTRACT),
        verifier_sha256=sha(Path(__file__)), check_count=len(rows),
        checks=rows, numerical=numerical,
        closure_flags=dict(
            conditional_all_constituent_feedback_verified=passed,
            trial_energy_and_geometric_mass_mismatch_verified=passed,
            finite_mass_cap=False, event_horizon=False,
            covariant_completion=False, supported_source_stress_closed=False,
            dynamical_stability=False, singularity_free_black_hole=False,
            observational_pass=False, official_theory_changed=False),
        decision='All constituents weaken while the total Gauss source grows '
                 'sublinearly without a finite cap. The complete static energy '
                 'differs from the attached metric ADM charge. This is not '
                 'a closed covariant black-hole model.'
                 if passed else 'Verification failed; inspect individual checks.'),
        indent=2, ensure_ascii=True))
    return 0 if passed else 1


def full_static_balance_main():
    '''Stage 9: independent full static variations, not an interior solver.'''
    rows = []

    def exact(name, actual, expected=0):
        residual = simp(actual-expected)
        rows.append(dict(name=name, passed=bool(residual == 0),
                         residual=str(residual)))

    def truth(name, value, evidence):
        rows.append(dict(name=name, passed=bool(value), evidence=str(evidence)))

    core_path = ROOT / ('RefG/work 3/Lagrangian_Formulation/'
        'One_Oscillon_Coframe_Localized_Core/'
        'w3_58_one_oscillon_coframe_localized_core_preregistration.md')
    truth('article_hash', sha(ARTICLE) == EXPECTED_SHA, sha(ARTICLE))
    truth('matter_action_hash', sha(core_path) ==
          'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db',
          sha(core_path))
    r,m,G,R0,P,Q,wh,om,ms,lam,g6 = s.symbols(
        'r m G R0 P Q omega_H Omega m_O lam g6', positive=True)
    n,a,ss = s.symbols('N A S', positive=True)
    h,ell,ellp,hp,x,xp = s.symbols('H ell ellp Hp chi chip', real=True)
    yy,lr,lt = s.symbols('y lr lt', positive=True)
    ff = s.Function('Fbar')(yy,lr,lt)
    invariant = {yy:s.exp(-2*h)/n**2,
                 lr:s.exp(2*h)*ellp**2/a**2,
                 lt:s.exp(2*h)*ell**2/ss**2}

    def put(expr):
        return expr.subs(invariant, simultaneous=True)

    Fy,Fr,Ft = (s.diff(ff,q) for q in (yy,lr,lt))
    Z = hp**2/a**2
    V = ms**2*x*x/2-lam*x**4/4+g6*x**6/6
    T,X = om**2*x*x/(2*n*n),xp*xp/(2*a*a)
    lm = n*a*ss*ss*(T-X-V)
    lf = n*a*ss*ss*(Q*put(ff)+wh*P*Z)
    matter = [T+X+V,T+X-V,T-X-V]
    medium = [Q*put(2*yy*Fy-ff)-wh*P*Z,
              Q*put(ff-2*lr*Fr)-wh*P*Z,
              Q*put(ff-lt*Ft)+wh*P*Z]
    for label,lag,stress in [('ordinary',lm,matter),('medium',lf,medium)]:
        for name,variable,target in [
            ('lapse',n,-a*ss*ss*stress[0]),
            ('radial',a,n*ss*ss*stress[1]),
            ('angular',ss,2*n*a*ss*stress[2])]:
            exact(label+'_'+name+'_Hilbert',s.diff(lag,variable),target)
    exact('ordinary_has_no_direct_H_source',s.diff(lm,h))
    exact('ordinary_charge_density',s.diff(lm,om),a*ss*ss*om*x*x/n)
    exact('ordinary_local_frequency',2*T/x**2,om**2/n**2)
    combo = put(yy*Fy-lr*Fr-lt*Ft)
    exact('independent_H_algebraic_vertex',s.diff(lf,h),-2*Q*n*a*ss*ss*combo)
    exact('independent_H_gradient_vertex',s.diff(lf,hp),2*wh*P*n*ss*ss*hp/a)
    exact('label_gradient_vertex',s.diff(lf,ellp),
          2*Q*n*ss*ss*s.exp(2*h)*ellp*put(Fr)/a)
    exact('label_algebraic_vertex',s.diff(lf,ell),
          2*Q*n*a*s.exp(2*h)*ell*put(Ft))

    N,A,S,H,L,C = [s.Function(z)(r) for z in ('N','A','S','H','ell','chi')]
    mapping = {n:N,a:A,ss:S,h:H,ell:L,ellp:s.diff(L,r),
               hp:s.diff(H,r),x:C,xp:s.diff(C,r)}

    def radial(expr):
        return expr.subs(mapping, simultaneous=True)

    def EL(lag,field):
        return s.diff(lag,field)-s.diff(s.diff(lag,s.diff(field,r)),r)

    Lg=P*(N*A+N*s.diff(S,r)**2/A+2*s.diff(N,r)*S*s.diff(S,r)/A)
    Lm,Lf=radial(lm),radial(lf)
    Eg={field:simp(EL(Lg,field)) for field in (N,A,S)}
    scalar_eq=s.diff(N*S*S*s.diff(C,r)/A,r)+N*A*S*S*(
        om**2*C/N**2-radial(s.diff(V,x)))
    exact('ordinary_full_amplitude_EL',EL(Lm,C),scalar_eq)
    rhoO,prO,ptO=map(radial,matter)
    conservation=s.diff(prO,r)+(rhoO+prO)*s.diff(N,r)/N+2*(prO-ptO)*s.diff(S,r)/S
    exact('ordinary_conservation_from_EL',conservation,
          s.diff(C,r)*scalar_eq/(N*A*S*S))
    qh=-N*S*S*s.diff(H,r)/A
    H_eq=s.diff(qh,r)-Q*N*A*S*S*radial(combo)/(wh*P)
    exact('independent_full_H_EL',EL(Lf,H),2*wh*P*H_eq)
    label_eq=s.diff(N*S*S*s.exp(2*H)*s.diff(L,r)*radial(put(Fr))/A,r) \
        -N*A*s.exp(2*H)*L*radial(put(Ft))
    exact('independent_full_label_EL',EL(Lf,L),-2*Q*label_eq)

    # Fresh 4D curvature with N,A,S still independent.
    t,th,ph=s.symbols('t theta phi', real=True)
    coords=[t,r,th,ph]
    metric=s.diag(-N*N,A*A,S*S,S*S*s.sin(th)**2)
    inv=metric.inv()
    conn=[[[simp(sum(inv[i,l]*(s.diff(metric[l,j],coords[k])
                +s.diff(metric[l,k],coords[j])-s.diff(metric[j,k],coords[l]))
                for l in range(4))/2) for k in range(4)]
                for j in range(4)] for i in range(4)]
    ric=s.Matrix(4,4,lambda i,j:simp(sum(
        s.diff(conn[k][i][j],coords[k])-s.diff(conn[k][i][k],coords[j])
        +sum(conn[k][i][j]*conn[l][k][l]-conn[l][i][k]*conn[k][j][l]
             for l in range(4)) for k in range(4))))
    curv=simp(s.trace(inv*ric))
    ein=(ric-metric*curv/2).applyfunc(simp)
    geometric=[simp(ein[0,0]/N**2),simp(ein[1,1]/A**2),
               simp(ein[2,2]/S**2)]
    exact('unrestricted_lapse_vs_curvature',Eg[N],P*A*S*S*geometric[0])
    exact('unrestricted_radial_vs_curvature',Eg[A],-P*N*S*S*geometric[1])
    exact('unrestricted_angular_vs_curvature',Eg[S],-2*P*N*A*S*geometric[2])
    exact('static_metric_momentum_constraint',ein[0,1])
    for field,factor,index in ((N,-A*S*S,0),(A,N*S*S,1),(S,2*N*A*S,2)):
        exact('complete_metric_EL_'+str(field),EL(Lg+Lm+Lf,field),
              Eg[field]+factor*radial(matter[index]+medium[index]))
    # Static spherical raw spatial-curvature term and its surface derivative.
    R3=2/S**2*(1-s.diff(S,r)**2/A**2-2*S*s.diff(S,r,2)/A**2
                +2*S*s.diff(S,r)*s.diff(A,r)/A**3)
    raw=P*N*A*S*S*R3/2
    boundary=2*P*N*S*s.diff(S,r)/A
    exact('radial_boundary_accounting',raw-Lg+s.diff(boundary,r))
    exact('spatial_curvature_lapse_constraint',R3/2,geometric[0])

    # Full covariant clock/phase/momentum equations on the declared zero-flux sector.
    cross,gi00,girr=s.symbols('gtr gtt grr',real=True)
    projected=(cross*hp)**2/gi00-girr*hp**2
    exact('projected_momentum_vertex_zero',
          s.diff(projected,cross).subs(cross,0))
    exact('projected_clock_vertex_zero',
          s.diff(projected,gi00).subs(cross,0))
    phi1=C*s.cos(om*t)
    phi2=C*s.sin(om*t)
    exact('ordinary_radial_momentum_zero',s.diff(phi1,t)*s.diff(phi1,r)
          +s.diff(phi2,t)*s.diff(phi2,r))
    exact('ordinary_phase_divergence_zero',s.diff(A*S*S*C*C*om/N,t))
    clock_time=radial(Q*s.exp(-2*h)*put(Fy)/n**2)
    exact('full_static_clock_divergence_zero',s.diff(N*A*S*S*clock_time,t))

    # Post-variation exterior. Silent F has zero value and ALL first derivatives.
    u=m/r
    ext={N:s.exp(-u),A:s.exp(u),S:r*s.exp(u),H:u,L:r,C:0}
    LH=wh*P*N*S*S*s.diff(H,r)**2/A
    LHstress=[-wh*P*s.diff(H,r)**2/A**2,
              -wh*P*s.diff(H,r)**2/A**2,wh*P*s.diff(H,r)**2/A**2]
    ext_stress=[]
    for i,name in enumerate(('rho','pr','pt')):
        got=simp(LHstress[i].subs(ext).subs(wh,1).doit())
        ext_stress.append(got)
        exact('exterior_full_Einstein_'+name,
              P*geometric[i].subs(ext).doit(),got)
    for field in (N,A,S,H):
        exact('exterior_independent_EL_'+str(field),
              EL(Lg+LH,field).subs(ext).subs(wh,1).doit())
    exact('exterior_H_flux',qh.subs(ext).doit(),m)
    exact('exterior_H_flux_equation',s.diff(qh,r).subs(ext).doit())
    exact('exterior_silent_clock_invariant',radial(invariant[yy]).subs(ext).doit(),1)
    exact('exterior_silent_radial_invariant',radial(invariant[lr]).subs(ext).doit(),1)
    exact('exterior_silent_tangential_invariant',radial(invariant[lt]).subs(ext).doit(),1)
    exact('exterior_Komar_source_combo',ext_stress[0]+ext_stress[1]+2*ext_stress[2])
    komar=S*S*s.diff(N,r)/(G*A)
    exact('exterior_Komar_mass',komar.subs(ext).doit(),m/G)
    adm=-r*r*s.diff(s.exp(2*u),r)/(2*G)
    exact('exterior_ADM_mass',s.limit(adm,r,s.oo),m/G)

    # Diagnose Stage 8, keeping the independent lapse constraint.
    U=s.Function('u')(r)
    rb=s.Function('rho_b')(r)
    lap=s.diff(U,r,2)+2*s.diff(U,r)/r
    R3iso=s.exp(-2*U)*(-4*lap-2*s.diff(U,r)**2)
    Nconstraint=-s.exp(2*U)*R3iso/(16*s.pi*G)+rb*s.exp(-U)
    trial={s.diff(U,r,2):-2*s.diff(U,r)/r-4*s.pi*G*rb*s.exp(-U)}
    old_res=simp(Nconstraint.subs(trial))
    exact('trial_unsatisfied_constraint',old_res,s.diff(U,r)**2/(8*s.pi*G))
    weightedH=-s.diff(U,r)**2/(8*s.pi*G)
    exact('existing_H_restores_metric_constraint',old_res+weightedH)
    gap=s.integrate(4*s.pi*r*r*old_res.subs(U,m/r).doit(),(r,R0,s.oo))
    exact('entire_old_gap_accounted',gap,m*m/(2*G*R0))
    a0,b0=s.Function('a0')(r),s.Function('b0')(r)
    Lis=r*r*s.exp(a0+b0)*(2*s.diff(a0,r)*s.diff(b0,r)+s.diff(b0,r)**2)/(8*s.pi*G)
    Eaa=simp(EL(Lis,a0).subs({a0:-m/r,b0:m/r}).doit())
    Ebb=simp(EL(Lis,b0).subs({a0:-m/r,b0:m/r}).doit())
    exact('retained_combination_only',Ebb-Eaa)
    exact('lost_independent_lapse_value',Eaa,-m*m/(8*s.pi*G*r*r))
    truth('reject_impose_scaling_before_variation',Eaa != 0 and Ebb != 0,
          'restricted EL vanishes but independent metric ELs do not')
    truth('reject_omit_actual_medium',simp(P*geometric[0].subs(ext).doit()) != 0,
          'exterior lapse is not vacuum in this geometry')
    wrong=simp((P*geometric[0].subs(ext).doit()-ext_stress[0])+
               P*s.exp(-2*u)*m*m/r**4)
    truth('reject_duplicate_positive_gradient_source',wrong != 0,str(wrong))

    # Integral jump test; no distribution product convention is needed.
    flux_inside=simp(qh.subs({N:s.exp(-m/R0),A:s.exp(m/R0),
                              S:r*s.exp(m/R0),H:m/R0}).doit())
    flux_outside=simp(qh.subs(ext).doit())
    exact('shell_inner_flux',flux_inside)
    exact('shell_outer_flux',flux_outside,m)
    jump=simp(flux_outside-flux_inside)
    exact('shell_integrated_H_residual',jump,m)
    truth('reject_shell_without_H_source',jump.is_positive,
          'jump=m>0; silent F and minimal matter have zero direct H source')
    C0=s.symbols('C0',real=True)
    harmonic=C0+m/r
    exact('silent_harmonic_H_equation',
          s.diff(r*r*s.diff(harmonic,r),r))
    exact('silent_central_pole_coefficient',s.limit(r*harmonic,r,0,dir='+'),m)
    truth('regular_silent_core_forces_zero_flux',
          s.limit(harmonic,r,0,dir='+') == s.oo,
          'm/r is unbounded at the centre for m>0; regular harmonic branch has m=0')

    passed=all(row['passed'] for row in rows)
    print(json.dumps(dict(
        status='INDEPENDENT_STATIC_SOURCE_BALANCE_VERIFIED' if passed else 'VERIFICATION_FAILED',
        python=platform.python_version(),sympy=s.__version__,
        article_sha256=sha(ARTICLE),matter_sha256=sha(core_path),
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),
        check_count=len(rows),checks=rows,
        closure_flags=dict(
            independent_static_equations_verified=passed,
            old_gap_equals_unsatisfied_constraint=passed,
            existing_medium_exterior_balance_restored=passed,
            unchanged_shell_excluded_by_H_flux=passed,
            action_derived_regular_interior=False,full_coupled_health=False,
            singularity_free_black_hole=False,observational_pass=False,
            new_constitutive_law_selected=False,official_theory_changed=False),
        decision='Independent variations restore the actual medium source and '
                 'the exterior mass balance. The old shell still violates '
                 'the independent H-flux equation; a regular nonsilent interior '
                 'response has not been selected or solved.'
                 if passed else 'Verification failed; inspect residuals.'),
        indent=2,ensure_ascii=True))
    return 0 if passed else 1


def centre_response_main():
    '''Stage 10: leading central jet and nondegenerate principal-cone gate.'''
    rows=[]

    def exact(name,actual,expected=0):
        residual=simp(actual-expected)
        rows.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))

    def truth(name,value,evidence):
        rows.append(dict(name=name,passed=bool(value),evidence=str(evidence)))

    truth('article_hash',sha(ARTICLE)==EXPECTED_SHA,sha(ARTICLE))
    intuitive=ROOT/'intuitive/RefG_GE.md'
    truth('intuitive_hash',sha(intuitive)==INTUITIVE_GE_SHA,
          sha(intuitive))
    r,y,b,P,Q,wh,Nc=s.symbols('r y b P Q omega_H Nc',positive=True)
    cf=s.symbols('cF',real=True,nonzero=True)
    yy,lr,lt=s.symbols('yy lr lt',positive=True)
    ff=cf*fmin(yy,s.diag(lr,lt,lt))
    exact('original_polynomial_folded',ff,
          cf*((yy+lr+2*lt-4)**2+16*(lr-1)*(lt-1)**2))
    iso={yy:y,lr:b,lt:b}
    Fy,Fr,Ft=[s.diff(ff,z) for z in (yy,lr,lt)]
    f0,fy0,fr0,ft0=[simp(z.subs(iso)) for z in (ff,Fy,Fr,Ft)]
    d=y+3*b-4
    DD=2*d+16*(b-1)**2
    JJ=simp((yy*Fy-lr*Fr-lt*Ft).subs(iso))
    KK=y+8*b*b-11*b+4
    exact('central_source',JJ,cf*(2*y*d-3*b*DD))
    exact('isotropic_folded_derivative',ft0,2*fr0)
    exact('central_F_value',f0,cf*(d*d+16*(b-1)**3))
    exact('central_F_radial_derivative',fr0,cf*DD)
    rhoF=Q*(2*y*fy0-f0)
    pF=Q*(f0-2*b*fr0)
    exact('central_pressure_isotropy',pF,Q*(f0-b*ft0))

    a2,n2,h2,z3,c2,cc,ww,ms,lam,g6=s.symbols(
        'a2 n2 h2 z3 chi2 chic omega_local mO lam g6',real=True)
    V=ms**2*cc**2/2-lam*cc**4/4+g6*cc**6/6
    rho=ww**2*cc**2/2+V+rhoF
    pressure=ww**2*cc**2/2-V+pF
    NN=Nc*(1+n2*r*r)
    AA=1+a2*r*r
    HH=h2*r*r
    jet={yy:y*(1-2*(h2+n2)*r*r),
         lr:b*(1+(2*h2+6*z3-2*a2)*r*r),
         lt:b*(1+(2*h2+2*z3)*r*r)}
    rawinv=[y*s.exp(-2*HH)/(1+n2*r*r)**2,
            b*s.exp(2*HH)*(1+3*z3*r*r)**2/AA**2,
            b*s.exp(2*HH)*(1+z3*r*r)**2]
    for name,z,raw in zip(('clock','radial','tangential'),(yy,lr,lt),rawinv):
        exact('jet_'+name,s.series(raw,r,0,4).removeO(),jet[z])

    geomrho=(1-1/AA**2+2*r*s.diff(AA,r)/AA**3)/r**2
    geompr=(1/AA**2-1)/r**2+2*s.diff(NN,r)/(NN*AA**2*r)
    geompt=(s.diff(NN,r,2)/(NN*AA**2)
            -s.diff(NN,r)*s.diff(AA,r)/(NN*AA**3)
            +s.diff(NN,r)/(NN*AA**2*r)-s.diff(AA,r)/(AA**3*r))
    exact('central_density_equation',s.limit(geomrho,r,0),6*a2)
    exact('central_radial_equation',s.limit(geompr,r,0),4*n2-2*a2)
    exact('central_angular_equation',s.limit(geompt,r,0),4*n2-2*a2)
    exact('central_H_gradient_stress_zero',
          s.limit(s.diff(HH,r)**2/AA**2,r,0))
    flux=-NN*r*r*s.diff(HH,r)/AA
    exact('central_H_flux_coefficient',s.limit(flux/r**3,r,0),-2*Nc*h2)
    exact('central_H_equation',
          s.limit((s.diff(flux,r)-Q*NN*AA*r*r*JJ/(wh*P))/r**2,r,0),
          -Nc*(6*h2+Q*JJ/(wh*P)))
    CJ=cc+c2*r*r
    scalar=s.diff(NN*r*r*s.diff(CJ,r)/AA,r)+NN*AA*r*r*(
        (ww*Nc)**2*CJ/NN**2-s.diff(V,cc).subs(cc,CJ))
    exact('central_ordinary_equation',s.limit(scalar/(Nc*r*r),r,0),
          6*c2+ww**2*cc-s.diff(V,cc))
    frj=s.series(Fr.subs(jet,simultaneous=True),r,0,4).removeO()
    ftj=s.series(Ft.subs(jet,simultaneous=True),r,0,4).removeO()
    label=s.diff(r*r*(1+(n2+2*h2+3*z3-a2)*r*r)*frj,r) \
        -r*(1+(n2+a2+2*h2+z3)*r*r)*ftj
    exact('label_lowest_order_cancels',s.expand(label).coeff(r,1))
    label3=4*cf*(5*KK*z3-(3*y+8*b*b-21*b+12)*a2
                     +(-y+8*b*b-13*b+4)*n2+4*(12*b*b-13*b+2)*h2)
    exact('label_next_order',s.expand(label).coeff(r,3),label3)
    Kpos=y+8*(b-s.Rational(11,16))**2+s.Rational(7,32)
    exact('central_label_completed_square',KK,Kpos)
    truth('central_label_denominator_positive',Kpos.is_positive,Kpos)
    residuals=s.Matrix([6*P*a2-rho,4*P*n2-2*P*a2-pressure,
                       6*wh*P*h2+Q*JJ,6*c2+ww**2*cc-s.diff(V,cc),label3])
    variables=(a2,n2,h2,c2,z3)
    exact('central_coefficient_determinant',residuals.jacobian(variables).det(),
          17280*P**3*cf*wh*KK)
    solution={a2:rho/(6*P),n2:(rho+3*pressure)/(12*P),
              h2:-Q*JJ/(6*wh*P),c2:(s.diff(V,cc)-ww**2*cc)/6}
    solution[z3]=simp(((3*y+8*b*b-21*b+12)*a2+
          (y-8*b*b+13*b-4)*n2-4*(12*b*b-13*b+2)*h2).subs(solution)/(5*KK))
    for variable,residual in zip(variables,residuals):
        exact('solved_central_'+str(variable),residual.subs(solution))
    kretsch=4*((s.diff(NN,r,2)/(NN*AA**2)-
                s.diff(NN,r)*s.diff(AA,r)/(NN*AA**3))**2
               +2*(s.diff(NN,r)/(NN*AA**2*r))**2
               +2*(s.diff(AA,r)/(AA**3*r))**2
               +((1-1/AA**2)/r**2)**2)
    exact('central_curvature_finite_coefficient',
          s.limit(kretsch,r,0),48*(n2*n2+a2*a2))

    eps,td,tz,wd,wz,vt,vz=s.symbols('eps td tz wd wz vt vz',real=True)
    Ypert=y*((1+eps*td)**2-eps**2*tz**2)
    Bpert=s.diag(b,b,b*((1+eps*wz)**2-eps**2*wd**2))
    L2=s.expand(cf*fmin(Ypert,Bpert)).coeff(eps,2)
    kt=2*cf*y*(d+2*y)
    kw=-cf*b*DD
    st=2*cf*y*d
    sw=-cf*b*(DD+4*b)
    mixed=8*cf*y*b
    exact('cartesian_scalar_principal_action',L2,
          kt*td*td+kw*wd*wd-st*tz*tz-sw*wz*wz+mixed*td*wz)
    BT=s.Matrix([[b*(1+eps**2*(vz*vz-vt*vt)),0,b*eps*vz],
                 [0,b,0],[b*eps*vz,0,b]])
    transverse=s.expand(cf*fmin(y,BT)).coeff(eps,2)
    tt=2*d-16*(b-1)
    exact('cartesian_transverse_principal_action',transverse,
          cf*b*(-DD*vt*vt+tt*vz*vz))
    pt,pw=s.symbols('p_theta p_w',real=True)
    vel={td:(pt-mixed*wz)/(2*kt),wd:pw/(2*kw)}
    ham=simp((pt*td+pw*wd-L2).subs(vel))
    exact('canonical_energy_mixed_shift',ham,
          (pt-mixed*wz)**2/(4*kt)+pw**2/(4*kw)+st*tz**2+sw*wz**2)
    speed=s.symbols('v_squared',real=True)
    vfast=d*(DD+4*b)/((d+2*y)*DD)
    determinant=(kt*speed-st)*(kw*speed-sw)-mixed**2*speed/4
    exact('scalar_principal_factorization',determinant,
          kt*kw*(speed-1)*(speed-vfast))
    exact('longitudinal_stiffness_sign',sw,-2*cf*b*KK)
    aa,DDpos,Cpos=s.symbols('a D_positive C_positive',positive=True)
    abstractfast=(-aa-2*y)*(DDpos+4*b)/(-aa*DDpos)
    excess=2*y/aa+4*b/DDpos+8*y*b/(aa*DDpos)
    exact('positive_branch_speed_excess',abstractfast-1,excess)
    truth('positive_branch_strictly_superluminal',excess.is_positive,excess)
    abstractsource=(-Cpos)*(2*y*(-aa-2*y)-3*b*DDpos)
    truth('positive_branch_has_desired_source',abstractsource.is_positive,
          abstractsource)
    truth('positive_c_has_negative_spatial_energy',
          (-2*Cpos*b*Kpos).is_negative,'sw=-2*c*b*K with K>0')

    witness={y:s.Rational(1,10),b:s.Rational(1,10),cf:-Cpos}
    exact('witness_actual_H_source',JJ.subs(witness),306*Cpos/125)
    exact('witness_scalar_speed_squared',vfast.subs(witness),s.Rational(77,68))
    exact('witness_transverse_speed_squared',(tt/DD).subs(witness),s.Rational(5,4))
    for name,coefficient in [('clock_inertia',kt),('label_inertia',kw),
                             ('clock_stiffness',st),('label_stiffness',sw),
                             ('transverse_stiffness',-cf*b*tt)]:
        value=simp(coefficient.subs(witness))
        truth('witness_positive_'+name,value.is_positive,value)
    exact('silent_point_zero_source',JJ.subs({y:1,b:1}))
    exact('silent_point_label_kinetic_degeneracy',kw.subs({y:1,b:1}))
    wrongcone=simp(((kt-st)*(kw-sw)))
    truth('reject_omit_mixed_principal_term',wrongcone!=0,str(wrongcone))
    wrongsource=simp((yy*Fy-lr*Fr-2*lt*Ft).subs(iso)-JJ)
    truth('reject_double_folded_tangential_source',wrongsource!=0,str(wrongsource))

    passed=all(row['passed'] for row in rows)
    print(json.dumps(dict(
        status='CENTRE_GATE_DIAGNOSED' if passed else 'VERIFICATION_FAILED',
        article_sha256=sha(ARTICLE),intuitive_sha256=sha(intuitive),
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),
        check_count=len(rows),checks=rows,
        closure_flags=dict(leading_centre_source_compatible=passed,
            positive_principal_energy_witness=passed,
            nondegenerate_common_cone_obstruction_verified=passed,
            nondegenerate_positive_energy_common_cone_pass=False,
            full_coupled_health=False,degenerate_branches_decided=False,
            eft_frequency_band_verified=False,global_interior_matched=False,
            singularity_free_black_hole=False,observational_pass=False,
            new_constitutive_law_selected=False,official_theory_changed=False),
        decision='The original F_min supplies a regular leading central source. '
                 'Every nondegenerate positive-energy scalar principal branch '
                 'has a mode outside the matter metric cone. Stop at this '
                 'restricted gate; no global interior or replacement law selected.'
                 if passed else 'Inspect failed exact checks.'),
        indent=2,ensure_ascii=True))
    return 0 if passed else 1


def separated_response_main():
    '''Stage 11: one new internal constitutive trial, no interior integration.'''
    rows=[]

    def exact(name,actual,expected=0):
        residual=simp(actual-expected)
        rows.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))

    def truth(name,value,evidence):
        rows.append(dict(name=name,passed=bool(value),evidence=str(evidence)))

    truth('article_hash',sha(ARTICLE)==EXPECTED_SHA,sha(ARTICLE))
    intuitive=ROOT/'intuitive/RefG_GE.md'
    truth('intuitive_hash',sha(intuitive)==INTUITIVE_GE_SHA,
          sha(intuitive))
    alpha,beta=s.symbols('alpha beta',real=True,nonzero=True)
    y,b,yy,lr,lt,r,P,Q,wh=s.symbols('y b yy lr lt r P Q omega_H',positive=True)

    def response(Y,B):
        return alpha*(Y-1)**2/2+beta*s.trace((B-s.eye(3))**2)/2

    F=response(yy,s.diag(lr,lt,lt))
    Fy,Fr,Ft=[s.diff(F,z) for z in (yy,lr,lt)]
    I1,I2=lr+2*lt,2*lr*lt+lt*lt
    exact('response_in_original_invariants',F,
          alpha*(yy-1)**2/2+beta*(I1*I1-2*I2-2*I1+3)/2)
    silent={yy:1,lr:1,lt:1}
    for name,expr in [('value',F),('clock',Fy),('radial',Fr),('tangential',Ft)]:
        exact('silent_'+name,expr.subs(silent))
    Hvertex=-2*yy*Fy+2*lr*Fr+2*lt*Ft
    exact('silent_independent_H_vertex',Hvertex.subs(silent))
    iso={yy:y,lr:b,lt:b}
    J=simp((yy*Fy-lr*Fr-lt*Ft).subs(iso))
    exact('central_actual_source',J,alpha*y*(y-1)+3*beta*b*(1-b))
    f0=F.subs(iso)
    rhoF=Q*(2*y*Fy.subs(iso)-f0)
    pF=Q*(f0-2*b*Fr.subs(iso))
    exact('central_pressure_isotropy',pF,Q*(f0-b*Ft.subs(iso)))
    a2,n2,h2,z3=s.symbols('a2 n2 h2 z3',real=True)
    jet={yy:y*(1-2*(h2+n2)*r*r),
         lr:b*(1+(2*h2+6*z3-2*a2)*r*r),
         lt:b*(1+(2*h2+2*z3)*r*r)}
    frj=Fr.subs(jet,simultaneous=True)
    ftj=Ft.subs(jet,simultaneous=True)
    label=s.diff(r*r*(1+(n2+2*h2+3*z3-a2)*r*r)*frj,r) \
        -r*(1+(n2+a2+2*h2+z3)*r*r)*ftj
    exact('central_label_lowest_order',s.expand(label).coeff(r,1))
    bracket=5*(3*b-1)*z3+(b-1)*n2+(4*b-2)*h2-(7*b-3)*a2
    exact('central_label_next_order',s.expand(label).coeff(r,3),2*beta*bracket)
    exact('central_label_coefficient',s.diff(2*beta*bracket,z3),10*beta*(3*b-1))
    exact('central_zero_stiffness_compatibility',bracket.subs(b,s.Rational(1,3)),
          s.Rational(2,3)*(a2-h2-n2))
    rhoO,pO=s.symbols('rho_ordinary p_ordinary',real=True)
    central={a2:(rhoO+rhoF)/(6*P),
             n2:(rhoO+rhoF+3*(pO+pF))/(12*P),h2:-Q*J/(6*wh*P)}
    central[z3]=simp(((7*b-3)*a2-(b-1)*n2-(4*b-2)*h2).subs(central)/(5*(3*b-1)))
    exact('central_solved_label',bracket.subs(central))
    exact('central_solved_H',6*wh*P*central[h2]+Q*J)
    ap,bp=s.symbols('alpha_positive beta_positive',positive=True)
    point={y:2,b:s.Rational(1,4),alpha:ap,beta:bp}
    exact('central_witness_source',J.subs(point),2*ap+9*bp/16)
    truth('central_witness_maximum_deficit',simp(central[h2].subs(point)).is_negative,
          simp(central[h2].subs(point)))

    eps,td,tz,wd,wz,vt,vz=s.symbols('eps td tz wd wz vt vz',real=True)
    Ypert=y*((1+eps*td)**2-eps**2*tz**2)
    BL=s.diag(b,b,b*((1+eps*wz)**2-eps**2*wd**2))
    L2=s.expand(response(Ypert,BL)).coeff(eps,2)
    kt=alpha*y*(3*y-1)
    st=alpha*y*(y-1)
    kl=beta*b*(1-b)
    sl=beta*b*(1-3*b)
    transverse_stiffness=beta*b*(1-2*b)
    exact('direct_scalar_principal',L2,kt*td**2-st*tz**2+kl*wd**2-sl*wz**2)
    BT=s.Matrix([[b*(1+eps**2*(vz*vz-vt*vt)),0,b*eps*vz],
                 [0,b,0],[b*eps*vz,0,b]])
    exact('direct_transverse_principal',
          s.expand(response(y,BT)).coeff(eps,2),kl*vt**2-transverse_stiffness*vz**2)
    for name,num,den,target in [
        ('clock',st,kt,(y-1)/(3*y-1)),
        ('longitudinal',sl,kl,(1-3*b)/(1-b)),
        ('transverse',transverse_stiffness,kl,(1-2*b)/(1-b))]:
        exact('speed_'+name,num/den,target)
    for name,coef in [('clock_inertia',kt),('clock_stiffness',st),
                      ('label_inertia',kl),('longitudinal_stiffness',sl),
                      ('transverse_stiffness',transverse_stiffness)]:
        truth('witness_positive_'+name,simp(coef.subs(point)).is_positive,coef.subs(point))
    for name,expr,value in [('clock',st/kt,s.Rational(1,5)),
                            ('longitudinal',sl/kl,s.Rational(1,3)),
                            ('transverse',transverse_stiffness/kl,s.Rational(2,3))]:
        exact('witness_speed_'+name,expr.subs(point),value)
    z=s.symbols('z',positive=True)
    centre_interval=z/(3*(1+z))
    healthy={beta:bp,b:centre_interval}
    for name,expr in [('inertia',kl),('longitudinal',sl),('transverse',transverse_stiffness)]:
        truth('entire_central_interval_'+name,simp(expr.subs(healthy)).is_positive,
              simp(expr.subs(healthy)))
    exact('negative_beta_branch_superluminal',(sl/kl).subs(b,1+z),3+2/z)
    exact('negative_alpha_branch_superluminal',
          (st/kt).subs(y,z/(3*(1+z))),1+2*z/3)

    bi,bj,bk=s.symbols('b_i b_j b_k',positive=True)
    anis=s.diag(bi*((1+eps*wz)**2-eps**2*wd**2),bj,bk)
    isolated=s.expand(response(y,anis)).coeff(eps,2)
    exact('anisotropic_longitudinal',isolated,
          beta*bi*((bi-1)*(wz*wz-wd*wd)+2*bi*wz*wz))
    anisT=s.Matrix([[bi,s.sqrt(bi*bj)*eps*vz,0],
                    [s.sqrt(bi*bj)*eps*vz,bj*(1+eps**2*(vz*vz-vt*vt)),0],
                    [0,0,bk]])
    exact('anisotropic_transverse',s.expand(response(y,anisT)).coeff(eps,2),
          beta*bj*((bj-1)*(vz*vz-vt*vt)+bi*vz*vz))
    transition=(1+3*z)/(3*(1+z))
    truth('open_transition_positive_inertia',
          simp(kl.subs({b:transition,beta:bp})).is_positive,
          'all 1/3<b_i<1, no assumed interpolation')
    truth('open_transition_negative_spatial_energy',
          simp(sl.subs({b:transition,beta:bp})).is_negative,
          'all 1/3<b_i<1')
    tangential=(1+2*z)/(2*(1+z))
    truth('safe_tangential_transition_negative_spatial_energy',
          simp(transverse_stiffness.subs({b:tangential,beta:bp})).is_negative,
          'wave and polarization tangent to the sphere, perpendicular to grad H')
    truth('beyond_silent_negative_inertia',
          simp(kl.subs({b:1+z,beta:bp})).is_negative,'all b_i>1 for beta>0')
    exact('silent_label_kinetic_degeneracy',kl.subs(b,1))

    t,x1,x2,x3=s.symbols('t x1 x2 x3',real=True)
    hh=s.Function('h')(t,x3)
    metric=s.diag(-1,s.exp(hh),s.exp(-hh),1)
    exact('direct_TT_curvature',P*ricci_scalar(metric,[t,x1,x2,x3])/2,
          P*(s.diff(hh,t)**2-s.diff(hh,x3)**2)/4)
    amplitude=s.symbols('amplitude',real=True)
    Ftt=response(1,s.diag(s.exp(-eps*amplitude),s.exp(eps*amplitude),1))
    potential=s.series(Q*Ftt,eps,0,3).removeO().expand().coeff(eps,2)
    exact('TT_potential_sign',potential,Q*beta*amplitude**2)
    mass2=-s.diff(potential,amplitude,2)/(P/2)
    exact('TT_mass_squared',mass2,-4*Q*beta/P)
    truth('positive_beta_negative_TT_mass_squared',mass2.subs(beta,bp).is_negative,
          mass2.subs(beta,bp))
    truth('negative_beta_repairs_TT_mass_sign',mass2.subs(beta,-bp).is_positive,
          'but the corresponding healthy-inertia label branch is superluminal')
    truth('reject_positive_F_as_positive_TT_energy',s.diff(potential,amplitude,2)!=0,
          'positive potential in L adds negative mass-squared with this convention')
    exact('zero_beta_is_degenerate_not_a_pass',kl.subs(beta,0))

    passed=all(row['passed'] for row in rows)
    print(json.dumps(dict(
        status='SEPARATED_RESPONSE_TRANSITION_EXCLUDED' if passed else 'VERIFICATION_FAILED',
        article_sha256=sha(ARTICLE),intuitive_sha256=sha(intuitive),
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),
        check_count=len(rows),checks=rows,
        closure_flags=dict(new_internal_constitutive_trial_tested=passed,
            silent_exterior_background_retained=passed,
            leading_centre_source_compatible=passed,
            centre_principal_energy_and_cone_witness=passed,
            static_transition_exclusion_verified=passed,
            silent_TT_negative_mass_squared_verified=passed,
            nonzero_coefficient_sign_escape_excluded=passed,
            globally_healthy_static_transition=False,accepted_new_constitutive_law=False,
            degenerate_branches_decided=False,flowing_branches_decided=False,
            full_coupled_health=False,eft_frequency_band_verified=False,
            singularity_free_black_hole=False,observational_pass=False,
            official_theory_changed=False),
        decision='Separated quadratic response repairs the central principal '
                 'speeds, but no smooth everywhere-positive-energy static '
                 'transition reaches its silent state. The required beta>0 '
                 'also gives negative silent TT mass-squared. Changing finite '
                 'nonzero coefficient signs cannot satisfy the central cone '
                 'and silent TT gates together. Stop with this family.'
                 if passed else 'Inspect failed exact checks.'),
        indent=2,ensure_ascii=True))
    return 0 if passed else 1


def feedback_interface_main():
    '''Stage 12: existing feedback and two conditional response discriminators.'''
    rows=[]

    def exact(name,actual,expected=0):
        residual=simp(actual-expected)
        rows.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))

    def truth(name,value,evidence):
        rows.append(dict(name=name,passed=bool(value),evidence=str(evidence)))

    truth('article_hash',sha(ARTICLE)==EXPECTED_SHA,sha(ARTICLE))
    sources=[
        ('W75','Cosmology_and_LSS/Active_Participation_Resonance_Feedback/'
         'w3_75_dynamical_relaxation_response_contract.md',
         '31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a'),
        ('W78','Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/'
         'w3_78_core_frequency_response_contract.md',
         'a1b575d97eb678f52a792cafb8ab5954206d961f8a4f2bd6351260394ad845a3'),
        ('W88','Strong_Field/W3-88_Native_Phase_Effective_Action/'
         'w3_88_native_phase_contract.md',
         '3295abe77253eee38b3fd8fb479145a8531d802d9087b63035315424e1080b60')]
    for name,relative,pin in sources:
        digest=sha(ROOT/'RefG'/'work 3'/relative)
        truth(name+'_source_hash',digest==pin,digest)

    b,P,Q,beta=s.symbols('b P Q beta',positive=True)
    kap,y=s.symbols('kappa y',real=True)
    xx=s.symbols('b11 b22 b33 b12 b13 b23',real=True)
    B=s.Matrix([[xx[0],xx[3],xx[4]],[xx[3],xx[1],xx[5]],
                [xx[4],xx[5],xx[2]]])
    delta=kap*(s.trace(B*B)-s.trace(B)**2/3)/2
    iso=dict(zip(xx,(b,b,b,0,0,0)))
    exact('entire_isotropic_curve_value',delta.subs(iso))
    for q in xx:
        exact('entire_isotropic_curve_first_'+str(q),s.diff(delta,q).subs(iso))
    exact('clock_first',s.diff(delta,y))
    exact('isotropic_H_source',
          sum(xx[i]*s.diff(delta,xx[i]) for i in range(3)).subs(iso))
    h=s.symbols('h',real=True)
    Bt=s.diag(s.exp(-h),s.exp(h),1)
    dt=kap*(s.trace(Bt*Bt)-s.trace(Bt)**2/3)/2
    expansion=s.series(dt,h,0,6).removeO().expand()
    exact('TT_shear_quadratic',expansion.coeff(h,2),kap)
    exact('TT_shear_quartic',expansion.coeff(h,4),5*kap/12)
    baseline=Q*beta*s.trace((Bt-s.eye(3))**2)/2
    potential2=s.series(baseline+Q*dt,h,0,3).removeO().expand()
    exact('TT_combined_potential',potential2,Q*(beta+kap)*h*h)
    mass2=-s.diff(potential2,h,2)/(P/2)
    exact('TT_combined_mass_squared',mass2,-4*Q*(beta+kap)/P)
    exact('TT_mass_squared_shift',mass2-mass2.subs(kap,0),-4*Q*kap/P)
    wrong=kap*s.trace((B-s.eye(3))**2)/2
    truth('reject_isotropic_preservation_for_wrong_witness',
          simp(wrong.subs(iso).subs({b:2,kap:1}))!=0,
          'tr[(B-I)^2] does not vanish on every isotropic state')

    # General relevant smooth Taylor jet in rho and three arbitrary medium
    # directions. U(0,Z)=0 eliminates every pure-medium Taylor coefficient.
    rho,e=s.symbols('rho epsilon',real=True)
    zs=s.symbols('z0:3',real=True)
    us=s.symbols('u0:11',real=True)
    medium=us[0]+sum(us[i+1]*zs[i] for i in range(3))
    for coef,(i,j) in zip(us[4:10],[(0,0),(0,1),(0,2),(1,1),(1,2),(2,2)]):
        medium+=coef*zs[i]*zs[j]
    U=rho*medium+us[10]*rho*rho/2
    exact('interaction_entire_zero_slice',U.subs(rho,0))
    for i,z in enumerate(zs):
        exact('zero_slice_first_'+str(i),s.diff(U,z).subs(rho,0))
        for j in range(i,3):
            exact('zero_slice_second_%d_%d' % (i,j),
                  s.diff(U,z,zs[j]).subs(rho,0))
    a,c=s.symbols('psi_real psi_imag',real=True)
    rho2=(a*a+c*c)/2
    Ufield=U.subs(rho,rho2)
    zero={a:0,c:0,**dict.fromkeys(zs,0)}
    for v in (a,c):
        exact('no_TT_amplitude_bilinear_'+str(v),
              s.diff(Ufield,zs[0],v).subs(zero))
    perturbed=U.subs({rho:e*e*rho2,**{z:e*z for z in zs}},simultaneous=True)
    exact('vacuum_quadratic_interaction',s.expand(perturbed).coeff(e,2),us[0]*rho2)
    exact('vacuum_TT_potential_correction',
          s.diff(s.expand(perturbed).coeff(e,2),zs[0],2))
    truth('unrepaired_positive_beta_TT_mass',(-4*Q*beta/P).is_negative,
          'classical exact/asymptotic vacuum block; no EFT-band claim')
    # A bulk term violates the assumption and does change the TT block.
    changed=Ufield+kap*zs[0]**2
    exact('bulk_term_control_changes_TT',s.diff(changed,zs[0],2).subs(zero),2*kap)
    truth('bulk_term_control_not_on_zero_slice',
          simp(changed.subs({a:0,c:0,zs[0]:1,kap:1}))!=0,
          'nonzero U(0,Z) is a different premise')

    A=s.symbols('A',positive=True)
    C,D,x,z=s.symbols('C D x z',real=True)
    E=A*x*x/2+C*x*z+D*z*z/2
    relaxed=-C*z/A
    exact('stationary_core_elimination',s.diff(E,x).subs(x,relaxed))
    curvature=s.diff(E.subs(x,relaxed),z,2)
    exact('static_relaxed_curvature',curvature,D-C*C/A)
    Cp=s.symbols('C_positive',positive=True)
    truth('relaxation_softens_static_curvature',
          simp((curvature-D).subs(C,Cp)).is_negative,
          'static positive eliminated block, not full dynamical spectrum')
    exact('stable_static_control',curvature.subs({A:1,C:s.Rational(1,2),D:1}),
          s.Rational(3,4))
    exact('unstable_despite_positive_diagonal_control',
          curvature.subs({A:1,C:2,D:1}),-3)

    passed=all(row['passed'] for row in rows)
    print(json.dumps(dict(
        status='FEEDBACK_INTERFACE_DISCRIMINATORS_VERIFIED' if passed
               else 'VERIFICATION_FAILED',
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),
        check_count=len(rows),checks=rows,
        closure_flags=dict(isotropic_response_nonselection_verified=passed,
            localized_amplitude_vacuum_no_repair_verified=passed,
            static_relaxation_sign_verified=passed,
            covariant_medium_response_derived=False,new_physical_law_selected=False,
            stage11_candidate_repaired=False,full_coupled_health=False,
            physical_eft_band_verified=False,singularity_free_black_hole=False,
            observational_pass=False,official_theory_changed=False),
        decision='Existing feedback does not determine the independent shear '
                 'response. Smooth localized amplitude coupling alone cannot '
                 'repair the rejected trial vacuum TT mass. Stop before '
                 'selecting a bulk law or integrating an interior.'
                 if passed else 'Inspect failed exact checks.'),
        indent=2,ensure_ascii=True))
    return 0 if passed else 1


def same_field_response_main():
    '''Stage 13: directional derivative of the inherited W76/W77 generator.'''
    rows=[]

    def exact(name,actual,expected=0):
        residual=simp(actual-expected)
        rows.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))

    def truth(name,value,evidence):
        rows.append(dict(name=name,passed=bool(value),evidence=str(evidence)))

    folder=ROOT/'RefG/work 3/Cosmology_and_LSS/Active_Participation_Resonance_Feedback'
    pins=[
        ('w3_76_same_field_resonant_exchange_contract.md',
         'e10781a73470220065c664196efe0c361dbfb1c6c2404864e895d6ad2380bd02'),
        ('w3_77_pair_phase_susceptibility_contract.md',
         'a69aa554ba09472176e04996a4f17d1057f18e4fb802a2533aebf47a432abb26')]
    for name,pin in pins:
        actual=sha(folder/name)
        truth(name,actual==pin,actual)
    D,k,A0,E0,cell=s.symbols('D k A0 E0 V_cell',positive=True)
    phase,eps,aa,bb,sigma,imb,Drate=s.symbols(
        'Delta epsilon a b sigma imbalance D_rate',real=True)
    K=A0*s.exp(-k*D)/D
    V=-K*s.cos(phase)
    vp=s.diff(V,D); vpp=s.diff(V,D,2)
    exact('profile_kernel_first',s.diff(K,D),-K*(k+1/D))
    exact('profile_kernel_second',s.diff(K,D,2),K*(k*k+2*k/D+2/D**2))
    exact('left_force',vp,-s.diff(K,D)*s.cos(phase))
    exact('phase_exchange',s.diff(V,phase),K*s.sin(phase))
    # Work identities on the explicit inherited leading equations.
    zdot=K*s.sin(phase)
    phasedot=-2*sigma*imb
    translation_work=-vp*Drate
    imbalance_work=2*sigma*imb*zdot
    interaction_work=vp*Drate+s.diff(V,phase)*phasedot
    exact('one_counted_energy_exchange',
          translation_work+imbalance_work+interaction_work)
    exact('ordinary_charge_exchange',zdot+(-zdot))
    wrong=translation_work+imbalance_work+vp*Drate-s.diff(V,phase)*phasedot
    truth('wrong_relative_symplectic_sign_detected',simp(wrong)!=0,wrong)

    # Cartesian Hessian; no prescribed direction, profile change or F_med.
    rr=s.Matrix(s.symbols('rx ry rz',real=True))
    rad=s.sqrt(rr.dot(rr))
    pot=-A0*s.exp(-k*rad)*s.cos(phase)/rad
    nn=rr/rad
    hessian=s.hessian(pot,list(rr))
    expected=vpp.subs(D,rad)*(nn*nn.T) \
        +(vp/D).subs(D,rad)*(s.eye(3)-nn*nn.T)
    for i in range(3):
        for j in range(i,3):
            exact('cartesian_Hessian_%d_%d' % (i,j),hessian[i,j],expected[i,j])

    # Independent exact isochoric affine path, diagonal in its eigenbasis.
    sx,sy=s.symbols('sx sy',real=True)
    weights=[sx,sy,-sx-sy]
    stretch=s.diag(*[s.exp(eps*w) for w in weights])
    exact('affine_volume_unchanged',stretch.det(),1)
    rnew=stretch*rr
    dist=s.sqrt(rnew.dot(rnew))
    adir=sum(weights[i]*rr[i]**2 for i in range(3))/rad**2
    bdir=sum(weights[i]**2*rr[i]**2 for i in range(3))/rad**2
    d1=s.diff(dist,eps).subs(eps,0)
    d2=s.diff(dist,eps,2).subs(eps,0)
    exact('affine_distance_first',d1,rad*adir)
    exact('affine_distance_second',d2,rad*(2*bdir-adir*adir))
    generic=D**2*vpp*aa*aa+D*vp*(2*bb-aa*aa)
    closed=K*s.cos(phase)*(2*(k*D+1)*bb-(k*k*D*D+3*k*D+3)*aa*aa)
    exact('directional_response_from_inherited_kernel',generic,closed)
    path_potential=-A0*s.exp(-k*dist)*s.cos(phase)/dist
    actual=s.diff(path_potential,eps,2).subs(eps,0)
    exact('independent_full_affine_energy_derivative',actual,
          closed.subs({D:rad,aa:adir,bb:bdir},simultaneous=True))
    cross=s.diff(D*vp*aa,phase)
    exact('direction_phase_mixing',cross,D*aa*s.diff(K,D)*s.sin(phase))
    omitted=D**2*vpp*aa**2
    truth('missing_prestress_detected',simp(generic-omitted)!=0,
          'nonzero initial force contributes through the exact affine path')

    # Dilation trace checks against W77; direction-resolved stress is new.
    scale=s.symbols('scale',real=True)
    dilated=V.subs(D,D*s.exp(scale))
    pressure=-s.diff(dilated,scale).subs(scale,0)/(3*cell)
    exact('W77_virial_pressure',pressure,D*s.diff(K,D)*s.cos(phase)/(3*cell))
    trace=sum((D*s.diff(K,D)*s.cos(phase)/cell)*nn[i]**2 for i in range(3))
    exact('directional_stress_trace',trace/3,pressure)
    exact('in_phase_response',closed.subs(phase,0),closed/s.cos(phase))
    exact('opposite_phase_reversal',closed.subs(phase,s.pi),-closed.subs(phase,0))
    exact('quadrature_frozen_directional_response',closed.subs(phase,s.pi/2))
    truth('quadrature_can_still_mix_phase',simp(cross.subs(phase,s.pi/2))!=0,
          'zero frozen positional curvature is not no interaction')
    exact('aligned_shape_control',closed.subs({aa:1,bb:1}),
          -K*s.cos(phase)*(k*k*D*D+k*D+1))
    exact('diagonal_direction_shape_control',closed.subs({aa:0,bb:1}),
          2*K*s.cos(phase)*(k*D+1))

    passed=all(row['passed'] for row in rows)
    print(json.dumps(dict(
        status='SAME_FIELD_DIRECTIONAL_RESPONSE_DERIVED' if passed
               else 'VERIFICATION_FAILED',
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),
        check_count=len(rows),checks=rows,
        closure_flags=dict(inherited_pair_directional_response_verified=passed,
            phase_translation_work_balance_verified=passed,
            dilation_trace_regression_verified=passed,
            new_constitutive_function_selected=False,
            full_field_finite_D_Hessian_error_bounded=False,
            relaxed_population_modulus_derived=False,
            collective_pressure_feedback_derived=False,
            article_medium_response_derived=False,
            globally_stable_population=False,singularity_free_black_hole=False,
            observational_pass=False,official_theory_changed=False),
        decision='A directional component follows from the existing same-field '
                 'fixed-charge pair generator. Full collective P_F and article '
                 'H/F_med identification remain unproved; no new medium law.'
                 if passed else 'Inspect failed exact checks.'),
        indent=2,ensure_ascii=True))
    return 0 if passed else 1


def closure_selection_main():
    '''Stage 14: exact pressure reduction and tests of full-closure routes.'''
    rows=[]

    def exact(name,actual,expected=0):
        residual=simp(actual-expected)
        rows.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))

    def truth(name,value,evidence):
        rows.append(dict(name=name,passed=bool(value),evidence=str(evidence)))

    truth('article_hash',sha(ARTICLE)==EXPECTED_SHA,sha(ARTICLE))
    sources=[
        ('W58','Lagrangian_Formulation/One_Oscillon_Coframe_Localized_Core/'
         'w3_58_one_oscillon_coframe_localized_core_preregistration.md',
         'ae16e3a326d2af5740936ab15d9aa9de2f0bd9fe4fb8e35b19c21b24ce8bf5db'),
        ('W75','Cosmology_and_LSS/Active_Participation_Resonance_Feedback/'
         'w3_75_dynamical_relaxation_response_contract.md',
         '31a1e6bd28b6698e64b790fd4692aba6616af5613c3919f322a790c7296d9f4a'),
        ('W79','Strong_Field/W3-79_Collective_Current_Backreaction/'
         'w3_79_collective_current_backreaction_contract.md',
         '7619daeda70d58b16da933b832db014fbd0cf66ecf921c7c25b7eb4558bee6aa')]
    for name,relative,pin in sources:
        digest=sha(ROOT/'RefG'/'work 3'/relative)
        truth(name+'_source_hash',digest==pin,digest)

    # Exact current rewrite, retaining the ordinary-sector identity.
    u,m2,lam,g6=s.symbols('s m2 lambda g6',positive=True)
    V=m2*u/2-lam*u**2/4+g6*u**3/6
    metric=s.diag(-1,1,1,1)
    jj=s.Matrix(s.symbols('j0:4',real=True))
    dtheta=s.Matrix(s.symbols('dtheta0:4',real=True))
    first=jj.dot(dtheta)+(jj.T*metric*jj)[0]/(2*u)-V
    js=-u*metric*dtheta
    mapping=dict(zip(jj,js))
    for i in range(4):
        exact('current_variation_'+str(i),s.diff(first,jj[i]).subs(mapping))
    X=-(dtheta.T*metric*dtheta)[0]
    exact('full_current_back_substitution',first.subs(mapping),u*X/2-V)
    du=s.symbols('ds',real=True)
    exact('retained_amplitude_gradient',-(du/(2*s.sqrt(u)))**2/2,-du**2/(8*u))

    mu2=m2-lam*u+g6*u**2
    mu=s.sqrt(mu2)
    number=u*mu
    pressure=simp(u*mu2/2-V)
    energy=simp(u*mu2/2+V)
    exact('homogeneous_amplitude_stationarity',mu2/2-s.diff(V,u))
    exact('ordinary_pressure',pressure,-lam*u**2/4+g6*u**3/3)
    exact('ordinary_energy',energy,m2*u-3*lam*u**2/4+2*g6*u**3/3)
    exact('ordinary_enthalpy',energy+pressure,number*mu)
    exact('ordinary_first_law',s.diff(energy,u),mu*s.diff(number,u))
    exact('ordinary_Gibbs_Duhem',s.diff(pressure,u),number*s.diff(mu,u))
    cs=u*(-lam+2*g6*u)/(2*m2-3*lam*u+4*g6*u**2)
    exact('ordinary_sound_derivative',s.diff(pressure,u)/s.diff(energy,u),cs)
    truth('pressure_sign_mutation_rejected',
          simp(energy-pressure-number*mu)!=0,
          'rho-p is not the ordinary enthalpy')

    # Independent full two-field dispersion before amplitude elimination.
    q,w,M,U=s.symbols('q w A_mass mu_squared',real=True)
    freq=s.symbols('frequency',real=True)
    matrix=s.Matrix([[q+M-freq**2,2*s.I*s.sqrt(U)*freq],
                     [-2*s.I*s.sqrt(U)*freq,q-freq**2]])
    dispersion=(q+M-w)*(q-w)-4*U*w
    exact('full_amplitude_phase_determinant',
          matrix.det(),dispersion.subs(w,freq**2))
    gap=M+4*U
    exact('zero_wavenumber_roots',dispersion.subs(q,0),w*(w-gap))
    exact('frequency_root_product',dispersion.subs(w,0),q*(q+M))
    exact('frequency_root_sum',-s.expand(dispersion).coeff(w,1),2*q+gap)
    exact('dispersion_discriminant',s.discriminant(dispersion,w),gap**2+16*U*q)
    A=2*u*(2*g6*u-lam)
    exact('amplitude_mass_from_original_potential',
          4*u*s.diff(V,u,2),A)
    exact('acoustic_limit_agrees_with_EOS',A/(A+4*mu2),cs)
    speed=s.symbols('speed_squared',real=True)
    exact('small_q_dispersion_coefficient',
          s.diff(dispersion.subs(w,speed*q),q).subs(q,0),M-speed*gap)
    exact('zero_amplitude_mass_quartic_soft_branch',
          s.series(dispersion.subs({M:0,w:q*q/(4*U)}),q,0,3).removeO())
    posM,posU=s.symbols('positive_A positive_mu2',positive=True)
    truth('upper_branch_acoustic_positive',(posM/(posM+4*posU)).is_positive,
          'A_mass>0 and mu_squared>0')
    truth('upper_branch_acoustic_subluminal',
          simp(1-posM/(posM+4*posU)).is_positive,'positive 4mu_squared/gap')
    negM,posGap=s.symbols('negative_A positive_gap',positive=True)
    truth('lower_branch_positive_gap_has_negative_acoustic',
          (-negM/posGap).is_negative,'A_mass<0, gap>0')

    # The proposed dictionary is tested on a static density interval.
    n,n0,mu0,N=s.symbols('n n0 mu0 N',positive=True)
    rho0=s.symbols('rho_star',real=True)
    lapse=(n/n0)**s.Rational(1,5)
    chem=mu0/lapse
    rho=rho0+s.Rational(5,4)*mu0*n0*(n/n0)**s.Rational(4,5)
    p=n*chem-rho
    exact('static_phase_equilibrium',chem*lapse,mu0)
    exact('static_energy_derivative',s.diff(rho,n),chem)
    exact('static_pressure',p,-rho0-mu0*n0*(n/n0)**s.Rational(4,5)/4)
    exact('static_dictionary_sound_sign',n*s.diff(chem,n)/chem,-s.Rational(1,5))
    exact('static_hydrostatic_balance',s.diff(p,n),
          -(rho+p)*s.diff(s.log(lapse),n))
    exact('energy_constant_cannot_repair_sign',
          s.diff(n*s.diff(chem,n)/chem,rho0))
    truth('wrong_positive_sound_sign_rejected',
          simp(n*s.diff(chem,n)/chem-s.Rational(1,5))!=0,
          'the static map fixes a negative sign')

    # Nonlinear F ambiguity, independent of every silent-neighbourhood jet.
    x,y,Q,epsilon=s.symbols('x y Q epsilon',positive=True)
    active=s.exp(-1/x**2)  # x=y-2>0; zero branch for y<=2.
    for order in range(5):
        exact('smooth_join_derivative_'+str(order),
              s.limit(s.diff(active,x,order),x,0,dir='+'))
    exact('silent_neighbourhood_branch',s.Piecewise(
        (0,y<=2),(s.exp(-1/(y-2)**2),True)).subs(y,1))
    active_y=s.exp(-1/(y-2)**2)
    source=epsilon*y*s.diff(active_y,y)
    density=Q*epsilon*(2*y*s.diff(active_y,y)-active_y)
    pF=Q*epsilon*active_y
    exact('nonlinear_source_witness',source.subs(y,3),6*epsilon/s.E)
    exact('nonlinear_energy_witness',density.subs(y,3),11*Q*epsilon/s.E)
    exact('nonlinear_pressure_witness',pF.subs(y,3),Q*epsilon/s.E)
    H,y0=s.symbols('H y0',real=True)
    f=s.Function('b')
    yh=y0*s.exp(-2*H)
    exact('direct_H_source_variation',
          -s.diff(epsilon*f(yh),H)/2,
          (epsilon*y*s.diff(f(y),y)).subs(y,yh))
    c=s.symbols('clock_normalization',positive=True)
    yn=c/N**2
    exact('independent_lapse_energy_variation',
          -Q*s.diff(N*epsilon*f(yn),N),
          (Q*epsilon*(2*y*s.diff(f(y),y)-f(y))).subs(y,yn))
    truth('zero_nonlinear_source_mutation_rejected',
          simp(source.subs(y,3))!=0,
          'silent-state matching does not force the source at y=3 to vanish')

    # Direct canonical-one-field replacement: exact source obstruction.
    null=s.Matrix([1,1,0,0])
    dfields=[s.Matrix(s.symbols('phi%d_d0:4' % a,real=True)) for a in range(2)]
    potential=s.symbols('arbitrary_potential',real=True)
    norm=sum((d.T*metric*d)[0] for d in dfields)
    tensor=sum((d*d.T for d in dfields),s.zeros(4))-metric*(norm/2+potential)
    canonical=sum(null.dot(d)**2 for d in dfields)
    exact('radial_vector_is_null',(null.T*metric*null)[0])
    exact('canonical_null_contraction',(null.T*tensor*null)[0],canonical)
    truth('canonical_null_source_nonnegative',canonical.is_nonnegative,
          'sum of two real squares; independent of the scalar potential')
    P,m,r=s.symbols('P mass_parameter radius',positive=True)
    h=m/r
    Z=s.exp(-2*h)*s.diff(h,r)**2
    exact('exterior_radial_null_source',-2*P*Z,-2*P*m*m*s.exp(-2*m/r)/r**4)
    truth('target_exterior_radial_null_source_negative',(-2*P*Z).is_negative,
          'the fixed nonzero exponential exterior cannot be a canonical scalar source')

    passed=all(row['passed'] for row in rows)
    print(json.dumps(dict(
        status='CLOSURE_ROUTES_RESOLVED_WITH_UNSELECTED_MEDIUM' if passed
               else 'VERIFICATION_FAILED',
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),
        check_count=len(rows),checks=rows,
        closure_flags=dict(ordinary_pressure_reduction_verified=passed,
            full_frozen_amplitude_phase_dispersion_verified=passed,
            direct_static_dictionary_excluded=passed,
            nonlinear_medium_freedom_verified=passed,
            canonical_only_exterior_substitution_excluded=passed,
            localized_population_fluid_limit_derived=False,
            collective_identification_derived=False,
            full_self_regulation_derived=False,
            new_medium_law_selected=False,healthy_global_medium=False,
            singularity_resolution=False,observational_pass=False,
            official_theory_changed=False),
        decision='The ordinary-sector pressure is derived. The direct static '
                 'map fails its sound-speed gate. The remaining medium action '
                 'is not selected by the recorded assumptions.'
                 if passed else 'Inspect failed checks.'),
        indent=2,ensure_ascii=True))
    return 0 if passed else 1


def self_regulation_audit_main():
    '''Separate readouts from constrained feedback; reproduce existing equilibria.'''
    import importlib.util
    checks = []

    def exact(name, value, expected=0):
        residual = simp(value-expected)
        checks.append(dict(name=name, passed=bool(residual == 0),
                           residual=str(residual)))

    def truth(name, value, detail):
        checks.append(dict(name=name, passed=bool(value), detail=detail))

    sf = HERE.parent
    pins = {
        'W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field.py':
            '99bc4331bec07219308bd15e43a945792ecd59c60ef959d17684944a6635aa77',
        'W3-64_Einstein_Continuation/w3_64_source_first_einstein_strong_field_preregistration.md':
            '25e16a499a60d36ef1972eafe70958233b7715ffe04c26d0a771ddd2f02e71b1',
        'W3-64_Einstein_Continuation/w3_64_result.json':
            'b0898d5e3fea3e977eb0c78b2a1f8730a5b4c168857d05bdaf95b3119b75d07b',
        'W3-65_First_Turning_Point/w3_65_fixed_alpha_first_turning_point.py':
            '5cc24de6951bbd57e0091b687ab467dac2070eb73403d71c52ff91386dae1b73',
        'W3-65_First_Turning_Point/w3_65_fixed_alpha_first_turning_point_preregistration.md':
            '385402e843850725ed562a449adb246b510b65038685cad6521d9ff1c8be3942',
        'W3-65_First_Turning_Point/w3_65_result.json':
            'e3256094f5123e70f747d501d84c7db1301e7a2ab00742fc914e254007c67b0b',
        'W3-66_Physical_Radial_Mode/w3_66_physical_radial_mode.py':
            '381d8fec0e9188536bc75c37ef0159b51a06967612fb73a1463f3b65a5e49e06',
        'W3-66_Physical_Radial_Mode/w3_66_physical_radial_mode_preregistration.md':
            '13f16dbb45299af763c3934a6a116b85f0f11085c2e7c5478af9249b41666245',
        'W3-66_Physical_Radial_Mode/w3_66_result.json':
            'a876dfb9a073d2960db7c12cb48f8ef43c944b91754f8b42a3260351d556e34f',
    }
    actual = {name: sha(sf/name) if (sf/name).is_file() else None for name in pins}
    truth('frozen_dependencies_exact', actual == pins,
          'All nine source, preregistration and result hashes checked before imports.')
    if actual != pins:
        print(json.dumps(dict(status='DEPENDENCY_FAILURE', checks=checks,
                              expected_hashes=pins, actual_hashes=actual),
                         indent=2, allow_nan=False))
        return 1

    # Static Killing frequency and FLRW comoving frequency are separate maps.
    Ne, No, Ae, Ao, energy, wave = s.symbols('N_e N_o A_e A_o E_K k_com', positive=True)
    omega = s.symbols('omega', positive=True)
    static_e, static_o = energy/Ne, energy/No
    exact('static_observer_Killing_energy', No*static_o, energy)
    exact('static_received_over_emitted_frequency', static_o/static_e, Ne/No)
    cosmic_e, cosmic_o = wave/Ae, wave/Ao
    exact('FLRW_null_dispersion', (-omega**2+wave**2/Ao**2).subs(omega, cosmic_o))
    exact('FLRW_received_over_emitted_frequency', cosmic_o/cosmic_e, Ae/Ao)

    def frequency_residual(candidate, domain):
        return simp((No*candidate-Ne) if domain == 'static' else (Ao*candidate-Ae))

    exact('static_frequency_validator', frequency_residual(static_o/static_e, 'static'))
    exact('FLRW_frequency_validator', frequency_residual(cosmic_o/cosmic_e, 'FLRW'))
    truth('swapped_domains_rejected',
          frequency_residual(Ae/Ao, 'static') != 0
          and frequency_residual(Ne/No, 'FLRW') != 0,
          'Independent endpoint lapses cannot be substituted for scale factors.')

    # One minimally coupled mass; energy and coordinate inertia differ.
    m, N, B, p = s.symbols('m N B p', positive=True)
    v = s.symbols('v', real=True)
    lag = -m*N*s.sqrt(1-B**2*v**2/N**2)
    canonical_energy = s.diff(lag, v)*v-lag
    rest = simp(canonical_energy.subs(v, 0))
    inertia = simp(s.diff(lag, v, 2).subs(v, 0))
    exact('particle_rest_Killing_energy', rest, m*N)
    exact('particle_coordinate_inertia', inertia, m*B**2/N)
    branch = {N:p, B:1/p}
    exact('common_branch_rest_energy', rest.subs(branch), m*p)
    exact('common_branch_coordinate_inertia', inertia.subs(branch), m/p**3)

    def rest_residual(candidate):
        return simp(candidate-rest.subs(branch))

    exact('rest_energy_validator', rest_residual(m*p))
    twice = simp((-lag).subs({v:0, m:m*p}).subs(branch))
    exact('extra_local_mass_factor_double_counts', twice, m*p**2)
    truth('double_counted_mass_rejected', rest_residual(twice) != 0,
          'The local rest mass stays fixed; m*p is already a Killing-energy readout.')

    # Allowed material variations relax the field stiffness after constraints.
    A, C = s.symbols('A C', positive=True)
    mix, h, x = s.symbols('B_mix h x', real=True)
    quadratic = A*h*h/2+mix*h*x+C*x*x/2
    stationary_x = s.solve(s.diff(quadratic, x), x)[0]
    relaxed = simp(quadratic.subs(x, stationary_x))
    stiffness = simp(s.diff(relaxed, h, 2))
    exact('material_stationarity', s.diff(quadratic, x).subs(x, stationary_x))
    exact('mixed_response_Schur_complement', stiffness, A-mix**2/C)
    exact('complete_square_identity', quadratic,
          C*(x+mix*h/C)**2/2+(A-mix**2/C)*h*h/2)
    determinant = s.hessian(quadratic, (h, x)).det()
    exact('mixed_Hessian_determinant', determinant, C*stiffness)
    witness = {A:1, C:1, mix:2}
    exact('positive_diagonal_negative_determinant', determinant.subs(witness), -3)
    truth('diagonal_only_stability_control_rejected',
          (stiffness.subs(witness) < 0) == s.true,
          'A=C=1 are positive, but the actual relaxed stiffness is -3.')
    truth('omitted_mixed_response_rejected', simp(A-stiffness) != 0,
          'Uses the same stiffness derived by eliminating the material variable.')

    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    numerical = {}
    try:
        m66 = load('w92_audit_w66', sf/'W3-66_Physical_Radial_Mode/w3_66_physical_radial_mode.py')
        m65 = load('w92_audit_w65', sf/'W3-65_First_Turning_Point/w3_65_fixed_alpha_first_turning_point.py')
        dep, mod = m66.dependencies()
        truth('upstream_source_ledger', dep['all_pass'], 'Original W66 dependency gate rerun.')
        if not dep['all_pass']:
            raise RuntimeError('Original W66 dependency gate failed')
        saved65 = json.loads(m66.P65R.read_text(encoding='utf-8'))
        saved66 = json.loads(m66.OUTPUT.read_text(encoding='utf-8'))
        rows = saved65['forward_branch']['records']
        pre = [r for r in rows if r['f0'] < m66.TURN]
        secants = []
        for left, right in zip(pre, pre[1:]):
            dq = right['charge']-left['charge']
            if dq == 0:
                raise RuntimeError('Zero charge increment in the saved branch')
            secants.append(dict(f0_interval=[left['f0'], right['f0']], delta_Q=dq,
                delta_Omega_over_delta_Q=(right['Omega']-left['Omega'])/dq))
        truth('saved_36_preturn_charge_increments_positive',
              len(secants) == 36 and all(r['delta_Q'] > 0 for r in secants),
              'Arithmetic on the pinned saved equilibrium samples.')
        truth('saved_36_marginal_mass_secants_decrease',
              len(secants) == 36 and all(r['delta_Omega_over_delta_Q'] < 0 for r in secants),
              'Sampled secants, not a continuum derivative-sign proof.')
        first_law = m65.first_law_gate(rows)
        truth('first_law_recomputed_from_saved_rows', first_law['pass'],
              str(first_law))
        truth('first_law_saved_value_reproduced',
              abs(first_law['normalized_l2_residual']
                  - saved65['branch_first_law']['normalized_l2_residual']) < 1e-15,
              'dM=Omega*dQ is reevaluated, not inferred from decreasing secants.')
        error = max(saved66['deterministic_eigenvalue_error'].values())
        modes = saved66['primary_modes']
        before_turn = [r for r in modes if r['f0'] < m66.TURN]
        after_turn = [r for r in modes if r['f0'] > m66.TURN]
        truth('saved_W66_radial_spectrum_verified_as_saved',
              saved66['artifact_valid'] and len(before_turn) == 5 and len(after_turn) == 4
              and all(r['Lambda'] > 5*error and r['physical_residuals_pass'] for r in before_turn)
              and all(r['Lambda'] < -5*error and r['physical_residuals_pass'] for r in after_turn),
              'Pinned saved fixed-charge radial spectrum; no spectral solver rerun here.')

        print('W92 audit: fresh original W65 anchor and continuation to f0=2.18',
              file=sys.stderr, flush=True)
        anchor, previous, _ = m65.anchor_gate(mod)
        if not anchor['pass']:
            raise RuntimeError('Original W65 anchor failed')
        targets = (2.16, 2.17, 2.18)
        fresh = []
        for f0 in m65.MAIN_F0_GRID[1:]:
            if f0 > targets[-1]+1e-11:
                break
            previous = m65.solve_at(mod, f0, previous)
            if any(abs(f0-t) < 1e-10 for t in targets):
                record = m65.compact_record(f0, m65.observe(mod, previous, f0, with_residuals=True))
                if not m65.basic_profile_pass(record):
                    raise RuntimeError('Original W65 profile gate failed at '+str(f0))
                fresh.append(record)
        truth('fresh_original_background_gates', len(fresh) == 3,
              'Original alpha=.04, radius=80, tolerance=1e-7, quadrature=8001; all profile gates passed.')
        names = ('ADM_mass', 'charge', 'Omega', 'central_lapse',
                 'charge_rms_radius', 'maximum_compactness')
        mismatch = []
        for row in fresh:
            old = min(rows, key=lambda r: abs(r['f0']-row['f0']))
            if abs(old['f0']-row['f0']) > 1e-12:
                raise RuntimeError('Fresh state has no matching registered saved state')
            mismatch.append(max(abs(row[k]-old[k])/max(abs(old[k]), 1e-30) for k in names))
        truth('fresh_backgrounds_reproduce_saved',
              len(mismatch) == 3 and max(mismatch) < 5e-4,
              'Original observable convergence budget; maximum relative differences '+str(mismatch))
        fresh_secants = []
        for left, right in zip(fresh, fresh[1:]):
            dq = right['charge']-left['charge']
            if dq <= 0:
                raise RuntimeError('Fresh charge failed to increase')
            fresh_secants.append(dict(f0_interval=[left['f0'], right['f0']], delta_Q=dq,
                delta_Omega_over_delta_Q=(right['Omega']-left['Omega'])/dq,
                delta_ADM_over_delta_Q=(right['ADM_mass']-left['ADM_mass'])/dq))
        truth('fresh_sampled_marginal_mass_decreases', len(fresh_secants) == 2
              and all(r['delta_Omega_over_delta_Q'] < 0 for r in fresh_secants),
              'Two newly recomputed adjacent equilibrium secants.')
        numerical = dict(first_law_from_saved_rows=first_law,
            saved_secants=secants, fresh_backgrounds=fresh, fresh_secants=fresh_secants,
            fresh_saved_relative_differences=mismatch,
            saved_radial_modes=[{k:r[k] for k in ('f0', 'Omega', 'Lambda')} for r in modes],
            saved_radial_error_bound=error,
            saved_first_law_nested_residuals=saved65['turning_point']['first_law_nested_step_residuals'])
    except Exception as exc:
        truth('numerical_execution_completed', False, type(exc).__name__+': '+str(exc))
    truth('upstream_files_unchanged',
          actual == {name:sha(sf/name) for name in pins}, 'All nine pinned files rehashed.')
    passed = all(row['passed'] for row in checks)
    result = dict(status='PASS_EXISTING_CONSTRAINED_FEEDBACK_AUDIT' if passed else 'AUDIT_FAILED',
        contract_sha256=sha(CONTRACT), verifier_sha256=sha(Path(__file__)),
        dependency_hashes=actual, check_count=len(checks), checks=checks, numerical=numerical,
        scope_flags=dict(readout_and_mixed_response_verified=passed,
            fresh_registered_equilibrium_subset_recomputed=passed,
            sampled_marginal_ADM_mass_weakening_verified=passed,
            radial_stability_evidence_is_saved=True, fresh_radial_spectrum_recomputed=False,
            nonlinear_evolution_performed=False, charge_identified_as_particle_count=False,
            unchanged_local_core_state_proved=False, new_medium_law_selected=False,
            full_foundation_self_regulation_derived=False, finite_mass_cap_derived=False,
            regular_black_hole_derived=False, observational_pass=False),
        interpretation='The existing jointly solved Einstein-scalar equilibria have decreasing '
            'sampled marginal ADM mass per conserved U(1) charge. Local core states vary along '
            'this family. Saved fixed-charge radial stability and new static recomputation '
            'are separate evidence; neither is a new nonlinear evolution or a pressure closure.')
    print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return 0 if passed else 1


def source_completeness_main():
    '''Stage 25: vary the complete clock projector; do not evolve new physics.'''
    checks = []

    def exact(name, value, expected=0):
        residual = simp(value-expected)
        checks.append(dict(name=name, passed=bool(residual == 0),
                           residual=str(residual)))

    pins = {
        ARTICLE: EXPECTED_SHA,
        ROOT/'intuitive/RefG_GE.md': INTUITIVE_GE_SHA,
        ROOT/'intuitive/RefG_EN.tex':
            '0b58fe40157d5049aba397090f947d9169089490eeeaa67145743915504b2b04',
        HERE/'nonlinear_equilibrium_evolution.py':
            '2c310a3a600b2ced39333c14a208a2fcb97ed6178c6906e0a55366e35ab1e4ca',
        HERE/'population_assembly_initial_data.py':
            'df0d16c7715a2c3e3e02ec3487f2cad2860bf772e69983de6e2fb5af295af97d',
    }
    # Article +---. Under delta g^ab=eps*l^a*l^b, with fixed scalar
    # covectors: Y=p.p, X=p.h, Z=h.h, a=l.p, b=l.h. l is initially null.
    actual = {str(p.relative_to(ROOT)): sha(p) if p.is_file() else None
              for p in pins}
    expected = {str(p.relative_to(ROOT)): h for p, h in pins.items()}
    if actual != expected:
        print(json.dumps(dict(status='DEPENDENCY_FAILURE',
            expected_hashes=expected, actual_hashes=actual), indent=2))
        return 1
    checks.append(dict(name='frozen_source_dependencies', passed=True))
    eps, X, Z, a, b = s.symbols('epsilon X Z a b', real=True)
    Y, kappa = s.symbols('Y kappa', positive=True)
    LH = -kappa*((X+eps*a*b)**2/(Y+eps*a*a)-(Z+eps*b*b))
    null_H = simp(-2*s.diff(LH, eps).subs(eps, 0))
    expected_H = -2*kappa*(b-X*a/Y)**2
    exact('full_clock_projector_metric_variation', null_H, expected_H)
    exact('static_clock_reduction', null_H.subs(X, 0), -2*kappa*b*b)
    exact('pure_clock_aligned_H_has_zero_projected_source',
          null_H.subs(b, X*a/Y))
    exact('dynamic_clock_normalization_and_mixed_terms',
          s.expand(null_H+2*kappa*b*b),
          4*kappa*X*a*b/Y-2*kappa*X*X*a*a/Y**2)
    # Incorrectly holding u^a fixed loses its metric normalization response.
    wrong_frozen_clock = -2*kappa*b*b
    witness = {Y:1, X:2, a:1, b:3, kappa:1}
    exact('moving_H_witness_full', null_H.subs(witness), -2)
    exact('moving_H_witness_frozen_clock',
          wrong_frozen_clock.subs(witness), -18)
    checks.append(dict(name='frozen_normalized_clock_rejected', passed=bool(
        simp((null_H-wrong_frozen_clock).subs(witness)) != 0)))
    # Holding the entire gamma^ab fixed would instead give zero source.
    checks.append(dict(name='frozen_entire_projector_rejected', passed=bool(
        null_H.subs(witness) != 0)))

    # Independent -+++ whole-action conversion: X_minus=-X_plus,
    # L_H=+kappa[Z_minus+X_minus**2/Y], Y=-gpp and T=-2*dL/dg.
    Xm = s.symbols('X_minus', real=True)
    LH_minus = kappa*(Z+eps*b*b+(Xm+eps*a*b)**2/(Y-eps*a*a))
    null_minus = simp(-2*s.diff(LH_minus, eps).subs(eps, 0))
    exact('whole_action_signature_conversion', null_minus.subs(Xm, -X), null_H)

    m, r, P = s.symbols('m r P', positive=True)
    radial_h = -m*s.exp(-m/r)/r**2
    exterior = null_H.subs({X:0, b:radial_h, kappa:P})
    exact('silent_exterior_radial_null_source', exterior,
          -2*P*m*m*s.exp(-2*m/r)/r**4)
    exact('conditional_zero_projected_gradient_source',
          null_H.subs(b, X*a/Y))
    pr, pi, gr, gi = s.symbols('P_re P_im grad_re grad_im', real=True)
    A = s.symbols('A', positive=True)
    rho_plus_pressure = A*(pr*pr+pi*pi+gr*gr+gi*gi)
    flux = A*(pr*gr+pi*gi)
    for sign in (-1, 1):
        square = A*((pr+sign*gr)**2+(pi+sign*gi)**2)
        exact('canonical_radial_null_square_'+str(sign),
              rho_plus_pressure+2*sign*flux,
              square)
        checks.append(dict(name='canonical_radial_null_nonnegative_'+str(sign),
                           passed=square.is_nonnegative is True))
    checks.append(dict(name='dependencies_unchanged', passed=all(
        sha(p) == h for p, h in pins.items())))
    passed = all(row['passed'] for row in checks)
    print(json.dumps(dict(
        status='PASS_SOURCE_CONTRACT_AUDIT' if passed else 'AUDIT_FAILED',
        contract_sha256=sha(CONTRACT), verifier_sha256=sha(Path(__file__)),
        dependency_hashes=actual, check_count=len(checks), checks=checks,
        projected_H_null_source=str(null_H),
        scope_flags=dict(covariant_projector_variation_verified=passed,
            unchanged_scalar_source_null_convergence=passed,
            medium_reduction_to_evolution_derived=False,
            medium_added_to_evolution=False, calibrated_physical_cutoff=False,
            healthy_global_medium=False, singularity_resolution=False,
            new_evolution_performed=False, official_theory_changed=False)),
        indent=2, allow_nan=False))
    return 0 if passed else 1


def joint_response_focusing_main():
    '''Stage 26: constrained local response versus the required null source.'''
    checks = []

    def exact(name, actual, expected=0):
        residual = simp(actual-expected)
        checks.append(dict(name=name, passed=bool(residual == 0),
                           residual=str(residual)))

    def truth(name, value):
        checks.append(dict(name=name, passed=bool(value)))

    pins = {ARTICLE:EXPECTED_SHA, ROOT/'intuitive/RefG_GE.md':INTUITIVE_GE_SHA,
        ROOT/'intuitive/RefG_EN.tex':
            '0b58fe40157d5049aba397090f947d9169089490eeeaa67145743915504b2b04',
        HERE/'nonlinear_equilibrium_evolution.py':
            '2c310a3a600b2ced39333c14a208a2fcb97ed6178c6906e0a55366e35ab1e4ca',
        HERE/'population_assembly_initial_data.py':
            'df0d16c7715a2c3e3e02ec3487f2cad2860bf772e69983de6e2fb5af295af97d'}
    actual = {str(p.relative_to(ROOT)):sha(p) if p.is_file() else None for p in pins}
    if any(actual[str(p.relative_to(ROOT))] != h for p,h in pins.items()):
        print(json.dumps(dict(status='DEPENDENCY_FAILURE', hashes=actual), indent=2))
        return 1
    truth('frozen_dependencies', True)

    eps, td, tz, ht, hz, q, v = s.symbols('eps td tz ht hz q v', real=True)
    kap, Q, y, b, k = s.symbols('kappa Q y b k', positive=True)
    # Positive-TT -+++ whole-action convention. No field is frozen when
    # expanding gamma^ab H_a H_b; Phi=t+eps*theta, H=q*t+v*z+eps*h.
    pt, pz = 1+eps*td, eps*tz
    Ht, Hz = q+eps*ht, v+eps*hz
    LH = kap*(-Ht**2+Hz**2+(pt*Ht-pz*Hz)**2/(pt**2-pz**2))
    H2 = simp(s.diff(LH, eps, 2).subs(eps, 0)/2)
    exact('full_affine_background_projector', H2,
          kap*((hz-q*tz)**2+v*v*tz*tz-2*v*ht*tz+2*q*v*td*tz))
    rt, rz = s.symbols('eta_t eta_z', real=True)
    shifted = simp(H2.subs({ht:rt+q*td, hz:rz+q*tz}))
    exact('temporal_deficit_derivative_cancels_after_field_shift', shifted,
          kap*(rz*rz-2*v*rt*tz+v*v*tz*tz))
    truth('shifted_principal_independent_of_q', not shifted.has(q))

    # Twice the spatially averaged Fourier density, after a time integration
    # by parts. The sine eta and cosine theta amplitudes are independent.
    eta_amp, theta_amp = s.symbols('eta_amp theta_amp', real=True)
    mode = kap*(k*k*eta_amp**2-2*v*k*eta_amp*td+v*v*k*k*theta_amp**2)
    eta_solution = v*td/k
    exact('elliptic_H_equation', s.diff(mode, eta_amp).subs(eta_amp, eta_solution))
    reduced = simp(mode.subs(eta_amp, eta_solution))
    exact('reduced_H_clock_kinetic_and_gradient', reduced,
          kap*v*v*(-td*td+k*k*theta_amp**2))
    truth('fixed_H_negative_control_detected',
          simp(reduced-mode.subs(eta_amp, 0)) != 0)

    fy, fb, fyy, fyb, fbb, wd, wz = s.symbols(
        'F_y F_b F_yy F_yb F_bb wd wz', real=True)
    dy = y*((1+eps*td)**2-eps**2*tz**2)-y
    db = b*((1+eps*wz)**2-eps**2*wd**2)-b
    jet = fy*dy+fb*db+fyy*dy**2/2+fyb*dy*db+fbb*db**2/2
    F2 = s.expand(jet).coeff(eps, 2)
    A, B, C, D, E = (y*fy+2*y*y*fyy, y*fy, -b*fb,
                     -b*fb-2*b*b*fbb, 4*y*b*fyb)
    exact('arbitrary_response_radial_principal', F2,
          A*td**2-B*tz**2+C*wd**2-D*wz**2+E*td*wz)
    Ae, Be, Ce, De, Ee = s.symbols('A_eff B_eff C D E', real=True)
    L2 = Ae*td**2-Be*tz**2+Ce*wd**2-De*wz**2+Ee*td*wz
    Hcan = s.diff(L2,td)*td+s.diff(L2,wd)*wd-L2
    exact('mixed_response_canonical_energy', Hcan,
          Ae*td**2+Ce*wd**2+Be*tz**2+De*wz**2)
    ptheta, pw = s.symbols('p_theta p_w', real=True)
    exact('mixed_response_momentum_shift',
          Hcan.subs({td:(ptheta-Ee*wz)/(2*Ae),wd:pw/(2*Ce)}),
          (ptheta-Ee*wz)**2/(4*Ae)+pw**2/(4*Ce)+Be*tz**2+De*wz**2)
    z=s.symbols('squared_speed', real=True)
    characteristic=s.Poly((Ae*z-Be)*(Ce*z-De)-Ee**2*z/4,z)
    root_product=simp(characteristic.nth(0)/characteristic.nth(2))
    exact('mixed_characteristic_root_product',root_product,Be*De/(Ae*Ce))
    ap,cp,dp,negative_stiffness=s.symbols('A_pos C_pos D_pos stiffness_size', positive=True)
    truth('negative_clock_stiffness_gives_one_negative_squared_characteristic',
          root_product.subs({Ae:ap,Ce:cp,De:dp,Be:-negative_stiffness}).is_negative is True)

    # Independent inverse-metric null variation l=(1,1) at g=diag(-1,1).
    Yeps, Xeps = 1-eps, -q+eps*(q+v)
    Zeps = -q*q+v*v+eps*(q+v)**2
    null_H = simp(-2*s.diff(kap*(Zeps+Xeps**2/Yeps), eps).subs(eps,0))
    null_F = -2*s.diff(Q*(fy*(-y*eps)+fb*b*eps),eps)
    exact('metric_variation_H_null_source', null_H, -2*kap*v*v)
    exact('metric_variation_F_null_source', null_F, 2*Q*(B+C))
    Stheta, Klabel = Q*B-kap*v*v, Q*C
    exact('joint_radial_source_energy_identity', null_F+null_H,
          2*(Stheta+Klabel))
    posS, posK = s.symbols('S_theta K_label', positive=True)
    ordinary = s.symbols('T_ordinary_ll', nonnegative=True)
    truth('strict_energy_implies_positive_medium_null_source',
          (2*(posS+posK)).is_positive is True)
    truth('nonnegative_ordinary_source_cannot_reverse_sign',
          (2*(posS+posK)+ordinary).is_positive is True)
    truth('NEC_boundary_has_negative_clock_stiffness_for_positive_label_inertia',
          (-posK).is_negative is True)
    exact('negative_source_control_clock_stiffness',
          Stheta.subs({Q:1,y:1,fy:1,kap:1,v:s.sqrt(3)}), -2)
    exact('negative_source_control_total',
          (null_F+null_H).subs({Q:1,y:1,fy:1,b:1,fb:-1,kap:1,v:s.sqrt(3)}), -2)

    # Minimal reciprocal-current fallback. It is a distinct new interaction,
    # not the article's already-minimal S_m. Stop at its source discriminator.
    n, mF, K, coupling, amp2, mu = s.symbols('n m_F K g s mu', positive=True)
    chi, epsn, xid, xiz, rr = s.symbols('chi epsn xid xiz r', real=True)
    energy = mF*n+K*n*n/2+coupling*n*amp2
    muF = s.diff(energy,n)
    exact('mixed_current_reciprocal_chemical_response',muF,mF+K*n+coupling*amp2)
    exact('mixed_current_single_counted_pressure',n*muF-energy,K*n*n/2)
    neq = (mu-mF-coupling*amp2)/K
    exact('fixed_chemical_potential_stationarity',
          s.diff(energy-mu*n,n).subs(n,neq))
    relaxed = simp((energy-mu*n).subs(n,neq))
    exact('induced_attractive_quartic',s.diff(relaxed,amp2,2),-coupling**2/K)
    # Current-conserving label expansion supplies interaction inertia too.
    nexp = n*(1-epsn*xiz-epsn**2*xid**2/2)
    medium_L = -mF*nexp-K*nexp**2/2-coupling*nexp*(chi+epsn*rr)**2
    exact('current_inertia_and_reciprocal_amplitude_vertex',
          s.expand(medium_L).coeff(epsn,2),
          n*(mF+K*n+coupling*chi**2)*xid**2/2-K*n*n*xiz**2/2
          +2*coupling*n*chi*rr*xiz-coupling*n*rr**2)
    a1,a2,ul=s.symbols('l_dchi l_dtheta u_l', real=True)
    fallback_null=a1*a1+amp2*a2*a2+n*muF*ul*ul
    truth('healthy_reciprocal_fallback_retains_NEC',fallback_null.is_nonnegative is True)
    truth('dependencies_unchanged',all(sha(p)==h for p,h in pins.items()))
    passed=all(row['passed'] for row in checks)
    print(json.dumps(dict(
        status='JOINT_RESPONSE_RADIAL_DEFOCUSING_EXCLUDED' if passed else 'AUDIT_FAILED',
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),
        dependency_hashes=actual,check_count=len(checks),checks=checks,
        source_identity='T_medium_ll=2*(S_theta+K_label)',
        fallback_equilibrium_domain='K>0 and mu>m_F+g*chi^2; fixed chemical potential, not fixed total charge',
        scope_flags=dict(joint_principal_source_identity_verified=passed,
            comoving_regular_principal_defocusing_excluded=passed,
            minimal_positive_enthalpy_current_fallback_defocusing_excluded=passed,
            finite_wavelength_instability_proved=False,physical_EFT_band_known=False,
            full_coupled_metric_constraint_reduction_verified=False,
            degenerate_or_relative_flow_branches_excluded=False,
            all_RefG_excluded=False,new_healthy_full_action_selected=False,
            singularity_resolution=False,new_collapse_run=False,
            official_theory_changed=False)),indent=2,allow_nan=False))
    return 0 if passed else 1


def derivative_medium_prototype_main():
    '''Stage 27: a new cubic scalar prototype, not the five-field article.'''
    import numpy as np
    from scipy.integrate import solve_ivp
    checks=[]

    def exact(name,value,target=0):
        residual=simp(value-target)
        checks.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))

    def truth(name,value):
        checks.append(dict(name=name,passed=bool(value)))

    pins={ARTICLE:EXPECTED_SHA,ROOT/'intuitive/RefG_GE.md':INTUITIVE_GE_SHA,
        ROOT/'intuitive/RefG_EN.tex':
            '0b58fe40157d5049aba397090f947d9169089490eeeaa67145743915504b2b04',
        HERE/'nonlinear_equilibrium_evolution.py':
            '2c310a3a600b2ced39333c14a208a2fcb97ed6178c6906e0a55366e35ab1e4ca',
        HERE/'population_assembly_initial_data.py':
            'df0d16c7715a2c3e3e02ec3487f2cad2860bf772e69983de6e2fb5af295af97d'}
    hashes={str(p.relative_to(ROOT)):sha(p) if p.is_file() else None for p in pins}
    if any(hashes[str(p.relative_to(ROOT))]!=h for p,h in pins.items()):
        print(json.dumps(dict(status='DEPENDENCY_FAILURE',hashes=hashes),indent=2))
        return 1
    truth('frozen_dependencies',True)

    # First, the simplest already-allowed normalized clock/label mixing.
    eps,tt,tz,wt,wz=s.symbols('eps theta_t theta_z label_t label_z',real=True)
    b=s.symbols('label_scale_squared',positive=True)
    normalized_mix=b*((1+eps*tt)*eps*wt-eps*tz*(1+eps*wz))**2/(
        (1+eps*tt)**2-eps**2*tz**2)
    exact('normalized_mixing_quadratic_expansion',
          s.diff(normalized_mix,eps,2).subs(eps,0)/2,b*(wt-tz)**2)
    inverse_metric=s.diag(-1,1)+eps*s.ones(2)
    clock_gradient=s.Matrix([1,0]);label_gradient=s.Matrix([0,s.sqrt(b)])
    null_mix=(clock_gradient.dot(inverse_metric*label_gradient))**2/(
        -clock_gradient.dot(inverse_metric*clock_gradient))
    exact('normalized_mixing_null_metric_variation',null_mix,b*eps**2/(1-eps))
    exact('normalized_mixing_background_value',null_mix.subs(eps,0))
    exact('normalized_mixing_background_null_source',s.diff(null_mix,eps).subs(eps,0))
    B,C,eta,mix=s.symbols('B C eta mixed_coefficient',real=True)
    exact('normalized_mixing_preserves_source_sum',(B-eta-mix)+(C+mix),B+C-eta)
    exact('strict_mixing_interval_width',(B-eta)-(-C),B+C-eta)
    exact('mixing_NEC_boundary_clock',(B-eta-mix).subs({eta:B+C,mix:-C}),0)
    exact('mixing_NEC_boundary_label',(C+mix).subs(mix,-C),0)

    x=s.symbols('X',real=True)
    coefficients=s.symbols('c0:6')
    trial=sum(c*x**i for i,c in enumerate(coefficients))
    equations=[s.diff(trial,x,j).subs(x,point)-target
        for point,targets in [(0,(0,1,1)),(s.Rational(1,2),(-4,-4,1))]
        for j,target in enumerate(targets)]
    solved=s.solve(equations,coefficients,dict=True)
    truth('unique_minimal_polynomial_for_declared_jets',len(solved)==1)
    K=s.expand(trial.subs(solved[0]))
    exact('declared_quintic',K,x+x*x/2-282*x**3+802*x**4-624*x**5)
    for point,targets in [(0,(0,1,1)),(s.Rational(1,2),(-4,-4,1))]:
        for j,target in enumerate(targets):
            exact('constitutive_jet_'+str(point)+'_'+str(j),s.diff(K,x,j).subs(x,point),target)

    P,g,a,ad,N=s.symbols('P g a a_dot lapse',positive=True)
    v,acc,H,Hd=s.symbols('phi_dot phi_ddot Hubble Hubble_dot',real=True)
    xv=v*v/2
    k0,k1,k2=[s.diff(K,x,j).subs(x,xv) for j in range(3)]
    rho=2*xv*k1-k0+6*g*H*v*xv
    pressure=k0-2*g*xv*acc
    J=v*k1+6*g*H*xv
    # Independent lapse/current/scale-factor variations of the action after
    # a boundary integration: L3 -> g*a^2*a_dot*phi_dot^3/N^3.
    mini=-3*P*a*ad*ad/N+a**3*N*K.subs(x,v*v/(2*N*N))+g*a*a*ad*v**3/N**3
    exact('independent_lapse_variation',s.diff(mini,N).subs({N:1,ad:a*H})/a**3,
          3*P*H*H-rho)
    exact('independent_shift_current',s.diff(mini,v).subs({N:1,ad:a*H})/a**3,J)
    mini1=mini.subs(N,1)
    moma=s.diff(mini1,ad)
    adotdot=a*(Hd+H*H)
    EL_a=(s.diff(moma,a)*ad+s.diff(moma,ad)*adotdot+s.diff(moma,v)*acc
          -s.diff(mini1,a)).subs(ad,a*H)
    exact('independent_scale_factor_variation',EL_a/(-3*a*a),
          P*(3*H*H+2*Hd)+pressure)
    D=k1+2*xv*k2+6*g*H*v+6*g*g*xv*xv/P
    acceleration=(-3*H*v*k1-9*g*H*H*v*v
                  +3*g*v**4*(k1+3*g*H*v)/(2*P))/D
    hubble_dot=-xv*(k1+3*g*H*v-g*acceleration)/P
    point={P:1,g:1,H:1,v:1}
    exact('on_shell_witness_acceleration',acceleration.subs(point),s.Rational(1,3))
    exact('on_shell_witness_Hubble_derivative',hubble_dot.subs(point),s.Rational(2,3))
    exact('on_shell_witness_Friedmann',(3*P*H*H-rho).subs(point))
    current_dot=s.diff(J,v)*acc+s.diff(J,H)*Hd
    exact('on_shell_witness_current',(current_dot+3*H*J).subs(
        {**point,acc:s.Rational(1,3),Hd:s.Rational(2,3)}))
    exact('on_shell_witness_Raychaudhuri',(2*P*Hd+rho+pressure).subs(
        {**point,acc:s.Rational(1,3),Hd:s.Rational(2,3)}))
    exact('on_shell_witness_negative_null_source',(rho+pressure).subs(
        {**point,acc:s.Rational(1,3)}),-s.Rational(4,3))
    exact('omitting_braiding_breaks_witness_constraint',(3*P*H*H-rho).subs(
        {**point,g:0}),3)

    # Full FLRW scalar lapse/shift elimination, unlike Stage26's WKB test.
    T,Sigma,zd,zlap,blap,lapsepert=s.symbols('Theta Sigma zeta_dot lap_zeta lap_shift lapse_pert',real=True)
    zgrad=s.symbols('gradient_zeta_squared_over_a_squared',real=True)
    Lscalar=-3*P*zd**2+P*zgrad+Sigma*lapsepert**2-2*T*lapsepert*blap+2*P*zd*blap+6*T*lapsepert*zd-2*P*lapsepert*zlap
    lapse_sol=P*zd/T
    shift_sol=(Sigma*lapse_sol+3*T*zd-P*zlap)/T
    exact('scalar_shift_constraint',s.diff(Lscalar,blap).subs(lapsepert,lapse_sol))
    exact('scalar_lapse_constraint',s.diff(Lscalar,lapsepert).subs(
        {lapsepert:lapse_sol,blap:shift_sol}))
    exact('reduced_scalar_kinetic_and_cross_term',Lscalar.subs(
        {lapsepert:lapse_sol,blap:shift_sol}),
        (P*P*Sigma/T**2+3*P)*zd**2+P*zgrad-2*P*P*zd*zlap/T)
    # The cross term in a^3 L is -2a P^2/Theta*zeta_dot*laplacian(zeta).
    # Its spatial and temporal boundary terms leave -d_t(a P^2/Theta)
    # times (spatial gradient zeta)^2. Verify this identity in one direction;
    # the three-dimensional result is its sum over spatial directions.
    time,space=s.symbols('time space',real=True)
    aa=s.Function('a')(time);th=s.Function('Theta')(time)
    zz=s.Function('zeta')(time,space);cross=aa*P**2/th
    zx=s.diff(zz,space);zt=s.diff(zz,time)
    exact('scalar_cross_term_boundary_identity',
          -2*cross*zt*s.diff(zx,space)+s.diff(cross,time)*zx**2
          -s.diff(cross*zx**2,time)+s.diff(2*cross*zt*zx,space))
    Td=s.symbols('Theta_dot',real=True)
    Fs_from_parts=(s.diff(aa*P**2/th,time)/aa-P).subs(
        {s.diff(aa,time):aa*H,s.diff(th,time):Td,th:T})
    exact('scalar_gradient_integration_by_parts',Fs_from_parts,
          P**2*(H/T-Td/T**2)-P)
    theta=P*H-g*v*xv
    theta_dot=P*Hd-3*g*xv*acc
    sigma=xv*k1+2*xv*xv*k2+12*g*H*v*xv-3*P*H*H
    Gs=P*P*sigma/theta**2+3*P
    Fs=P*P*(H/theta-theta_dot/theta**2)-P
    exact('background_scalar_gradient_from_reduction',
          Fs_from_parts.subs({T:theta,Td:theta_dot}),Fs)
    exact('independent_kinetic_formula',Gs,P*P*xv*D/theta**2)
    jetpoint={**point,acc:s.Rational(1,3),Hd:s.Rational(2,3)}
    exact('witness_Gs',Gs.subs(jetpoint),9)
    exact('witness_Fs',Fs.subs(jetpoint),s.Rational(1,3))
    exact('witness_scalar_speed_squared',(Fs/Gs).subs(jetpoint),s.Rational(1,27))
    exact('unbraided_stability_formula_is_inapplicable',
          (Fs+P*Hd/H**2).subs(jetpoint),1)
    exact('tensor_speed_squared',P/P,1)
    truth('positive_tensor_energy',P.is_positive is True)
    exact('constant_medium_GR_branch_energy',rho.subs(v,0),0)
    exact('constant_medium_GR_branch_current',J.subs(v,0),0)

    kfun=[s.lambdify(x,s.diff(K,x,j),'numpy') for j in range(3)]

    def diagnose(state):
        phi,vel,hub,scale=state
        xx=vel*vel/2
        kv,kx,kxx=[float(f(xx)) for f in kfun]
        den=kx+2*xx*kxx+6*hub*vel+6*xx*xx
        av=(-3*hub*vel*kx-9*hub*hub*vel*vel
            +1.5*vel**4*(kx+3*hub*vel))/den
        hv=-xx*(kx+3*hub*vel-av)
        th=hub-vel*xx
        thdot=hv-3*xx*av
        sig=xx*kx+2*xx*xx*kxx+12*hub*vel*xx-3*hub*hub
        gs=sig/th**2+3
        fs=hub/th-thdot/th**2-1
        density=2*xx*kx-kv+6*hub*vel*xx
        press=kv-2*xx*av
        current=vel*kx+6*hub*xx
        return dict(D=den,Theta=th,Gs=gs,Fs=fs,cs2=fs/gs,
            NEC=density+press,Friedmann=3*hub*hub-density,
            charge=scale**3*current+1,acceleration=av,Hubble_dot=hv,
            kinetic_identity=gs-xx*den/th**2)

    def rhs(t,state):
        d=diagnose(state)
        return np.array([state[1],d['acceleration'],d['Hubble_dot'],state[2]*state[3]])

    def failure(d):
        if not all(np.all(np.isfinite(value)) for value in d.values()):return 'nonfinite'
        for name in ('D','Gs','Fs'):
            if d[name]<=0: return name+'_nonpositive'
        if abs(d['Theta'])<=1e-8:return 'Theta_degenerate'
        if d['cs2']>1:return 'scalar_superluminal'
        if d['NEC']>=0:return 'NEC_nonnegative'
        return None

    def integrate(step,end,guard=False):
        count=round(abs(end)/step);dt=end/count
        state=np.array([0.,1.,1.,1.]);rows=[]
        for i in range(count+1):
            t=i*dt;d=diagnose(state);bad=failure(d)
            rows.append(dict(t=t,state=state.copy(),**d))
            if bad and guard:return rows,dict(first_failed_time=t,reason=bad,
                last_passing_time=rows[-2]['t'] if len(rows)>1 else None,
                Fs=d['Fs'],Gs=d['Gs'],cs2=d['cs2'])
            if i<count:
                a1=rhs(t,state);a2=rhs(t+dt/2,state+dt*a1/2)
                a3=rhs(t+dt/2,state+dt*a2/2);a4=rhs(t+dt,state+dt*a3)
                state=state+dt*(a1+2*a2+2*a3+a4)/6
        return rows,None

    runs={};steps=(2e-5,1e-5,5e-6)
    for direction in (-1,1):
        for step in steps:
            rows,guard=integrate(step,direction*.001)
            runs[direction,step]=rows
            truth('sampled_health_'+str(direction)+'_'+str(step),all(failure(r) is None for r in rows))
    allrows=[r for rows in runs.values() for r in rows]
    for field in ('Friedmann','charge','kinetic_identity'):
        truth('numerical_'+field+'_bound',max(abs(r[field]) for r in allrows)<1e-8)
    state_errors=[];dop_errors=[]
    for direction in (-1,1):
        coarse=runs[direction,steps[0]]
        for step,stride in [(steps[1],2),(steps[2],4)]:
            finer=runs[direction,step][::stride]
            matching_grid=(len(coarse)==len(finer) and all(
                abs(a['t']-b['t'])<1e-14 for a,b in zip(coarse,finer)))
            truth('matching_refinement_grid_'+str(direction)+'_'+str(step),matching_grid)
            error=(max(float(np.max(abs(a['state']-b['state'])))
                for a,b in zip(coarse,finer)) if matching_grid else None)
            state_errors.append(error)
        times=np.array([r['t'] for r in coarse])
        reference=solve_ivp(rhs,(0.,direction*.001),[0.,1.,1.,1.],
            method='DOP853',t_eval=times,rtol=1e-11,atol=1e-13,max_step=1e-4)
        reference_ok=(reference.success and len(reference.t)==len(times)
            and reference.y.shape==(4,len(times))
            and np.allclose(reference.t,times,rtol=0,atol=1e-14))
        truth('independent_integrator_completed_'+str(direction),reference_ok)
        dop_errors.append(float(np.max(abs(reference.y.T-np.array(
            [r['state'] for r in coarse])))) if reference_ok else None)
    truth('registered_refinement_agreement',all(e is not None and e<1e-8 for e in state_errors))
    truth('independent_integrator_agreement',all(e is not None and e<1e-8 for e in dop_errors))
    probes=[]
    for direction in (-1,1):
        for step in (1e-5,5e-6):
            rows,guard=integrate(step,direction*.005,guard=True)
            probes.append(dict(direction=direction,step=step,guard=guard,
                last_sample_time=rows[-1]['t']))
    summary={name:dict(min=min(r[name] for r in allrows),max=max(r[name] for r in allrows))
             for name in ('Gs','Fs','cs2','NEC','D','Theta')}
    summary.update(max_Friedmann_residual=max(abs(r['Friedmann']) for r in allrows),
        max_current_drift=max(abs(r['charge']) for r in allrows),
        refinement_state_errors=state_errors,independent_integrator_errors=dop_errors)
    truth('dependencies_unchanged',all(sha(p)==h for p,h in pins.items()))
    passed=all(row['passed'] for row in checks)
    print(json.dumps(dict(status='LOCAL_DERIVATIVE_MEDIUM_WITNESS_VERIFIED' if passed else 'PROTOTYPE_FAILED',
        contract_sha256=sha(CONTRACT),verifier_sha256=sha(Path(__file__)),dependency_hashes=hashes,
        check_count=len(checks),checks=checks,polynomial=str(K),
        accepted_sampled_interval=[-.001,.001] if passed else None,
        numerical=summary,wider_guard_probes=probes,
        scope_flags=dict(new_constitutive_hypothesis=True,exact_on_shell_witness=passed,
            FLRW_lapse_shift_reduction_verified=passed,local_linear_health_and_NEC_violation=passed,
            sampled_interval_verified=passed,continuous_interval_certified=False,
            exact_GR_constant_medium_branch=passed,healthy_branch_connection_proved=False,
            original_five_field_reduction_derived=False,nonzero_oscillon_coupled_solution=False,
            spacelike_radial_health_proved=False,physical_EFT_band_known=False,
            UV_completion_proved=False,
            global_nonsingular_history=False,regular_black_hole=False,
            original_solver_changed=False,official_theory_changed=False)),indent=2,allow_nan=False))
    return 0 if passed else 1


if __name__ == '__main__':
    if sys.argv[1:] == ['--derivative-medium-prototype-only']:
        raise SystemExit(derivative_medium_prototype_main())
    if sys.argv[1:] == ['--joint-response-focusing-only']:
        raise SystemExit(joint_response_focusing_main())
    if sys.argv[1:] == ['--source-completeness-only']:
        raise SystemExit(source_completeness_main())
    if sys.argv[1:] == ['--self-regulation-audit-only']:
        raise SystemExit(self_regulation_audit_main())
    if sys.argv[1:] == ['--scale-feedback-only']:
        raise SystemExit(scale_feedback_main())
    if sys.argv[1:] == ['--full-source-balance-only']:
        raise SystemExit(full_static_balance_main())
    if sys.argv[1:] == ['--centre-response-only']:
        raise SystemExit(centre_response_main())
    if sys.argv[1:] == ['--separated-response-only']:
        raise SystemExit(separated_response_main())
    if sys.argv[1:] == ['--feedback-interface-only']:
        raise SystemExit(feedback_interface_main())
    if sys.argv[1:] == ['--same-field-response-only']:
        raise SystemExit(same_field_response_main())
    if sys.argv[1:] == ['--closure-selection-only']:
        raise SystemExit(closure_selection_main())
    if sys.argv[1:]:
        raise SystemExit('Usage: python -B verify_medium_health_horizon_diagnostic.py '
                         '[--scale-feedback-only | --full-source-balance-only | '
                         '--centre-response-only | --separated-response-only | '
                         '--feedback-interface-only | --same-field-response-only | '
                         '--closure-selection-only | --self-regulation-audit-only | '
                         '--source-completeness-only | --joint-response-focusing-only | '
                         '--derivative-medium-prototype-only]')
    raise SystemExit(main())
