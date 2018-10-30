## StoreManager-V2  :department_store:
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)  [![Coverage Status](https://coveralls.io/repos/github/kwanj-k/storemanager-v2/badge.svg?branch=ch-readme-%23161404824)](https://coveralls.io/github/kwanj-k/storemanager-v2?branch=ch-readme-%23161404824&service=github)


## Summary

Store Manager is a web application that helps store owners manage sales and product inventory records. 

## NOTE
* The project is managed using PivotalTracker board [click here](https://www.pivotaltracker.com/n/projects/2202775)

* To see documentation [click here](https://storemanager-v2.herokuapp.com/api/v2)

* To see API on heroku [click here](https://storemanager-v2.herokuapp.com/api/v2)



## Getting Started 

* Clone the repository: 

    ```https://github.com/kwanj-k/storemanager-v2.git```

* Navigate to the cloned repo. 

### Prerequisites

```
1. Python3
2. Flask
3. Postman
4. Postgres
5. Psycopg2
```

## Installation 
After navigating to the cloned repo;

Create a virtualenv and activate it ::

    create a directory 
    cd into the directory
    virtualenv -p python3 venv
    source venv/bin activate

Install the dependencies::

    pip install -r requirements.txt 

Set up the database:: [Refer here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04#creating-a-new-role)


## Configuration

After activativating the virtualenv, run:

    ```
    export FLASK_APP="run.py"
    export FLASK_DEBUG=1
    export APP_SETTINGS="development"
    export Dev_URL="dbname=dbname user=username password=password"
    export Test_URL="dbname=dbname user=username password=password"
    export SECRET="iamasecrettheunsadtheunsulliedtheundead"

    ```
## Running Tests
Run:
```
pytest --cov-report term-missing --cov=app
```

### Testing on Postman/Docs
Fire up postman and start the development server by:
  ```
  $ flask run
  ```

To use the docs [click here]( http://127.0.0.1:5000/api/v2/)

On Post man:

    Navigate to  http://127.0.0.1:5000/api/v2/


Test the following endpoints:
### Note

* A super admin can access both admin and attendant routes
* An admin can access his/her routes and attendant routes only
* An attendant can only access his/her routes
* One who adds a store is by default the only superadmin


### Unsrestricted endpoints

| EndPoint                       | Functionality                           |
| -------------------------------|:---------------------------------------:|
| POST     /stores               | Create a store                          |
| POST     /auth/login           | Login a user                            |
|                                                                          |



### Attendant endpoints

| EndPoint                       | Functionality                           |
| -------------------------------|:---------------------------------------:|                                                                 
| GET      /products             | Get all the products                    |
| GET      /products/Id/         | Get  a product by id                    |
| POST     /products/Id/         | Add a product to cart                   |
| GET      /cart                 | View cart                               |
| PUT      /cart/Id              | Update a product in a cart              |
| DELETE   /cart/Id              | Delete a product in a cart              |
| POST     /cart                 | Sell an entire cart                     |
| DELETE   /cart                 | Delete an entire cart                   |
| POST     /auth/logout          | Logout a user                           |
|                                                                          |

### Admin endpoints

| EndPoint                                    | Functionality                           |
| --------------------------------------------|:---------------------------------------:|                                                    
| POST     /attendant/                        | Add a store attendant                   |
| POST     /categories/                       | Create a category                       |
| PUT      /categories/Id                     | Update a category                       |
| DELETE   /categories/Id                     | Delete a category                       | 
| POST     /products/                         | Add a product without setting category  |
| POST     /categories/Id/products            | Add a product  to a category directly   |  
| PUT      /products/Id/                      | Update the information of a product     |
| DELETE   /products/Id/                      | Remove a product                        |
| POST    /categories/Id//products/Id/        | Give a product a given category         |
| GET      /sales/                            | Get all the the sale records            |
|                                                                          |



### Super Admin endpoint

| EndPoint                       | Functionality                           |
| -------------------------------|:---------------------------------------:|
| POST     /admin/               | Add an admin                            | 
|                                                                          |





## Authors

* **Kelvin Mwangi** - *Initial work* - [kwanj-k](https://github.com/kwanj-k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

#### Contribution
Fork the repo, create a PR to this repository's develop.
