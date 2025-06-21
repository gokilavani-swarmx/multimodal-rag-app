# Use the official Python image from the Docker Hub
FROM python:3.12-slim

RUN apt-get update 
RUN apt-get install -y libgl1
RUN apt-get install -y pkg-config libhdf5-dev
RUN apt-get install -y libglib2.0-dev

RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service in the background and pull the required model
RUN ollama start & \
    sleep 5 && \
    ollama pull llama3.2:latest \
    ollama pull llava:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir .

# Expose the port the app runs on
EXPOSE 8001

# CMD ["streamlit", "run", "app/streamlit_app.py", "&&", "streamlit", "run", "streamlit_app"]

CMD ["sh", "-c", "ollama serve & python ./src/api/main.py & streamlit run ./src/app/streamlit_app.py --server.port 8001" ]