#  GGUF Serve

AIO docker image to serve any GGUF model as a LangServe endpoint

## Usage

Running ggufserve will expose the desired model as a REST endpoint using LangServe in port 8000. 

Ways to consume it can be found in the [client jupyter notebook](https://github.com/ADRIANPGA/ggufserve/blob/main/client.ipynb)

### Pull and run

Check [dockerhub repo](https://hub.docker.com/repository/docker/adrianpga/ggufserve/general) to find available versions of the image and run it as shown in [run folder](https://github.com/ADRIANPGA/ggufserve/tree/main/run)

### Build and run

```sh
 docker build . -t ggufserve:{tag}

 docker-compose up -d ### Docker compose way

  docker run -d ggufserve:1.0.0-Llama-3-8B-Instruct-Q4 \ 
   --port 8000:8000 --name local-llm \
   -e TEMPERATURE=0.9 \
   --gpus all ### Docker run way
 ```

 ### Customization

 Every model parameter can be modified using environment variables injection as seen in the examples.

 All environment variables are:
  - N_GPU_LAYERS
    - Default: 16
  - N_GPU_BATCH_SIZE
    - Default: 2048
  - N_CTX
    - Default: 8192
  - TEMPERATURE
    - Default: 0.75
  - TOP_P
    - Default: 1.0
  - MAX_TOKENS
    - Default: 750
  - USE_MLOCK
    - Default: True
  - VERBOSE
    - Default: True


## Details
Starting with Ubuntu 22 with CUDA, Python and all project pip dependencies are installed, where llama-cpp-python is compiled with CUDA support. After that, the server.py is run launching a LangServe exposing the model in port 8000, alongside with a openapi specification in /docs endpoint.

> [!NOTE]  
> Size could probably be reduced starting from python and just installing cuda afterwards, but for [errors](https://stackoverflow.com/questions/76340960/cuda-to-docker-container)] this path is faster in terms of development time.

```sh
### If you want to check CUDA is correctly installed
export PATH=/usr/local/cuda/bin:$PATH
nvcc --version
```
