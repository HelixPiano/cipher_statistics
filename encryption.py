import numpy as np
import prime_array as pa
import key_streams as ks


def encrypt_text(plaintext, algorithm, shift_id, reverse_text, reverse_gematria, interrupter, key, interrupter_array):
    if reverse_text:
        plaintext = plaintext[::-1]

    # What happens with interrupters at this point?
    if reverse_gematria:
        plaintext = atbash(plaintext)

    ct = plaintext.copy()
    ct = apply_shift(ct, interrupter, shift_id)

    if algorithm.lower() == 'vigenere':
        ct = vigenere_encryption(ct, interrupter, key, interrupter_array)
    elif algorithm.lower() == 'autokey':
        ct = autokey_encryption(ct, interrupter, key, interrupter_array)
    else:
        assert False
    return ct


def vigenere_encryption(ct, interrupter, key, interrupter_array=None):
    key_index = 0
    key_length = len(key)

    if interrupter_array is None:
        interrupter_array = np.asarray(ct == interrupter, dtype=bool)

    interrupter_array = interrupter_array.flatten()
    ct = ct.squeeze()
    for index, element in enumerate(ct):
        if interrupter_array[index]:
            continue
        ct[index] = (ct[index] + key[key_index % key_length]) % 29
        key_index += 1
    return ct


def autokey_encryption(ct, interrupter, key, interrupter_array=None):
    ct = ct.squeeze()
    plaintext = ct.copy()
    counter = 0
    index = 0

    if interrupter_array is None:
        interrupter_array = np.asarray(ct == interrupter, dtype=bool)
    interrupter_array = interrupter_array.flatten()

    while counter < len(key):
        if interrupter_array[index]:
            index += 1
            continue
        ct[index] = (plaintext[index] + key[counter]) % 29
        index += 1
        counter += 1

    position = 0
    for i in range(index, len(ct)):
        if interrupter_array[i]:
            continue
        ct[i] = (ct[i] + plaintext[position]) % 29
        position += 1

    return ct


def translate_to_english(input_text, reverse_gematria):
    dic = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", "S", "T", "B", "E", "M", "L",
           "ING", "OE", "D", "A", "AE", "Y", "IA", "EA"]
    if reverse_gematria:
        dic.reverse()
    translation = ""
    for index in np.nditer(input_text):
        translation += dic[index]
    return translation


def atbash(plaintext):
    return np.remainder(28 - plaintext, 29)


def apply_shift(ct_numbers, interrupter, shift_id):
    # Indices 1-2, 3-4, and 5-6 are swapped, so that decryption undoes the encryption operation.
    # So Index 1 in encryption is the inverse operation of Index 1 in decryption
    ct_numbers = ct_numbers.squeeze()
    shift_index = 0
    prime = pa.numpy_prime_array()

    if shift_id == 1:
        for index, element in enumerate(ct_numbers):
            if element == interrupter:
                continue
            ct_numbers[index] -= prime[shift_index] - 1
            shift_index += 1
    elif shift_id == 2:
        for index, element in enumerate(ct_numbers):
            if element == interrupter:
                continue
            ct_numbers[index] += prime[shift_index] - 1
            shift_index += 1
    elif shift_id == 3:
        for index, element in enumerate(ct_numbers):
            if element == interrupter:
                continue
            ct_numbers[index] -= prime[shift_index]
            shift_index += 1
    elif shift_id == 4:
        for index, element in enumerate(ct_numbers):
            if element == interrupter:
                continue
            ct_numbers[index] += prime[shift_index]
            shift_index += 1
    elif shift_id == 5:
        for index, element in enumerate(ct_numbers):
            if element == interrupter:
                continue
            ct_numbers[index] -= shift_index
            shift_index += 1
    elif shift_id == 6:
        for index, element in enumerate(ct_numbers):
            if element == interrupter:
                continue
            ct_numbers[index] += shift_index
            shift_index += 1
    return np.remainder(ct_numbers, 29)


def key_switch_algorith(plaintext):
    ct = plaintext.copy()
    Circumferences = np.array([6, 11, 5, 6, 2, 20, 1, 19, 5, 19, 10, 6, 19, 16])
    Divinity = np.array([24, 11, 2, 11, 10, 11, 17, 27])
    integercy = np.zeros(len(plaintext), dtype=np.int32)

    for i in range(len(ct) - 1):
        if ((ct[i + 1] + Divinity[(i + 1) % 8]) % 29) == ((ct[i] + Divinity[i % 8]) % 29):
            if ((ct[i + 1] + Circumferences[(i + 1) % 14]) % 29) == ((ct[i] + Circumferences[i % 14]) % 29):
                continue
            else:
                integercy[i] = (ct[i] + Circumferences[i % 14]) % 29
        else:
            integercy[i] = (ct[i] + Divinity[i % 8]) % 29
    return integercy


def long_oeis_sequence(plaintext):
    ct = plaintext.copy()
    key = ks.oeis_key()
    max_index = len(key) - 1
    for i in range(len(ct) - 1):
        ct[i] = (ct[i] + (key[i % max_index] % 29)) % 29
    return ct


def random_otp(plaintext):
    ct = plaintext.copy()
    ct = (ct + np.random.randint(low=0,high=28, size=len(ct), dtype=np.int8)) % 29
    return ct
