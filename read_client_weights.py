
import torch



def read_client_weights(client_id):
    file_name = f"client{client_id}_data.pth"
    print(client_id)
    try:
        weights = torch.load(file_name)
        return weights
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Assuming all weights have been collected.")
        return None


def aggregate_weights():
    # Initialize accumulator
    avg_weights = None
    client_id = 0

    while True:
        weights = read_client_weights(client_id)
        if weights is not None:
            if avg_weights is None:
                 avg_weights = weights
            else:
                # Add client weights to accumulator
                for i, key in enumerate(avg_weights):
                    avg_weights[i] += weights[i]
        else:
            print(f"All weights have been collected from {client_id} clients. Stopping aggregation.")
            break

        client_id += 1


    # Compute average
    if avg_weights is not None:
        num_clients = client_id  # Number of clients counted
        for i, key in enumerate(avg_weights):
            avg_weights[i] /= num_clients

    return avg_weights

# Example usage
average_weights = aggregate_weights()
#print(average_weights)

