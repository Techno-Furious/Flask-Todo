# Flask To-Do Application

![Flask](https://img.shields.io/badge/Flask-3.0.3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.35.5-blue.svg)

A comprehensive, feature-rich To-Do application built using Flask, a lightweight Python web framework. This application allows users to create, organize, track, and manage tasks efficiently.

### [Live Demo](https://flask-todo-blue.vercel.app/)

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [Technologies Used](#technologies-used)

## Features

- **Task Management:** Create, update, and delete tasks with title, description, priority, and category
- **Due Dates:** Set and track due dates for tasks
- **Task Prioritization:** Assign High, Medium, or Low priority to tasks
- **Categories:** Organize tasks by custom categories
- **Task Status:** Track completed and active tasks
- **Statistics Dashboard:** View task completion statistics and analytics
- **Search Functionality:** Search for tasks by title or description
- **Sorting & Filtering:** Sort and filter tasks by various criteria
- **Subtasks:** Break down complex tasks into smaller subtasks
- **Drag & Drop:** Reorder tasks with intuitive drag and drop functionality
- **Responsive Design:** Works on desktop, tablet, and mobile devices

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

### Deploying to Vercel

This application is configured for easy deployment on Vercel:

1. Fork this repository to your GitHub account.
2. Sign up for a [Vercel account](https://vercel.com/) (it's free and you can sign up with your GitHub account).
3. Create a new project on Vercel and import your GitHub repository.
4. Vercel will automatically detect the configuration from `vercel.json` and deploy the application.
5. Your application will be live at `https://your-project-name.vercel.app`

#### Environment Variables (if needed)

If you need to use a different database in production, set these environment variables in your Vercel project settings:
- `POSTGRES_URL_SQL`: Your database connection URL

### Deployment Note

Vercel's free tier has a serverless architecture, which means:
- Cold starts may occur if the application hasn't been used recently
- Database connections will be reconnected for each request
- The SQLite database in this project will be reset on each deployment (use a persistent database like PostgreSQL for production)

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) for Python
- **Flask-Migrate**: Database migration handling for Flask/SQLAlchemy
- **Bootstrap 5**: Front-end framework for responsive design
- **Chart.js**: JavaScript library for data visualization
- **SQLite**: Lightweight disk-based database (development)
- **PostgreSQL**: Advanced open-source database (production option)
- **Vercel**: Hosting and serverless deployment platform