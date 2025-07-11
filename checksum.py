import hashlib


class Checksum:
    def __init__(self):
        pass

    def generate(self, data) -> str:
        """
        Generates a SHA-512 checksum for given data.

        Args:
            data (bytes): Data to generate checksum for.

        Returns:
            str: SHA-512 checksum of the given data as a hexadecimal string.
        """
        hashy = hashlib.sha512(data) 
        return hashy.hexdigest()
    

    def verify(self, a: str, b: str) -> bool:
        """
        Verifies whether two checksums are equal.

        Args:
            a (str): The first checksum to compare.
            b (str): The second checksum to compare.

        Returns:
            bool: Whether the two checksums are equal.
        """
        return a == b