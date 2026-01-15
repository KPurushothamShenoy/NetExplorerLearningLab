# 🌐 Net-Explorer Learning Lab

Net-Explorer Learning Lab is an interactive, full-stack educational platform designed to teach networking fundamentals through hands-on containerization. It allows users to visualize the **OSI Model** while interacting with live **Docker** environments and archiving performance reports to **AWS S3**.



## 🚀 Key Features
- **Dynamic Lab Provisioning:** Uses Python's `subprocess` to orchestrate Docker containers on-demand.
- **Interactive OSI Stack:** A real-time UI that tracks user progress through the 7 layers of networking.
- **Cloud Persistence:** Automated report generation and upload to AWS S3 using `boto3`.
- **Secure Authentication:** User management system built with Flask-Login and Bcrypt password hashing.

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Database:** MySQL
- **DevOps/Cloud:** Docker, AWS S3

🎥 Project Demo ▶️ Watch Demo Video:

Creating Account : https://youtu.be/gZkFmzSUTts
Overall Working :  https://youtu.be/J1G6O1cZZlo

## 🏗️ Project Structure
net-explorer-lab/

├── venv/ # Python Virtual Environment

├── app.py # Main Flask application (Routes & Auth)

├── config.py # Configuration for MySQL, Docker, & AWS

├── requirements.txt # Python package dependencies

├── .env # Environment variables (DB, AWS, Secrets)

├── docker/

│ └── lab-node/

│ └── Dockerfile # Custom image for networking simulations

├── static/ # Frontend Assets

│ ├── css/

│ │ └── style.css # Custom styling & OSI animations

│ ├── js/

│ │ ├── main.js # General UI interactions

│ │ ├── lab-engine.js # Docker API & Task validation logic

│ │ └── osi-visual.js # Dynamic OSI layer rendering

│ └── img/ # Icons and diagrams

└── templates/ # Jinja2 HTML Templates

├── base.html # Main layout (Navbar/Footer)

├── index.html # Landing page & Dashboard

├── login.html # User authentication

├── register.html # New user signup

├── lab.html # The interactive simulation interface

└── history.html # S3-backed performance reports

## Docker Initialization
Intialize Docker From Your System
#docker build -t net_explorerlearning-node ./docker/lab-node

