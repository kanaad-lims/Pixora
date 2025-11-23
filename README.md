# Pixora

<p align="center">

  <!-- Library Badges -->
  <img src="https://img.shields.io/badge/DeepFace-0.0.95-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/TensorFlow-2.20.0-orange?style=for-the-badge&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-2.3.3-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/OpenCV-4.9.0-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

  <!-- Repo Badges -->
  <br>
  <img src="https://img.shields.io/github/stars/kanaad-lims/Pixora?style=for-the-badge" />
  <img src="https://img.shields.io/github/forks/kanaad-lims/Pixora?style=for-the-badge" />

  <!-- Logo -->
  <br><br>
  
</p>
<p align="center">
<img src="https://github.com/kanaad-lims/Pixora/blob/876f2ea4b5952911dcfafdb443c25692fa5665d4/pixora_logo.png" 
       alt="Pixora Logo" width="300">
</p>

# Overview
Pixora is a lightweight, fast, and accurate face-recognition tool that lets you upload a folder of images and instantly match faces through a clean, browser-based interface.
The user can upload a folder of images along with a query image like a selfie, based on which the app returns all the matching indivisual as well as grouped photos.
The photos are easily downloadable from the app.

<p align="center">
  <img src="https://github.com/kanaad-lims/Pixora/blob/616936eca553cc84353f979e5eeea1293d0c76fd/Banners/pixora_UI.png" alt="Centered image" width="600">
</p>

The current version of Pixora runs on CPU.

---

# Features
- Supports images with multiple formats (.png, .jpg, .jpeg)
- Supports subfolder structures
- Automatic face detection and extraction
- User Friendly interface
- Dynamic image serving
- Completely free and Open source.

---

# Tech Stack
- Python (recommended version 3.10, can work with 3.13)
- Tensorflow (version 2.20 for compatibility)
- Flask
- DeepFace library
- HTML
- JavaScript

---

# Before you start
- This project uses DeepFace library for Image recognition task.
- It is recommended to install DeepFace library first, and inside a virtual environment.
- For a detailed installation guide click [here.](https://viso.ai/computer-vision/deepface)
- Head over to DeepFace [repository](https://github.com/serengil/deepface?tab=readme-ov-file) by [Sefik Ilkin Serengil](https://github.com/serengil) for further information.

---

# Pixora Installation
**1. Clone the repository**:
```
git clone https://github.com/kanaad-lims/Pixora.git
cd pixora
```
**2. (Optional) Create a virtual environment.**
- Recommended for users with python version > 3.10 though python version 3.13 is also supported.
- DeepFace requires Tensorflow installation. TF version 2.20 runs on python 3.13 with CPU acceleration.

```
python -m venv pixora-env
```
else create a venv for specific python version.
```
-- E.g python==3.10
python3.10 -m venv pixora-env
```
**3. Activate the environment.**
```
pixora-env\Scripts\activate
```
**4. Install dependencies.**
- It is expected to install deepface library into the venv first before installing requirements.
- Hence, `requirements.txt` does not contain deepface and tensorflow installation.

```
pip install -r requirements.txt
```
**5. Run the App.**
- After successful installation of the requirements and verification of versions, run the app in the terminal
```
python app.py
```
**6. Open in Browser.**
- `http://127.0.0.1:8000/`
- You can change the port and host as per your choice.

---

# How Pixora Works

Pixora performs face recognition through a simple but well-organized pipeline that connects the browser, the Flask backend, and the DeepFace library. Below is a step-by-step breakdown of the entire workflow.

---

### 1. User Uploads a Folder of Images (Database)
- The user selects a folder using a directory-upload input.
- The browser sends **every image file** in that folder (including those inside subfolders) to `/upload_db` as `files[]`.
- **Pixora Backend Action:**
  - Receives all files.
  - Recreates the folder structure automatically.
  - Saves everything inside:
    ```text
    uploaded_images/
    ```
- This folder becomes the **face database** DeepFace will search in.

---

### 2. User Uploads a Query Image
- The user selects a single image that contains the face to be recognized.
- Pixora shows an **instant preview** of the uploaded query image.
- When submitted, Pixora saves the image into:
    ```text
    query_image/
    ```
- This image will be compared against all images in the database.

---

### 3. Pixora Starts Recognition
When the user clicks **“Start Recognition”**, the frontend sends the query image via `POST /recognize`.

The backend then executes the following logic:

1. **Load Image:** Loads the saved query image.
2. **Call Function:** Calls the recognition function:
    ```python
    matched = recognition(img_path, db_path, confidence_threshold)
    ```
3. **DeepFace Processing:**
    - **Face Detection:** Detects the face within the query image.
    - **Embedding Extraction:** A Convolutional Neural Network (CNN) encodes the face features.
    - **Comparison:** Performs a 1-to-N comparison against every image in `uploaded_images/`.
    - **Scoring:** Computes similarity and confidence scores.
    - **Filtering:** Returns all images whose embeddings match above the threshold.

**Output:** A list of *absolute file paths* pointing to matched images.

---

### 4. Pixora Converts Absolute Paths to Web-Accessible URLs
DeepFace outputs absolute disk paths which cannot be sent directly to the browser.

- **Raw Output (Absolute):**
    ```bash
    D:/Pixora/uploaded_images/person1/img1.jpg
    ```
- **Pixora Conversion (Relative):**
    ```bash
    /get_image/person1/img1.jpg
    ```

This conversion allows the browser to fetch matched images safely from the server.

---

### 5. Frontend Displays the Matched Images
Each URL returned by the backend is added to the UI’s results grid.

**The Flow:**
1. Pixora sends a `GET` request to `/get_image/<path>`.
2. Flask serves the image file directly from `uploaded_images/`.
3. The browser displays each match as a **240 × 240** tile.

> **Result:** This produces a clean, grid-based face recognition results interface.

---

### 6. Full Processing Loop Summary

1. **Upload folder** → stored in `uploaded_images/`
2. **Upload query image** → stored in `query_image/`
3. **DeepFace** compares embeddings across the entire uploaded dataset.
4. **Matched image paths** are converted to browser-friendly URLs.
5. **Frontend** displays matches in a clean responsive grid.

---

## ⚠️ Warning
- Pixora is designed for small to medium datasets.
- Inference time depends on the number of images (due to 1 to N matching) and also on the detection_backend.
- By default the detection_backend is set to `opencv` for fast inferencing.
- Some limitations in matched images can be observed. They are largely dependent on threshold value as well as detection_backend.

---

# Licence
MIT Licence

# Author
Kanaad M. Limaye
