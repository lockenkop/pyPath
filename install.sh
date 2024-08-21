
# make sure we are in a virtual environment if not create it and activate it
if [ -z "$VIRTUAL_ENV" ]; then
    python3 -m venv venv
    source venv/bin/activate
fi

source .venv/bin/activate

pip install -e .
