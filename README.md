# Nethub Backend

## Table of contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Purpose](#purpose)
4. [Technologies Used](#technologies-used)
5. [Repository Structure](#repository-structure)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

## Introduction
* This is the backend for Nethub, a modern e-commerce platform for technology products.
* Built with Flask, it handles all core functionalities including product management, user authentication, and admin operations.
* Designed to work seamlessly with the frontend, providing a secure and scalable API for managing users, products, and orders.

## Key Features
* User authentication and role management (admin/user)
* CRUD operations for products, categories, and orders
* Admin dashboard support
* RESTful API design for frontend integration
* Utility functions for email notifications, data validation, and more
* Secure handling of sensitive data and password hashing

## Purpose
* To provide a robust backend for a growing e-commerce platform.
* Enables iterative development, allowing the frontend to integrate features like browsing, cart management, and order processing
* Serves as both a professional portfolio project and a functional tool for real-world business use.

## Technologies Used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-ED8B00?style=for-the-badge&logo=python&logoColor=white)

- **Backend Framework:** Flask (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Flask-Migrate (Alembic)
- **Validation:** Flask-WTF

## Repository Structure

```text
/nethub-backend
├── run.py                 # Application entry point
├── app/
│   ├── __init__.py        # Application factory
│   ├── routes/            # Application routes and views
│   ├── utils/             # Utility functions and helpers
│   ├── forms.py           # Form classes and validations
│   └── models.py          # Database models
└── migrations/            # Database migration history
```

## Installation
* To get started with this repository, follow these steps:
1. **Clone the repository**: Clone the repository to your local machine
    ```sh
        git clone https://github.com/Emogy-reunion/nethub_backend.git
    ```
## Usage
1. **Navigate to the project directory**:
    ```sh
        cd nethub_backend
    ```

2. **Create virtual environment**: Ensure you have python and virtualenv installed. Create and then activate a virtual environment
    ```sh
        python3 -m virtualenv myenv : in this case myenv in the environment (feel free to name it as you like)
        source myenv/bin/activate
    ```

3. **Install dependencies**: Install the required dependencies from `requirements.txt`
    ```sh
        pip install -r requirements.txt
    ```

4. **Run the application**
    ```sh
        python3 run.py
    ```
* This application should now be running, and you can access it in your browser at  `http://127.0.0.1:5000`.

## Contributing
* Contributions are welcome! Whether you are fixing a bug, improving the documentation, or adding new features, your help is appreciated.
* To contribute:
1. **Fork** the repository
2. **Clone** your fork
3. **Create a new branch** for your changes
4. **Make your changes** and commit them
5. **Push** to your fork
6. **Open a pull a request** and describe your changes

* Please make sure to follow the project's code style and write clear, concise commit messages.

## License
* This project is licence under the MIT License

## Contact
* If you have any questions, feel free to reach out
    - Email: markvictormugendi@gmail.com
