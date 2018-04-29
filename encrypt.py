from Crypto.Cipher import AES
import os
# Encryption
random_key = os.urandom(16)
print("random key",random_key,"\n")
encryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')
msg = "Session Key was received"

cipher_text = encryption_suite.encrypt(msg)
print(cipher_text)
# Decryption
decryption_suite = AES.new("iamakeytest12345", AES.MODE_CFB, 'This is an IV456')
plain_text = decryption_suite.decrypt(cipher_text)
print(plain_text.decode("utf-8"))
