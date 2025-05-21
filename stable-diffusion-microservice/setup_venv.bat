@echo off
REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies for both server and gateway
pip install -r requirements.server.txt -r requirements.gateway.txt

REM Generate gRPC code
python generate_grpc.py

echo Setup complete! Virtual environment is activated and dependencies are installed.