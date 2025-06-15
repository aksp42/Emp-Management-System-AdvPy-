#💼 Employee Management System
An Advanced Python-Based Console Project by Akanksha Singh

A modern, interactive, and extensible console-based Employee Management System, built entirely as a solo project by Akanksha Singh, a student of B.Tech CSE - Data Science.

This project replicates the core backend functionality of a real-world company’s employee and payroll system, implementing features like:

  ->Company-wise data grouping
  ->Dynamic salary calculations
  ->JSON-based persistent storage
  ->OOP principles including inheritance, abstraction, encapsulation, and decorators
All wrapped in a user-friendly command-line interface.

🚀 Key Features
🏢 Company Registration – Register any company before managing employees
👥 Employee Types – Full-Time, Part-Time, and Manager roles
💸 Dynamic Salary Calculation – Based on hourly/monthly logic
📂 JSON-based Data Storage – Grouped and stored company-wise
📊 Real-Time Payroll Reports – With timestamps for every entry
🕒 Time-Based Greetings – Adds realistic touch to CLI experience
✨ Clean CLI Interface – Designed for intuitive navigation
📦 Excel Report Support (Optional) – via excel_report.py for extended reporting

🛠️ Tech Stack & Concepts Used
Technology / Concept	Description
🐍 Python 3	Core programming language
📁 JSON	For structured data persistence
💡 OOP Principles	Abstraction, Inheritance, Encapsulation
🔁 Decorators	Property decorators for safe attribute access
💻 Command Line Interface	Text-based user interaction

🧪 JSON Structure Example
json
Copy
Edit
{
  "NeoEdge Analytics": {
    "EMP001": {
      "Name": "Ravi Kumar",
      "Department": "IT",
      "Monthly_salary": 50000,
      "Type": "Full Time"
    }
  },
  "Orbyte Systems": {
    "EMP045": {
      "Name": "Kiran A.",
      "Hourly_rate": 300,
      "Hours_worked_per_month": 80,
      "Type": "Part Time"
    }
  }
}
🔹 Why this structure?
Instead of flatly saving all employee data, the JSON is organized company-wise, just like in real-world SaaS models. This approach offers:

✅ Multi-company support
✅ Future-proof scalability
✅ Cleaner file structure

🙋‍♀️ About the Developer
👩‍💻 Akanksha Singh
🎓 B.Tech CSE – Data Science
🔥 Passionate Pythonista | Logical Thinker | Curious Coder
📬 Email: akanksha24d@gmail.com
🌐 GitHub: aksp42

“Crafted with dedication, tested with curiosity, and shared with ❤️.”
