# CS50 Final Project - Personal Portfolio Website

Video Demo: https://youtu.be/7NczC-J_i0g

## Introduction

This repository contains the code for "My Webpage" a personal portfolio website. In addition to the HTML, CSS, and JavaScript files that define the structure and appearance of the website, a Python file named `app.py` is included. This Python file utilizes the Flask web framework to handle user authentication, registration, and reporting functionality.

## Technologies used

- HTML, CSS, JS
- Jinja
- SQLite
- Python, Flask

## Project Structure

- '/static': Contains CSS and JS files, favicon and images used in project.
- '/templates': Stores templates of different sites of website (using Jinja syntax)
- 'app.py': The main Flask application - it includes the routing logic, configuration settings, and integration with the backend functionalities.
- 'helpers.py': Python file with function to generate apology and function to look if user is loged in. (Used from PSET 9).
- 'report.db': Database containing two tables. First table is storing usernames, hashed passwords. Second is storing user_ids and their reports.
- 'README.md': The documentation file you are currently reading, providing an overview of the project.

## Features

### 1. Frontend

#### 1.1 Responsive Design

The website is built with a responsive design, ensuring optimal viewing and interaction across a variety of devices and screen sizes.

#### 1.2 Navigation Bar

The navigation bar provides easy access to various sections of the website, such as Home, About, Portfolio, and Contact. The navigation items are designed to smoothly scroll to their respective sections. On mobile devices, it is implemented as a hamburger menu.

#### 1.3 Sections

The "About Me" section offers a brief introduction, detailing my journey as a developer. It includes tabs showcasing my programming skills and certifications.
The "Portfolio" section highlights my coding project. It includes a link to my GitHub profile, allowing visitors to explore my contributions.
The "Contact" section provides multiple ways to get in touch, including email, phone, and links to social media profiles.

#### 1.4 Footer

The footer includes a form for reporting bugs, a link to view messages (backend functionality), and options for user authentication (register and log in).

### 2. Backend

#### 2.1 User Authentication

- **Register**: Users can register by providing a username and password. The backend validates the user input, hashes the password, and inserts the user's information into the database.
- **Login**: Registered users can log in by providing their username and password. The backend verifies the credentials against the stored hash in the database.
- **Logout**: Users can log out, and their session is cleared.

#### 2.2 Reporting System

- **Report Bug**: Authenticated users can submit bug reports through a form, and the backend inserts the user ID along with the reported message into the database.
- **View Reports**: Authenticated users can view their submitted bug reports on a separate page.

#### 2.3 Database Integration

- **SQLite**: The backend seamlessly integrates with an SQLite database, providing a reliable and lightweight storage solution. The database stores user information, including usernames and hashed passwords, and bug reports submitted by users.
