
# Virtualevn:
* pip install virtualenv
* python3 -m venv venv
* source venv/bin/activate

# Packages:
python3 -m pip install -r requirements.txt

# Run tests:
* run all login tests: pytest tests/test_login.py
* run one test: pytest tests/test_login.py -k test_login_with_email
