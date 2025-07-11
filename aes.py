from Crypto.Cipher import AES
import consts


class Criptography:
    def __init__(self, key: bytes):
        """
        Initializes the Criptography object with the given key.

        Args:
            key (bytes): The key to use for encrypting and decrypting data.

        Raises:
            ValueError: The key is not on the correct size"""
        self.key = key


    def encrypt(self, data: str) -> dict:
        """
        Encrypts the given data.

        Args:
            data (str): The data to encrypt.

        Returns:
            dict: A dictionary containing the encrypted data, nonce and tag.
        """
        cipher = AES.new(self.key, AES.MODE_EAX, mac_len=consts.MAC_SIZE)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode(consts.ENCODING))
        
        return {
            "ciphertext": ciphertext,
            "nonce": nonce,
            "tag": tag
        }
    

    def decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes) -> str | None:
        """
        Decrypts the given ciphertext with the given nonce and tag.

        Args:
            nonce (bytes): The nonce used for encryption.
            ciphertext (bytes): The encrypted data.
            tag (bytes): The authentication tag used for verifying the integrity of the encrypted data.

        Returns:
            str: The decrypted data, or None if the decryption fails.
        """
        cipher = AES.new(self.key, AES.MODE_EAX, nonce, mac_len=consts.MAC_SIZE)
        
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode(consts.ENCODING)
        except (ValueError, KeyError):
            return None
        

if __name__ == "__main__":
    criptography = Criptography(b"abcdefghijklmnop")
    cript = criptography.encrypt("test")

    text = criptography.decrypt(cript["nonce"], cript["ciphertext"], cript["tag"])

    print(text)