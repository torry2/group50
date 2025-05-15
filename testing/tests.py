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

class AuthenticationTest(unittest.TestCase):
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
        
    def test_user_registration(self):
        rv = self.client.post("/auth/register", data={
            "username": "testuser",
            "password": "testpassword"
        })
        self.assertEqual(rv.status_code, 201)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")
        
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")
            self.assertTrue(user.check_password("testpassword"))
    
    def test_duplicate_registration(self):
        """Test registration with an existing username"""
        rv = self.client.post("/auth/register", data={
            "username": "testuser1",
            "password": "testpassword1"
        })
        self.assertEqual(rv.status_code, 201)
        
        rv = self.client.post("/auth/register", data={
            "username": "testuser1", 
            "password": "testpassword2"
        })
        self.assertEqual(rv.status_code, 409)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "error")
        self.assertIn("exists", payload["message"].lower())
    
    def test_login_success(self):
        self.client.post("/auth/register", data={
            "username": "testuser2",
            "password": "testpassword2"
        })
        
        rv = self.client.post("/auth/login", data={
            "username": "testuser2",
            "password": "testpassword2"
        })

        self.assertEqual(rv.status_code, 200)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")
        self.assertIn("redirect_url", payload)
        
    def test_login_wrong_pw(self):
        self.client.post("/auth/register", data={
            "username": "testuser3",
            "password": "testpassword3"
        })
        
        rv = self.client.post("/auth/login", data={
            "username": "testuser3",
            "password": "3passwordtest"
        })
        self.assertEqual(rv.status_code, 401)
        
    def test_login_not_registered(self):
        rv = self.client.post("/auth/login", data={
            "username": "testuser99",
            "password": "testpassword99"
        })
        self.assertEqual(rv.status_code, 401)
        
        rv = self.client.post("/auth/login", data={
            "username": "",
            "password": ""
        })
        self.assertEqual(rv.status_code, 400)
    
    def test_logout(self):
        self.client.post("/auth/register", data={
            "username": "testuser4",
            "password": "testpassword4"
        })

        self.client.post("/auth/login", data={
            "username": "testuser4",
            "password": "testpassword4"
        })
        
        rv = self.client.get("/auth/logout")
        self.assertEqual(rv.status_code, 200)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")
        
        # Verify we're logged out by trying to access authenticated endpoint
        rv = self.client.get("/api/data/get-income-budget")
        self.assertNotEqual(rv.status_code, 200)

class TransactionDeletionTest(unittest.TestCase):
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

    def test_delete_transaction_success(self):
        self.register_and_login()
        rv = self.client.post("/api/data/add-transaction", data={
            "name": "Noodles",
            "category": "Food",
            "amount": "25.50"
        })
        self.assertEqual(rv.status_code, 201)
    
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            tx = Transactions.query.filter_by(userid=user.id).first()
            tx_id = tx.id
        
        rv = self.client.delete(f"/api/data/delete-transaction/{tx_id}")
        self.assertEqual(rv.status_code, 200)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")
        self.assertIn("deleted", payload["message"].lower())

        with self.app.app_context():
            tx = Transactions.query.filter_by(id=tx_id).first()
            self.assertIsNone(tx, "Transaction should be deleted")
        
    def test_delete_nonexistent_transaction(self):
        self.register_and_login()
    
        rv = self.client.delete(f"/api/data/delete-transaction/999")
        self.assertEqual(rv.status_code, 404)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "error")
        self.assertIn("not found", payload["message"].lower())
    
    def test_delete_another_users_transaction(self):
        self.register_and_login("testuser1", "testpassword1")
        self.client.post("/api/data/add-transaction", data={
            "name": "Uniqlo",
            "category": "Shopping",
            "amount": "120.00"
        })
    
        with self.app.app_context():
            user = User.query.filter_by(username="testuser1").first()
            tx = Transactions.query.filter_by(userid=user.id).first()
            tx_id = tx.id
    
        self.client.get("/auth/logout")
    
        self.register_and_login("testuser2", "testpassword2")
    
        rv = self.client.delete(f"/api/data/delete-transaction/{tx_id}")
        self.assertEqual(rv.status_code, 404)
    
        with self.app.app_context():
            tx_check = Transactions.query.filter_by(id=tx_id).first()
            self.assertIsNotNone(tx_check)
        
    def test_delete_transaction_unauthenticated(self):
        self.register_and_login()
        self.client.post("/api/data/add-transaction", data={
            "name": "Movie",
            "category": "Entertainment",
            "amount": "50.25"
        })
    
        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            tx = Transactions.query.filter_by(userid=user.id).first()
            tx_id = tx.id
    
        self.client.get("/auth/logout")
    
        rv = self.client.delete(f"/api/data/delete-transaction/{tx_id}")
        self.assertNotEqual(rv.status_code, 200)

        with self.app.app_context():
            tx_check = Transactions.query.filter_by(id=tx_id).first()
            self.assertIsNotNone(tx_check)

class AccountSettingsTest(unittest.TestCase):
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
        return username, password
    
    def test_password_update_success(self):
        username, old_password = self.register_and_login()
        new_password = "newpassword"
        
        rv = self.client.post("/auth/update", data={
            "new_password": new_password,
            "currency": "AUD"  # Including currency as it's part of the form
        })
        self.assertEqual(rv.status_code, 200)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")
        
        self.client.get("/auth/logout")
        
        rv = self.client.post("/auth/login", data={
            "username": username,
            "password": old_password
        })
        self.assertEqual(rv.status_code, 401)
        
        rv = self.client.post("/auth/login", data={
            "username": username,
            "password": new_password
        })
        self.assertEqual(rv.status_code, 200)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")
        
    def test_password_update_unauthenticated(self):
        # No login, try to update password
        rv = self.client.post("/auth/update", data={
            "new_password": "newpassword",
            "currency": "AUD"
        })
        self.assertEqual(rv.status_code, 401)
        
    def test_account_deletion_success(self):
        username, _ = self.register_and_login()
        
        # Adding transactions
        self.client.post("/api/data/add-transaction", data={
            "name": "Noodles",
            "category": "Food",
            "amount": "10.00"
        })
        
        # Adding income and budgets
        self.client.post("/api/data/set-income-budget", data={
            "income": 5000,
            "currency": "AUD",
            "food_budget": 100,
            "rent_budget": 100,
            "utilities_budget": 100,
            "shopping_budget": 100,
            "entertainment_budget": 100,
            "other_budget": 100,
            "goal1_budget": 100,
            "goal2_budget": 100,
            "goal3_budget": 100
        })
        
        # Verify user exists before deletion
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            self.assertIsNotNone(user)
            user_id = user.id
            
            # Verify transaction exists
            transaction = Transactions.query.filter_by(userid=user_id).first()
            self.assertIsNotNone(transaction)
            
            # Verify income and budgets is set
            financials = Financials.query.filter_by(userid=user_id).first()
            self.assertIsNotNone(financials)
        
        # Delete the account
        rv = self.client.post("/api/settings/delete")
        self.assertEqual(rv.status_code, 200)
        payload = rv.get_json()
        self.assertEqual(payload["status"], "success")
        self.assertIn("deleted", payload["message"].lower())
        
        # Verify user and related data are deleted
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            self.assertIsNone(user)
            
            transactions = Transactions.query.filter_by(userid=user_id).all()
            self.assertEqual(len(transactions), 0)
            
            financials = Financials.query.filter_by(userid=user_id).first()
            self.assertIsNone(financials)

if __name__ == "__main__":
    unittest.main()