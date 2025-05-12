FROM python:3.10-slim

# Install system dependencies including X11 and Qt requirements
RUN apt-get update && apt-get install -y     libgl1-mesa-glx     libglib2.0-0     libx11-6     libxext6     libxcb1     libxkbcommon-x11-0     libx11-xcb1     libxrender1     libxi6     libqt5gui5     && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Optional: Ensure PyQt5 is installed
RUN pip install PyQt5

# Start the GUI app
CMD ["python", "main.py"]
