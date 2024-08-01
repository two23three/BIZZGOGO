import os
from datetime import datetime, timedelta
from random import choice, randint
import uuid
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, User, Role, Income, IncomeCategory, Expense, ExpenseCategory, Debt, DebtPayment, FinancialReport, Transaction, Asset, SavingsGoal, Setting

# Configure your database URI here
DATABASE_URI = 'postgresql://mike:nU6Li3vmuDYEQptTz86PNMhOsaYCqNKu@dpg-cqlljsg8fa8c73b454k0-a.oregon-postgres.render.com/mydatabase_0nn3'
# DATABASE_URI = 'postgresql://postgres:newpassword@localhost/mydatabase'

# Set up the database connection and session
engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# # Create tables if they don't exist
# db.create_all()

fake = Faker()

def create_roles():
    roles = ['Admin', 'User', 'Manager']
    for role_name in roles:
        role = Role(name=role_name, description=fake.sentence())
        session.add(role)
    session.commit()

def create_users():
    roles = session.query(Role).all()
    for _ in range(10):
        user = User(
            name=fake.name(),
            phone_number=fake.phone_number(),
            email=fake.email(),
            password_hash=fake.password(),
            role_id=choice(roles).id,
            referral_code=str(uuid.uuid4()),
            # referred_by=choice([None, str(uuid.uuid4())])
        )
        user.set_password(fake.password())
        session.add(user)
    session.commit()

def create_income_categories():
    categories = ['Salary', 'Investment', 'Other']
    for category_name in categories:
        category = IncomeCategory(name=category_name, description=fake.sentence())
        session.add(category)
    session.commit()

def create_expense_categories():
    categories = ['Food', 'Rent', 'Utilities']
    for category_name in categories:
        category = ExpenseCategory(name=category_name, description=fake.sentence())
        session.add(category)
    session.commit()

def create_incomes():
    users = session.query(User).all()
    categories = session.query(IncomeCategory).all()
    for _ in range(10):
        income = Income(
            user_id=choice(users).id,
            amount=round(randint(1000, 5000) / 100, 2),
            category_id=choice(categories).id,
            date=fake.date_this_year(),
            description=fake.sentence(),
            is_recurring=choice([True, False])
        )
        session.add(income)
    session.commit()

def create_expenses():
    users = session.query(User).all()
    categories = session.query(ExpenseCategory).all()
    for _ in range(10):
        expense = Expense(
            user_id=choice(users).id,
            amount=round(randint(100, 2000) / 100, 2),
            category_id=choice(categories).id,
            date=fake.date_this_year(),
            description=fake.sentence(),
            is_recurring=choice([True, False])
        )
        session.add(expense)
    session.commit()

def create_debts():
    users = session.query(User).all()
    for _ in range(10):
        debt = Debt(
            user_id=choice(users).id,
            name=fake.word(),
            principal_amount=round(randint(500, 10000) / 100, 2),
            interest_rate=round(randint(1, 20) / 100, 2),
            remaining_balance=round(randint(500, 10000) / 100, 2),
            due_date=fake.date_this_year(),
            description=fake.sentence()
        )
        session.add(debt)
    session.commit()

def create_debt_payments():
    debts = session.query(Debt).all()
    for _ in range(10):
        payment = DebtPayment(
            debt_id=choice(debts).id,
            amount=round(randint(100, 2000) / 100, 2),
            payment_date=fake.date_this_year()
        )
        session.add(payment)
    session.commit()

def create_financial_reports():
    users = session.query(User).all()
    report_types = ['Monthly', 'Annual', 'Quarterly']
    for _ in range(10):
        report = FinancialReport(
            user_id=choice(users).id,
            report_type=choice(report_types),
            report_data=fake.text()
        )
        session.add(report)
    session.commit()

def create_transactions():
    users = session.query(User).all()
    for _ in range(10):
        transaction = Transaction(
            user_id=choice(users).id,
            amount=round(randint(100, 5000) / 100, 2),
            transaction_type=choice(['Income', 'Expense']),
            category_id=choice([None, randint(1, 10)]),
            date=fake.date_this_year(),
            description=fake.sentence()
        )
        session.add(transaction)
    session.commit()

def create_assets():
    users = session.query(User).all()
    for _ in range(10):
        asset = Asset(
            user_id=choice(users).id,
            name=fake.word(),
            value=round(randint(1000, 100000) / 100, 2),
            purchase_date=fake.date_this_year(),
            description=fake.sentence()
        )
        session.add(asset)
    session.commit()

def create_savings_goals():
    users = session.query(User).all()
    for _ in range(10):
        goal = SavingsGoal(
            user_id=choice(users).id,
            name=fake.word(),
            target_amount=round(randint(5000, 50000) / 100, 2),
            current_amount=round(randint(1000, 50000) / 100, 2),
            start_date=fake.date_this_year(),
            end_date=fake.date_this_year() + timedelta(days=365),
            description=fake.sentence()
        )
        session.add(goal)
    session.commit()

def create_settings():
    users = session.query(User).all()
    setting_names = ['Theme', 'Language', 'Notifications']
    for _ in range(10):
        setting = Setting(
            user_id=choice(users).id,
            setting_name=choice(setting_names),
            setting_value=fake.word()
        )
        session.add(setting)
    session.commit()

def main():
    create_roles()
    create_users()
    create_income_categories()
    create_expense_categories()
    create_incomes()
    create_expenses()
    create_debts()
    create_debt_payments()
    create_financial_reports()
    create_transactions()
    create_assets()
    create_savings_goals()
    create_settings()

if __name__ == '__main__':
    main()
    session.close()
