#Install before continuing:

uwsgi (server),

poetry (dependecy manager),

pyenv (python version manager).

#Set a ve python version:

poetry env use C:\Users\yray4\.pyenv\pyenv-win\versions\3.8.10

#Activate ve:
venv\Scripts\activate

#Run wsgi server:

waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"

curl -v -XGET http://localhost:5000/api/v1/hello-world-15


#For testing:

coverage run app_tests.py

coverage report

