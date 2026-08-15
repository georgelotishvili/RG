'''Acquire and integrity-check public PHANGS products for W3-18.'''

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import astropy
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.wcs import WCS

CLAIM_ID = 'W3_17_PHANGS_DATA_INTEGRITY'
MODEL_VERSION = 'W3-17-v1.1-PHANGS-DR5'
ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'PHANGS_data' / 'raw'
MANIFEST_DIR = ROOT / 'PHANGS_data' / 'manifests'
RESULT_PATH = ROOT / 'w3_17_result.json'

PRODUCTS: dict[str, dict[str, Any]] = {
    'hst_human': {
        'filename': 'hlsp_phangs-cat_hst_acs-uvis_dr5-targets_v1_human-class1+2-primary.fits',
        'url': 'https://archive.stsci.edu/hlsps/phangs-cat/dr5/hlsp_phangs-cat_hst_acs-uvis_dr5-targets_v1_human-class1%2B2-primary.fits',
        'expected_bytes': 9_878_400,
        'expected_sha256': '66c8780960ecd88f1f14001c8baf3e74ddea7bc7133b933f924560f425ec3c71',
        'survey': 'PHANGS-HST',
        'release': 'PHANGS-CAT DR5',
        'doi': '10.17909/jray-9798',
    },
    'hst_machine': {
        'filename': 'hlsp_phangs-cat_hst_acs-uvis_dr5-targets_v1_machine-class1+2-primary.fits',
        'url': 'https://archive.stsci.edu/hlsps/phangs-cat/dr5/hlsp_phangs-cat_hst_acs-uvis_dr5-targets_v1_machine-class1%2B2-primary.fits',
        'expected_bytes': 23_051_520,
        'expected_sha256': 'f919e3dc2f31196e1d94f0561ed8a3bb4e14ba07c3bce57388f757326719f244',
        'survey': 'PHANGS-HST',
        'release': 'PHANGS-CAT DR5',
        'doi': '10.17909/jray-9798',
    },
    'pattern_speed': {
        'filename': 'pattern_speed_table_v1p0.fits',
        'url': 'https://raw.githubusercontent.com/thomaswilliamsastro/phangs_pattern_speeds/33e814890d5ede0d46bd351c0f65a54443560538/pattern_speed_table_v1p0.fits',
        'expected_bytes': 97_920,
        'expected_sha256': 'f3284c78fe7da6bd04e7ae0b662e2c9b824303c1cca60f259834ea6895538528',
        'survey': 'PHANGS',
        'release': 'Williams et al. table v1.0 at commit 33e814890d5ede0d46bd351c0f65a54443560538',
        'doi': '10.3847/1538-3881/abe243',
    },
    'rotation_curve': {
        'filename': 'PHANGS_RC_all_kpc.ecsv',
        'url': 'https://www.canfar.net/storage/vault/file/phangs/RELEASES/Lang_etal_2020/PHANGS_RC_all_kpc.ecsv',
        'expected_bytes': 87_470,
        'expected_sha256': '8f570093da3aed1c00748cc728e609e66b8bd372fb6eca3c55d04576c2953e79',
        'survey': 'PHANGS-ALMA',
        'release': 'Lang et al. 2020 rotation curves',
        'doi': '10.3847/1538-4357/ab9953',
    },
    'spiral_narrow': {
        'filename': 'NGC4303_spiral_mask_narrow.fits',
        'url': 'https://www.canfar.net/storage/vault/file/phangs/RELEASES/Querejeta_etal_2024/NGC4303_spiral_mask_narrow.fits',
        'expected_bytes': 4_314_240,
        'expected_sha256': 'b5223a3381c71476dded60143770a6e555d63ec333069496e45a3f9e55fc94a7',
        'survey': 'PHANGS',
        'release': 'Querejeta et al. 2024 narrow spiral mask',
        'doi': '10.1051/0004-6361/202449733',
    },
    'spiral_broad': {
        'filename': 'NGC4303_spiral_mask.fits',
        'url': 'https://www.canfar.net/storage/vault/file/phangs/RELEASES/Querejeta_etal_2024/NGC4303_spiral_mask.fits',
        'expected_bytes': 4_314_240,
        'expected_sha256': '0c3031d95247df3c2f2994fa90b2fa63c5119806f5af1b399f9883f057d14434',
        'survey': 'PHANGS',
        'release': 'Querejeta et al. 2024 broad spiral mask',
        'doi': '10.1051/0004-6361/202449733',
    },
    'environment_mask': {
        'filename': 'NGC4303_env_mask_simple.fits.gz',
        'url': 'https://www.canfar.net/storage/vault/file/phangs/RELEASES/PHANGS_env_masks/env_masks_simple/NGC4303_env_mask_simple.fits.gz',
        'expected_bytes': 19_771,
        'expected_sha256': 'c73061a00aecd6ab01807a9677ad850a1f41b4f40e272a3710dd6cfcb9c0d6d5',
        'survey': 'PHANGS',
        'release': 'Querejeta et al. 2021 environment masks',
        'doi': '10.1051/0004-6361/202140695',
    },
    'spiral_parameters': {
        'filename': 'table_spiral_arms.csv',
        'url': 'https://www.canfar.net/storage/vault/file/phangs/RELEASES/PHANGS_env_masks/table_spiral_arms.csv',
        'expected_bytes': 12_325,
        'expected_sha256': '7d3184f74fd59313d06cb4355503969bef38a2ac467872a6d900275bab1a1dc9',
        'survey': 'PHANGS',
        'release': 'Querejeta et al. 2021 analytic spiral fits',
        'doi': '10.1051/0004-6361/202140695',
    },
    'environment_components': {
        'filename': 'table_components.csv',
        'url': 'https://www.canfar.net/storage/vault/file/phangs/RELEASES/PHANGS_env_masks/table_components.csv',
        'expected_bytes': 2_443,
        'expected_sha256': 'a98c18f40dd9596a222d2c8e3841f716999094590d44554e3f0da5049af763c1',
        'survey': 'PHANGS',
        'release': 'Querejeta et al. 2021 environment-mask component dictionary',
        'doi': '10.1051/0004-6361/202140695',
    },
    'hst_readme': {
        'filename': 'hlsp_phangs-cat_dr5-targets_v1_primary-readme.txt',
        'url': 'https://archive.stsci.edu/hlsps/phangs-cat/dr5/hlsp_phangs-cat_dr5-targets_v1_primary-readme.txt',
        'expected_bytes': 26_953,
        'expected_sha256': '041d134424ed5bdfb1612d26ea56f0cbcd1c79b86a24e200e853d78dd9e98f9b',
        'survey': 'PHANGS-HST',
        'release': 'PHANGS-CAT DR5 data dictionary',
        'doi': '10.17909/jray-9798',
    },
}

DATA_ROLES = {
    'hst_human': 'primary overlapping fit/development catalog',
    'hst_machine': 'overlapping robustness catalog; not independent validation',
    'hst_readme': 'authoritative age, mass, uncertainty, and quality-field dictionary',
    'pattern_speed': 'external post-fit pattern-speed check',
    'rotation_curve': 'fixed forward-model kinematic input',
    'spiral_narrow': 'primary arm template',
    'spiral_broad': 'arm-template robustness product',
    'environment_mask': 'current-position selection and excluded-region mask',
    'spiral_parameters': 'geometry and future centerline crosscheck; not fit outcome',
    'environment_components': 'environment-component semantics check',
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def download(url: str, destination: Path) -> bool:
    '''Download atomically and report whether bytes were retrieved now.'''
    if destination.exists():
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + '.part')
    request = urllib.request.Request(url, headers={'User-Agent': 'RefG-W3-17/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=180) as response, partial.open('wb') as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
        os.replace(partial, destination)
    finally:
        if partial.exists():
            partial.unlink()
    return True


def text_values(column: Any) -> np.ndarray:
    return np.asarray([
        value.decode('utf-8', errors='replace').strip().upper()
        if isinstance(value, (bytes, np.bytes_))
        else str(value).strip().upper()
        for value in column
    ])


def find_column(columns: list[str], candidates: list[str]) -> str | None:
    lookup = {name.upper(): name for name in columns}
    return next((lookup[name.upper()] for name in candidates if name.upper() in lookup), None)


def validate_hst(path: Path, expected_rows: int) -> dict[str, Any]:
    table = Table.read(path)
    columns = list(table.colnames)
    aliases = {
        'id': ['ID_PHANGS_CLUSTER'],
        'galaxy': ['PHANGS_GALAXY'],
        'ra': ['PHANGS_RA'],
        'dec': ['PHANGS_DEC'],
        'human_class': ['PHANGS_CLUSTER_CLASS_HUMAN'],
        'ml_class': ['PHANGS_CLUSTER_CLASS_ML_VGG'],
        'ml_quality': ['PHANGS_CLUSTER_CLASS_ML_VGG_QUAL'],
        'non_detection': ['PHANGS_NON_DETECTION_FLAG'],
        'no_coverage': ['PHANGS_NO_COVERAGE_FLAG'],
        'age': ['PHANGS_DR5_THILKER25_AGE'],
        'age_lo': ['PHANGS_DR5_THILKER25_AGE_LIMLO'],
        'age_hi': ['PHANGS_DR5_THILKER25_AGE_LIMHI'],
        'mass': ['PHANGS_DR5_THILKER25_MASS'],
        'reduced_chi2': ['PHANGS_DR5_THILKER25_REDUCED_MINCHISQ'],
    }
    resolved = {key: find_column(columns, names) for key, names in aliases.items()}
    galaxies = text_values(table[resolved['galaxy']]) if resolved['galaxy'] else np.array([])
    target_rows = int(np.count_nonzero(np.char.find(galaxies, 'NGC4303') >= 0))
    target = np.char.find(galaxies, 'NGC4303') >= 0
    numeric_names = ['ra', 'dec', 'age', 'age_lo', 'age_hi', 'mass', 'non_detection', 'reduced_chi2']
    numeric_finite = bool(all(
        np.any(np.isfinite(np.asarray(table[resolved[name]][target], dtype=float)))
        for name in numeric_names if resolved[name]
    ))
    age = np.asarray(table[resolved['age']][target], dtype=float) if resolved['age'] else np.array([])
    mass = np.asarray(table[resolved['mass']][target], dtype=float) if resolved['mass'] else np.array([])
    return {
        'rows': len(table),
        'expected_rows': expected_rows,
        'row_count_valid': len(table) == expected_rows,
        'resolved_core_columns': resolved,
        'core_columns_valid': all(resolved.values()),
        'ngc4303_rows': target_rows,
        'ngc4303_present': target_rows > 0,
        'ngc4303_numeric_fields_have_finite_values': numeric_finite,
        'ngc4303_positive_age_values': int(np.count_nonzero(np.isfinite(age) & (age > 0))),
        'ngc4303_positive_mass_values': int(np.count_nonzero(np.isfinite(mass) & (mass > 0))),
        'fits_age_unit': str(table[resolved['age']].unit) if resolved['age'] else None,
        'fits_mass_unit': str(table[resolved['mass']].unit) if resolved['mass'] else None,
        'all_columns': columns,
    }


def validate_products(paths: dict[str, Path]) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    checks['hst_human'] = validate_hst(paths['hst_human'], 15_528)
    checks['hst_machine'] = validate_hst(paths['hst_machine'], 36_307)

    pattern = Table.read(paths['pattern_speed'])
    pcols = list(pattern.colnames)
    target = np.flatnonzero(text_values(pattern['GALAXY']) == 'NGC4303')
    row = pattern[target[0]] if len(target) == 1 else None
    checks['pattern_speed'] = {
        'rows': len(pattern),
        'required_columns_valid': all(name in pcols for name in [
            'GALAXY', 'DIST', 'INCL', 'PA', 'OM_P_MUSE_MASS',
            'OM_P_MUSE_MASS_ERR_UP', 'OM_P_MUSE_MASS_ERR_DOWN',
            'OM_P_MUSE_MASS_QUAL',
        ]),
        'ngc4303_unique': len(target) == 1,
        'ngc4303_values_finite': bool(row is not None and all(np.isfinite(float(row[name])) for name in [
            'DIST', 'INCL', 'PA', 'OM_P_MUSE_MASS',
            'OM_P_MUSE_MASS_ERR_UP', 'OM_P_MUSE_MASS_ERR_DOWN',
        ])),
        'ngc4303_quality_one': bool(row is not None and int(row['OM_P_MUSE_MASS_QUAL']) == 1),
        'omega_unit': str(pattern['OM_P_MUSE_MASS'].unit),
    }

    rotation = Table.read(paths['rotation_curve'], format='ascii.ecsv')
    rcols = list(rotation.colnames)
    robj = text_values(rotation['obj']) if 'obj' in rcols else np.array([])
    selected = robj == 'NGC4303'
    radius_values = np.asarray(rotation['radius'][selected], dtype=float)
    velocity_values = np.asarray(rotation['Vrot'][selected], dtype=float)
    err_up = np.asarray(rotation['VrotErr+'][selected], dtype=float)
    err_down = np.asarray(rotation['VrotErr-'][selected], dtype=float)
    checks['rotation_curve'] = {
        'rows': len(rotation),
        'required_columns_valid': all(
            name in rcols for name in ['obj', 'radius', 'Vrot', 'VrotErr+', 'VrotErr-']
        ),
        'ngc4303_rows': int(np.count_nonzero(selected)),
        'ngc4303_radius_min_kpc': float(np.min(rotation['radius'][selected])) if np.any(selected) else None,
        'ngc4303_radius_max_kpc': float(np.max(rotation['radius'][selected])) if np.any(selected) else None,
        'ngc4303_finite_positive': bool(
            np.all(np.isfinite(radius_values)) and np.all(radius_values > 0)
            and np.all(np.isfinite(velocity_values)) and np.all(velocity_values > 0)
            and np.all(np.isfinite(err_up)) and np.all(err_up >= 0)
            and np.all(np.isfinite(err_down)) and np.all(err_down >= 0)
        ),
        'ngc4303_radius_strictly_ordered': bool(np.all(np.diff(radius_values) > 0)),
        'radius_unit': str(rotation['radius'].unit),
        'velocity_unit': str(rotation['Vrot'].unit),
    }

    for key in ['spiral_narrow', 'spiral_broad', 'environment_mask']:
        with fits.open(paths[key]) as hdul:
            hdu = next((item for item in hdul if item.data is not None), None)
            if hdu is None:
                raise ValueError(f'{key}: no image data')
            data = np.asarray(hdu.data)
            wcs = WCS(hdu.header)
            checks[key] = {
                'shape': list(data.shape),
                'expected_shape_valid': list(data.shape) == [1071, 995],
                'finite_fraction': float(np.mean(np.isfinite(data))),
                'nonzero_pixels': int(np.count_nonzero(np.nan_to_num(data))),
                'celestial_wcs': bool(wcs.has_celestial),
                'unique_values': [float(v) for v in np.unique(data[np.isfinite(data)])[:20]],
            }

    spiral_fields = [
        'galaxy', 'segment', 'width_pc', 'rmin_fit', 'rmax_fit', 'aa', 'bb',
        'x_center_px', 'y_center_px', 'pa_deg', 'incl_deg', 'distance_mpc',
        's4g_match', 'azimuth_min_deg', 'azimuth_max_deg',
    ]
    with paths['spiral_parameters'].open('r', encoding='utf-8-sig', newline='') as stream:
        data_lines = [line for line in stream if line.strip() and not line.lstrip().startswith('#')]
    rows = list(csv.DictReader(data_lines, fieldnames=spiral_fields))
    target_rows = [row for row in rows if row['galaxy'].strip().upper() == 'NGC4303']
    checks['spiral_parameters'] = {
        'rows': len(rows),
        'ngc4303_rows': len(target_rows),
        'ngc4303_present': len(target_rows) >= 2,
        'columns': spiral_fields,
    }
    readme = paths['hst_readme'].read_text(encoding='utf-8', errors='strict')
    required_readme_tokens = [
        'PHANGS_DR5_THILKER25_AGE [Myr]',
        'PHANGS_DR5_THILKER25_MASS [M_solar]',
        'PHANGS_DR5_THILKER25_AGE_LIMLO [Myr]',
        'PHANGS_DR5_THILKER25_AGE_LIMHI [Myr]',
        'PHANGS_DR5_THILKER25_REDUCED_MINCHISQ',
        'PHANGS_NON_DETECTION_FLAG',
    ]
    checks['hst_readme'] = {
        'required_semantics_valid': all(token in readme for token in required_readme_tokens),
        'age_unit': 'Myr',
        'mass_unit': 'M_solar',
        'absolute_age_limits_documented': 'Lower limit error estimate (1-sigma) in age.' in readme
        and 'Upper limit error estimate (1-sigma) in age.' in readme,
    }

    with paths['environment_components'].open('r', encoding='utf-8-sig', newline='') as stream:
        component_rows = list(csv.DictReader(stream))
    ngc4303_components = next(
        (row for row in component_rows if row['Galaxy'].strip().upper() == 'NGC4303'), None
    )
    mask_values = set(checks['environment_mask']['unique_values'])
    checks['environment_components'] = {
        'rows': len(component_rows),
        'ngc4303_present': ngc4303_components is not None,
        'ngc4303_spiral_component': bool(
            ngc4303_components is not None and ngc4303_components['Spiral arms'] == '1'
        ),
        'simple_mask_class_map': {
            '6': 'spiral outside bar',
            '7': 'interarm',
        },
        'required_simple_classes_present': {6.0, 7.0}.issubset(mask_values),
    }
    return checks


def main() -> None:
    run_time = datetime.now(timezone.utc).isoformat()
    RAW.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    file_records: list[dict[str, Any]] = []
    file_checks: list[bool] = []
    for key, product in PRODUCTS.items():
        path = RAW / product['filename']
        retrieved_now = download(product['url'], path)
        size = path.stat().st_size
        digest = sha256(path)
        expected_size = product.get('expected_bytes')
        expected_hash = product.get('expected_sha256')
        size_ok = expected_size is not None and size == expected_size
        hash_ok = expected_hash is not None and digest == expected_hash
        file_checks.append(bool(size_ok and hash_ok))
        paths[key] = path
        file_records.append({
            'product_id': key,
            'relative_path': rel(path),
            'bytes': size,
            'sha256': digest,
            'url': product['url'],
            'survey': product['survey'],
            'release': product['release'],
            'doi': product['doi'],
            'data_role': DATA_ROLES[key],
            'license_or_terms': 'Public archive product; no separate license string exposed in the downloaded file metadata.',
            'retrieved_in_this_run': retrieved_now,
            'retrieval_utc_from_local_mtime': datetime.fromtimestamp(
                path.stat().st_mtime, timezone.utc
            ).isoformat(),
            'validated_utc': run_time,
            'expected_bytes': product.get('expected_bytes'),
            'expected_sha256': product.get('expected_sha256'),
            'size_valid': size_ok,
            'hash_valid': hash_ok,
        })

    validations = validate_products(paths)
    schema_checks = [
        validations['hst_human']['row_count_valid'],
        validations['hst_human']['core_columns_valid'],
        validations['hst_human']['ngc4303_present'],
        validations['hst_human']['ngc4303_numeric_fields_have_finite_values'],
        validations['hst_human']['ngc4303_positive_age_values'] > 0,
        validations['hst_human']['ngc4303_positive_mass_values'] > 0,
        validations['hst_machine']['row_count_valid'],
        validations['hst_machine']['core_columns_valid'],
        validations['hst_machine']['ngc4303_present'],
        validations['hst_machine']['ngc4303_numeric_fields_have_finite_values'],
        validations['hst_machine']['ngc4303_positive_age_values'] > 0,
        validations['hst_machine']['ngc4303_positive_mass_values'] > 0,
        validations['hst_readme']['required_semantics_valid'],
        validations['hst_readme']['absolute_age_limits_documented'],
        validations['pattern_speed']['required_columns_valid'],
        validations['pattern_speed']['ngc4303_unique'],
        validations['pattern_speed']['ngc4303_values_finite'],
        validations['pattern_speed']['ngc4303_quality_one'],
        'km' in validations['pattern_speed']['omega_unit'],
        'kpc' in validations['pattern_speed']['omega_unit'],
        validations['rotation_curve']['required_columns_valid'],
        validations['rotation_curve']['ngc4303_rows'] >= 10,
        validations['rotation_curve']['ngc4303_radius_min_kpc'] <= 3.0,
        validations['rotation_curve']['ngc4303_radius_max_kpc'] >= 5.0,
        validations['rotation_curve']['ngc4303_finite_positive'],
        validations['rotation_curve']['ngc4303_radius_strictly_ordered'],
        validations['rotation_curve']['radius_unit'] == 'kpc',
        'km' in validations['rotation_curve']['velocity_unit'],
        validations['spiral_narrow']['celestial_wcs'],
        validations['spiral_narrow']['nonzero_pixels'] > 0,
        validations['spiral_narrow']['expected_shape_valid'],
        validations['spiral_broad']['celestial_wcs'],
        validations['spiral_broad']['nonzero_pixels'] > 0,
        validations['spiral_broad']['expected_shape_valid'],
        validations['environment_mask']['celestial_wcs'],
        validations['environment_mask']['expected_shape_valid'],
        validations['spiral_parameters']['ngc4303_present'],
        validations['environment_components']['ngc4303_present'],
        validations['environment_components']['ngc4303_spiral_component'],
        validations['environment_components']['required_simple_classes_present'],
    ]
    closure = {
        'downloads_complete': all(path.exists() for path in paths.values()),
        'file_sizes_and_pinned_hashes_valid': all(file_checks),
        'schemas_valid': all(bool(value) for value in schema_checks),
        'target_overlap_present': bool(
            validations['hst_human']['ngc4303_present']
            and validations['pattern_speed']['ngc4303_unique']
            and validations['rotation_curve']['ngc4303_rows'] >= 10
        ),
    }
    all_pass = all(closure.values())
    manifest = {
        'schema_version': '1.0',
        'claim_id': CLAIM_ID,
        'claim': 'Pinned PHANGS inputs are content-addressed, schema-valid, and overlap on NGC 4303.',
        'type': 'DATA_INTEGRITY',
        'model_version': MODEL_VERSION,
        'status': 'PASS' if all_pass else 'FAIL',
        'evidence_strength': 'N/A: integrity gate, not a physical result',
        'contract': {
            'ASSUMPTIONS': ['HTTPS products are the named public releases.'],
            'DOMAIN': 'Named files and NGC 4303 overlap only.',
            'CONVENTIONS': 'SHA-256 over raw bytes; exact byte counts.',
            'FREEDOM_LEDGER': 'N/A: no fit.',
            'DEPENDENCIES': 'N/A: root acquisition gate.',
            'METHOD': 'Atomic download, hash/size verification, schema checks.',
            'PASS_CONDITION': 'All closure flags true.',
            'FAIL_CONDITION': 'Missing/mismatched file, invalid schema, or absent overlap.',
            'FALSIFIER': 'A product mismatch or invalid required schema.',
            'RESIDUAL': 'N/A: no physical equation.',
            'ERROR_BOUND': 'Cryptographic byte identity and exact schema predicates.',
            'VALIDITY_HEALTH': 'Archive identity and readability only.',
            'BRANCHES': 'N/A: no model branch.',
            'OBSERVABLE_MAP': 'N/A: delegated to W3-18.',
            'FORWARD_MODEL': 'N/A: delegated to W3-18.',
            'DATA_ROLE': DATA_ROLES,
            'IDENTIFIABILITY': 'N/A: no physical fit.',
            'BENCHMARK': 'Pinned hashes/sizes and release schemas.',
            'CLOSURE_FLAGS': closure,
            'CROSSCHECK': 'FITS/ECSV/CSV readers validate the byte products.',
            'PROVENANCE': 'Full per-file records below.',
            'FILES': [record['relative_path'] for record in file_records],
        },
        'closure_flags': closure,
        'sample_flow': {
            'hst_human_total': validations['hst_human']['rows'],
            'hst_human_ngc4303': validations['hst_human']['ngc4303_rows'],
            'hst_machine_total': validations['hst_machine']['rows'],
            'hst_machine_ngc4303': validations['hst_machine']['ngc4303_rows'],
        },
        'results': validations,
        'uncertainty': 'N/A: file integrity only.',
        'crosschecks': {
            'all_pinned_checks': all(file_checks),
            'all_schema_checks': all(schema_checks),
        },
        'provenance': {
            'validation_utc': run_time,
            'source_path': Path(__file__).name,
            'source_sha256': sha256(Path(__file__)),
            'python': sys.version.split()[0],
            'platform': platform.platform(),
            'numpy': np.__version__,
            'astropy': astropy.__version__,
            'files': file_records,
        },
        'files': {
            'source': Path(__file__).name,
            'result': RESULT_PATH.name,
            'manifest': 'PHANGS_data/manifests/w3_17_manifest.json',
        },
    }
    text = json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    RESULT_PATH.write_text(text, encoding='utf-8')
    (MANIFEST_DIR / 'w3_17_manifest.json').write_text(text, encoding='utf-8')
    print(json.dumps({
        'claim_id': CLAIM_ID,
        'status': manifest['status'],
        'closure_flags': closure,
        'human_ngc4303_rows': validations['hst_human']['ngc4303_rows'],
        'result': RESULT_PATH.name,
    }, indent=2))
    if not all_pass:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
