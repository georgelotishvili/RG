import os
import json
import time
import numpy as np
from astroquery.simbad import Simbad

def format_galaxy_name(filename):
    name = filename.replace('_rotmod.dat', '')
    # Insert space after known prefixes
    for prefix in ['NGC', 'UGC', 'UGCA', 'DDO', 'ESO', 'IC', 'PGC']:
        if name.startswith(prefix):
            num_part = name[len(prefix):]
            # Strip leading zeros for NGC/UGC/IC etc might help SIMBAD, but let's try with zeros first
            return f"{prefix} {num_part}"
    return name

def main():
    Simbad.add_votable_fields('B', 'V')
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    galactic_dynamics_dir = os.path.dirname(script_dir)
    sparc_dir = os.path.join(galactic_dynamics_dir, "SPARC_data")
    
    results = {}
    files = [f for f in os.listdir(sparc_dir) if f.endswith('_rotmod.dat')]
    
    print(f"Found {len(files)} galaxies. Fetching colors from SIMBAD...")
    
    for i, f in enumerate(files):
        galaxy_id = f.replace('_rotmod.dat', '')
        query_name = format_galaxy_name(f)
        
        print(f"[{i+1}/{len(files)}] Querying {query_name} (ID: {galaxy_id})...")
        try:
            res = Simbad.query_object(query_name)
            if res is not None and 'B' in res.colnames and 'V' in res.colnames:
                b_mag = res['B'][0]
                v_mag = res['V'][0]
                
                if np.ma.is_masked(b_mag) or np.ma.is_masked(v_mag):
                    print(f"  -> Missing B or V magnitude in SIMBAD.")
                else:
                    b_minus_v = b_mag - v_mag
                    results[galaxy_id] = {
                        'simbad_id': str(res['main_id'][0]),
                        'B': float(b_mag),
                        'V': float(v_mag),
                        'B_V': float(b_minus_v)
                    }
                    print(f"  -> Success: B-V = {b_minus_v:.3f}")
            else:
                # Try querying without space or with stripped zeros if it failed
                if query_name != galaxy_id:
                     res2 = Simbad.query_object(galaxy_id)
                     if res2 is not None and 'B' in res2.colnames and 'V' in res2.colnames:
                         b_mag = res2['B'][0]
                         v_mag = res2['V'][0]
                         if not (np.ma.is_masked(b_mag) or np.ma.is_masked(v_mag)):
                             b_minus_v = b_mag - v_mag
                             results[galaxy_id] = {
                                 'simbad_id': str(res2['main_id'][0]),
                                 'B': float(b_mag),
                                 'V': float(v_mag),
                                 'B_V': float(b_minus_v)
                             }
                             print(f"  -> Success (fallback): B-V = {b_minus_v:.3f}")
                             continue
                print(f"  -> Not found or missing B/V data.")
        except Exception as e:
            print(f"  -> Error: {e}")
        
        time.sleep(0.4) # Respect SIMBAD rate limit (usually 2-3 queries per second is safe)

    out_path = os.path.join(script_dir, 'sparc_colors.json')
    with open(out_path, 'w') as outf:
        json.dump(results, outf, indent=2)

    print(f"\nDone. Successfully retrieved colors for {len(results)} out of {len(files)} galaxies.")
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    main()
