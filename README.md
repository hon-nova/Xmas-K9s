# Xmas-K9s Project

An online ticket sales application for the Christmas season 2025 across Canadian provinces, featuring an AI agent to assist with ticket and order verification before event entry.

## Table of Contents

- [Xmas-K9s Project](#xmas-k9s-project)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
    - [Frontend](#frontend)
    - [Backend](#backend)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Frontend Setup](#frontend-setup)
    - [Backend Setup](#backend-setup)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Project Structure](#project-structure)
  - [Deployment](#deployment)
  - [Demo](#demo)
  - [Contributing](#contributing)
  - [Contact](#contact)

## About the Project

The Xmas-K9s project aims to provide a seamless online platform for purchasing tickets for various Christmas events scheduled across different Canadian provinces in 2025. A unique aspect of this application is the integration of an AI agent, which plays a crucial role in verifying purchased tickets and orders, ensuring a smooth entry process for event attendees. This system enhances security and efficiency for both users and event organizers.

## Features

*   **User Authentication:** Secure user registration and login functionalities to manage personal profiles and ticket purchases.
*   **Ticket Page:** A comprehensive section to browse, select, and purchase tickets for various Christmas events.
*   **24/7 Chatbot (AI Agent):** An integrated AI agent powered by Google's Gemini-2.5-flash model, available around the clock to assist users with ticket and order verification, and provide event information. It includes Human-in-the-Loop (HITL) and interruption capabilities for enhanced interaction.
*   **Profile Management:** Users can view and manage their personal information, past orders, and ticket details.

## Technologies Used

This project leverages a modern stack for both its frontend and backend, ensuring a robust, scalable, and user-friendly experience.

### Frontend

*   **React.js:** A declarative, component-based JavaScript library for building user interfaces.
*   **Vite:** A fast build tool that significantly improves the frontend development experience.
*   **TypeScript:** A typed superset of JavaScript that compiles to plain JavaScript, enhancing code quality and maintainability.
*   **Tailwind CSS:** A utility-first CSS framework for rapidly building custom designs.
*   **Zustand:** A small, fast, and scalable state-management solution.

### Backend

*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.9+ based on standard Python type hints.
*   **Microservices Architecture:** The backend is designed with a microservices approach, promoting scalability and modularity.
*   **PostgreSQL (on Neon):** A powerful, open-source object-relational database system, hosted on Neon for serverless capabilities.
*   **SQLAlchemy ORM:** A Python SQL toolkit and Object Relational Mapper that gives developers the full power and flexibility of SQL.
*   **LangGraph:** A library for building stateful, multi-actor applications with LLMs, used here for orchestrating the AI agent.
    *   **Features:** Human-in-the-Loop (HITL) and interruptions for dynamic AI agent interaction.
*   **Google Model:** `gemini-2.5-flash` for the core AI agent functionalities.

## Getting Started

Follow these instructions to get your project up and running locally.

### Prerequisites

Ensure you have the following installed on your machine:

*   Node.js (LTS version recommended)
*   npm or yarn
*   Python 3.9+
*   Docker and Minikube (for local Kubernetes cluster)
*   `kubectl` (Kubernetes command-line tool)

### Installation

Clone the repository:

```bash
git clone https://github.com/hon-nova/Xmas-K9s
cd Xmas-K9s 
```

### Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install # or yarn install
```

To run the frontend in development mode:

```bash
npm run dev # or yarn dev
```

The frontend application should now be accessible in your browser, typically at `http://localhost:5173`.

### Backend Setup

Navigate to the backend directory, create a virtual environment, install dependencies, and configure environment variables:

```bash
cd backend/english
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

**Environment Variables:**
Create a `.env` file in the `backend` directory fill in your details, especially for the Neon PostgreSQL connection string and Google Gemini API key.

```ini
# .env example
DATABASE_URL="postgresql://user:password@host:port/database"
GOOGLE_API_KEY="your_gemini_api_key_here"
# Add any other necessary environment variables
```

**Database Migrations:**
Run database migrations using SQLAlchemy (or your chosen migration tool, if any, for FastAPI projects often handled manually or with tools like Alembic if integrated).

*(Note: Specific migration commands might vary depending on your FastAPI/SQLAlchemy setup. You might need to generate migrations first if not already done.)*

To run the backend development server:

```bash
uvicorn english.app.main:app --reload --port 8005 
```

The backend API should be running, typically at `http://localhost:8005`.

## Usage

Once both the frontend and backend are running:

1. Access the frontend application via your browser
2. Explore the "Ticket Page" - available Christmas events
3. Register a new user or log in with existing credentials
4. Interact with the 24/7 Chatbot for assistance with ticket verification
5. Manage your details and view your orders on the "Profile" page

## API Endpoints

The backend exposes the following primary API endpoints:

| Endpoint        | Description                                                                                             |
| :-------------- | :------------------------------------------------------------------------------------------------------ |
| `/api/auth`     | Handles user authentication (registration, login, token management).                                    |
| `/api/bot`      | Manages interactions with the AI chatbot, processing user queries and providing responses.              |
| `/api/profile`  | Allows users to retrieve and update their profile information and view order history.                   |

*(Note: Specific methods (GET, POST, PUT, DELETE) for each endpoint would be detailed in API documentation, e.g., Swagger UI if enabled in FastAPI.)*

## Project Structure

```
.
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── store/          # Zustand store
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── styles/
│   │        ├── home.module.css # in-line styles
│   │        ├── ...
│   │   └── index.css       # Tailwind CSS setup
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── backend/
│   ├──core/
│   │     ├── models/
│   │     ├── config.py          
│   │     └── ...
│   └──english/             
│         ├──app/   
│         ├── routes/
│         │    ├── services/
│         │    ├── ...
│         │    ├── main.py
│         ├── requirements.txt
│         ├── Dockerignore
│         └── Dockerfile
│         
├── k8s/                    # Kubernetes manifests
│   ├── deployment.yaml
│   ├── svc.yaml
│   ├── ingress.yaml
│   ├── configMap.yaml
│   ├── secret.yaml
│   └── ...
├── .gitignore
├── README.md
└── LICENSE
```

## Deployment

The project is designed to be deployed on a Kubernetes cluster, with local development and testing facilitated by Minikube.

**Local Kubernetes Cluster (Minikube):**

1.  **Start Minikube:**
    ```bash
    minikube start
    ```
2.  **Enable Ingress Controller:**
    ```bash
    minikube addons enable ingress
    ```
3.  **Build Docker Images:**
    Ensure Dockerfiles are present for both frontend and backend. Build images in the Minikube Docker daemon:
    ```bash
    eval $(minikube docker-env) # Connects your shell to Minikube's Docker daemon
    docker build -t xmas-k9s-frontend:latest ./frontend
    docker build -t xmas-k9s-backend:latest ./backend
    eval $(minikube docker-env -u) # Disconnect from Minikube's Docker daemon
    ```
4.  **Apply Kubernetes Manifests:**
    Navigate to your Kubernetes manifest directory (`k8s/`) and apply the deployments, services, and ingress rules:
    ```bash
    kubectl apply -f k8s/
    ```
5.  **Access the Application:**
    Retrieve the Ingress IP and add it to your `/etc/hosts` file (or equivalent) for local domain resolution.
    ```bash
    minikube ip
    # Add an entry like: <minikube-ip> your-app-domain.local to your /etc/hosts file
    ```
    Then, access the application via `http://your-app-domain.local` in your browser.


<!-- ![Demo](frontend-research/public/assets/demo.gif) -->

<!-- ![Demo](frontend-research/public/assets/output.mp4) -->

## Demo

<!-- [▶️ Watch Demo Video (1:05)](frontend-research/public/assets/output.mp4) -->

<video width="800" controls>
  <source src="frontend-research/public/assets/output.mp4" type="video/mp4">
  Your browser doesn't support video playback.
</video>

## Contributing

We welcome contributions to the Xmas-K9s project! To contribute:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request, detailing your changes and their purpose.

## Contact

Hon Nguyen - [hon.mybcit@gmail.com](mailto:hon.mybcit@gmail.com)
Project Link: [https://github.com/hon-nova/Xmas-K9s](https://github.com/hon-nova/Xmas-K9s)****