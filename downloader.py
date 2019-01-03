# coding=utf-8

import os
import glob
import time
import sys

from driver_builder import DriverBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import random
import struct
import hashlib
from Cryptodome.Cipher import AES
from element import ButtonElement, InputElement, SelectElement

with open(sys.argv[1]) as cred_file:
    cred = json.load(cred_file)

username = cred["krx_user"]
password = cred["krx_pass"]
secret = cred["passphrase"]

driver_builder = DriverBuilder()
driver = driver_builder.get_driver(download_location=os.getcwd(), headless=True)
driver.get("http://index.krx.co.kr")
wait = WebDriverWait(driver, 20)

# Click 'Sign in' Button
sign_in = ButtonElement(driver, (By.CSS_SELECTOR, "a.sign-in"))

account_type = SelectElement(driver, (By.XPATH, "//select[@name='kind']/option[text()='법인회원']"))

id_input = InputElement(driver, (By.CSS_SELECTOR, "input[name='id']"))
id_input.value(username)

passwd_input = InputElement(driver, (By.CSS_SELECTOR, "input[name='pw']"))
passwd_input.value(password)

login_btn = ButtonElement(driver, (By.CSS_SELECTOR, "button.login"))

index_select = SelectElement(driver, (By.XPATH, "//select[@name='package']/option[text()='KOSPI 200 Series_P']"))
search_btn = ButtonElement(driver, (By.CSS_SELECTOR, "button.btn-board.btn-board-search"))

download_btn = ButtonElement(driver, (By.CSS_SELECTOR, "button.btn-board.btn-board-download"))


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
    iv = bytes(random.randint(0, 0xFF) for i in range(16))

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


time.sleep(3)


for file in glob.glob("*.zip"):
    encrypt_file(secret, file)
    os.remove(file)
driver.close()
