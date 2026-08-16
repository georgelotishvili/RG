'''W3-18 preregistered PHANGS vortex--stellar clock pilot for NGC 4303.'''

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
import warnings
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import astropy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy
from astropy.io import fits
from astropy.table import Table
from astropy.wcs import FITSFixedWarning, WCS
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import differential_evolution, minimize


CLAIM_ID = 'W3_18_PHANGS_VORTEX_STELLAR_CLOCK'
MODEL_VERSION = 'W3-18-v1.1-PREREGISTERED'
UPSTREAM_CLAIM = 'W3_17_PHANGS_DATA_INTEGRITY'
UPSTREAM_VERSION = 'W3-17-v1.1-PHANGS-DR5'
PINNED_PREREG_SHA256 = '24eebb2970afb6d2e0ba200c797f68f6890046449defbc7594a718f395207638'
PINNED_UPSTREAM_SOURCE_SHA256 = '4fe132df22cb7538202c9e47051e46127a559846c63840606cc66c116761c19a'
PINNED_UPSTREAM_RESULT_SHA256 = 'a60c6ce326dc116c3d8c2416b160f39538d582afd8cd6417835791abad766430'
ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'PHANGS_data' / 'raw'
UPSTREAM_SOURCE = ROOT / 'w3_17_phangs_data_manifest.py'
UPSTREAM_RESULT = ROOT / 'w3_17_result.json'
PREREG = ROOT / 'w3_18_phangs_clock_preregistration.md'
RESULT_PATH = ROOT / 'w3_18_result.json'
PLOT_PATH = ROOT / 'phangs_vortex_stellar_clock_test.png'

SEED = 317180
RNG = np.random.default_rng(SEED)
N_THETA = 360
THETA_GRID = np.arange(N_THETA, dtype=float) * (2.0 * np.pi / N_THETA)
DTHETA = 2.0 * np.pi / N_THETA
KMSKPC_TO_RADMYR = 1.0227121650537077e-3
RA0_DEG = 185.478750
DEC0_DEG = 4.473639
DISTANCE_KPC = 16.99e3
INCLINATION_RAD = np.deg2rad(23.5)
PA_RAD = np.deg2rad(312.4)
RADIAL_EDGES = np.asarray([3.0, 3.5, 4.0, 4.5, 5.0])
SIGMA_GRID_DEG = np.arange(1.0, 46.0, 1.0)
WILLIAMS_OMEGA = 43.5184106896
WILLIAMS_ERR_UP = 5.2826302933
WILLIAMS_ERR_DOWN = 10.0196621899


@dataclass
class ClockData:
    ids: np.ndarray
    theta: np.ndarray
    radius: np.ndarray
    age: np.ndarray
    age_lo: np.ndarray
    age_hi: np.ndarray
    omega_m: np.ndarray
    block: np.ndarray
    templates: np.ndarray
    correlations: np.ndarray
    selection_fraction: np.ndarray
    segment_counts: np.ndarray
    normalization_residual: float
    sample_flow: dict[str, int]
    mask_name: str
    catalog_kind: str
    age_max: float


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def verify_upstream() -> tuple[dict[str, Any], str]:
    if not UPSTREAM_SOURCE.exists() or not UPSTREAM_RESULT.exists():
        raise RuntimeError('W3-17 source/result missing')
    if not PREREG.exists() or sha256(PREREG) != PINNED_PREREG_SHA256:
        raise RuntimeError('frozen W3-18 preregistration hash mismatch')
    if sha256(UPSTREAM_SOURCE) != PINNED_UPSTREAM_SOURCE_SHA256:
        raise RuntimeError('pinned W3-17 source hash mismatch')
    if sha256(UPSTREAM_RESULT) != PINNED_UPSTREAM_RESULT_SHA256:
        raise RuntimeError('pinned W3-17 result hash mismatch')
    artifact = json.loads(UPSTREAM_RESULT.read_text(encoding='utf-8'))
    if artifact.get('claim_id') != UPSTREAM_CLAIM:
        raise RuntimeError('W3-17 claim mismatch')
    if artifact.get('model_version') != UPSTREAM_VERSION:
        raise RuntimeError('W3-17 version mismatch')
    if artifact.get('status') != 'PASS':
        raise RuntimeError('W3-17 did not pass')
    if not artifact.get('closure_flags') or not all(artifact['closure_flags'].values()):
        raise RuntimeError('W3-17 closure flags are not all true')
    actual_source_hash = sha256(UPSTREAM_SOURCE)
    if artifact['provenance']['source_sha256'] != actual_source_hash:
        raise RuntimeError('W3-17 result is stale relative to its source')
    for record in artifact['provenance']['files']:
        path = ROOT / record['relative_path']
        if not path.exists():
            raise RuntimeError('missing raw product: {}'.format(record['relative_path']))
        if path.stat().st_size != record['bytes'] or sha256(path) != record['sha256']:
            raise RuntimeError('raw product changed: {}'.format(record['relative_path']))
    return artifact, sha256(UPSTREAM_RESULT)


def text_values(column: Any) -> np.ndarray:
    return np.asarray([
        value.decode('utf-8', errors='replace').strip().lower()
        if isinstance(value, (bytes, np.bytes_))
        else str(value).strip().lower()
        for value in column
    ])


def read_image(filename: str) -> tuple[np.ndarray, WCS]:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', FITSFixedWarning)
        with fits.open(RAW / filename) as hdul:
            hdu = next(item for item in hdul if item.data is not None)
            data = np.asarray(hdu.data, dtype=float)
            wcs = WCS(hdu.header)
    wcs.sip = None
    if not wcs.has_celestial:
        raise RuntimeError(f'no celestial WCS in {filename}')
    return data, wcs


def deproject(ra_deg: np.ndarray, dec_deg: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    east = (ra_deg - RA0_DEG) * np.cos(np.deg2rad(DEC0_DEG)) * 3600.0
    north = (dec_deg - DEC0_DEG) * 3600.0
    major = east * np.sin(PA_RAD) + north * np.cos(PA_RAD)
    minor = (-east * np.cos(PA_RAD) + north * np.sin(PA_RAD)) / np.cos(INCLINATION_RAD)
    radius = np.hypot(major, minor) * DISTANCE_KPC / 206265.0
    theta = np.mod(np.arctan2(minor, major), 2.0 * np.pi)
    return radius, theta


def disk_to_sky(radius_kpc: np.ndarray, theta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    major = radius_kpc * np.cos(theta)
    minor_projected = radius_kpc * np.sin(theta) * np.cos(INCLINATION_RAD)
    east_kpc = major * np.sin(PA_RAD) - minor_projected * np.cos(PA_RAD)
    north_kpc = major * np.cos(PA_RAD) + minor_projected * np.sin(PA_RAD)
    east_arcsec = east_kpc * 206265.0 / DISTANCE_KPC
    north_arcsec = north_kpc * 206265.0 / DISTANCE_KPC
    ra = RA0_DEG + east_arcsec / (3600.0 * np.cos(np.deg2rad(DEC0_DEG)))
    dec = DEC0_DEG + north_arcsec / 3600.0
    return ra, dec


def sample_image(data: np.ndarray, wcs: WCS, ra: np.ndarray, dec: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x, y = wcs.world_to_pixel_values(ra, dec)
    xi = np.rint(x).astype(int)
    yi = np.rint(y).astype(int)
    inside = (xi >= 0) & (xi < data.shape[1]) & (yi >= 0) & (yi < data.shape[0])
    values = np.full(np.shape(ra), np.nan, dtype=float)
    values[inside] = data[yi[inside], xi[inside]]
    return values, inside


def rotation_curve() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    table = Table.read(RAW / 'PHANGS_RC_all_kpc.ecsv', format='ascii.ecsv')
    chosen = text_values(table['obj']) == 'ngc4303'
    radius = np.asarray(table['radius'][chosen], dtype=float)
    velocity = np.asarray(table['Vrot'][chosen], dtype=float)
    error_up = np.asarray(table['VrotErr+'][chosen], dtype=float)
    error_down = np.asarray(table['VrotErr-'][chosen], dtype=float)
    if len(radius) < 10 or not np.all(np.diff(radius) > 0):
        raise RuntimeError('invalid NGC 4303 rotation curve')
    return radius, velocity, error_up, error_down


def circular_runs(mask: np.ndarray) -> int:
    flag = np.asarray(mask, dtype=bool)
    if not np.any(flag):
        return 0
    if np.all(flag):
        return 1
    return int(np.count_nonzero(flag & ~np.roll(flag, 1)))


def build_ring_templates(
    radii: np.ndarray,
    blocks: np.ndarray,
    arm_data: np.ndarray,
    arm_wcs: WCS,
    env_data: np.ndarray,
    env_wcs: WCS,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    ring_r = radii[:, None] * np.ones((1, N_THETA))
    ring_theta = np.ones((len(radii), 1)) * THETA_GRID[None, :]
    ra, dec = disk_to_sky(ring_r, ring_theta)
    arm_values, arm_inside = sample_image(arm_data, arm_wcs, ra, dec)
    env_values, env_inside = sample_image(env_data, env_wcs, ra, dec)
    arm_binary = (arm_values > 0) & arm_inside
    selection = np.isin(env_values, [6.0, 7.0]) & env_inside
    if np.any(np.sum(arm_binary, axis=1) == 0) or np.any(np.sum(selection, axis=1) == 0):
        raise RuntimeError('empty arm or selection ring in frozen domain')

    templates = np.empty((len(SIGMA_GRID_DEG), len(radii), N_THETA), dtype=np.float32)
    correlations = np.empty_like(templates)
    selection_float = selection.astype(float)
    selection_fft = np.fft.fft(selection_float, axis=1)
    for index, sigma_intrinsic in enumerate(SIGMA_GRID_DEG):
        total_sigma = math.sqrt(3.0 ** 2 + sigma_intrinsic ** 2)
        smoothed = gaussian_filter1d(
            arm_binary.astype(float), total_sigma, axis=1, mode='wrap'
        )
        smoothed /= np.sum(smoothed, axis=1, keepdims=True) * DTHETA
        corr = np.fft.ifft(
            selection_fft * np.conj(np.fft.fft(smoothed, axis=1)), axis=1
        ).real * DTHETA
        templates[index] = smoothed.astype(np.float32)
        correlations[index] = corr.astype(np.float32)

    crosscheck_residual = 0.0
    for row in range(min(10, len(radii))):
        direct = np.asarray([
            np.sum(selection_float[row] * np.roll(templates[0, row], shift)) * DTHETA
            for shift in range(N_THETA)
        ])
        crosscheck_residual = max(
            crosscheck_residual,
            float(np.max(np.abs(direct - correlations[0, row]))),
        )
    if crosscheck_residual > 2e-6:
        raise RuntimeError('FFT selection normalization failed direct crosscheck')

    segment_counts = np.zeros(4, dtype=int)
    for block in range(4):
        members = blocks == block
        if np.any(members):
            segment_counts[block] = circular_runs(np.mean(arm_binary[members], axis=0) > 0.5)
    return (
        templates, correlations, np.mean(selection_float, axis=1),
        segment_counts, crosscheck_residual,
    )


def load_clock_data(catalog_kind: str, mask_name: str, age_max: float) -> ClockData:
    catalog_files = {
        'human': 'hlsp_phangs-cat_hst_acs-uvis_dr5-targets_v1_human-class1+2-primary.fits',
        'machine': 'hlsp_phangs-cat_hst_acs-uvis_dr5-targets_v1_machine-class1+2-primary.fits',
    }
    table = Table.read(RAW / catalog_files[catalog_kind])
    target = text_values(table['PHANGS_GALAXY']) == 'ngc4303'
    table = table[target]
    n = len(table)
    ra = np.asarray(table['PHANGS_RA'], dtype=float)
    dec = np.asarray(table['PHANGS_DEC'], dtype=float)
    age = np.asarray(table['PHANGS_DR5_THILKER25_AGE'], dtype=float)
    age_lo = np.asarray(table['PHANGS_DR5_THILKER25_AGE_LIMLO'], dtype=float)
    age_hi = np.asarray(table['PHANGS_DR5_THILKER25_AGE_LIMHI'], dtype=float)
    mass = np.asarray(table['PHANGS_DR5_THILKER25_MASS'], dtype=float)
    non_detection = np.asarray(table['PHANGS_NON_DETECTION_FLAG'], dtype=float)
    chi2 = np.asarray(table['PHANGS_DR5_THILKER25_REDUCED_MINCHISQ'], dtype=float)
    human_class = np.asarray(table['PHANGS_CLUSTER_CLASS_HUMAN'], dtype=float)
    ml_class = np.asarray(table['PHANGS_CLUSTER_CLASS_ML_VGG'], dtype=float)
    ml_quality = np.asarray(table['PHANGS_CLUSTER_CLASS_ML_VGG_QUAL'], dtype=float)
    ids = np.asarray([str(value).strip() for value in table['ID_PHANGS_CLUSTER']])
    radius, theta = deproject(ra, dec)

    finite = np.isfinite(ra) & np.isfinite(dec) & np.isfinite(age)
    finite &= np.isfinite(age_lo) & np.isfinite(age_hi) & np.isfinite(mass)
    finite &= np.isfinite(non_detection) & np.isfinite(chi2)
    positive = finite & (age > 0) & (age_lo > 0) & (age_hi > 0) & (mass > 0)
    massive = positive & (mass >= 1.0e4)
    detected = massive & (non_detection <= 1)
    fit_quality = detected & (chi2 < 10)
    width = np.full(n, np.inf)
    width[positive] = 0.5 * (np.log10(age_hi[positive]) - np.log10(age_lo[positive]))
    age_precision = fit_quality & (width <= 0.30)
    if catalog_kind == 'human':
        classification = np.isin(human_class, [1.0, 2.0])
    else:
        classification = np.isin(ml_class, [1.0, 2.0]) & (ml_quality >= 0.90)
    classified = age_precision & classification
    age_window = ((age >= 1) & (age <= 3)) | ((age >= 6) & (age <= age_max))
    aged = classified & age_window
    radial = aged & (radius >= RADIAL_EDGES[0]) & (radius < RADIAL_EDGES[-1])

    arm_data, arm_wcs = read_image(mask_name)
    env_data, env_wcs = read_image('NGC4303_env_mask_simple.fits.gz')
    env_value, env_inside = sample_image(env_data, env_wcs, ra, dec)
    arm_value, arm_inside = sample_image(arm_data, arm_wcs, ra, dec)
    footprint = radial & env_inside & arm_inside
    environmental = footprint & np.isin(env_value, [6.0, 7.0])
    keep = environmental
    block = np.digitize(radius[keep], RADIAL_EDGES) - 1

    curve_r, curve_v, _, _ = rotation_curve()
    vrot = np.interp(radius[keep], curve_r, curve_v)
    omega_m = vrot / radius[keep]
    templates, correlations, selection_fraction, segment_counts, norm_residual = build_ring_templates(
        radius[keep], block, arm_data, arm_wcs, env_data, env_wcs
    )
    sample_flow = {
        'target_rows': n,
        'finite_core': int(np.count_nonzero(finite)),
        'positive_core': int(np.count_nonzero(positive)),
        'mass_cut': int(np.count_nonzero(massive)),
        'non_detection_cut': int(np.count_nonzero(detected)),
        'sed_chi2_cut': int(np.count_nonzero(fit_quality)),
        'age_precision_cut': int(np.count_nonzero(age_precision)),
        'classification_cut': int(np.count_nonzero(classified)),
        'anchor_or_clock_age': int(np.count_nonzero(aged)),
        'radial_domain': int(np.count_nonzero(radial)),
        'shared_mask_footprint': int(np.count_nonzero(footprint)),
        'environment_6_or_7': int(np.count_nonzero(environmental)),
        'anchor_final': int(np.count_nonzero(keep & (age >= 1) & (age <= 3))),
        'clock_final': int(np.count_nonzero(keep & (age >= 6) & (age <= age_max))),
    }
    for index in range(4):
        member = keep & (radius >= RADIAL_EDGES[index]) & (radius < RADIAL_EDGES[index + 1])
        sample_flow[f'block_{index}_total'] = int(np.count_nonzero(member))
        sample_flow[f'block_{index}_clock'] = int(
            np.count_nonzero(member & (age >= 6) & (age <= age_max))
        )
        sample_flow[f'block_{index}_anchor'] = int(
            np.count_nonzero(member & (age >= 1) & (age <= 3))
        )
    return ClockData(
        ids=ids[keep], theta=theta[keep], radius=radius[keep], age=age[keep],
        age_lo=age_lo[keep], age_hi=age_hi[keep], omega_m=omega_m,
        block=block, templates=templates, correlations=correlations,
        selection_fraction=selection_fraction, segment_counts=segment_counts,
        normalization_residual=norm_residual,
        sample_flow=sample_flow, mask_name=mask_name,
        catalog_kind=catalog_kind, age_max=age_max,
    )


def interp_rows(values: np.ndarray, angles: np.ndarray) -> np.ndarray:
    position = np.mod(angles, 2.0 * np.pi) / DTHETA
    left = np.floor(position).astype(int) % N_THETA
    fraction = position - np.floor(position)
    right = (left + 1) % N_THETA
    rows = np.arange(len(angles))
    return values[rows, left] * (1.0 - fraction) + values[rows, right] * fraction


def parameter_bounds(q_fixed: float | None) -> tuple[list[tuple[float, float]], int]:
    if q_fixed is None:
        return [
            (0.0, 4.0), (0.0, 80.0), (1.0, 45.0), (0.0, 0.8),
            *[(np.deg2rad(-45.0), np.deg2rad(45.0)) for _ in range(4)],
        ], 2
    return [
        (0.0, 80.0), (1.0, 45.0), (0.0, 0.8),
        *[(np.deg2rad(-45.0), np.deg2rad(45.0)) for _ in range(4)],
    ], 1


def unpack(parameters: np.ndarray, q_fixed: float | None) -> tuple[float, float, int, float, np.ndarray]:
    if q_fixed is None:
        q, omega_p, sigma_value, background = parameters[:4]
        offsets = parameters[4:8]
    else:
        q = q_fixed
        omega_p, sigma_value, background = parameters[:3]
        offsets = parameters[3:7]
    sigma_index = int(np.clip(np.rint(sigma_value), 1, 45)) - 1
    return float(q), float(omega_p), sigma_index, float(background), np.asarray(offsets)


def nll(
    parameters: np.ndarray,
    data: ClockData,
    orientation: int,
    q_fixed: float | None = None,
    ages: np.ndarray | None = None,
    weights: np.ndarray | None = None,
) -> float:
    q, omega_p, sigma_index, background, offsets = unpack(parameters, q_fixed)
    use_ages = data.age if ages is None else ages
    shift = orientation * q * (data.omega_m - omega_p) * KMSKPC_TO_RADMYR * use_ages
    shift += offsets[data.block]
    template = data.templates[sigma_index]
    correlation = data.correlations[sigma_index]
    arm_density = interp_rows(template, data.theta - shift)
    selected_norm = interp_rows(correlation, shift)
    density = (1.0 - background) * arm_density + background / (2.0 * np.pi)
    normalization = (1.0 - background) * selected_norm + background * data.selection_fraction
    probability = density / normalization
    if np.any(~np.isfinite(probability)) or np.any(probability <= 0):
        return 1.0e100
    use_weights = np.ones(len(data.age)) if weights is None else weights
    return float(-np.sum(use_weights * np.log(probability)))


def local_polish(
    full: np.ndarray,
    data: ClockData,
    orientation: int,
    q_fixed: float | None,
    ages: np.ndarray | None = None,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, float, bool]:
    bounds, sigma_position = parameter_bounds(q_fixed)
    sigma_value = int(np.clip(np.rint(full[sigma_position]), 1, 45))
    keep = [index for index in range(len(full)) if index != sigma_position]
    reduced0 = full[keep]
    reduced_bounds = [bounds[index] for index in keep]

    def expand(reduced: np.ndarray) -> np.ndarray:
        output = np.empty(len(full), dtype=float)
        output[keep] = reduced
        output[sigma_position] = sigma_value
        return output

    result = minimize(
        lambda reduced: nll(expand(reduced), data, orientation, q_fixed, ages, weights),
        reduced0, method='L-BFGS-B', bounds=reduced_bounds,
        options={'ftol': 1.0e-12, 'gtol': 1.0e-8, 'maxiter': 2000},
    )
    polished = expand(result.x)
    return polished, float(result.fun), bool(result.success and np.isfinite(result.fun))


def grid_polish(
    full: np.ndarray,
    data: ClockData,
    orientation: int,
    q_fixed: float | None,
    ages: np.ndarray | None = None,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, float, bool]:
    _, sigma_position = parameter_bounds(q_fixed)
    candidates: list[tuple[float, np.ndarray]] = []
    for sigma_value in range(1, 46):
        start = np.asarray(full, dtype=float).copy()
        start[sigma_position] = sigma_value
        polished, objective, success = local_polish(
            start, data, orientation, q_fixed, ages, weights
        )
        if success:
            candidates.append((objective, polished))
    if not candidates:
        return np.asarray(full, dtype=float), float('inf'), False
    objective, selected = min(candidates, key=lambda item: item[0])
    return selected, objective, True


def fit_model(data: ClockData, orientation: int, q_fixed: float | None) -> dict[str, Any]:
    bounds, sigma_position = parameter_bounds(q_fixed)
    integrality = [False] * len(bounds)
    integrality[sigma_position] = True
    runs: list[dict[str, Any]] = []
    for seed in [SEED, SEED + 1, SEED + 2]:
        result = differential_evolution(
            lambda values: nll(values, data, orientation, q_fixed),
            bounds=bounds, seed=seed, popsize=15, maxiter=400, tol=1.0e-8,
            polish=False, updating='immediate', workers=1,
            integrality=integrality,
        )
        polished, objective, local_success = grid_polish(
            np.asarray(result.x), data, orientation, q_fixed
        )
        runs.append({
            'seed': seed,
            'parameters': polished,
            'nll': objective,
            'de_success': bool(result.success),
            'local_success': local_success,
            'message': str(result.message),
        })
    best = min(runs, key=lambda item: item['nll'])
    spread = float(max(item['nll'] for item in runs) - min(item['nll'] for item in runs))
    q, omega_p, sigma_index, background, offsets = unpack(best['parameters'], q_fixed)
    k = 8 if q_fixed is None else 7
    return {
        'orientation': orientation,
        'q_fixed': q_fixed,
        'q': q,
        'omega_p_km_s_kpc': omega_p,
        'sigma_intrinsic_deg': int(SIGMA_GRID_DEG[sigma_index]),
        'background_fraction': background,
        'block_offsets_deg': np.rad2deg(offsets).tolist(),
        'nll': best['nll'],
        'bic': float(2.0 * best['nll'] + k * np.log(len(data.age))),
        'parameters': best['parameters'],
        'optimizer_seed_spread': spread,
        'optimizer_converged': bool(
            spread <= 1.0e-5 and all(item['local_success'] for item in runs)
        ),
        'runs': runs,
    }


def fixed_q_start(free_parameters: np.ndarray) -> np.ndarray:
    return np.concatenate([
        free_parameters[1:4],
        free_parameters[4:8],
    ])


def profile_q(
    data: ClockData,
    free_fits: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    q_grid = np.round(np.arange(0.0, 4.0001, 0.02), 2)
    branch_nll = {orientation: np.empty(len(q_grid)) for orientation in [-1, 1]}
    branch_omega = {orientation: np.empty(len(q_grid)) for orientation in [-1, 1]}
    branch_sigma = {orientation: np.empty(len(q_grid), dtype=int) for orientation in [-1, 1]}
    for orientation in [-1, 1]:
        base = fixed_q_start(free_fits[orientation]['parameters'])
        center_index = int(np.argmin(np.abs(q_grid - free_fits[orientation]['q'])))
        initial_bases = []
        for sigma_value in range(1, 46):
            start = base.copy()
            start[1] = sigma_value
            initial_bases.append(start)

        def evaluate(q_index: int, bases: list[np.ndarray]) -> list[np.ndarray]:
            candidates: list[tuple[float, np.ndarray]] = []
            updated: list[np.ndarray] = []
            for sigma_value, start in enumerate(bases, start=1):
                polished, objective, success = local_polish(
                    start, data, orientation, float(q_grid[q_index])
                )
                if success:
                    candidates.append((objective, polished))
                    updated.append(polished)
                else:
                    updated.append(start)
            if not candidates:
                branch_nll[orientation][q_index] = np.inf
                branch_omega[orientation][q_index] = np.nan
                branch_sigma[orientation][q_index] = -1
                return updated
            objective, selected = min(candidates, key=lambda item: item[0])
            branch_nll[orientation][q_index] = objective
            branch_omega[orientation][q_index] = selected[0]
            branch_sigma[orientation][q_index] = int(np.rint(selected[1]))
            return updated

        center_bases = evaluate(center_index, initial_bases)
        bases = [value.copy() for value in center_bases]
        for q_index in range(center_index + 1, len(q_grid)):
            bases = evaluate(q_index, bases)
        bases = [value.copy() for value in center_bases]
        for q_index in range(center_index - 1, -1, -1):
            bases = evaluate(q_index, bases)

    combined = np.minimum(branch_nll[-1], branch_nll[1])
    best = float(np.min(combined))
    intervals: dict[str, list[float] | None] = {}
    components: dict[str, list[list[float]]] = {}
    for label, threshold in [('68', 1.0), ('95', 4.0), ('99.7', 9.0)]:
        accepted_mask = 2.0 * (combined - best) <= threshold
        accepted = q_grid[accepted_mask]
        intervals[label] = [float(accepted[0]), float(accepted[-1])] if len(accepted) else None
        accepted_indices = np.flatnonzero(accepted_mask)
        if len(accepted_indices):
            groups = np.split(
                accepted_indices,
                np.where(np.diff(accepted_indices) > 1)[0] + 1,
            )
            components[label] = [
                [float(q_grid[group[0]]), float(q_grid[group[-1]])]
                for group in groups
            ]
        else:
            components[label] = []
    preferred = np.where(branch_nll[-1] <= branch_nll[1], -1, 1)
    best_index = int(np.argmin(combined))
    return {
        'q_grid': q_grid,
        'combined_nll': combined,
        'branch_nll': branch_nll,
        'branch_omega': branch_omega,
        'branch_sigma_deg': branch_sigma,
        'preferred_orientation': preferred,
        'best_grid_q': float(q_grid[best_index]),
        'best_grid_nll': float(combined[best_index]),
        'intervals': intervals,
        'interval_components': components,
        'touches_boundary': bool(
            intervals['99.7'] is None
            or intervals['99.7'][0] <= 0.0
            or intervals['99.7'][1] >= 4.0
        ),
    }


def split_normal_draw(center: float, down: float, up: float, z: np.ndarray) -> np.ndarray:
    return center + np.where(z >= 0, z * up, z * down)


def radial_health(data: ClockData) -> dict[str, Any]:
    curve_r, curve_v, curve_up, curve_down = rotation_curve()
    draws = 10_000
    local_rng = np.random.default_rng(SEED + 20)
    z_curve = local_rng.normal(size=draws)
    z_pattern = local_rng.normal(size=draws)
    omega_pattern = split_normal_draw(
        WILLIAMS_OMEGA, WILLIAMS_ERR_DOWN, WILLIAMS_ERR_UP, z_pattern
    )
    velocity_draws = curve_v[None, :] + np.where(
        z_curve[:, None] >= 0,
        z_curve[:, None] * curve_up[None, :],
        z_curve[:, None] * curve_down[None, :],
    )
    output: dict[str, Any] = {}
    stable_blocks = 0
    leveraged_blocks = 0
    valid_blocks = 0
    for block in range(4):
        radii = data.radius[data.block == block]
        right = np.searchsorted(curve_r, radii, side='right')
        right = np.clip(right, 1, len(curve_r) - 1)
        left = right - 1
        fraction = (radii - curve_r[left]) / (curve_r[right] - curve_r[left])
        velocity_at_radii = (
            velocity_draws[:, left] * (1.0 - fraction[None, :])
            + velocity_draws[:, right] * fraction[None, :]
        )
        delta_draws = velocity_at_radii / radii[None, :] - omega_pattern[:, None]
        median_delta_draws = np.median(delta_draws, axis=1)
        positive = float(np.mean(median_delta_draws > 0))
        negative = float(np.mean(median_delta_draws < 0))
        sign_probability = max(positive, negative)
        nominal_delta_at_radii = (
            np.interp(radii, curve_r, curve_v) / radii - WILLIAMS_OMEGA
        )
        nominal_delta = float(np.median(nominal_delta_at_radii))
        leverage_deg = float(np.rad2deg(
            np.median(np.abs(nominal_delta_at_radii)) * KMSKPC_TO_RADMYR * 44.0
        ))
        sign_stable = sign_probability >= 0.95
        leverage_valid = leverage_deg > 6.0
        block_valid = sign_stable and leverage_valid
        stable_blocks += int(sign_stable)
        leveraged_blocks += int(leverage_valid)
        valid_blocks += int(block_valid)
        output[str(block)] = {
            'radius_median_kpc': float(np.median(radii)),
            'radius_count': int(len(radii)),
            'nominal_median_delta_omega_km_s_kpc': nominal_delta,
            'phase_leverage_6_to_50_myr_deg': leverage_deg,
            'positive_sign_probability': positive,
            'negative_sign_probability': negative,
            'sign_probability': sign_probability,
            'sign_stable_95': sign_stable,
            'leverage_over_6deg': leverage_valid,
            'block_valid': block_valid,
        }
    output['stable_block_count'] = stable_blocks
    output['leveraged_block_count'] = leveraged_blocks
    output['valid_block_count'] = valid_blocks
    output['required_valid_blocks'] = 3
    output['correlated_error_approximation'] = 'one coherent asymmetric Lang deviate across all radii'
    return output


def normalization_residual(data: ClockData, fit: dict[str, Any]) -> float:
    return data.normalization_residual


def public_fit(fit: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in fit.items()
        if key not in {'parameters', 'runs'}
    } | {
        'optimizer_runs': [
            {
                'seed': run['seed'],
                'nll': run['nll'],
                'de_success': run['de_success'],
                'local_success': run['local_success'],
                'message': run['message'],
            }
            for run in fit['runs']
        ]
    }


def make_plot(
    data: ClockData,
    fits: dict[str, dict[str, Any]],
    profile: dict[str, Any],
    health: dict[str, Any],
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), constrained_layout=True)
    clock = data.age >= 6
    for block in range(4):
        chosen = data.block == block
        axes[0, 0].scatter(
            data.radius[chosen], data.age[chosen], s=18, alpha=0.65,
            label=f'block {block + 1}', marker='o' if np.any(clock[chosen]) else 's',
        )
    axes[0, 0].axhspan(1, 3, color='grey', alpha=0.12, label='anchor 1--3 Myr')
    axes[0, 0].set(xlabel='Deprojected radius [kpc]', ylabel='DR5 age [Myr]', title='Frozen NGC 4303 sample')
    axes[0, 0].legend(fontsize=8, ncol=2)

    labels = ['M0 s=-1', 'M1 s=-1', 'M0 s=+1', 'M1 s=+1']
    keys = ['m0_minus', 'm1_minus', 'm0_plus', 'm1_plus']
    bics = [fits[key]['bic'] for key in keys]
    axes[0, 1].bar(labels, np.asarray(bics) - min(bics), color=['#6c8ebf', '#d79b00', '#6c8ebf', '#d79b00'])
    axes[0, 1].axhline(10, color='black', ls='--', lw=1)
    axes[0, 1].set(ylabel='BIC - best BIC', title='Common ticking and free q')
    axes[0, 1].tick_params(axis='x', rotation=25)

    q_grid = profile['q_grid']
    delta = 2.0 * (profile['combined_nll'] - np.min(profile['combined_nll']))
    axes[1, 0].plot(q_grid, delta, color='#7b3294', lw=2)
    for level, label in [(1, '68%'), (4, '95%'), (9, '99.7%')]:
        axes[1, 0].axhline(level, ls='--', lw=0.8, label=label)
    axes[1, 0].axvline(1, color='black', lw=1.2, label='q=1')
    axes[1, 0].set(xlabel='Clock ratio q', ylabel='2 Delta log likelihood', title='Profile likelihood', ylim=(0, min(20, np.nanmax(delta))))
    axes[1, 0].legend(fontsize=8)

    blocks = np.arange(4) + 1
    sign_prob = [health[str(i)]['sign_probability'] for i in range(4)]
    leverage = [health[str(i)]['phase_leverage_6_to_50_myr_deg'] for i in range(4)]
    axes[1, 1].bar(blocks - 0.16, sign_prob, width=0.32, label='sign probability')
    axes[1, 1].axhline(0.95, color='#2b8cbe', ls='--', lw=1)
    twin = axes[1, 1].twinx()
    twin.bar(blocks + 0.16, leverage, width=0.32, color='#e34a33', alpha=0.65, label='phase leverage')
    twin.axhline(6, color='#e34a33', ls=':', lw=1)
    axes[1, 1].set(xlabel='0.5-kpc radial block', ylabel='Sign stability probability', title='Identifiability health', xticks=blocks, ylim=(0, 1.05))
    twin.set_ylabel('6--50 Myr phase leverage [deg]')

    fig.suptitle('PHANGS NGC 4303 vortex--stellar clock pilot', fontsize=15)
    fig.savefig(PLOT_PATH, dpi=180)
    plt.close(fig)


def main() -> None:
    upstream, upstream_result_hash = verify_upstream()
    data = load_clock_data('human', 'NGC4303_spiral_mask_narrow.fits', 50.0)
    health = radial_health(data)

    raw_fits = {
        'm0_minus': fit_model(data, -1, 1.0),
        'm1_minus': fit_model(data, -1, None),
        'm0_plus': fit_model(data, 1, 1.0),
        'm1_plus': fit_model(data, 1, None),
    }
    free_by_orientation = {-1: raw_fits['m1_minus'], 1: raw_fits['m1_plus']}
    profile = profile_q(data, free_by_orientation)
    best_m0 = min([raw_fits['m0_minus'], raw_fits['m0_plus']], key=lambda item: item['bic'])
    best_m1 = min([raw_fits['m1_minus'], raw_fits['m1_plus']], key=lambda item: item['bic'])
    delta_bic = float(best_m0['bic'] - best_m1['bic'])
    orientation_delta = float(abs(raw_fits['m1_minus']['bic'] - raw_fits['m1_plus']['bic']))
    interval_997 = profile['intervals']['99.7']
    q_one_index = int(np.flatnonzero(profile['q_grid'] == 1.0)[0])
    profile_crosscheck = {
        'm0_nll_minus_profile_q1_nll': float(
            best_m0['nll'] - profile['combined_nll'][q_one_index]
        ),
        'profile_grid_min_nll_minus_continuous_m1_nll': float(
            profile['best_grid_nll'] - best_m1['nll']
        ),
    }
    primary_effect_thresholds_met = bool(
        delta_bic >= 10.0
        and interval_997 is not None
        and interval_997[0] > 1.0
    )
    sample_blocks = sum(
        data.sample_flow[f'block_{i}_clock'] > 0
        and data.sample_flow[f'block_{i}_anchor'] > 0
        for i in range(4)
    )

    closure = {
        'data_integrity': upstream['status'] == 'PASS' and all(upstream['closure_flags'].values()),
        'schema_valid': upstream['closure_flags']['schemas_valid'],
        'wcs_valid': data.sample_flow['shared_mask_footprint'] == data.sample_flow['radial_domain'],
        'sample_size_valid': bool(
            data.sample_flow['clock_final'] >= 50
            and sample_blocks >= 3
            and int(np.max(data.segment_counts)) >= 2
        ),
        'shared_footprint_valid': False,
        'radial_leverage_valid': bool(
            health['valid_block_count'] >= 3
        ),
        'orientation_identified': orientation_delta >= 10.0,
        'optimizer_converged': all(fit['optimizer_converged'] for fit in raw_fits.values()),
        'likelihood_normalized': data.normalization_residual <= 2.0e-6,
        'q_profile_finite': not profile['touches_boundary'],
        'pattern_speed_external_consistency': False,
        'permutation_complete': False,
        'block_bootstrap_complete': False,
        'injection_recovery_complete': False,
        'injection_recovery_valid': False,
        'robustness_complete': False,
        'pass_statistical_thresholds': False,
    }
    closure['pass_statistical_thresholds'] = bool(
        primary_effect_thresholds_met
        and closure['orientation_identified']
        and closure['pattern_speed_external_consistency']
        and closure['permutation_complete']
        and closure['block_bootstrap_complete']
        and closure['injection_recovery_valid']
        and closure['robustness_complete']
    )
    blocking_reasons = []
    if not closure['shared_footprint_valid']:
        blocking_reasons.append('No HST exposure/weight map or footprint polygon was present, so full-annulus selection normalization is unverified.')
    if not closure['radial_leverage_valid']:
        blocking_reasons.append(
            '{} radial blocks satisfied both the frozen 95% sign-stability and 6-degree leverage requirements; at least 3 were required.'.format(
                health['valid_block_count']
            )
        )
    if not closure['orientation_identified']:
        blocking_reasons.append('The two discrete rotation branches differ by less than Delta BIC=10.')
    if not closure['q_profile_finite']:
        blocking_reasons.append('The 99.7% q profile reaches a frozen parameter boundary, so the clock ratio is not fully identified.')
    blocking_reasons.append(
        'Distance and disk-geometry nuisance propagation was not completed; the frozen coherent asymmetric draw is used for the unavailable Lang joint covariance.'
    )

    make_plot(data, raw_fits, profile, health)
    result = {
        'schema_version': '1.0',
        'claim_id': CLAIM_ID,
        'claim': 'NGC 4303 cluster phase drift constrains a recent spiral-geometry to stellar-evolution clock ratio q.',
        'type': 'OBSERVATIONAL_NUMERICAL_TEST',
        'model_version': MODEL_VERSION,
        'status': 'OPEN',
        'evidence_type': 'NUMERICAL_EVIDENCE',
        'evidence_strength': 'N/A: mandatory identifiability and footprint gates remain open',
        'falsifier_triggered': False,
        'mechanism_status': 'OPEN',
        'refg_cosmological_clock_status': 'OPEN: no numerical RefG q prediction was supplied',
        'contract': {
            'CLAIM_ID': CLAIM_ID,
            'CLAIM': 'The common-ticking q=1 benchmark is compared with the directional q>1 mechanism in NGC 4303.',
            'TYPE': 'Observational circular forward-model pilot.',
            'MODEL_VERSION': MODEL_VERSION,
            'ASSUMPTIONS': 'See the frozen preregistration; no assumption was promoted by this result.',
            'DOMAIN': 'NGC 4303, 3--5 kpc, anchors 1--3 Myr, clocks 6--50 Myr.',
            'CONVENTIONS': 'Nearest categorical WCS lookup; SIP disabled; q=1 common ticking.',
            'FREEDOM_LEDGER': 'q, Omega_p, discrete orientation, integer sigma_int, f_bg, four offsets.',
            'DEPENDENCIES': [UPSTREAM_CLAIM, PINNED_UPSTREAM_SOURCE_SHA256, PINNED_UPSTREAM_RESULT_SHA256],
            'METHOD': 'Selection-normalized circular mask likelihood with three-seed global fits and the full frozen q grid.',
            'PASS_CONDITION': 'All preregistered atomic gates and statistical thresholds.',
            'FAIL_CONDITION': 'Completed valid gate misses a pass threshold; not reached because mandatory channels remain open.',
            'FALSIFIER': 'Not triggered; no frozen numerical q_pred exists.',
            'RESIDUAL': 'Circular likelihood residual represented by the profile likelihood.',
            'ERROR_BOUND': 'Central-value fit completed; angular selection and distance/geometry propagation block full uncertainty closure. Lang errors use the frozen coherent-draw approximation.',
            'VALIDITY_HEALTH': health,
            'BRANCHES': 'Both orientation branches and q=1/free-q branches were computed.',
            'OBSERVABLE_MAP': 'Doppler rotation curve plus stellar age to accumulated arm-relative phase.',
            'FORWARD_MODEL': 'Back-rotated cluster phase to selection-normalized arm-template likelihood.',
            'DATA_ROLE': upstream['contract']['DATA_ROLE'],
            'IDENTIFIABILITY': blocking_reasons,
            'BENCHMARK': 'Identical likelihood with q fixed to 1; BIC and likelihood profile.',
            'CLOSURE_FLAGS': closure,
            'CROSSCHECK': 'Direct-vs-FFT normalization passed; mandatory permutations/bootstrap/robustness were not promoted after precondition failure.',
            'PROVENANCE': 'Pinned hashes below.',
            'FILES': [Path(__file__).name, PREREG.name, UPSTREAM_RESULT.name, RESULT_PATH.name, PLOT_PATH.name],
        },
        'closure_flags': closure,
        'sample_flow': data.sample_flow,
        'results': {
            'fits': {key: public_fit(value) for key, value in raw_fits.items()},
            'best_common_ticking': public_fit(best_m0),
            'best_free_q': public_fit(best_m1),
            'two_delta_log_likelihood': float(2.0 * (best_m0['nll'] - best_m1['nll'])),
            'delta_bic_m0_minus_m1': delta_bic,
            'orientation_delta_bic_free_q': orientation_delta,
            'q_profile_intervals': profile['intervals'],
            'q_profile_interval_components': profile['interval_components'],
            'q_profile_touches_boundary': profile['touches_boundary'],
            'q_profile_best_grid_q': profile['best_grid_q'],
            'q_profile_best_grid_nll': profile['best_grid_nll'],
            'profile_fit_crosscheck': profile_crosscheck,
            'primary_model_comparison_thresholds_met': primary_effect_thresholds_met,
            'radial_health': health,
            'segment_counts_by_block': data.segment_counts.tolist(),
            'likelihood_normalization_residual': data.normalization_residual,
        },
        'uncertainty': {
            'completed': False,
            'reason': 'Mandatory sign-stability, angular-selection footprint, and distance/geometry preconditions failed before confirmatory controls.',
            'profile_q_grid': profile['q_grid'].tolist(),
            'profile_two_delta_log_likelihood': (
                2.0 * (profile['combined_nll'] - np.min(profile['combined_nll']))
            ).tolist(),
        },
        'crosschecks': {
            'direct_fft_normalization': data.normalization_residual,
            'permutation': 'NOT_RUN_AFTER_PRECONDITION_FAILURE',
            'block_bootstrap': 'NOT_RUN_AFTER_PRECONDITION_FAILURE',
            'injection_recovery': 'NOT_RUN_AFTER_PRECONDITION_FAILURE',
            'broad_mask': 'NOT_RUN_AFTER_PRECONDITION_FAILURE',
            'age_6_100': 'NOT_RUN_AFTER_PRECONDITION_FAILURE',
            'machine_catalog': 'NOT_RUN_AFTER_PRECONDITION_FAILURE',
        },
        'blocking_reasons': blocking_reasons,
        'provenance': {
            'run_utc': datetime.now(timezone.utc).isoformat(),
            'source_sha256': sha256(Path(__file__)),
            'preregistration_sha256': sha256(PREREG),
            'upstream_source_sha256': sha256(UPSTREAM_SOURCE),
            'upstream_result_sha256': upstream_result_hash,
            'raw_manifest_file_count': len(upstream['provenance']['files']),
            'seed': SEED,
            'python': sys.version.split()[0],
            'platform': platform.platform(),
            'numpy': np.__version__,
            'scipy': scipy.__version__,
            'astropy': astropy.__version__,
            'matplotlib': matplotlib.__version__,
        },
        'files': {
            'source': Path(__file__).name,
            'preregistration': PREREG.name,
            'upstream_result': UPSTREAM_RESULT.name,
            'result': RESULT_PATH.name,
            'plot': {'path': PLOT_PATH.name, 'sha256': sha256(PLOT_PATH)},
        },
    }
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    print(json.dumps({
        'claim_id': CLAIM_ID,
        'status': result['status'],
        'n_clusters': len(data.age),
        'best_q': best_m1['q'],
        'delta_bic_m0_minus_m1': delta_bic,
        'q_intervals': profile['intervals'],
        'blocking_reasons': blocking_reasons,
        'result': RESULT_PATH.name,
    }, indent=2))


if __name__ == '__main__':
    main()
