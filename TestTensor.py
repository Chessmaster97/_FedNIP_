import torch

# Load the data
loaded_data = torch.load('client0_data.pth')

# Check the type
data_type = type(loaded_data)
print(f"The type of loaded data is: {data_type}")

trainloader = torch.load(f'trainloader3.pth')
print(len(trainloader))