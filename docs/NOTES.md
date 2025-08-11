# Technical notes & mapping from legacy scripts

## Legacy files
- **Course Taker.ipynb**: Single-course script; polled a specific CRN and, if capacity > enroll, logged into Kepler and tried to add it.
- **ders_kayit_gonderilecek.ipynb**: Multi-course variant; added Pushbullet, 15-minute sleep, and optional auto-enroll.
- **untitled.py**: Older .py distributed as an EXE; used `resource_path` for PyInstaller and Pushbullet; relied on deprecated Selenium calls.

## Modernized choices
- Switched to Selenium 4 APIs (`By`, `WebDriverWait`, `Service`) and `webdriver-manager` (no manual driver download).
- Moved secrets to environment variables via `.env` (never commit plaintext credentials).
- CLI via `argparse` (no interactive `input()` needed in non-notebook runs).
- Jitter around the default 15-minute interval to avoid systematic bursts.
- Idempotent notifications per CRN per run.

## Known fragile points
- XPaths for SIS/Kepler can change any semester. If a step fails, start by opening DevTools and revalidating the selectors in `src/selectors.py`.
