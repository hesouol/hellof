import setuptools

setuptools.setup(
    name="hellofresh",
    version="0.1.0",
    author="Henrique Oliveira",
    author_email="hesouol@gmail.com",
    description="HelloFresh - Recipes ETL",
    long_description="HelloFresh - Recipes ETL",
    url="https://github.com/hesouol/hellofresh",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
