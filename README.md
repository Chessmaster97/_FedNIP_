# Federated Learning on Non-IID Data with Local-drift Decoupling and Correction
Code for paper - **[Federated Learning on Non-IID Data with Local-drift Decoupling and Correction]**

We provide code to run FedDC, FedAvg, 
[FedDyn](https://openreview.net/pdf?id=B7v4QMR6Z9w), 
[Scaffold](https://openreview.net/pdf?id=B7v4QMR6Z9w), and [FedProx](https://arxiv.org/abs/1812.06127) methods.


## Prerequisite
* Install the libraries listed in requirements.txt
    ```
    pip install -r requirements.txt
    ```

## Datasets preparation
**We give datasets for the benchmark, including CIFAR10, CIFAR100, MNIST, EMNIST-L and the synthetic dataset.**




You can obtain the datasets when you first time run the code on CIFAR10, CIFAR100, MNIST, synthetic datasets.
EMNIST needs to be downloaded from this [link](https://www.nist.gov/itl/products-and-services/emnist-dataset).


For example, you can follow the following steps to run the experiments:

```python example_code_mnist.py```
```python example_code_cifar10.py```
```python example_code_cifar100.py```

1. Run the following script to run experiments on the MNIST dataset for all above methods:
    ```
    python example_code_mnist.py
    ```
2. Run the following script to run experiments on CIFAR10 for all above methods:
    ```
    python example_code_cifar10.py
    ```
3. Run the following script to run experiments on CIFAR100 for all above methods:
    ```
    python example_code_cifar10.py
