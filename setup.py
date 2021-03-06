from distutils.core import setup

# TODO Synchronize version with __init__.py of pytheas package.

setup(
    name = "Pytheas",
    version = "0.2.1",
    author = "Chad Estioco",
    author_email = "chadestioco@gmail.com",
    url = "https://github.com/skytreader/pytheas",
    packages = ["pytheas",],
    install_requires = ["gevent", "greenlet"],
    license = "MIT",
    description = "Framework for a fetch-and-send daemon.",
)
