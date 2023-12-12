import torch

def check_gpu(model):
    if torch.cuda.is_available():
        print("CUDA (GPU support) is available.")
        print("Model is on CUDA:", next(model.parameters()).is_cuda)
    else:
        print("CUDA is not available. The model is on the CPU.")