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
    # Input CRN and submit
    field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(CRN_INPUT))
    field.clear(); field.send_keys(crn)
    driver.find_element(*SUBMIT_BTN).click()
    # Confirm modal (best effort)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(CONFIRM_BTN)).click()
    except Exception:
        pass
    return True

def main():
    parser = argparse.ArgumentParser(description="Check one CRN and (optionally) enroll when a seat opens.")
    parser.add_argument("--course-code", required=True, help="Course code, e.g., END, ISL")
    parser.add_argument("--crn", required=True, help="CRN to watch")
    parser.add_argument("--interval", type=int, default=15, help="Minutes between checks (default: 15)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--notify", action="store_true", help="Send Pushbullet notifications if configured")
    parser.add_argument("--enroll", action="store_true", help="Attempt to add the course in Kepler if a seat opens")
    args = parser.parse_args()

    log = setup_logging()
    settings = Settings()
    notifier = PushbulletNotifier(settings.pushbullet_token)

    driver = build_driver(headless=args.headless)
    notified = False

    try:
        while True:
            driver.get(sis_url_for_course(args.course_code))
            cell = WebDriverWait(driver, 10).until(EC.presence_of_element_located(row_by_crn(args.crn)))
            row = cell
            capacity = int(row.find_element(*CAPACITY_TD).text)
            enrolled = int(row.find_element(*ENROLLED_TD).text)
            cname = row.find_element(*COURSE_NAME_TD).text

            log.info(f"{cname} (CRN {args.crn}): capacity={capacity}, enrolled={enrolled}")
            if capacity > enrolled:
                if not notified and args.notify:
                    notifier.send(cname, f"{cname} has a seat. CRN {args.crn}")
                    log.info("Notification sent.")
                    notified = True
                if args.enroll:
                    ok = try_add_course(driver, args.crn, settings, log)
                    log.info("Enrollment attempted." if ok else "Enrollment skipped/failed.")
                    break  # stop after an attempt
            sleep_with_jitter(args.interval)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
