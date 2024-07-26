from setuptools import setup


def grab_version():
    with open("fish/version.py") as file:
        line = file.readline().rstrip()
        version = line.split(" = ")[1].replace('"', "")
    return version


setup(
    name="fish",
    version=grab_version(),
    author="Oran Looney",
    author_email="olooney@gmail.com",
    description="Example FastAPI Model Server",
    python_requires=">=3.11",
    packages=["fish"],
    package_data={
        "fish": ["data/*"],
    },
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
        ],
    },
    scripts=["scripts/run_server.py"],
)
