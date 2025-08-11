"""
XPaths and CSS selectors used across the project.
Adjust here if portals change structure.
"""
from selenium.webdriver.common.by import By

SIS_BASE = "https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS"

def sis_url_for_course(course_code: str) -> str:
    # The legacy scripts navigated to the page and then filtered by course code.
    # In practice, you can pass derskodu= param to land on the filtered table.
    return f"{SIS_BASE}&derskodu={course_code.upper()}"

# Row locators
def row_by_crn(crn: str):
    # Finds the <td> cell that contains the CRN text, then we climb to its row
    return (By.XPATH, f"//*[contains(text(), '{crn}')]")

# Relative to the CRN <td>'s row
CAPACITY_TD = (By.XPATH, "./../td[10]")
ENROLLED_TD = (By.XPATH, "./../td[11]")
COURSE_NAME_TD = (By.XPATH, "./../td[3]")

# Kepler (may change; update if needed)
KEPLER_LOGIN_URL = "https://kepler-beta.itu.edu.tr/ogrenci/DersKayitIslemleri/DersKayit"
USERNAME = (By.XPATH, "//*[@id='ContentPlaceHolder1_tbUserName']")
PASSWORD = (By.XPATH, "//*[@id='ContentPlaceHolder1_tbPassword']")
LOGIN_BTN = (By.XPATH, "//*[@id='ContentPlaceHolder1_btnLogin']")

# Navigation inside Kepler (legacy UI paths; validate each term)
ICON_NOTE = (By.XPATH, "//i[@class='icon icon-note']")
SUBNAV_DERS_KAYIT = (By.XPATH, "//div[contains(@class,'sub-nav') and contains(@class,'sub-nav-open')]//li[2]//a[1]")

# CRN input and buttons (validate as needed)
CRN_INPUT = (By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[3]/div/form/div[1]/div/div[1]/div/input")
SUBMIT_BTN = (By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[3]/div/form/button")
CONFIRM_BTN = (By.XPATH, "//*[@id='modals-container']/div/div[2]/div/div[3]/button[2]")
