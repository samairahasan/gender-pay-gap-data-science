import subprocess
import sys
import os

BASE_DIR = os.path.dirname(__file__)
scripts = [
    "scripts/01_clean_gender_pay_gap.py",
    "scripts/02_clean_gross_hourly_pay.py",
    "scripts/03_clean_female_employment.py",
    "scripts/04_merge.py",
    "scripts/05_analysis_and_outputs.py",
]

for script in scripts:
    path = os.path.join(BASE_DIR, script)
    print("\n" + "=" * 60)
    print(f"Running {path}")
    print("=" * 60)

    result = subprocess.run([sys.executable, path], capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print("❌ ERROR:")
        print(result.stderr)
        sys.exit(1)

print("\n✅ Pipeline complete: all outputs successfully generated.")