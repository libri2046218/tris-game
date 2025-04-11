# 🎮 Tris-Game

A simple implementation of the famous tic-tac-toe game with a client-server architecture and a REST API twist. 🕹️✨

## ✨ Features

- 🎲 **Tic-Tac-Toe Gameplay**: Enjoy the classic game of tic-tac-toe.
- 🖧 **Client-Server Architecture**: Built with a client-server model to demonstrate network communication.
- 🌐 **REST API Integration**: Leverages REST APIs for seamless interaction between client and server.
- 🐳 **Dockerized and Orchestrated**: Includes Dockerfiles and docker-compose for easy deployment.

## 🛠️ Technologies Used

- 💻 **Programming Language**: Python
- 🖼️ **Frontend**: HTML
- 🔌 **Backend**: REST API
- 📦 **Containerization**: Docker

## 🚀 Getting Started

### 📋 Prerequisites

To run this project, ensure you have the following installed:

- 🐍 Python 3.8 or higher
- 🐳 Docker (optional, for containerized deployment)

### ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/libri2046218/tris-game.git
   cd tris-game
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Run the api-server:
   ```bash
   uvicorn /src/api-server/api-server:app --port 8000
   ```

4. Run the html-server:
   ```bash
   uvicorn /src/html-server/html-server:app --port 8001
   ```

5. Open the client in your browser:
   Navigate to `localhost:8001` in your browser to start playing. 🎉

### 🐳 Docker Deployment

1. Build the Docker image:
   ```bash
   cd src
   docker compose up.
   ```
2. Access the game:
   Open your browser and go to `http://localhost:8001`. 🌐

## 📖 Usage

- Start the server and open the client to play the game. 🎯
- Use the REST API for programmatic interactions (API documentation to be added). 📄

## 🤝 Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome. 🌟

## 📜 License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). ⚖️

## 📬 Contact

For inquiries or feedback, please reach out to the repository owner: [libri2046218](https://github.com/libri2046218). ✉️
