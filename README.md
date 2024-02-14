# SSIS (Simple Student Information System) with Cloudinary CRUD

SSIS-Cloudinary CRUD is a web application built using Flask, a micro web framework for Python. This application allows users to manage student information, colleges, and courses with CRUD (Create, Read, Update, Delete) functionality. Additionally, it integrates with Cloudinary for image uploads.

## Features

- **User Authentication**: Users can sign up for an account or sign in with their credentials.
- **CRUD Operations**: Users can perform CRUD operations on student records, colleges, and courses.
- **Cloudinary Integration**: Images can be uploaded and stored using Cloudinary.
- **Search Functionality**: Users can search for students, colleges, and courses based on various criteria.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.10.0
- Flask
- Flask-WTF
- Flask-Login
- Flask-MySQL
- Cloudinary Python SDK

You can install these dependencies using pip:

```bash
pip install flask flask-wtf flask-login flask-mysql cloudinary
