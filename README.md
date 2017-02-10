[![Coverage Status](https://coveralls.io/repos/github/Muthama-Kahohi/Bucketlist_API/badge.svg?branch=develop)](https://coveralls.io/github/Muthama-Kahohi/Bucketlist_API?branch=develop)



# Bucketlist API
This is a python based API that keeps records of a users bucketlist.
Allows updating and deleting all with authentication via tokens.

## Specifications
The API is token based. Registration is through a username and a hashed password. Once a user logs in they are given token that is used for methods that are not public. Below is a detailed table on the endpoints as well as their methods.

| Endpoint                                                        | Methods Allowed  | Functionality       | Public Access|
| --------------------------------------------------------------- | :---------------:| -------------------:| ------------:|
| /bucketlist/api/auth/register                                   | POST             | Registers a new user| YES          |
| /bucketlist/api/auth/login                                      | POST             | Log in a user       | YES	      |
| /bucketlist/api/bucketlists                                     | POST, GET        | create, retrieve    | NO           |
| /bucketlist/api/bucketlists/<int:id>                            | GET, PUT, DELETE | create, get, delete | NO           |
| /bucketlist/api/bucketlists/<int:id>/items                      | POST             | create an item      | NO           |
| /bucketlist/api/bucketlists/<int:bucket_id>/items/<int:item_id> | GET, DELETE, PUT | create, get, delete | NO           |

## Installation
1. git clone the [repo](https://github.com/Muthama-Kahohi/Bucketlist_API.git)
2. create a virtualenv `virtualenv venv`
3. Activate the environment `source venv\bin\activate`
3. pip install requirements by running `pip install -r requirements.txt`
4. run the server `python run.py`

## How to use
You can send and requests and receive responses using Postman or curl.

## Registration
Registration requires a username and a password to be sent a request and if valid shoud return a status code 201 to indicate creation.
![Imgur](http://i.imgur.com/anG2P40.png)

## Log in
Logging in using a username and a password. The response, if valid is a token and a 200 status code for ok
![Imgur](http://i.imgur.com/Fv8fG3w.png)

##Creating a bucketlist
Request shoud have an authorization header that contains the token as the value. The request body has the name of the bucketlist.
![Imgur](http://i.imgur.com/LQdeENA.png)

When passing on request that require authentication. The Authorization token has to be added to the headers as shown below.
![Imgur](http://i.imgur.com/QIOvbNE.png)

## Dependencies
### [Nose](https://jensv.github.io/2014-07-28-stanford/novice/testing/nose.html)
Used for testing
### [itsdangerous](http://pythonhosted.org/itsdangerous/)
Used for password hashing to enhance security
### [Flask-restful](http://flask-restful-cn.readthedocs.io/en/0.3.5/)
Flask extension for the rapid development of API's