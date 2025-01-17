import requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()


def get_cookies_with_playwright():
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto("https://login.app.rigohr.com/login")

        # Fill in the login form
        page.fill("input[name='Username']", os.getenv("EMAIL"))
        page.fill("input[name='Password']", os.getenv("EMAIL_PASSWORD"))

        # Submit the login form
        page.click("button[type='submit']")

        # Wait for the page to load and for cookies to be set
        page.wait_for_load_state("networkidle")

        # Capture cookies from the browser context
        cookies = context.cookies()

        # Close the browser
        browser.close()

        # Convert cookies to a format usable by requests
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        return cookies_dict


def make_api_request(cookies, development=False):
    # API endpoint
    url = "https://api.app.rigohr.com/v1/core-hr/employees/team/who-is-out?dayType=1"

    # Headers from the cURL command
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://app.rigohr.com',
        'priority': 'u=1, i',
        'referer': 'https://app.rigohr.com/hr/employee/team-update',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'tenantid': '92e47fd0-f814-40d7-b880-64430c6be99b',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }

    # Send the GET request with cookies
    response = requests.get(url, headers=headers, cookies=cookies)

    # Check the response status
    if response.status_code == 200:
        response = response.json()
        if development:
            print(response)
        return response

    raise ValueError("Status Code Not matched.")


def _parser(data):
    data = data.get("Data", [])

    using_value = []

    for d in data:
        temp = {}
        temp['Name'] = d.get("Name")
        temp['From'] = d.get("FromDateEng")[:-9]
        temp['To'] = d.get("ToDateEng")[:-9]
        temp['Event'] = d.get("RequestType")
        temp['Substitute'] = d.get("Substitute")

        using_value.append(temp)

    return using_value


def get_who_is_out():
    cookies = get_cookies_with_playwright()
    value = make_api_request(cookies=cookies)
    return _parser(value)


if __name__ == "__main__":
    value = get_who_is_out()
    print(value)
