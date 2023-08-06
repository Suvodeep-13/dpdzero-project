# dpdzero-project

# dpdzero

This is a assignment Project for dpdzero


## Installation

Install my-project with pip

```bash
  1.Clone the repo: git clone https://github.com/Suvodeep-13/dpdzero-project.git
  2.Create python virtual enviroment:  python3 -m venv env
  3.Activate the virtual environment: source env/bin/activate
  4.Run command : pip install django
                  pip install djangorestframework
                  pip install djangorestframework-jwt
  5.move to base directory: cd dpdzero
  6.Migrate DB changes: python manage.py migrate
  7.Run Application: python manage.py runserver
```
    
## Define

- framework: django rest_framework
- db: sqllite (django default db)
    - Schema:
    -    Forgienkey " " "    Data:
     - User:  -----------> "" user
       - email '""""         ""    key 
       - username        """   value 
       - password             
       - age
       - gender
