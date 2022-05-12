import torch
DEVICE = torch.device("cuda:0")
print("Using device:", DEVICE)
device = DEVICE  # At least one of the modules expects this name.

if torch.cuda.is_available():
    print("cuda available")
else:
    print ("cuda not available")
    