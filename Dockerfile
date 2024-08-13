FROM python:3.9-slim

WORKDIR /app

# Install required dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/sengkunii/Loan_Predict_Project.git .

# Copy the pickle file into the container
COPY Model_ml.pkl /app/Model_ml.pkl

# Update pip
RUN pip install --upgrade pip

# Modify requirements.txt to remove pywin32==306
RUN sed -i '/pywin32==306/d' requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Healthcheck for Streamlit app
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "Bank_Loan_Prediction.py", "--server.port=8501", "--server.address=0.0.0.0"]
