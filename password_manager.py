import database
import aes
import consts
import checksum
import os
import excepts

class PasswordManager:
    def __init__(self, db_path: str, key_path: str, key: bytes):
        """
        Initializes a PasswordManager object.

        Args:
            db_path (str): The path to the SQLite database to store password data in.
            key_path (str): The path to the file to store the checksum of the key in.
            key (bytes): The key to use for encrypting and decrypting password data.

        Raises:
            excepts.InvalidKey: The key is invalid.
        """
        check = checksum.Checksum()
        self.first_start = True

        if len(key) > consts.MAC_SIZE:
            raise excepts.InvalidKey
        else:
            key = key.ljust(consts.MAC_SIZE, b" ")

        self.key = key
        self.key_stored = check.generate(self.key)
        self.key_path = key_path
        if os.path.exists(key_path):
            self.key_stored = open(self.key_path, "r").read()
            self.first_start = False
        else:
            open(key_path, "w+").write(self.key_stored)
        
        self.db_path = db_path
        self.db = database.Database(self.db_path)

        key_checksum = check.generate(key)

        if key_checksum != self.key_stored:
            raise excepts.InvalidKey

        self.criptography = aes.Criptography(self.key)


    def register_password(self, entity: str, username: str, password: str):
        """
        Registers a new password entry into the database.

        Args:
            entity (str): The name of the entity or service for which the password is being stored.
            username (str): The username associated with the entity.
            password (str): The password to store.

        """
        cript = self.criptography.encrypt(password)
        self.db.register_password(entity, username, cript["ciphertext"], cript["nonce"], cript["tag"])

    
    def get_password(self, entry: int) -> str | None:
        """
        Retrieves a password entry from the database based on its ID.

        Args:
            entry (int): The ID of the password entry to retrieve.

        Returns:
            str: The decrypted password.
            None: If the decryption fails.
        """
        raw_data = self.db.get_password(entry)

        decrypted = self.criptography.decrypt(raw_data["nonce"], raw_data["encrypted_password"], raw_data["tag"])
        
        return decrypted
    

    def get_list(self) -> tuple[list, list]:
        passwords = self.db.get_all()

        entities = [password["entity"] for password in passwords]

        return passwords, entities
    

    def delete_password(self, entry: int):
        self.db.remove_password(entry)

    
    def modify_password(self, entry: int, entity: str, username: str, password: str):
        cript = self.criptography.encrypt(password)
        self.db.edit_password(entry, entity, username, cript["ciphertext"], cript["nonce"], cript["tag"])


    def reset(self):
        self.db.connection.close()
        
        os.remove(self.db_path)
        os.remove(self.key_path)

        self.__init__(self.db_path, self.key_path, self.key)

if __name__ == "__main__":
    mgr = PasswordManager(consts.DB_PATH, key_path="key", key=b"aaaaaaaaaaaaaaaa")

    mgr.register_password("test", "test", "test")
    print(mgr.get_password(1))

    print(mgr.get_password(1))

