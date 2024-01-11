import csv
import numpy as np
from matplotlib import pyplot as plt
from pyemd import emd_samples
from sklearn.cluster import KMeans
from collections import Counter

def calculateEMD():
    file = open(f"./partition-reports/clientsplittrain.csv", "r")
    data = list(csv.reader(file, delimiter=","))
    file.close()

    # Extract class labels from the second row
    class_labels = data[1][1:-1]
    print(f'class_labels {class_labels}')

    # Initialize an empty dictionary to store the results
    result_dict = {}

    # Iterate through the data starting from the third row
    for row in data[2:]:
        client_name = row[0].strip()  # Remove leading/trailing whitespace from the client name
        client_values = [float(val) * float(row[-1]) for val in row[1:-1]]  # Multiply each value by the total amount
        client_dict = {label: int(value) for label, value in zip(class_labels, client_values)}
        result_dict[client_name] = client_dict

    print(result_dict)

    # Compute the EMD distances between clients
    clients = list(result_dict.keys())
    n_clients = len(clients)

    emd_distances = np.zeros((n_clients, n_clients))

    print(emd_distances)

    # Create a dictionary to store the data distributions
    data_distributions = {}

    # Iterate through the clients and populate the data distributions dictionary
    for client in clients:
        data_distributions[client] = list(result_dict[client].values())

    print(f"data distr {data_distributions}")

    # Compute the EMD distances using the Earth Mover's Distance
    for i in range(n_clients):
        for j in range(n_clients):
            emd_distances[i, j] = emd_samples(data_distributions[clients[i]], data_distributions[clients[j]])

    # Initialize variables for elbow method
    max_clusters = min(n_clients, n_clients // 3)  # Maximum number of clusters to consider
    distortions = []

    # Perform K-means clustering for different numbers of clusters
    for n_clusters in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(emd_distances)
        cluster_labels = kmeans.predict(emd_distances)
        cluster_counts = Counter(cluster_labels)
        single_client_clusters = [cluster for cluster, count in cluster_counts.items() if count == 1]
        for single_cluster in single_client_clusters:
            single_cluster_idx = np.where(cluster_labels == single_cluster)[0][0]
            distances_to_other_clusters = emd_distances[single_cluster_idx]
            nearest_cluster = np.argmin(distances_to_other_clusters)
            cluster_labels[single_cluster_idx] = nearest_cluster

        distortions.append(kmeans.inertia_)

    # Find the optimal number of clusters using the elbow method
    distortions = np.array(distortions)
    distortion_diff = np.diff(distortions)
    elbow_index = np.argmax(distortion_diff) + 1  # Index of the elbow point
    optimal_n_clusters = min(n_clients, elbow_index + 1)  # Adjust this based on the elbow curve

    # Apply K-means clustering to the EMD distances with the optimal number of clusters
    kmeans = KMeans(n_clusters=optimal_n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(emd_distances)

    print(f"client labels {cluster_labels}")

        # Assign cluster labels to clients
    client_clusters = {client: cluster for client, cluster in zip(clients, cluster_labels)}
    print(f"client clusters {client_clusters}" )

    # Convert client_clusters dictionary to a list of tuples with numeric IDs
    client_clusters_list = [(int(client_id.split()[-1]), group) for client_id, group in client_clusters.items()]

    # Define the output CSV file path
    output_file = f'client_clusters.csv'

    # Write the client_clusters data to the CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Clientid', 'Group'])  # Write the header
        writer.writerows(client_clusters_list)

    print(f"Client clusters data has been saved to '{output_file}'")
