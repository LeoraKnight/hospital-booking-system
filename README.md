# 🏥 Hospital Booking System

A Python-based hospital booking system designed using object-oriented programming principles and multiple design patterns. This project simulates a simplified healthcare management platform where patients, staff, and administrators can interact through role-based access.

---

## 🔑 Features
- **Role-based login system** (Staff / Admin)
- **Patient record management**
- **Booking and room management**
- **Secure password handling** (SHA-256 hashing)
- **State management** for appointments (booked, cancelled, completed)
- **Persistent data storage** using text files
- **Modular, reusable code** with clear class structures
- **Implemented design patterns**: Factory, Singleton, State

---

## 🛠️ Technologies Used
- Python 3
- Object-Oriented Programming (OOP)
- File I/O for persistence
- Design Patterns

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/LeoraKnight/hospital-booking-system.git
2.   cd hospital-booking-system
3. Run the program: python __init__.py

hospital-booking-system/
│── __init__.py          # Entry point
│── admin_menu.py        # Admin menu options
│── booking_admin.py     # Admin booking functions
│── booking_staff.py     # Staff booking functions
│── createadmin.py       # Script to create admin accounts
│── entities.py          # Core entities (patients, rooms, etc.)
│── factories.py         # Factory design pattern
│── login.py             # Login handling
│── patients.py          # Patient management
│── room_types.py        # Room type definitions
│── rooms.py             # Room management
│── staff.py             # Staff entity handling
│── staff_menu.py        # Staff menu options
│
├── Data/                # Data storage
│   └── patients.txt
│   └── bookings.txt
│
├── Design/              # Diagrams of system design
│
├── Logins/              # Login credentials for demo admin/staff
│
├── __pycache__/         # Python cache (ignored in Git)
│
├── README.md
└── .gitignore
