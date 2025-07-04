
# C-Scientist

**C-Scientist** is an object-oriented Python application built with PyQt, designed to provide traders and analysts with a comprehensive platform for tracking blockchain activities, and managing cryptocurrency portfolios. By integrating real-time data analytics, interactive charts, and a user-friendly interface, C-Scientist empowers users to make informed trading decisions.

## 🚀 Features

- **Chain Activity Monitoring**: Stay updated with real-time blockchain events and transactions.
- **Portfolio Management**: Track your crypto assets, view performance metrics, and analyze portfolio distribution.
- **Interactive Charts**: Visualize market trends and portfolio performance using dynamic charts.
- **Authentication Module**: Secure user authentication to protect sensitive data.
- **News Aggregator**: Access the latest news and updates from the cryptocurrency world.
- **Chatbot Assistant**: Get instant answers to your queries with the integrated chatbot.

## 🧱 Project Structure

```
c-scientist/
├── analytics/                          # Modules for data analysis and processing
├── authentication/                     # User authentication and session management
├── charts/                             # Chart generation and visualization tools
├── chatbot/                            # Chatbot integration and response handling
├── data/                               # Data models and database interactions
├── news/                               # News fetching and aggregation
├── reviews/                            # User reviews and feedback management
├── main.py                             # Application entry point
├── requirements.txt                    # Python dependencies
├── Pipfile                             # Project dependencies and scripts
├── README.Docker.md                    # Docker setup instructions
├── LICENSE                             # GPL-2.0 License
├── Dockerfile                          # Docker build file
├── compose.yml                         # Docker params file
├── favicon.ico                         # App icon
├── AppImageBuilder.yml                 # Config for building app image
├── c-scientist-latest-x86_64.AppImage  # App Image
└── .gitignore                          # Git ignore rules
```

## 🧪 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Brantyyn/c-scientist.git
   cd c-scientist
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   python3 main.py
   ```

## 🐳 Docker Deployment

For containerized deployment, refer to the [Docker Setup Guide](README.Docker.md).

## App Image Build
**Build using:**

```bash
appimage-builder --recipe AppImageBuilder.yml
```

**To see the logs add** ```bash --log DEBUG``` **flag**

## 🛠️ Technologies Used

- **Programming Language**: Python 3
- **GUI Framework**: PyQt
- **Data Visualization**: pyqtgraph
- **APIs**: Binance, Bybit

## 🧑‍💻 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add Your Feature"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Create a Pull Request**

## 📄 License

This project is licensed under the [GNU General Public License v2.0](LICENSE).




