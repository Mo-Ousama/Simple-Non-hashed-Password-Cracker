import hashlib
import itertools
import base64
import os
from colorama import Fore, Style

def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

def hash_sha256(password):
    return hashlib.sha256(password.encode()).hexdigest()

def brute_force_attack(target_hash, charset, max_length, hash_function):
    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            candidate = ''.join(attempt)
            if hash_function(candidate) == target_hash:
                return candidate
    return None

def dictionary_attack(target_hash, dictionary_file, hash_function):
    if not os.path.exists(dictionary_file):
        print(f"❌ File not found: {dictionary_file}")
        return None
    
    with open(dictionary_file, 'r', encoding='utf-8') as file:
        for word in file:
            word = word.strip()
            if hash_function(word) == target_hash:
                return word
    return None

def decode_base64(encoded_str):
    try:
        return base64.b64decode(encoded_str).decode('utf-8')
    except Exception as e:
        return f"Error decoding Base64: {e}"

def crack_password(target_hash, dictionary_file=None, brute_force=False, charset='abcdefghijklmnopqrstuvwxyz', max_length=4, hash_function=hash_md5):
    print(Fore.YELLOW + "[+] Attempting to crack password..." + Style.RESET_ALL)
    
    # Try dictionary attack first
    if dictionary_file:
        result = dictionary_attack(target_hash, dictionary_file, hash_function)
        if result:
            print(Fore.GREEN + f"[✔] Password found using Dictionary Attack: {result}" + Style.RESET_ALL)
            return result
    
    # Fallback to brute force if enabled
    if brute_force:
        result = brute_force_attack(target_hash, charset, max_length, hash_function)
        if result:
            print(Fore.GREEN + f"[✔] Password found using Brute Force: {result}" + Style.RESET_ALL)
            return result
    
    print(Fore.RED + "[✘] Password not found." + Style.RESET_ALL)
    return None

# User Input
password = input("Enter the password to hash: ")
hash_type = input("Enter hash type (md5/sha1/sha256): ")

dictionary_file = "common_passwords.txt"
use_brute_force = input("Use brute force if dictionary attack fails? (y/n): ").lower() == 'y'

if hash_type == "md5":
    target_hash = hash_md5(password)
    hash_function = hash_md5
elif hash_type == "sha1":
    target_hash = hash_sha1(password)
    hash_function = hash_sha1
elif hash_type == "sha256":
    target_hash = hash_sha256(password)
    hash_function = hash_sha256
else:
    print(Fore.RED + "Invalid hash type!" + Style.RESET_ALL)
    exit()

crack_password(target_hash, dictionary_file=dictionary_file, brute_force=use_brute_force, max_length=4, hash_function=hash_function)
