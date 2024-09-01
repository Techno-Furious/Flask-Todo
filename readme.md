# Flask To-Do Application

![Flask](https://img.shields.io/badge/Flask-2.0.2-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.35.5-blue.svg)

A simple, elegant To-Do application built using Flask, a lightweight Python web framework. This application allows users to create, read, update, and delete tasks.

### [Live Demo](https://flask-todo-blue.vercel.app/)

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [Technologies Used](#technologies-used)

## Features

- **Add Tasks:** Users can add tasks with a title and description.
- **Update Tasks:** Users can edit the title and description of existing tasks.
- **Delete Tasks:** Users can delete tasks that are no longer needed.
- **Search Tasks:** Users can search for tasks by title.
- **Responsive Design:** The application is responsive and works well on all devices.
- **Simple UI:** A clean and intuitive user interface for easy navigation.

## Getting Started

### Prerequisites

- **Python 3.9+**: Make sure you have Python installed on your system.
- **Pip**: Python package installer.

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Techno-Furious/Flask-Todo.git
   cd Flask-Todo
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```sh
   flask db upgrade
   ```

5. **Run the application:**

   ```sh
   flask run
   ```

6. **Visit the application:**
   Open your browser and go to `http://127.0.0.1:5000/`.


## Running Locally

To run this application on your local machine, follow the instructions in the [Getting Started](#getting-started) section above.

## Deployment

This application is deployed on Vercel and can be accessed [here](https://flask-todo-blue.vercel.app/).

To deploy this Flask application to Vercel:

1. **Create a `vercel.json` file** in your project root with the following content:

   ```json
   {
     "builds": [
       { "src": "app.py", "use": "@vercel/python" }
     ],
     "routes": [
       { "src": "/(.*)", "dest": "app.py" }
     ]
   }
   ```

2. **Push the changes to your GitHub repository**.

3. **Connect your repository to Vercel** and deploy.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **SQLite**: A C library that provides a lightweight, disk-based database.
- **HTML/CSS**: For building the front-end of the application.
- **Jinja2**: A templating engine for Python used with Flask.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.