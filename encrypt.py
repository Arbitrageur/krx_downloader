import os, random, struct
import hashlib
from Cryptodome.Cipher import AES
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend

# copied from https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto

def encrypt_file(passphrase, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    key = hashlib.sha256(passphrase.encode()).digest()
    # iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    iv = bytes([random.randint(0, 0xFF) for i in range(16)])
    # backend = default_backend()
    # cipher = Cipher(algorithms.AES(key), modes.CBC(iv.encode()), backend=backend)
    # encryptor = cipher.encryptor()

    encryptor = AES.new(key, AES.MODE_CBC, iv)

    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    # outfile.write(encryptor.finalize())
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                # outfile.write(encryptor.update(chunk))
                outfile.write(encryptor.encrypt(chunk))

def decrypt_file(passphrase, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    key = hashlib.sha256(passphrase.encode()).digest()

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        # backend = default_backend()
        # cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        # decryptor = cipher.decryptor()
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        print(iv.hex())
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
