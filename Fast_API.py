import  uvicorn


if __name__ == "__main__":
    uvicorn.run("app.app:app", host= "0.0.0.0", port=8000, reload=True) # в папке app найди файл app и в этом файле найди API которое называется app



















