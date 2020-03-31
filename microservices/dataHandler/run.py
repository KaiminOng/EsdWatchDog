from dataHandler import app


if __name__ == '__main__':
    print("Data Handler service is running...")
    app.run(host='esdwatchdog.com', port=5000, debug=True)