About
-----

> "Teach a man to fish, and you feed him for a day. Teach a data scientist to
> wrap a a model in a JSON REST API endpoint inside a Docker container, and you
> feed them for life."

Install
-------

Clone the git repo:

    git clone https://github.com/olooney/fish.git

This project provides a python package `fish`. Before installing it,
you should create an isolated environment, using conda or venv. For example:

    conda create -n fish python=3.11.3
    conda activate fish

For development, install `fish` in editable mode:

    pip install -e .[dev]

The `[dev]` will install additional dependencies needed only for development.
To install it normally, use:

    pip install .

The above will install the package with recent, up-to-date versions of all
dependences, which should work in most cases. However, if you are having
version compabability problems, you can run:

    pip install -r requirements.txt

to install all dependencies on the exact versions used for development.


Build and Test
--------------

In the root `fish` directory, run:
    
    pytest

To run the full suite of unit tests. Please do not submit a pull request
until all unit tests are passing.

Please also run:

    black .

To automatically force all `.py` files to adhere to the strict black style
guides.

Finally, the build the wheel for the package, run:

    python setup.py bdist_wheel

This will create a `.whl` file in the `dist` directory, which you can then
distribute as you see fit.


Running the Local Server
------------------------

To run the local test server, run:

    python scripts/run_server.py

This will start a local uvicorn instance serving on `localhost:8000` by
default; the port can be controlled by the PORT environment variable.

Visit `http://localhost:8000/ping` to check if the server has started
correctly.

Visit `http://localhost:8000/docs` for the interactive swagger docs.


Building and Running in Docker
------------------------------

Ensure you have Docker installed, and in the root project directory run:

    docker build -t olooney/fish .

On my machine this builds a 232 MB image, which is fairly light.

If the build was successful, you can run the image as a server with:

    docker run --rm -e OPENAI_API_KEY=secret -p 8000:8000 olooney/fish

You may also find it useful (for debugging) to run a shell inside the container:

    docker run --rm -it olooney/fish bash



Hackathon Backlog
-----------------

- [X] model class
- [X] test model
- [X] unit tests
- [X] add API
- [X] pydantic types
- [X] unit tests
- [X] Dockerfile


Backlog
-------

- [ ] Authentication?
- [ ] DEV/PROD flags?
- [X] Bulk Inference?
- [ ] CLI?
- [ ] Logging?

