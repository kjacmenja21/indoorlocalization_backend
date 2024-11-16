#!/bin/sh

# Start the FastAPI application using Gunicorn
exec uvicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:4000 app.main:app