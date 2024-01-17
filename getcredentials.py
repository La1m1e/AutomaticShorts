file_pathc = 'credentials.txt'


def read_credentials():
    credentials = {}
    with open(file_pathc, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            key = parts[0]
            value = parts[1] if len(parts) > 1 else None
            credentials[key] = value
    return credentials


def credentials(key):
    cred_dict = read_credentials()
    return cred_dict.get(key)
