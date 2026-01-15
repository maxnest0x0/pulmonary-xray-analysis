# Pulmonary X-ray Analysis
Lung X-ray image analysis system for pathology detection and lesion visualization

## Installation for Debian 13
### Make sure Git LFS is installed or install it
It is required to download the model file automatically.
```sh
$ sudo apt update
$ sudo apt install git-lfs
$ git lfs install
```

### Clone the repository
```sh
$ git clone https://github.com/maxnest0x0/pulmonary-xray-analysis.git
$ cd pulmonary-xray-analysis
```

### Set up Python environment
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### Install dependencies
You may want to use the CPU version of PyTorch to speed up installation and reduce dependency size.
To install the full version, skip the first command.
```sh
$ pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
$ pip install --requirement requirements.txt
```

### Run the program
This will start the service at http://localhost:8000/.
CUDA will be used if possible, but the CPU also does the job quickly enough.
```sh
$ python main.py
```

## Usage
### Web page
For users, we host the web page at http://176.222.54.175:8000/.

### API
For developers, we provide an API endpoint.
API documentation is available via [Swagger UI](http://176.222.54.175:8000/docs) and [Redoc](http://176.222.54.175:8000/redoc).

## Screencast
https://github.com/user-attachments/assets/fdc5891e-56bb-44ec-b975-c4dec183c8f4
