# oblivion/backend/Dockerfile (Corrected)

# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev

# Install PyTorch and Torchvision first using the official index URL for CPU versions
RUN pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu

# Now, copy and install the rest of the dependencies
COPY ./oblivion/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/generated_files

# Copy the application code into the container
COPY ./oblivion/backend/app /app/app
COPY ./tools /tools

# Set the PYTHONPATH so the application can find the 'tools' module
ENV PYTHONPATH=/

# Expose the port the app runs on
EXPOSE 8000

# The command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]