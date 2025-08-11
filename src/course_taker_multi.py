import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .selectors import sis_url_for_course, row_by_crn, CAPACITY_TD, ENROLLED_TD, COURSE_NAME_TD,     KEPLER_LOGIN_URL, USERNAME, PASSWORD, LOGIN_BTN, CRN_INPUT, SUBMIT_BTN, CONFIRM_BTN
from .utils import build_driver, sleep_with_jitter, setup_logging
from .config import Settings
from .notifier_pushbullet import PushbulletNotifier

def try_add_course(driver, crn, settings, log):
    if not (settings.itu_username and settings.itu_password):
        log.warning("Enroll requested but ITU credentials are missing. Skipping add.")
        return False
    driver.get(KEPLER_LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(USERNAME)).send_keys(settings.itu_username)
    driver.find_element(*PASSWORD).send_keys(settings.itu_password)
    driver.find_element(*LOGIN_BTN).click()
    field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(CRN_INPUT))
    field.clear(); field.send_keys(crn)
    driver.find_element(*SUBMIT_BTN).click()
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(CONFIRM_BTN)).click()
    except Exception:
        pass
    return True

def main():
    parser = argparse.ArgumentParser(description="Check multiple CRNs on a 15-min loop and (optionally) enroll.")
    parser.add_argument("--course-code", required=True, help="Course code, e.g., END, ISL")
    parser.add_argument("--crn", required=True, nargs="+", help="One or more CRNs to watch (space-separated)")
    parser.add_argument("--interval", type=int, default=15, help="Minutes between checks (default: 15)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--notify", action="store_true", help="Send Pushbullet notifications if configured")
    parser.add_argument("--enroll", action="store_true", help="Attempt to add available CRNs in Kepler when seats open")
    args = parser.parse_args()

    log = setup_logging()
    settings = Settings()
    notifier = PushbulletNotifier(settings.pushbullet_token)

    driver = build_driver(headless=args.headless)
    notified = set()  # CRNs we've already notified about

    try:
        while True:
            driver.get(sis_url_for_course(args.course_code))
            for crn in list(args.crn):  # iterate over a copy; we may remove if enrolled
                cell = WebDriverWait(driver, 10).until(EC.presence_of_element_located(row_by_crn(crn)))
                row = cell
                capacity = int(row.find_element(*CAPACITY_TD).text)
                enrolled = int(row.find_element(*ENROLLED_TD).text)
                cname = row.find_element(*COURSE_NAME_TD).text

                log.info(f"{cname} (CRN {crn}): capacity={capacity}, enrolled={enrolled}")
                if capacity > enrolled:
                    if crn not in notified and args.notify:
                        notifier.send(cname, f"{cname} has a seat. CRN {crn}")
                        log.info(f"Notification sent for {crn}.")
                        notified.add(crn)
                    if args.enroll:
                        ok = try_add_course(driver, crn, settings, log)
                        log.info(f"Enrollment attempted for {crn}." if ok else f"Enrollment skipped/failed for {crn}.")
                        # After an attempt, remove this CRN from further checks this run
                        args.crn.remove(crn)
            if not args.crn:
                log.info("No more CRNs to watch. Exiting.")
                break
            sleep_with_jitter(args.interval)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
