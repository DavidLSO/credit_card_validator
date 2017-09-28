# Validate Credit Card 

You and Fredrick are good friends. Yesterday, Fredrick received credit cards from ABCD Bank. He wants to verify whether his credit card numbers are valid or not. You happen to be great at regex so he is asking for your help!

A valid credit card from ABCD Bank has the following characteristics:

1. It must start with a 4, 5 or 6.
2. It must contain exactly 16 digits.
3. It must only consist of digits (0-9).
4. It may have digits in groups of 4, separated by one hyphen "-".
5. It must NOT use any other separator like ' ' , '_', etc.
6. It must NOT have 4 or more consecutive repeated digits.

## Installation and Configuring VirtualEnv
1. `pip install virtualenv`
2. `virtualenv -p python3 credit-card-validator-env`
3. `cd credit-card-validator-env`
4. `source bin/activate`

## Installation
1. `cd credit_card_validator`
2. `pip install -r requirements.txt`
3. `python manage.py runserver`

##Hosted
[https://credit-card-validator.herokuapp.com/](https://credit-card-validator.herokuapp.com/)
