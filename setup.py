from setuptools import setup, find_packages

setup(
    name="evolutionapi_client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "Pillow",    # O nome do pacote é Pillow (o import é PIL)
        "PyMuPDF",   # O nome do pacote é PyMuPDF (o import é fitz)
    ],
)