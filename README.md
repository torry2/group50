# CITS3403 Semester 1 2025: Group Project

Group Information: 50
| Student ID | Name | Github |
|----------|----------|----------|
| 24313178 | Torry Hogan | [torry2](https://github.com/torry2) |
| 23941237 | Jaiden Lacsher | [JaidenLCoder](https://github.com/JaidenLCoder) |
| 23905993 | Punit Patil | [Punit750](https://github.com/Punit750) |
| 23840306 | Lian Hao Kueh | [KLianHao](https://github.com/KLianHao) |

## CashNest
"Your Personal Financial Companion"

CashNest is a comprehensive financial management application designed to simplify your financial journey. Our platform offers a seamless experience to help users take control of their finances through intuitive budgeting tools, intelligent expense tracking, and collaborative goal-setting features.

- Smart Budget Management: Create customized budgets tailored to your financial situation and lifestyle. Easily allocate funds across different categories and receive intelligent insights to optimize your spending patterns.
- Goal-Based Savings: Set achievable financial goals with detailed timelines and milestones. Whether you're saving for a vacation, emergency fund, or retirement, CashNest provides the tools to visualize and reach your targets.
- Collaborative Financial Planning: Share selected financial goals with family members, partners, or friends. Work together toward shared objectives while maintaining privacy for personal finances.
- Comprehensive Expense Tracking: Monitor your expenditures in real-time with automatic categorization and insightful analytics. Identify spending trends and opportunities to save with visual reports and actionable recommendations.
- Unified Financial Dashboard: Access all your financial information in one intuitive platform, with secure connections to your accounts for a complete overview of your financial health.

CashNest helps you build a secure financial future through smart planning, collaborative goal-setting, and detailed tracking—empowering you to make informed financial decisions every day.

### Deployment
The application uses python with a virtual environment and runs with the Flask WSGI. Settings can be managed via the `.flaskenv` or `config.py` configuration.
- The default configuration binds to `127.0.0.1` on port `8000`, update the `FLASK_RUN_HOST` and `FLASK_RUN_PORT` as necessary.
- We assume you are in the working directory or know the relative path.

Linux/MacOS:
```
# Congigure Envionment and Dependencies 
python3 -m venv venv
source venv/bin/activate
./venv/bin/pip install -r requirements.txt

# Deploy
./venv/bin/flask run 
```

Windows:
```
# Congigure Envionment and Dependencies 
python -m venv venv
source venv/Scripts/activate
.\venv\Scripts\pip.exe install -r requirements.txt

# Deploy
.\venv\Scripts\flask.exe run
```

### Testing
The application includes unit testing and headless selenium testing, this is available in `/testing` and `/testing/selenium`.

##### Unit Tests
To conduct unit tests ensure the dependencies are installed via venv as instructed by deployment, then use the python module `unittest` in the `/testing` directory.
```
./venv/bin/python3 -m unittest
```

##### Selenium
Our testing uses the Chrome webdriver, ensure Google Chrome is installed.
- These tests are written only for Unix
Use the Virutal Envionment from Deployment from prior:
```
./venv/bin/pip install -r /testing/selenium/requirements.txt
./venv/bin/python3 testing/selenium/test.py
```
- If the tests fail due to a slow browser, try increasing the `DELAY`