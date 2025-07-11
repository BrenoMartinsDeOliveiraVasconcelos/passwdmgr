import sqlite3
import consts
import os


class Database:
    def __init__(self, db_path: str):
        """
        Initializes the Database object, establishes a connection to the SQLite database
        located at the given path, and sets up the database schema by executing the SQL
        script from 'dbscript.sql'.

        Args:
            db_path (str): The file path to the SQLite database.
        """

        self.db_path = db_path

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(open(os.path.join(consts.PROGRAM_PATH, "dbscript.sql"), "r").read())


        self.connection.commit()

    
    def register_password(self, entity: str, username: str, password: bytes, nonce: bytes, tag: bytes):
        """
        Inserts a new password entry into the database.

        Args:
            entity (str): The name of the entity or service for which the password is being stored.
            username (str): The username associated with the entity.
            password (bytes): The encrypted password.
            nonce (bytes): The nonce value used in the encryption process.
            tag (bytes): The authentication tag used for verifying the integrity of the encrypted password.
        """

        self.cursor.execute("INSERT INTO data (entity, username, encrypted_password, nonce, tag) VALUES (?, ?, ?, ?, ?)", (entity, username, password, nonce, tag))
        self.connection.commit()

    
    def get_password(self, entry: int) -> dict:

        """
        Retrieves a password entry from the database based on its ID.

        Args:
            entry (int): The ID of the password entry to retrieve.

        Returns:
            dict: A dictionary containing the retrieved password entry's information.
        """
        self.cursor.execute("SELECT * FROM data WHERE id = ?", (entry,))
        data = self.cursor.fetchone()

        return_dict = {
            "id": data[0],
            "entity": data[1],
            "username": data[2],
            "encrypted_password": data[3],
            "nonce": data[4],
            "tag": data[5]
        }

        return return_dict
    

    def remove_password(self, entry: int):
        """
        Removes a password entry from the database based on its ID.

        Args:
            entry (int): The ID of the password entry to remove.
        """
        self.cursor.execute("DELETE FROM data WHERE id = ?", (entry,))
        self.connection.commit()

    
    def edit_password(self, entry: int, entity: str, username: str, password: bytes, nonce: bytes, tag: bytes):
        """
        Edits an existing password entry in the database.

        Args:
            entry (int): The ID of the password entry to edit.
            entity (str): The name of the entity or service for which the password is being stored.
            username (str): The username associated with the entity.
            password (bytes): The encrypted password.
            nonce (bytes): The nonce value used in the encryption process.
            tag (bytes): The authentication tag used for verifying the integrity of the encrypted password.
        """
        self.cursor.execute("UPDATE data SET entity = ?, username = ?, encrypted_password = ?, nonce = ?, tag = ? WHERE id = ?", (entity, username, password, nonce, tag, entry))
        self.connection.commit()


    def get_all(self):
        self.cursor.execute("SELECT * FROM data")
        
        data = self.cursor.fetchall()

        entries = [row[0] for row in data]
        return_list = []

        for entry in entries:
            return_list.append(self.get_password(entry))

        return return_list


if __name__ == "__main__":
    db = Database(consts.DB_PATH)

    print(db.get_all())

