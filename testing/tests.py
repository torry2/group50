import unittest
from app import create_app, db
from app.models import Transactions, User, Financials
from config import TestConfig

class TransactionsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_and_login(self, username="testuser", password="testpass"):
        rv = self.client.post("/auth/register", data={
            "username": username,
            "password": password
        })
        self.assertEqual(rv.status_code, 201)
        
        rv = self.client.post("/auth/login", data={
            "username": username,
            "password": password
        })
        self.assertEqual(rv.status_code, 200)

    def test_add_transaction_success(self):
        """Checks adding transactions work and that it fields are correct in the DB as well"""
        self.register_and_login()
        rv = self.client.post("/api/data/add-transaction", data={
            "name": "Lunch",
            "category": "Food",
            "amount": "15.50"
        })
        self.assertEqual(rv.status_code, 201)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")

        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            tx = Transactions.query.filter_by(userid=user.id).first()
            self.assertIsNotNone(tx)
            self.assertEqual(tx.name, "Lunch")
            self.assertEqual(tx.category, "Food")
            self.assertAlmostEqual(float(tx.amount), 15.50, places=2)

    def test_add_transaction_missing_field(self):
        """Checks that the website actually blocks adding a transaction when fields are missing"""
        self.register_and_login()
        rv = self.client.post("/api/data/add-transaction", data={
            "name": "",
            "category": "Food",
            "amount": "-5"
        })
        self.assertEqual(rv.status_code, 400)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "error")
        self.assertIn("errors", payload)

    def test_add_transaction_missing_all_fields(self):
        """Checks that website blocks adding a transaction with all fields missing/empty"""
        self.register_and_login()
        rv = self.client.post("/api/data/add-transaction", data={})
        self.assertEqual(rv.status_code, 400)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "error")
        self.assertIn("errors", payload)

class IncomeBudgetsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_and_login(self, username="testuser", password="testpass"):
        rv = self.client.post("/auth/register", data={
            "username": username,
            "password": password
        })
        self.assertEqual(rv.status_code, 201)
        rv = self.client.post("/auth/login", data={
            "username": username,
            "password": password
        })
        self.assertEqual(rv.status_code, 200)

    def test_set_get_income_budgets(self):
        """Checks if setting income and budgets correctly updates the database"""
        self.register_and_login()
    
        test_income = 5000
        test_budget = 100
        test_currency = "AUD"
    
        # Setting the income and budgets via API
        rv = self.client.post("/api/data/set-income-budget", data={
            "income": test_income,
            "currency": test_currency,
            "food_budget": test_budget,
            "rent_budget": test_budget,
            "utilities_budget": test_budget,
            "shopping_budget": test_budget,
            "entertainment_budget": test_budget,
            "other_budget": test_budget,
            "goal1_budget": test_budget,
            "goal2_budget": test_budget,
            "goal3_budget": test_budget
        })
        self.assertEqual(rv.status_code, 200)
    
        # Check the database directly to verify the values were stored correctly
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user, "User should exist in database")
        
            financials = Financials.query.filter_by(userid=user.id).first()
            self.assertIsNotNone(financials, "Financial record should exist for user")
        
            # Verify the correctness of the data in all the fields
            self.assertAlmostEqual(float(financials.income), test_income, places=2)
            self.assertEqual(financials.currency, test_currency)
            self.assertAlmostEqual(float(financials.food), test_budget, places=2)
            self.assertAlmostEqual(float(financials.rent), test_budget, places=2)
            self.assertAlmostEqual(float(financials.utilities), test_budget, places=2)
            self.assertAlmostEqual(float(financials.shopping), test_budget, places=2)
            self.assertAlmostEqual(float(financials.entertainment), test_budget, places=2)
            self.assertAlmostEqual(float(financials.other), test_budget, places=2)
            self.assertAlmostEqual(float(financials.goal1), test_budget, places=2)
            self.assertAlmostEqual(float(financials.goal2), test_budget, places=2)
            self.assertAlmostEqual(float(financials.goal3), test_budget, places=2)

    def test_set_income_budgets_missing_field(self):
        """Checks that the website actually blocks setting the income and budgets when fields are missing"""
        self.register_and_login()

        test_income = 5000
        test_budget = 100
        test_currency = "AUD"
    
        rv = self.client.post("/api/data/set-income-budget", data={
            "income": test_income,
            "currency": test_currency,
            "food_budget": test_budget,
            "rent_budget": test_budget,
            "utilities_budget": "",
            "shopping_budget": test_budget,
            "entertainment_budget": test_budget,
            "other_budget": test_budget,
            "goal1_budget": test_budget,
            "goal2_budget": test_budget,
            "goal3_budget": test_budget
        })
        self.assertEqual(rv.status_code, 400)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "error")
        self.assertIn("errors", payload)
    
    def test_set_income_budgets_missing_all_fields(self):
        """Checks that website blocks setting the income and budgets with all fields missing/empty"""
        self.register_and_login()
        rv = self.client.post("/api/data/set-income-budget", data={})
        self.assertEqual(rv.status_code, 400)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "error")
        self.assertIn("errors", payload)

if __name__ == "__main__":
    unittest.main()