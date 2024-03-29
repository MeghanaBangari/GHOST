# sys.path

# need to do pip install
## from AES import encrypt, decrypt
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import pyperclip as py

from getpass import getpass

import binascii
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Protocol.KDF import PBKDF2
import math


def get_private_key(password):
    salt = b"this is a salt"
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(passwrd, message):
    msglist = []
    key = get_private_key(passwrd)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(bytes(message, "utf-8"))
    msg = binascii.hexlify(msg)
    for letter in str(msg):
        msglist.append(letter)
    msglist.remove("b")
    msglist.remove("'")
    msglist.remove("'")
    encryptedMsg = ""
    for letter in msglist:
        encryptedMsg += letter
    return encryptedMsg


def decrypt(passwrd, message):
    msglist = []
    key = get_private_key(passwrd)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = cipher.decrypt(binascii.unhexlify(bytes(message, "utf-8")))[len(iv):]
    for letter in str(msg):
        msglist.append(letter)
    msglist.remove("b")
    msglist.remove("'")
    msglist.remove("'")
    decMsg = ""
    for letter in msglist:
        decMsg += letter
    return decMsg

# Function to check
# Log base 2


def Log2(x):
    if x == 0:
        return False
    return (math.log10(x) /
            math.log10(2))


# Function to check
# if x is power of 2
def isPowerOfTwo(n):
    return (math.ceil(Log2(n)) ==
            math.floor(Log2(n)))


# XOR of the two Binary Strings
def xor(a, b, n):
    ans = ""

    # Loop to iterate over the
    # Binary Strings
    for i in range(n):

        # If the Character matches
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans


def binaryToDecimal(n):
    return int(n, 2)


# SM="secret message" #secret message
# CM="cover message"  #cover message

MS_SK = "121"  # extracted from 12.15
SM_binary = ""
ZWC = {"00": u'\u200C', "01": u'\u202C', "10": u'\u202D', "11": u'\u200E'}
ZWC_reverse = {u'\u200C': "00", u'\u202C': "01",
               u'\u202D': "10", u'\u200E': "11"}


def embedFunc(SM, CM):
    global MS_SK, SM_binary, ZWC, ZWC_reverse
    for letter in SM:
        n = ord(letter)
        factors = []
        for i in range(1, n + 1):
            if (n + 1) % i == 0:
                factors.append(i)

        odd_factors_list = []
        for i in range(len(factors)):
            if (factors[i] % 2 != 0):
                odd_factors_list.append(factors[i])
        alpha = -99999
        for odd_factor in odd_factors_list:
            power_exists = isPowerOfTwo(int((n + 1) / odd_factor))
            if (power_exists):
                power = math.log10(int((n + 1) / odd_factor)) / math.log10(2)
                if (power > alpha):
                    alpha = int(power)
        if (alpha == -99999 and n % 2 == 0):
            alpha = 0
        # print("alpha=",alpha)
        alpha_binary = '{0:06b}'.format(alpha)
        # print("alpha in 6-bit binary format=",alpha_binary)
        beta = int((((n + 1) / pow(2, alpha)) - 1) / 2)
        # print("beta=",beta)
        beta_binary = '{0:06b}'.format(beta)
        # print("beta in 6-bit binary format=",beta_binary)
        SM_binary = SM_binary + alpha_binary + beta_binary
    MS_SK_binary = '{0:08b}'.format(int(MS_SK))
    # MS_SK_binary=MS_SK_binary.strip("0")
    # print(MS_SK_binary)
    LSK = len(MS_SK_binary)
    if (len(SM_binary) % LSK == 0):
        P = 0
    else:
        P = 1
    NC = int((len(SM_binary) / LSK) + P)

    hash_position_bits = NC * MS_SK_binary

    hashed_SM_binary = xor(SM_binary, hash_position_bits, len(SM_binary))

    HM_SK = ""
    i = 0
    x = ""
    while (i < len(MS_SK_binary) - 1):
        x = MS_SK_binary[i] + MS_SK_binary[i + 1]
        HM_SK += ZWC[x]
        i += 2

    # print("HM_SK=",HM_SK)
    HM_ZWC = ""
    i = 0
    x = ""
    while (i < len(hashed_SM_binary) - 1):
        x = hashed_SM_binary[i] + hashed_SM_binary[i + 1]
        HM_ZWC += ZWC[x]
        i += 2
    # print("HM_ZWC=",HM_ZWC)
    HM = HM_SK + HM_ZWC
    # print("HM=",HM)
    CM_HM = CM[:-1] + HM + CM[-1]
    return CM_HM

# Extracing Algo


def xor(a, b, n):
    ans = ""

    # Loop to iterate over the
    # Binary Strings
    for i in range(n):

        # If the Character matches
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans


def binaryToDecimal(n):
    return int(n, 2)


SM_extract = ""
MR_SK = "121"
hashed_SM_binary_extract = ""
ZWC_reverse = {u'\u200C': "00", u'\u202C': "01",
               u'\u202D': "10", u'\u200E': "11"}


# CM_HM=input("Enter the cover message:")
# password=input("Enter password:")

def extractFunc(CM_HM):
    global SM_extract, MR_SK, hashed_SM_binary_extract, ZWC_reverse
    for letter in CM_HM:
        if (letter in ZWC_reverse):
            hashed_SM_binary_extract += ZWC_reverse[letter]

    # print("----",len(hashed_SM_binary_extract))
    MS_SK_extract = hashed_SM_binary_extract[0:8]
    # print("~~~~~",MS_SK_extract)
    MR_SK_binary = '{0:08b}'.format(int(MR_SK))
    # MR_SK_binary=MR_SK_binary.strip("0")
    # print(MR_SK_binary)

    if (MS_SK_extract == MR_SK_binary):
        hashed_SM_binary_extract = hashed_SM_binary_extract[8:]
        LSK_extract = len(MR_SK_binary)
        if ((len(hashed_SM_binary_extract) % LSK_extract) == 0):
            P = 0
        else:
            P = 1
        NC_extract = int((len(hashed_SM_binary_extract) / LSK_extract) + P)
        hash_position_bits_extract = NC_extract * MR_SK_binary
        SM_binary_extract = xor(
            hashed_SM_binary_extract, hash_position_bits_extract, len(hashed_SM_binary_extract))
        # print("length=",len(hashed_SM_binary_extract))
        # print("length=",len(SM_binary_extract))
        while (len(SM_binary_extract) >= 12):
            alpha_beta = SM_binary_extract[0:12]
            SM_binary_extract = SM_binary_extract[12:]
            alpha_extract = alpha_beta[0:6]
            beta_extract = alpha_beta[6:12]
            # print("aplha=",alpha_extract,"beta=",beta_extract)
            alpha_final = binaryToDecimal(alpha_extract)
            beta_final = binaryToDecimal(beta_extract)
            # print("aplha=",alpha_final,"beta=",beta_final)
            n_final = ((pow(2, alpha_final) * (2 * beta_final + 1)) - 1)
            SM_extract = SM_extract + chr(n_final)
    # print("Encrypted secret message received:", SM_extract)
    return SM_extract


# SM=input("Enter secret message:")
# CM=input("Enter cover message:")
# password=input("Enter password for encryption:")
# neeeded - pip install pycrypto
key = get_random_bytes(16)


def hideFunc(SM, password, CM):
    encSM = encrypt(password, SM)
    # print("Encrypted secret message going to send:", encSM, end="\n\n")
    CM_HM = embedFunc(encSM, CM)
    # print("Cover message=",CM_HM, end="\n\n")
    py.copy(CM_HM)
    return CM_HM


def revealFunc(CM_HM, password):
    SM_extract = extractFunc(CM_HM)
    # print("Your secret message:", decrypt(password,SM_extract))
    return decrypt(password, SM_extract)

# variables needed, password, cover message, secret message to use functions hideFUn, reveal FUn
