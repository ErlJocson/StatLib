import setuptools

setuptools.setup(
    name="StatLib",               
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_required=[
        'pandas',
        'numpy',
        'scipy',
        'seabord',
        'matplotlib'
    ]
)