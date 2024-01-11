# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower ClientManager."""
import os
import random
import threading
from abc import ABC, abstractmethod
from logging import INFO
from typing import Dict, List, Optional

from flwr.common.logger import log

import globalvariables
from ClientProxy import ClientProxy
from Criterion import Criterion


class ClientManager(ABC):
    """Abstract base class for managing Flower clients."""

    @abstractmethod
    def num_available(self) -> int:
        """Return the number of available clients.

        Returns
        -------
        num_available : int
            The number of currently available clients.
        """

    @abstractmethod
    def register(self, client: ClientProxy) -> bool:
        """Register Flower ClientProxy instance.

        Parameters
        ----------
        client : flwr.server.client_proxy.ClientProxy

        Returns
        -------
        success : bool
            Indicating if registration was successful. False if ClientProxy is
            already registered or can not be registered for any reason.
        """

    @abstractmethod
    def unregister(self, client: ClientProxy) -> None:
        """Unregister Flower ClientProxy instance.

        This method is idempotent.

        Parameters
        ----------
        client : flwr.server.client_proxy.ClientProxy
        """

    @abstractmethod
    def all(self) -> Dict[str, ClientProxy]:
        """Return all available clients."""

    @abstractmethod
    def wait_for(self, num_clients: int, timeout: int) -> bool:
        """Wait until at least `num_clients` are available."""

    @abstractmethod
    def sample(
            self,
            num_clients: int,
            min_num_clients: Optional[int] = None,
            criterion: Optional[Criterion] = None,
    ) -> List[ClientProxy]:

        """Sample a number of Flower ClientProxy instances."""



class SimpleClientManager(ClientManager):
    """Provides a pool of available clients."""


    def __init__(self) -> None:
        self.clients: Dict[str, ClientProxy] = {}
        self._cv = threading.Condition()


    def __len__(self) -> int:
        """Return the number of available clients.

        Returns
        -------
        num_available : int
            The number of currently available clients.
        """
        return len(self.clients)

    def num_available(self) -> int:
        """Return the number of available clients.

        Returns
        -------
        num_available : int
            The number of currently available clients.
        """

        return len(self)

    def wait_for(self, num_clients: int, timeout: int = 86400) -> bool:
        """Wait until at least `num_clients` are available.

        Blocks until the requested number of clients is available or until a
        timeout is reached. Current timeout default: 1 day.

        Parameters
        ----------
        num_clients : int
            The number of clients to wait for.
        timeout : int
            The time in seconds to wait for, defaults to 86400 (24h).

        Returns
        -------
        success : bool
        """
        with self._cv:
            return self._cv.wait_for(
                lambda: len(self.clients) >= num_clients, timeout=timeout
            )

    def register(self, client: ClientProxy) -> bool:
        """Register Flower ClientProxy instance.

        Parameters
        ----------
        client : flwr.server.client_proxy.ClientProxy

        Returns
        -------
        success : bool
            Indicating if registration was successful. False if ClientProxy is
            already registered or can not be registered for any reason.
        """
        if client.cid in self.clients:
            return False

        self.clients[client.cid] = client
        with self._cv:
            self._cv.notify_all()

        return True

    def unregister(self, client: ClientProxy) -> None:
        """Unregister Flower ClientProxy instance.

        This method is idempotent.

        Parameters
        ----------
        client : flwr.server.client_proxy.ClientProxy
        """
        if client.cid in self.clients:
            del self.clients[client.cid]

            with self._cv:
                self._cv.notify_all()

    def all(self) -> Dict[str, ClientProxy]:
        """Return all available clients."""
        return self.clients

    def sample(
            self,
            num_clients: int,
            min_num_clients: Optional[int] = None,
            criterion: Optional[Criterion] = None,
    ) -> List[ClientProxy]:
        """Sample a number of Flower ClientProxy instances."""
        # Define the content you want to write
        content = "This is the content I want to write to a file."

        # Define the file path
        file_path = "vilxample.txt"

        # Write the content to the file
        with open(file_path, "w") as file:
            file.write(content)
        # Block until at least num_clients are connected.
        if min_num_clients is None:
            min_num_clients = num_clients
        self.wait_for(min_num_clients)
        # Sample clients which meet the criterion
        available_cids = list(self.clients)
        if criterion is not None:
            available_cids = [
                cid for cid in available_cids if criterion.select(self.clients[cid])
            ]

        if num_clients > len(available_cids):
            log(
                INFO,
                "Sampling failed: number of available clients"
                " (%s) is less than number of requested clients (%s).",
                len(available_cids),
                num_clients,
            )
            return []

        if globalvariables.serverround < 1:
            return []

        sampled_cids = available_cids

        if not globalvariables.warmup and globalvariables.strategy == "FedNIP":
            import json
            import random
            from ChooseClient import get_top_performers_and_random_clients

            def select_clients():
                # Read tracklist.json file
                with open('tracklist.json', 'r') as file:
                    data = json.load(file)

                # Retrieve clusters and clients from data
                clusters = data['clusters']
                clients = data['clients']

                # Find the cluster with the lowest chosen count
                min_chosen_count = float('inf')
                selected_cluster = None

                for cluster in clusters:
                    chosen_count = cluster['chosen_count']
                    if chosen_count < min_chosen_count:
                        min_chosen_count = chosen_count
                        selected_cluster = cluster

                # Retrieve cluster ID, clients, and chosen count
                cluster_id = selected_cluster['id']
                cluster_client_ids = selected_cluster['clients']
                chosen_count = selected_cluster['chosen_count']

                # Update the chosen count for the selected cluster
                chosen_count += 1
                selected_cluster['chosen_count'] = chosen_count

                # Convert client IDs to strings
                cluster_clients = [str(client_id) for client_id in cluster_client_ids]

                # Save the updated data back to tracklist.json file
                with open('tracklist.json', 'w') as file:
                    json.dump(data, file, indent=2)

                return cluster_id, cluster_clients

            file_path1 = "top_performers.json"
            file_path2 = "random_performers.json"

            # Write an empty JSON object to the file
            with open(file_path1, "w") as file:
                json.dump([], file)
            # Write an empty JSON object to the file
            with open(file_path2, "w") as file:
                json.dump([], file)

            def update_client_data(file_path, client_id, accuracy):
                if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
                    with open(file_path, "r") as file:
                        existing_data = json.load(file)
                else:
                    existing_data = []

                # Define the new data to be added
                new_data = {"clientID": client_id, "accuracy": float(0.00)}

                # Append the new data to the existing data
                existing_data.append(new_data)

                # Write the updated data back to the JSON file
                with open(file_path, "w") as file:
                    json.dump(existing_data, file, indent=4)

            # Example usage

            cluster_id, cluster_clients = select_clients()
            from globalvariables import currentcluster
            currentcluster = cluster_id

            from overwritecurrentcluster import overwrite_current_cluster

            overwrite_current_cluster('globalvariables.py', cluster_id)

            print("I am in the clientmanager: Cluster ID:", cluster_id)
            print("Cluster Clients:", cluster_clients)

            with open("tracklist.json", "r") as file:
                tracklist_data = json.load(file)

            topperformers, randomperformers = get_top_performers_and_random_clients(tracklist_data, 0.1, 0.1,
                                                                                    cluster_id=cluster_id)
            for i in topperformers:
                update_client_data("top_performers.json", i, 0)

            for j in randomperformers:
                update_client_data("random_performers.json", j, 0)

            samplelist = topperformers + randomperformers
            sampled_cids = list(map(str, samplelist))
            print(sampled_cids)
            print(cluster_clients)

        return [self.clients[cid] for cid in sampled_cids]

