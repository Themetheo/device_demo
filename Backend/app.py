from flask import Flask, request, jsonify, redirect
from datetime import datetime
from Config.loader import load_table_url

app = Flask(__name__)
logs = []

@app.route("/log", methods=["POST"])
def log_device():
    data = request.json
    data["server_time"] = datetime.now().isoformat()
    logs.append(data)
    print(f"📥 LOG: {data}")
    return jsonify({"status": "ok"})

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

@app.route("/logs")
def show_logs():
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True)
