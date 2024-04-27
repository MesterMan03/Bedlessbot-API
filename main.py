
import logging

from flask import Flask, jsonify, request

from st import ST

import binascii

app = Flask(__name__)

st = ST("qa_pairs.txt")

# Read secret data from file
with open("secret", "rb") as f:
    # read from hex
    shared_secret = binascii.unhexlify(f.read())

# Configure logging
logging.basicConfig(filename="error.log", level=logging.ERROR)
logging.basicConfig(filename="info.log", level=logging.INFO)


@app.route("/", methods=["POST"])
def root():
    global shared_secret

    # Check for secret key in Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header is None or auth_header != shared_secret:
        ip_address = request.remote_addr
        logging.error(f"Authorization header missing from IP address: {ip_address}")
        return "Authorization header missing or invalid", 401

    # Retrieve data from the request body
    data = request.get_json()

    if "text" in data:
        text = data.get("text", "")

        # Run the search
        try:
            answer = st.search(text)
            if answer == None:
                return jsonify({"answer": "No answer found"}), 204
            if answer:
                return jsonify({"answer": answer[1]})
        except Exception as e:

            ip_address = request.remote_addr
            logging.error(
                f"Failed to give answer to IP address: {ip_address}. Error: {str(e)}"
            )
            return "", 500

    return "", 418


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=False, port=8912)
