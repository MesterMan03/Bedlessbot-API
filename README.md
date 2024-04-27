# Bedlessbot-API

Bedlessbot-API is an API that handles all machine-learning related stuff for [Bedlessbot](https://github.com/MesterMan03/Bedlessbot)

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/MesterMan03/Bedlessbot-API.git
cd Bedlessbot-API
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the required packages**:

```bash
pip install -r requirements.txt
```

4. **Configure the secret**:

You need to create a `secret` file of arbitrary data represented as hex which the clients will have to provide in the Authorization header. You can use the following command to generate a random secret:

```bash
python -c "import secrets; print(secrets.token_hex(64))"
```

This will generate a 64-byte hex string which you can use as the secret. Save this string in a file named `secret` in the root directory of the project. You may use more or less bytes as needed.

## Usage

-   **Start the API**:

```bash
python main.py
```

-   **API Endpoints**:
    -   POST `/`: The main endpoint for the API. This endpoint requires the `Authorization` header with the secret as the value. The body is expected to be a JSON object with the following keys:
        -   `text?`: When this is provided, a sentence transformer will be executed on the text and the result will be returned. The training file is `qa_pairs.txt`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions, feel free to open an issue or submit a pull request.
