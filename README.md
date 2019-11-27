# DiagnoSkin server
DiagnoSkin server is a lightweight web api that supports image-based clinical diagnosis of skin leisures. The api is implemented using [Flask-RESTful](https://github.com/flask-restful/flask-restful) framework. It is configurable through the config.json file to allow us to use different machine learning models. Upon startup the server loads the classification model from the location specified in the config and launches the web server to handle https traffic for the authenticated users of the DiagnoSkin app.
