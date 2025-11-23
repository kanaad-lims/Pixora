from flask import Flask, request, jsonify, render_template, send_from_directory
from face import recognition
import os

app = Flask(__name__)

UPLOAD_FOLDER = "query_image"
DB_FOLDER = "uploaded_images"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DB_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('modern.html')


## Upload the folder of images.
@app.route('/upload_db', methods=['POST'])
def upload_db():
    files = request.files.getlist("files[]")

    if not files:
        return jsonify({"error": 'No files uploaded'}), 400
    
    for file in files:
        save_path = os.path.join(DB_FOLDER, file.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)


    return jsonify({
        "message": "Images uploaded successfully",
        "count": len(files)
    }), 200
    

## Upload the query image and run inference.
@app.route('/recognize', methods=['POST'])
def recognize():
    file = request.files.get("image")

    if file is None:
        return jsonify({"error": 'No image uploaded'}), 400
    
    query_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(query_path)

    try:
        #Running inference
        matched = recognition(img_path=query_path, db_path=DB_FOLDER, confidence_threshold=58)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    web_paths = []
    for full_path in matched:
        rel = full_path.replace("\\", "/")

        # Remove DB_FOLDER prefix from absolute path
        if DB_FOLDER + "/" in rel:
            rel = rel.split(DB_FOLDER + "/")[1]

        web_paths.append("/get_image/" + rel)

    return jsonify({"matched": web_paths})


# Serving the images
@app.route('/get_image/<path:filename>')
def get_image(filename):
    return send_from_directory(DB_FOLDER, filename)

if __name__ == '__main__':
    app.run(port=8000, debug=True) # debug=False if deployment la gelo tar.