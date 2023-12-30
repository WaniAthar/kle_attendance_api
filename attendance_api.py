from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display

from bs4 import BeautifulSoup

def fetch_student_data(username, password):
    with Display(size=(1024, 768), color_depth=24, visible=False) as display:
        chrome_options = Options()
        chrome_options.use_chromium = True
        chrome_options.headless = True  # Add this line for headless mode
        chrome_options.add_argument('--disable-gpu')  # Add this line for headless mode
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-sandbox')

        # chromedriver_path = '/path/to/chromedriver'  # Replace with your actual path to chromedriver

        login_url = 'https://student.kletech.ac.in/code/'
        # Create a Chrome WebDriver instance with the specified options and service
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(login_url)

        months = {
            '01':'Jan',
            '02':'Feb',
            '03':'Mar',
            '04':'Apr',
            '05':'May',
            '06':'Jun',
            '07':'Jul',
            '08':'Aug',
            '09':'Sep',
            '10':'Oct',
            '11':'Nov',
            '12':'Dec'
        }
        # split passwrord
        passlist = password.split('-')
        dd=passlist[2]
        mm = months[passlist[1]]
        yyyy = passlist[0]

        # not works like this
        login_payload = {
            'username': username,
            'dd': dd,
            'mm': mm,
            'yyyy': yyyy
        }
        
        # Extract form data
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        dd_field = wait.until(EC.presence_of_element_located((By.ID, 'dd')))
        mm_field = wait.until(EC.presence_of_element_located((By.ID, 'mm')))
        yyyy_field = wait.until(EC.presence_of_element_located((By.ID, 'yyyy')))

        # Enter data into fields
        username_field.send_keys(login_payload['username'])
        dd_field.send_keys(login_payload['dd'])
        mm_field.send_keys(login_payload['mm'])
        yyyy_field.send_keys(login_payload['yyyy'])

        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, 'submit')))
        submit_button.click()


        # Wait for the login to complete
        try:
            element_present = EC.presence_of_element_located((By.ID, 'page_bg'))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for dashboard page to load")

        
        # Fetching Personal Data
        dashboard_url = 'https://student.kletech.ac.in/code/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard'
        # Wait for the dashboard page to load
        driver.get(dashboard_url)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'page-header'))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for dashboard page to load")
        dashboard_soup = BeautifulSoup(driver.page_source, 'html.parser')

        personal_keys = ["name", "usn", "semester", "credits_earned", "credits_to_earn"]
        personal_values = [div.text.strip().replace("Credits Earned : ", "").replace("Credits to Earn : ", "") 
                        for div in dashboard_soup.find_all('div', {'class': 'tname2'})]
        personal_data = dict(zip(personal_keys, personal_values))
        print(personal_data)
        # Fetching Attendance Data
        course_codes = [div.text for div in dashboard_soup.find_all('div', {'class': 'courseCode'})]
        course_names = [div.text for div in dashboard_soup.find_all('div', {'class': 'coursename'})]
        course_teachers = [div.text.strip().replace("  ", " ") for div in dashboard_soup.find_all('div', {'class': 'tname'})]
        course_attendances = [div.text.strip().replace("Attendance", "").replace("\n", "") for div in dashboard_soup.find_all('div', {'class': 'att'})]
        course_cie_marks = [div.text.strip().replace("Internal Assessment", "").replace("\n", "") for div in dashboard_soup.find_all('div', {'class': 'cie'})]

        
        attendance_data = []
        j = 0
        for i in range(len(course_names)):
                if i == 0 or course_names[i] != course_names[i-1]:
                    attendance_data.append({
                        "course_name": course_names[i],
                        "course_code": course_codes[i],
                        "course_teacher": course_teachers[j],
                        "course_attendance": course_attendances[i],
                        "cie_marks": course_cie_marks[i]
                    })
                    j+=1


        # Close the browser
        driver.quit()

        print(personal_data)
        print(attendance_data)
    # Merging and returning the data
    return {
        "personal_data": personal_data,
        "attendance_data": attendance_data
    }


def fetch_calendar_of_events(username, password):
    with Display(size=(1024, 768), color_depth=24, visible=False) as display:
        chrome_options = Options()
        chrome_options.use_chromium = True
        chrome_options.headless = True  # Add this line for headless mode
        chrome_options.add_argument('--disable-gpu')  # Add this line for headless mode
        chrome_options.add_argument('--no-sandbox')
        # chromedriver_path = '/path/to/chromedriver'  # Replace with your actual path to chromedriver

        login_url = 'https://student.kletech.ac.in/code/'
        # Create a Chrome WebDriver instance with the specified options and service
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(login_url)

        months = {
            '01':'Jan',
            '02':'Feb',
            '03':'Mar',
            '04':'Apr',
            '05':'May',
            '06':'Jun',
            '07':'Jul',
            '08':'Aug',
            '09':'Sep',
            '10':'Oct',
            '11':'Nov',
            '12':'Dec'
        }
        # split passwrord
        passlist = password.split('-')
        login_payload = {
            'username': username,
            'dd': passlist[2],
            'mm': months[passlist[1]],
            'yyyy': passlist[0]
        }

        # Extract form data
        driver.find_element(By.ID, 'username').send_keys(login_payload['username'])
        driver.find_element(By.ID, 'dd').send_keys(login_payload['dd'])
        driver.find_element(By.ID, 'mm').send_keys(login_payload['mm'])
        driver.find_element(By.ID, 'yyyy').send_keys(login_payload['yyyy'])
        
        
        submit_button = driver.find_element("name", "submit")
        submit_button.click()


        # Wait for the login to complete
        try:
            element_present = EC.presence_of_element_located((By.ID, 'page_bg'))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for dashboard page to load")

        dashboard_url = 'https://student.kletech.ac.in/code/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard'
        driver.get(dashboard_url)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'page-header'))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for dashboard page to load")
        
        dashboard_soup = BeautifulSoup(driver.page_source, 'html.parser')
        coe_url = "https://student.kletech.ac.in/code/"+dashboard_soup.find("div", class_="atag").find("a", class_="atagblock").get("href")
        driver.get(coe_url)
        # Wait for the dashboard page to load
        try:
            element_present = EC.presence_of_element_located((By.ID, 'page-header'))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for dashboard page to load")
        coe_soup = BeautifulSoup(driver.page_source, 'html.parser')
        coe_table = coe_soup.find_all('table')
        coe_soup.find('style').extract()

        for i in range(3):
            coe_table[i].extract()
        main_coe_table = coe_soup.find('table')
        rows_to_remove = main_coe_table.find_all('tr')[:13]
        for row in rows_to_remove:
            row.extract()
        table_form = coe_soup.find('form') 
        table_form = table_form.find('div')
        table_form.find_next('div').extract()
        table_form.find_next('div').extract()
        table_form.find_next('div').extract()
        coe = repr(coe_soup).replace("\n", "").replace("\t", "").replace("\r", "")
        driver.quit()
        
        coe = {"coe":coe}

    return coe

# Replace with your actual credentials
# fetch_student_data("01fe02bcs054", "2002-04-01")
fetch_student_data('01fe20bcs054', '2002-04-01')
print(fetch_calendar_of_events('01fe20bcs054', '2002-04-01'))
