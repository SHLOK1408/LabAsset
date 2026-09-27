# LabAsset - Laboratory Equipment Tracking System

LabAsset is a dynamic web application developed using Flask for tracking laboratory equipment and its current status.

The project demonstrates software development and DevOps practices including Git, GitHub, automated testing, linting, Docker containerization, CI/CD using GitHub Actions, and cloud deployment using Render.

## Features

- View laboratory equipment inventory
- Add new equipment with validation
- Issue available equipment
- Return issued equipment
- Send equipment for maintenance
- Mark maintained equipment as available
- Search equipment by Asset ID or equipment name
- Filter equipment by status
- Dashboard showing equipment statistics
- JSON API for equipment data
- Health-check endpoint
- Display deployed Git commit ID

## Technology Stack

- Python
- Flask
- HTML
- CSS
- Jinja2
- Pytest
- Flake8
- Docker
- Gunicorn
- Git and GitHub
- GitHub Actions
- Render

## Project Structure

```text
LabAsset/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── app.py
├── pytest.ini
├── requirements.txt
└── README.md