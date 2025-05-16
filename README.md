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

- **Smart Budget Management**: Create customized budgets tailored to your financial situation and lifestyle. Easily allocate funds across different categories and receive intelligent insights to optimize your spending patterns.
- **Goal-Based Savings**: Set achievable financial goals with detailed timelines and milestones. Whether you're saving for a vacation, emergency fund, or retirement, CashNest provides the tools to visualize and reach your targets.
- **Collaborative Financial Planning**: Share selected financial goals with family members, partners, or friends. Work together toward shared objectives while maintaining privacy for personal finances.
- **Comprehensive Expense Tracking**: Monitor your expenditures in real-time with automatic categorization and insightful analytics. Identify spending trends and opportunities to save with visual reports and actionable recommendations.
- **Unified Financial Dashboard**: Access all your financial information in one intuitive platform, with secure connections to your accounts for a complete overview of your financial health.

CashNest helps you build a secure financial future through smart planning, collaborative goal-setting, and detailed tracking—empowering you to make informed financial decisions every day.

### Deployment
The application is a Flask application, we assume you have Python appropriately installed and added to PATH.
- Configuration can be modified in `.flaskenv`
- We assume you are in the working directory or know the relative path

Linux/MacOS:
```
# Congigure Envionment and Dependencies 
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Run
./venv/bin/flask run 
```

Windows:
```
# Congigure Envionment and Dependencies 
python -m venv venv
.\venv\Scripts\pip.exe install -r requirements.txt

# Run
.\venv\Scripts\flask.exe run
```

### Testing
The application includes unit testing and Selenium testing, this is available in `/testing` and `/testing/selenium`.
- Use the virtual environment created from Deployment

##### Unit Tests
The python unittest module is used, ensure your Python version supports this.

```
# Linux/MacOS
./venv/bin/python3 -m unittest ./testing/tests.py

# Windows
.\venv\Scripts\python.exe -m unittest .\testing\tests.py
```

##### Selenium
Chromium is used, ensure Google Chrome (or relevant webdriver) is installed.

Linux/MacOS
```
# Install Requirements
./venv/bin/pip install -r ./testing/selenium/requirements.txt

# Run Tests
./venv/bin/python3 ./testing/selenium/tests.py
```

Windows:
```
# Install Requirements
.\venv\Scripts\pip.exe install -r .\testing\selenium\requirements.txt

# Run Tests
.\venv\Scripts\python.exe .\testing\selenium\tests.py
```
