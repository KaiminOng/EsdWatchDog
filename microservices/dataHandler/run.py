from dataHandler import app


if __name__ == '__main__':
    print("Data Handler service is running...")
    app.run(host='0.0.0.0', port=5000)