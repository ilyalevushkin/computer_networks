#!/bin/bash

cd ..
cd ..
cd ..
source project_env/bin/activate
cd backend_squares/squares
python3 manage.py test squares_app.tests.unit
python3 manage.py test squares_app.tests.integration
python3 manage.py test squares_app.tests.e2e
deactivate