from app import app


def run_server():
    print("Start server...")
    app.run(host='0.0.0.0', port=9091, debug=True)


if __name__ == "__main__":
    run_server()
