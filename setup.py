import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='gym_VacuumWorld',
     version='0.0.1',
     scripts=[] ,
     author="Brian Blais",
     author_email="bblais@bryant.edu",
     description="Vacuum World environment in OpenAI gym",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/bblais/gym-VacuumWorld",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     #install_requires=['gym'],
 )

 