from abc import ABC, abstractmethod
import json
from datetime import datetime
import os

class Employee(ABC):
    def __init__(self, employee_id: str, name: str, department: str):
        self._employee_id = employee_id
        self._name = name
        self._department = department

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def name(self):
        return self._name

    @property
    def department(self):
        return self._department

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    def display_details(self) -> str:
        return f"ID: {self._employee_id}, Name: {self._name}, Department: {self._department}"

    def to_dict(self) -> dict:
        return {
            "Employee_id": self.employee_id,
            "Name": self.name,
            "Department": self.department,
            "Type": "Employee"
        }

class FullTimeEmployee(Employee):
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float):
        super().__init__(employee_id, name, department)
        self.monthly_salary = monthly_salary

    @property
    def monthly_salary(self):
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value):
        if value >= 0:
            self._monthly_salary = value
        else:
            raise ValueError("Salary cannot be negative.")

    def calculate_salary(self) -> float:
        return self._monthly_salary

    def display_details(self) -> str:
        return super().display_details() + f", Monthly Salary: ₹{self._monthly_salary}"

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({"Monthly_salary": self.monthly_salary, "Type": "Full Time"})
        return base

class PartTimeEmployee(Employee):
    def __init__(self, employee_id: str, name: str, department: str, hourly_rate: float, hours_worked_per_month):
        super().__init__(employee_id, name, department)
        self.hourly_rate = hourly_rate
        self.hours_worked_per_month = hours_worked_per_month

    @property
    def hourly_rate(self):
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        if value >= 0:
            self._hourly_rate = value
        else:
            raise ValueError("Hourly rate cannot be negative.")

    @property
    def hours_worked_per_month(self):
        return self._hours_worked_per_month

    @hours_worked_per_month.setter
    def hours_worked_per_month(self, value):
        if value >= 0:
            self._hours_worked_per_month = value
        else:
            raise ValueError("Hours worked cannot be negative.")

    def calculate_salary(self) -> float:
        return self.hourly_rate * self.hours_worked_per_month

    def display_details(self) -> str:
        return super().display_details() + f", Hourly Rate: ₹{self.hourly_rate}, Hours/Month: {self.hours_worked_per_month}"

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "Hourly_rate": self.hourly_rate,
            "Hours_worked_per_month": self.hours_worked_per_month,
            "Type": "Part Time"
        })
        return base

class Manager(FullTimeEmployee):
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float, bonus: float):
        super().__init__(employee_id, name, department, monthly_salary)
        self.bonus = bonus

    @property
    def bonus(self):
        return self._bonus

    @bonus.setter
    def bonus(self, value):
        if value >= 0:
            self._bonus = value
        else:
            raise ValueError("Bonus cannot be negative.")

    def calculate_salary(self) -> float:
        return super().calculate_salary() + self.bonus

    def display_details(self) -> str:
        return super().display_details() + f", Bonus: ₹{self.bonus}"

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({"Bonus": self.bonus, "Type": "Manager"})
        return base

# ================= Company Logic =================

class Company:
    def __init__(self, name, data_file='employees.json'):
        self.name = name
        self._employees = {}
        self._data_file = data_file
        self._load_data()

    def _load_data(self):
        try:
            with open(self._data_file, 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    print("Invalid data format.⚠️Resetting employee data.")
                    return
                company_data = data.get(self.name, {})
                for emp_id, emp_dict in company_data.items():
                    emp_type = emp_dict.get("Type")
                    emp_map = {
                        "Full Time": lambda d: FullTimeEmployee(d['Employee_id'], d['Name'], d['Department'], d['Monthly_salary']),
                        "Part Time": lambda d: PartTimeEmployee(d['Employee_id'], d['Name'], d['Department'], d['Hourly_rate'], d['Hours_worked_per_month']),
                        "Manager": lambda d: Manager(d['Employee_id'], d['Name'], d['Department'], d['Monthly_salary'], d['Bonus'])
                    }
                    if emp_type in emp_map:
                        self._employees[emp_id] = emp_map[emp_type](emp_dict)
        except FileNotFoundError:
            self._employees = {}

    def _save_data(self):
        try:
            with open(self._data_file, 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    data = {}
        except FileNotFoundError:
            data = {}
        data[self.name] = {emp_id: emp.to_dict() for emp_id, emp in self._employees.items()}
        with open(self._data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def add_employee(self, employee: Employee) -> bool:
        if employee.employee_id in self._employees:
            return False
        self._employees[employee.employee_id] = employee
        self._save_data()
        return True

    def remove_employee(self, employee_id: str) -> bool:
        if employee_id in self._employees:
            del self._employees[employee_id]
            self._save_data()
            return True
        return False

    def find_employee(self, employee_id: str):
        return self._employees.get(employee_id)

    def calculate_total_payroll(self) -> float:
        return sum(emp.calculate_salary() for emp in self._employees.values())

    def display_all_employees(self):
        if not self._employees:
            print("No employees to display.")
        for emp in self._employees.values():
            print(emp.display_details())

    def generate_payroll_report(self):
        print("\nPayroll Report:")
        print(f"{'ID':<10}{'Name':<25}{'Type':<22}{'Salary':>5}")
        for employee in self._employees.values():
            emp_type = type(employee).__name__
            salary = employee.calculate_salary()
            salary_str = f"₹{salary:,.2f}"
            print(f"{employee.employee_id:<10}{employee.name:<20}{emp_type:<20}{salary_str:>15}")
        print(f"\nTotal Payroll: ₹{self.calculate_total_payroll():,.2f}")

def initial_banner():
    print("=" * 60)
    print("\tWelcome to Employee Management System")
    print("=" * 60)

def welcome_banner(company_name, existing=True):
    if existing:
        print(f"\nWelcome back to {company_name}'s Employee Management System")
    else:
        print(f"\nCompany '{company_name}' registered successfully!🎉")

def company_exists(company_name, filename="employees.json"):
    if not os.path.exists(filename):
        return False
    with open(filename, "r") as file:
        try:
            data = json.load(file)
            return isinstance(data, dict) and company_name in data
        except json.JSONDecodeError:
            return False

def greet_by_time():
    hour = datetime.now().hour
    if hour < 12:
        print("Good Morning, User! 🙏")
    elif hour < 17:
        print("Good Afternoon, User! 🙏")
    else:
        print("Good Evening, User! 🙏")

def main():
    initial_banner()
    company_name = input("\n🏢 Enter Company Name: ").strip().title()
    exists = company_exists(company_name)
    welcome_banner(company_name, existing=exists)
    greet_by_time()

    company = Company(company_name)

    while True:
        print("\n--- Employee Management System ---")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. View All Employees")
        print("4. Calculate Total Payroll")
        print("5. Search Employee")
        print("6. Generate Payroll Report")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        emp = None
        if choice == "1":
            while True:
                print("\n1. Full-Time\n2. Part-Time\n3. Manager")
                emp_type = input("Choose employee type: ").strip()

                if emp_type in ["1", "2", "3"]:
                    break
                else:
                    print("Invalid employee type.⚠️ \nPlease choose 1, 2, or 3.")

            try:
                emp_id = input("Enter ID: ").strip()
                company_name = input("Enter Name: ").strip()
                dept = input("Enter Department: ").strip()

                if emp_type == "1":
                    salary = float(input("Enter Monthly Salary: "))
                    emp = FullTimeEmployee(emp_id, company_name, dept, salary)
                elif emp_type == "2":
                    rate = float(input("Enter Hourly Rate: "))
                    hours = float(input("Enter Hours Worked: "))
                    emp = PartTimeEmployee(emp_id, company_name, dept, rate, hours)
                elif emp_type == "3":
                    salary = float(input("Enter Monthly Salary: "))
                    bonus = float(input("Enter Bonus: "))
                    emp = Manager(emp_id, company_name, dept, salary, bonus)

                if company.add_employee(emp):
                    print("Employee added successfully.✅")
                else:
                    print("Employee ID already exists.⚠️")

            except ValueError:
                print("Invalid numeric input. Try again.❌")

        elif choice == "2":
            emp_id = input("Enter employee ID to remove: ").strip()
            if company.remove_employee(emp_id):
                print("Employee removed.✅")
            else:
                print("Employee not found.❌")

        elif choice == "3":
            company.display_all_employees()

        elif choice == "4":
            print(f"Total Payroll: ₹{company.calculate_total_payroll():,.2f}")

        elif choice == "5":
            emp_id = input("Enter employee ID to search: ").strip()
            emp = company.find_employee(emp_id)
            if emp:
                print("Employee Found:\n", emp.display_details())
            else:
                print("Employee not found.❌")

        elif choice == "6":
            company.generate_payroll_report()

        elif choice == "7":
            print(f"\n🔚 Thank you for using {company_name} Employee Management System.")
            print("💡 Built with logic and innovation.")
            print("🧑‍💻Created by: Akanksha Singh")
            print("📧 Contact: akanksha24d@gmail.com")
            print("🖥️  Exiting system... Goodbye!\n")
            break

        else:
            print("Invalid choice. Try again.❌")

if __name__ == "__main__":
    main()
