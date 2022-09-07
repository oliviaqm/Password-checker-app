import requests
import hashlib # to do sha1 hashing
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    #print(res)
    if res.status_code != 200:  # if not able to fetch data from the API
        raise RuntimeError(f'Error fetching :{res.status_code}, check the API and try again.')
    return res

def read_res(response):
    print(response.text)

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines()) #return a tuple with hash, count (of number of times hashed password has been pwned)
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    #check password if it exists in API response
    # print(password.encode('utf-8'))
    # print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    print(first5_char, tail)
    response = request_api_data(first5_char)
    # return read_res(response)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change your password')
        else:
            print(f'{password} was not found. Carry on!')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))