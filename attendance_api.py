import requests
from bs4 import BeautifulSoup

# Define the login credentials
# username = '01FE20BCS054'
# password = '2002-04-01'
def get_data(username, password):
    personal_data = {}
    attendance_data = []


    # Start a session and get the login page
    session = requests.Session()
    login_url = 'https://student.kletech.ac.in/code/index.php'
    login_page = session.get(login_url)

    # Parse the login page and extract the form data
    soup = BeautifulSoup(login_page.content, 'html.parser')
    form = soup.find('form', {'id': 'login-form'})

    # print(soup.prettify())
    form_data = {}
    for field in form.find_all('input'):
        if field.get('name'):
            form_data[field['name']] = field.get('value', '')

    # # Update the form data with the login credentials
    form_data['username'] = username
    form_data['passwd'] = password

    # # Submit the login form
    session.post(login_url, data=form_data)

    # Get the dashboard page and parse the HTML content
    dashboard_url = 'https://student.kletech.ac.in/code/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard'
    dashboard_page = session.get(dashboard_url)
    dashboard_soup = BeautifulSoup(dashboard_page.content, 'html.parser')
    # print(dashboard_soup.prettify())

    # extract the data of all the divs of name tname2 and store it in a dictionary
    personal_values = [div for div in dashboard_soup.find_all(
        'div', {'class': 'tname2'})]
    personal_keys = ["name", "usn", "semester",
                    "credits_earned", "credits_to_earn"]

    # create a dictionary to store the data

    for i in range(len(personal_keys)):
        personal_data[personal_keys[i]] = personal_values[i].text.replace("  ", "").replace(
            "\n", "").replace("\t", "").replace("Credits Earned : ", "").replace("Credits to Earn : ", "")


    course_codes = [div for div in dashboard_soup.find_all(
        'div', {'class': 'courseCode'})]
    course_name = [div for div in dashboard_soup.find_all(
        'div', {'class', 'coursename'})]
    course_teacher = [div for div in dashboard_soup.find_all(
        'div', {'class': 'tname'})]
    course_attendance = [div for div in dashboard_soup.find_all('div', {
        'class': 'att'})]
    course_cie = [div for div in dashboard_soup.find_all('div', {
        'class': 'cie'})]
    for i in range(len(course_codes)):
        attendance_data.append({
            "course_name": course_name[i].text,
            "course_code": course_codes[i].text,
            "course_teacher": course_teacher[i].text.replace("  ", " "),
            "course_attendance": course_attendance[i].text.replace("Attendance", "").replace("\n", ""),
            "cie_marks": course_cie[i].text.replace("Internal Assessment", "").replace("\n", "")
        })
    return attendance_data, personal_data
