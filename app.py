"""Small web interface for processing bookshelf text files."""
from io import BytesIO

from flask import Flask, render_template, request, send_file

from main import processar_linhas

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MiB


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    uploaded_file = request.files.get("file")
    if uploaded_file is None or not uploaded_file.filename:
        return render_template("index.html", error="Choose a text file to process."), 400

    try:
        content = uploaded_file.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return render_template(
            "index.html", error="The file must be encoded as UTF-8."
        ), 400

    results = processar_linhas(content.splitlines())
    return render_template(
        "index.html",
        results=results,
        result_text="\n".join(results),
        uploaded_name=uploaded_file.filename,
    )


@app.post("/download")
def download():
    result_text = request.form.get("result_text", "")
    data = BytesIO((result_text + ("\n" if result_text else "")).encode("utf-8"))
    data.seek(0)
    return send_file(
        data,
        mimetype="text/plain; charset=utf-8",
        as_attachment=True,
        download_name="series_completas.txt",
    )


@app.errorhandler(413)
def file_too_large(_error):
    return render_template(
        "index.html", error="The file is too large. Maximum size is 2 MiB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
