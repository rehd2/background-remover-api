# Background Remover API

A simple Flask API that removes image backgrounds using AI (rembg + ONNX).

---

## Features

- Remove image backgrounds
- Multiple models (default, person, illustration)
- Returns transparent PNG
- Token-protected API
- Easy deployment (Render / Railway)

---

## Tech Stack

- Flask
- rembg
- ONNX Runtime
- Pillow
- Flask-CORS

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API token

Create a `.env` file in the `background_remover` directory and add your API token

```env
API_TOKEN=your_secure_token_here
```

### 3. Run the app

```bash
python app.py
```

### 4. API Endpoint

- URL: `http://localhost:5000/api/v1/removebg`
- Method: POST
- Form Data:
  - `image`: (file) The image to process
  - `model`: (string, optional) Model to use (`default`, `person`, `illustration`)
- Headers:
  - `Authorization: Bearer <your_secure_token_here>`
- Response: Processed image (PNG with transparent background)

## Example cURL Request

```bash
curl -X POST http://localhost:5000/api/v1/removebg \
  -H "Authorization: Bearer your_secure_token_here" \
  -F "image=@/path/to/your/image.jpg" \
  -F "model=default" \
  --output output.png
```
