# For easing the cuda install we start from cuda image and install python after
ARG CUDA_IMAGE="12.1.1-devel-ubuntu22.04"
FROM nvidia/cuda:${CUDA_IMAGE}

# We need to set the host to 0.0.0.0 to allow outside access
ENV HOST 0.0.0.0

# Install python, pip and other dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git build-essential python3 python3-pip gcc wget 
RUN apt-get install -y ocl-icd-opencl-dev opencl-headers clinfo libclblast-dev libopenblas-dev

# setting build related env vars
ENV CUDA_DOCKER_ARCH=all
ENV LLAMA_CUDA=1

# Set the working directory
WORKDIR /

# Every needed package is installed from requirements.txt
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Install llama-cpp-python (build with cuda)
RUN CMAKE_ARGS="-DLLAMA_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=all-major" pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade --verbose


# Set the working directory
WORKDIR /app

# Copy needed files
COPY ./model/model.gguf /app/model.gguf
COPY ./code/server.py /app/server.py

# Port to expose to run the server
EXPOSE 8000

# Web server script is run when the container is started
CMD ["python3", "server.py"]