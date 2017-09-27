import re
from django.contrib import messages
from django.shortcuts import render
from credit_card_validator.validator.forms import ValidatorForm


def validate(request):
    results = []
    form = ValidatorForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            data, validator = handle_data(**form.cleaned_data)
            if validator:
                results = CreditCard(numbers=data).validate()
            else:
                messages.add_message(request, messages.ERROR, """
                File on upload does not meet input criteria (greater than 0 less than 100)
                """, extra_tags='danger')

    return render(request, 'index.html', context=dict(
        form=form,
        results=results
    ))


def handle_data(number, file):
    result = []
    validator = True
    if file:
        for idx, line in enumerate(file):
            line = re.sub(r"\W+", '', line.decode("utf-8"))
            if idx == 0 and (0 >= int(line) or int(line) >= 100):
                validator = False
                break
            elif idx != 0:
                result.append(line)
    if validator and number:
        result.append(number)
    return result, validator


class CreditCard:
    def __init__(self, numbers=None):
        self.numbers = numbers
        self.current_number = None
        self.current_result = True

    def validate(self):
        results = []
        for n in self.numbers:
            self.current_number = n
            result_methods = [
                ('It must start with a 4, 5 or 6.', self.verify_must_start()),
                ('It must contain exactly 16 digits.', self.verify_must_contains_16_digits()),
                ('It must only consist of digits (0-9).', self.verify_must_contains_only_0_9()),
                ('It may have digits in groups of 4, separated by one hyphen "-"', self.verify_group_separated()),
                ('It must NOT use any other separator like " " , "_", etc.', self.verify_contains_other_separator()),
                (' It must NOT have 4 or more consecutive repeated digits',
                 self.verify_more_consecutive_repeated_digit()),
            ]

            results.append(dict(
                number=n,
                results=result_methods,
                is_valid=self.is_valid(result_methods)
            ))
        return results

    def verify_must_start(self):
        """
        It must start with a 4, 5 or 6.
        :return bool:
        """
        start = [4, 5, 6]
        return int(self.current_number[0]) in start

    def verify_must_contains_16_digits(self):
        """
         It must contain exactly 16 digits.
        :param number:
        :return bool:
        """
        fragments = self.current_number.split('-')
        return len(''.join(fragments)) == 16

    def verify_must_contains_only_0_9(self):
        """
        It must only consist of digits (0-9).
        :return bool:
        """
        return len(re.findall(r'[a-z]|[A-Z]', self.current_number)) == 0

    def verify_group_separated(self):
        """
        It may have digits in groups of 4, separated by one hyphen "-".
        :return bool:
        """
        fragments = self.current_number.split('-')
        if len(fragments) > 1:
            for f in fragments:
                if len(f) != 4:
                    return False
        return True

    def verify_contains_other_separator(self):
        """
        It must NOT use any other separator like ' ' , '_', etc.
        :return bool:
        """
        blank_space = re.findall(r'[\s]', self.current_number)
        separators = re.findall(r'[\s,\W]', self.current_number)
        separators = separators.remove('-') if '-' in separators else separators

        if blank_space is None:
            blank_space = []
        if separators is None:
            separators = []

        return len(blank_space) == 0 and len(separators) == 0

    def verify_more_consecutive_repeated_digit(self):
        """
        It must NOT have 4 or more consecutive repeated digits
        :return bool:
        """
        return len(re.findall(r'(\w)\1{3}', self.current_number)) == 0

    @staticmethod
    def is_valid(result_methods):
        for k, v in result_methods:
            if not v:
                return False
        return True
