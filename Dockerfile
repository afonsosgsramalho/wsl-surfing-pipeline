FROM python:3.11

#set directory for the app
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

#install python requirements
RUN pip install --no-cache-dir -r requirements.txt

#copy all the files to the container
COPY . .

#define the port number the container should expose
EXPOSE 8501

#run the python command to initialize the app
ENTRYPOINT ["streamlit", "run", "streamlit_app/index.py", "--server.port=8501", "--server.address=0.0.0.0"]
