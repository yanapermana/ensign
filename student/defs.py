import os
import string
import random
import hashlib
import binascii

alphanumeric = list(string.ascii_letters + string.digits)

def generate_invitation_code():
	token = 'ensign-'
	for idx in xrange(19):
		token += random.choice(alphanumeric)
	return token

def password_hashing(password, salt):
	derivation_key = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
	print derivation_key.encode('hex')
	print salt.encode('hex')
	return binascii.hexlify(derivation_key), binascii.hexlify(salt)

print password_hashing('test','woot')
