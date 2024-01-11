import torch
import globalvariables
from extractamountofcsv import extract_amount_from_csv

def calculate_average_weights():
    total_weights = None
    total_samples = 0

    for client_idx in range(globalvariables.num_clients + 1):
        try:
            client_data_path = f'client{client_idx}_data.pth'
            client_weights = torch.load(client_data_path)

            # Load the corresponding amount of data for the client
            client_amount = extract_amount_from_csv()[client_idx]

            # Apply weighting to the client's weights
            weighted_client_weights = [torch.tensor(w) * client_amount for w in client_weights]

            if total_weights is None:
                total_weights = weighted_client_weights
            else:
                total_weights = [total_weights[i] + weighted_client_weights[i] for i in range(len(total_weights))]

            total_samples += client_amount

        except FileNotFoundError:
            break

    # Normalize by the total amount of data
    average_weights = [w / total_samples for w in total_weights]

    return average_weights
