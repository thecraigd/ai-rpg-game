# Use the official AWS Lambda Python 3.9 image
FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9

# Add build argument for requirements file
ARG REQUIREMENTS_FILE=requirements-function.txt

# Copy only the requirements file first
COPY ${REQUIREMENTS_FILE} ${LAMBDA_TASK_ROOT}/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy only the necessary files
COPY app ${LAMBDA_TASK_ROOT}/app/
COPY handler.py ${LAMBDA_TASK_ROOT}/

# Set the working directory
WORKDIR ${LAMBDA_TASK_ROOT}