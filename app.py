from flask import Flask, request, send_file, abort
import flask_cors
from rembg import remove, new_session
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure API_TOKEN is set in environment variables
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set in the environment variables.")

# Initialize Flask app
app = Flask(__name__)
flask_cors.CORS(app, resources={r"/api/v1/*": {"origins": "*"}})  # Enable CORS for all /api/v1/* endpoints
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Limit upload size to 10MB

model_sessions = {}  # Dictionary to store rembg sessions for different models

def get_session(model_name):
    """
    Get the rembg session for the specified model. If the model is not loaded, it will be loaded and stored in the model_sessions dictionary.
    Args:    model_name (str): The name of the model to use. Can be "u2net", "human", or "illustration".
    Returns:   The rembg session for the specified model.
    """
    if model_name not in model_sessions:
        model_sessions[model_name] = new_session(model_name)
    return model_sessions[model_name]

@app.route("/")
def index():
    return "Background Remover API is running. Use POST /api/v1/removebg with your token to remove backgrounds from images ❤️."

@app.route("/api/v1/removebg", methods=["POST"])
def remove_bg():
    """
    Endpoint to remove background from an image.

    Expects a multipart/form-data request with the following fields:
    - image: The image file to process.
    - model: (optional) The model to use for background removal. 
             Can be one of "u2net", "human", or "illustration". 
             Defaults to "u2net" if not provided.
    Returns:
    - A PNG image with the background removed.
    """

    token = request.headers.get("Authorization")
    if token != f"Bearer {API_TOKEN}":
        abort(401, description=f"Unauthorized")

    # get image
    file = request.files.get('image')
    if file is None:
        abort(400, description="Missing 'image' file field")

    # model sessions
    model_map = {
        "default": "u2net",
        "person": "u2net_human_seg",
        "illustration": "isnet-anime",
    }

    # user selected model
    model = request.form.get("model", "default").lower()

    # actaul rembg model
    model_name = model_map.get(model, "u2net")  # default to "u2net" if model is not recognized

    # get session | fallback ( use default )
    session = get_session(model_name)

    # open image with PIL
    try:
        image = Image.open(file.stream)
    except Exception as e:
        abort(400, description=f"Error opening image: {str(e)}")

    # remove background
    output_image = remove(image, session=session)

    # create a bytes buffer to hold the output image
    buffer = io.BytesIO()

    # save the output image to the buffer in PNG format
    output_image.save(buffer, format="PNG")
    buffer.seek(0)  # set the buffer position to the beginning

    return send_file(buffer, mimetype="image/png")

if __name__ == "__main__":
    app.run()
