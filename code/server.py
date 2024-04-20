import os

from langchain_community.llms import LlamaCpp

from fastapi import FastAPI
from langserve import add_routes

# Get n_gpu_layers and n_batch from os variables if present or use default values
n_gpu_layers = int(os.getenv("N_GPU_LAYERS", 16))
n_gpu_batch_size = int(os.getenv("N_GPU_BATCH_SIZE", 1))
n_ctx = int(os.getenv("N_CTX", 8192))
temperature = float(os.getenv("TEMPERATURE", 0.75))
top_p = float(os.getenv("TOP_P", 1.0))
max_tokens = int(os.getenv("MAX_TOKENS", 750))
use_mlock = bool(os.getenv("USE_MLOCK", True))
verbose = bool(os.getenv("VERBOSE", True))

# Print a JSON variable of mapped environment variables
print(
    {
        "N_GPU_LAYERS": n_gpu_layers,
        "N_GPU_BATCH_SIZE": n_gpu_batch_size,
        "N_CTX": n_ctx,
        "TEMPERATURE": temperature,
        "TOP_P": top_p,
        "MAX_TOKENS": max_tokens,
        "USE_MLOCK": use_mlock,
        "VERBOSE": verbose
    }
)

app = FastAPI(
    title="TechChallenge 2024 GGUF Backup server",
    version="1.0",
    description="Langserve server for GGUF model",
)

llm = LlamaCpp(
    model_path="model.gguf",
    temperature=temperature,
    n_ctx=n_ctx,
    use_mlock=use_mlock,
    max_tokens=max_tokens,
    top_p=top_p,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_gpu_batch_size,
    verbose=verbose
)

add_routes(
    app,
    llm
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)