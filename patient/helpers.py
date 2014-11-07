# -*- coding: UTF-8 -*-
from uuid import uuid4
from django.contrib.auth.models import User
import re


def get_initials(name):
    initials = name.split(' ')
    for i in range(len(initials)):
        initials[i] = initials[i][:1]
    return initials


def sanitize_name(name):
    s = name.lower().replace(u'ø', 'o').replace(u'æ', 'a').replace(u'å', 'a')
    s = re.sub('[^0-9a-z]+', '', s)
    return s


def username_exists(username):
    return User.objects.filter(username=username).exists()


def generate_username(first_name, last_name, birth_year):
    first_name = sanitize_name(first_name)
    last_name = sanitize_name(last_name)
    birth_year = str(birth_year)[-2:]
    first_name_initials = get_initials(first_name)
    last_name_initials = get_initials(last_name)

    suggestions = []
    for i in range(2, min(6, len(first_name) + 1)):
        suggestion = first_name[:i]
        for s in last_name_initials:
            suggestion += s
        suggestions.append(suggestion)

    for i in range(2, min(6, len(last_name) + 1)):
        suggestion = ''
        for s in first_name_initials:
            suggestion += s
        suggestion += last_name[:i]
        suggestions.append(suggestion)

    num_suggestions = len(suggestions)
    for i in range(num_suggestions):
        suggestions.append(suggestions[i] + birth_year)
    for i in range(num_suggestions):
        suggestions.append(suggestions[i] + uuid4().hex[:3])

    for suggestion in suggestions:
        if not username_exists(suggestion):
            return suggestion

    return uuid4().hex[:10]
