# SRM Autologin
This is a simple python script to automate the login process of the SRMIST WiFi Captive Portal.

It uses selenium to create a browser instance and verifies if the user is in the hostel or in an academic building via http requests, and logs in accordingly.

To use it yourself, you need to have the following installed:
python-dotenv, selenium, requests

```bash
pip install -r requirements.txt
```

You also need to have a `.env` file in the same directory as the script with the following variables:
```bash
username=your_username
password=your_password
```
