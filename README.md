# my_flask_app
my repo for my application on flask


### Build container

> docker build -t my_flask_app:v0.1 .


### Run docker container

> docker run -d -ti --name my_flask_app -p 5000:5000 -v $PWD:/my_flask_app sivin79/my_flask_app

`$PWD folder with config`

> docker run -d -ti --name my_flask_app -p 5000:5000 -v /APP_FOLDER:/my_flask_app my_flask_app:v0.1

123


