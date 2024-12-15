from flask import Flask, request, render_template, jsonify
from markitdown import MarkItDown
import os

app = Flask(__name__)
markitdown = MarkItDown()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "no file provided"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "no file selected"}), 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        
        # todo: convert preserving images - check markitdown
        try:
            result = markitdown.convert(file_path)
            markdown_content = result.text_content
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.remove(file_path)

        return render_template("index.html", markdown_content=markdown_content)

    return render_template("index.html", markdown_content="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
