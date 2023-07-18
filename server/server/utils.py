import random
import string

def generate_identifier(counts=44):
  words = string.ascii_letters + string.digits + '_'
  key = "".join(random.sample(words, counts))
  return key