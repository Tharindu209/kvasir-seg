# KVASIR Segmentation Prediction API

This project provides an API for segmentation prediction using the KVASIR dataset. It utilizes a U-Net model with a ResNet-50 encoder for performing segmentation tasks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

Follow these steps to install and set up the project:

```sh
# Clone the repository
git clone https://github.com/yourusername/kvasir-seg.git
cd kvasir-seg
```

```sh
# Create a virtual environment
python -m venv env

# Activate the virtual environment
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

```sh
# Install the required dependencies
pip install -r requirements.txt
```

## Notebook: kvasir_segmentation.ipynb

Inside this repository, there is a Jupyter Notebook named `kvasir_segmentation.ipynb` that demonstrates how to train and evaluate the segmentation model using PyTorch. After training, the best model checkpoint is saved as `best_model.pth`, which can be added to the `app/models` folder for deployment.

## Usage

To start the FastAPI server, run the following command:

1. Ensure you have a virtual environment activated:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

2. Install the required dependencies
    ```sh
    pip install -r requirements.txt
    ```

3. Run the server with Uvicorn:
    ```sh
    uvicorn app.main:app --reload
    ```

4. You can then access the API at `http://127.0.0.1:8000`.

### Example

To get a welcome message, you can send a GET request to the root endpoint:

```sh
curl -X GET "http://127.0.0.1:8000/"
```

## API Endpoints

| Method | Endpoint                         | Description                                   |
|------- |----------------------------------|-----------------------------------------------|
| GET    | /                                | Read Root                                     |
| POST   | /auth/signup                     | Create new user                               |
| POST   | /auth/login                      | Create access and refresh tokens for user     |
| POST   | /auth/logout                     | Logout user                                   |
| GET    | /auth/me                         | Get details of currently logged in user       |
| POST   | /image/upload                    | Upload Image                                  |
| DELETE | /image/{image_id}                | Delete Image                                  |
| GET    | /image/                          | List Images                                   |
| GET    | /image/original/{image_id}       | Get Original Image                            |
| GET    | /image/segmented/{image_id}      | Get Segmented Image                           |
| POST   | /segmentation/process/{image_id} | Process Image                                 |


## Features

- Load and configure a U-Net segmentation model with a ResNet-50 encoder.
- API endpoints for segmentation prediction.
- CORS support for specified origins.
- JWT token-based authentication for secure endpoints
- Jupyter Notebook **kvasir_segmentation.ipynb** for model training and evaluation

## Tech Stack

- FastAPI
- PyTorch
- Supabase

## Contributing
We welcome contributions to the project. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request.

## License
This project is licensed under the MIT License 

## Contact
Tharindu Damruwan - tharindudamruwan23@gmail.com

Project Link: https://github.com/Tharindu209/kvasir-seg.git