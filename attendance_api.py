import requests
from bs4 import BeautifulSoup

# Define the base URL
base_url = 'https://student.kletech.ac.in/code/'
# Function to start a session and login
def login(username, password):
    session = requests.Session()
    login_page = session.get(base_url)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    form = soup.find('form', {'id': 'login-form'})

    form_data = {field['name']: field.get('value', '') for field in form.find_all('input') if field.get('name')}
    form_data['username'] = username
    form_data['passwd'] = password

    session.post(base_url, data=form_data)
    return session

# Function to fetch personal data
def fetch_student_data(username, password):
    session = login(username, password)
    
    # Fetching Personal Data
    dashboard_url = f'{base_url}index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard'
    dashboard_page = session.get(dashboard_url)
    dashboard_soup = BeautifulSoup(dashboard_page.content, 'html.parser')

    personal_keys = ["name", "usn", "semester", "credits_earned", "credits_to_earn"]
    personal_values = [div.text.strip().replace("Credits Earned : ", "").replace("Credits to Earn : ", "") 
                       for div in dashboard_soup.find_all('div', {'class': 'tname2'})]
    personal_data = dict(zip(personal_keys, personal_values))

    # Fetching Attendance Data
    course_codes = [div.text for div in dashboard_soup.find_all('div', {'class': 'courseCode'})]
    course_names = [div.text for div in dashboard_soup.find_all('div', {'class': 'coursename'})]
    course_teachers = [div.text.strip().replace("  ", " ") for div in dashboard_soup.find_all('div', {'class': 'tname'})]
    course_attendances = [div.text.strip().replace("Attendance", "").replace("\n", "") for div in dashboard_soup.find_all('div', {'class': 'att'})]
    course_cie_marks = [div.text.strip().replace("Internal Assessment", "").replace("\n", "") for div in dashboard_soup.find_all('div', {'class': 'cie'})]

    attendance_data = [{
            "course_name": course_names[i],
            "course_code": course_codes[i],
            "course_teacher": course_teachers[i],
            "course_attendance": course_attendances[i],
            "cie_marks": course_cie_marks[i]
        } for i in range(len(course_codes))]

    # Merging and returning the data
    return {
        "personal_data": personal_data,
        "attendance_data": attendance_data
    }



# Function to fetch calendar of events data
def fetch_calendar_of_events(username, password):
    session = login(username, password)
    dashboard_url = f'{base_url}index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard'
    dashboard_page = session.get(dashboard_url)
    dashboard_soup = BeautifulSoup(dashboard_page.content, 'html.parser')
    coe_url = base_url+dashboard_soup.find("div", class_="atag").find("a", class_="atagblock").get("href")
    coe_page = session.get(coe_url)
    coe_soup = BeautifulSoup(coe_page.content, 'html.parser')
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
    
    coe = {"coe":coe}
    return coe

