from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from datetime import datetime
from Config.loader import load_table_url
from Backend.log_utils import (
    add_log_to_buffer,
    flush_logs_to_monthly_csv,
    flush_logs_to_google_sheet
)

app = Flask(__name__, template_folder="../templates", static_folder="../static")

CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log", methods=["POST"])
def log_device():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        data.setdefault("event", "unknown")
        data["server_time"] = datetime.now().isoformat()
        add_log_to_buffer(data)
        print(f"📥 LOG: {data}")
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/get-url/<table_id>")
def get_url(table_id):
    try:
        table_name = f"โต๊ะ {table_id}"
        url = load_table_url(table_name)
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/redirect/<table_id>")
def redirect_table(table_id):
    try:
        table_name = f"โต๊ะ {table_id}"
        url = load_table_url(table_name)
        return redirect(url)
    except Exception as e:
        return f"❌ ไม่พบโต๊ะ {table_id}: {e}", 404

@app.route("/flush")
def flush_logs():
    flush_logs_to_monthly_csv()
    flush_logs_to_google_sheet()
    return jsonify({"status": "flushed"})

if __name__ == "__main__":
    app.run(debug=True)
