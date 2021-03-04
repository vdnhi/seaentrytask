import re


def validate_username(username):
	return username.isalnum() and username == username.lower() and username[0].isalpha()


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def validate_email(email):
	return re.search(regex, email)


def validate_fullname(fullname):
	return fullname.replace(" ", "").isalpha()
