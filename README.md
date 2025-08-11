# ITU Course Taker (Ethical, Rate-Limited)

Automates checking Istanbul Technical University (İTÜ) course quotas and (optionally) attempts enrollment when a seat opens. 
Designed to be **polite**: default check interval is 15 minutes to match ITÜ's update cadence and avoid hammering the servers.

> ⚠️ **Disclaimer**  
> Use at your own risk, and respect the University's Terms of Service. This software is for educational purposes.  
> Do not run with aggressive polling. The defaults (15 minutes + small jitter) are intended to be gentle.

## What it does

- Opens the public course quota page and checks capacity vs. enrolled for given CRN(s).
- Sends one-time notifications when a seat is available (Pushbullet optional).
- If you opt in and provide credentials, it will navigate to Kepler and attempt to add the CRN(s).
- Deduplicates notifications and avoids repeatedly pinging on the same opening.
- Logs actions to the console.

## Repository layout

```
itu-course-taker/
├─ src/
│  ├─ course_taker_single.py     # Check one course code + one CRN
│  ├─ course_taker_multi.py      # Check one course code + multiple CRNs (15‑minute loop)
│  ├─ config.py                  # Env/CLI handling
│  ├─ notifier_pushbullet.py     # Optional Pushbullet integration
│  ├─ selectors.py               # XPaths/locators for SIS & Kepler
│  └─ utils.py                   # Shared helpers (driver, waits, logging, jitter)
├─ docs/
│  └─ NOTES.md                   # Technical notes & how the legacy scripts mapped here
├─ .env.example
├─ .gitignore
├─ LICENSE
├─ requirements.txt
└─ README.md
```

## Install

1. **Python 3.9+** recommended.  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick start (single CRN)

```bash
python -m src.course_taker_single --course-code END --crn 21102 --interval 15
```

- Add `--headless` to run without opening a browser window.
- Add `--notify` to enable Pushbullet notifications (requires `PUSHBULLET_TOKEN` in `.env` or environment).
- Add `--enroll` to attempt adding the course when a seat is found (requires `ITU_USERNAME` and `ITU_PASSWORD`).

## Quick start (multiple CRNs)

```bash
python -m src.course_taker_multi --course-code END --crn 21102 21105 21314 --interval 15 --notify
```

## Configure credentials (optional)

Copy `.env.example` to `.env` and fill in:

```
ITU_USERNAME=your_itu_username
ITU_PASSWORD=your_itu_password
PUSHBULLET_TOKEN=your_pushbullet_access_token
```

> Tip: If you prefer not to store credentials in a file, export them as environment variables instead.

## Ethical defaults

- Interval defaults to **15 minutes**.  
- A small random **jitter** (±60 sec) is applied to avoid synchronized spikes.
- Notifications for the same CRN opening are **sent once** per run.

## Updating selectors

Universities update portals from time to time. If a selector breaks, edit `src/selectors.py`. The current ones are based on the legacy working scripts, but may require tweaks.

## Acknowledgements

- Built with Selenium and webdriver-manager.

---

© 2025 M. Mert Adana. Released under the MIT License.

See also: [Provenance & Context](docs/PROVENANCE.md) for the background and the ethical redesign rationale.

## Origin story

During course registration at İTÜ, high demand made enrollment competitive. I wrote a Python script to auto-check quotas and attempt enrollment.
Initial high-frequency polling triggered a warning from the university's IT department about excessive requests (see [Provenance](docs/PROVENANCE.md)).
I then redesigned the tool to **respect update intervals (15 minutes)** and added **random jitter**. This repository reflects that responsible approach.
