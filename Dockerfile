# Use a lightweight Conda-based image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file for Conda dependencies
COPY environment.yml .

# Install Conda dependencies
RUN conda env create -f environment.yml && conda clean -a

# Activate the environment and ensure it works in subsequent layers
RUN echo "source activate pyocc" > ~/.bashrc
ENV PATH=/opt/conda/envs/pyocc/bin:$PATH

# Copy the requirements.txt file for pip dependencies
COPY requirements.txt .

# Install pip dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
