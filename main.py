from website import create_app

app = create_app()

if __name__ == '__main__':  # run the web server only if run this file
    app.run(debug=True )  # every time we change our code it will re run webserver
