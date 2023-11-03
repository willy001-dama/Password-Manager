from backend import database, encryptor


class DatabaseUtility:
    def __init__(self):
        self.database_handle = database.DatabaseOps()
        self.encrypt_handle = encryptor.Encryptor()

    def insert_login(self, username, password):
        statement = """INSERT INTO User ('username', 'password') VALUES (?, ?)"""
        values = (username, password)
        self.database_handle.insert_record(statement, values)

    def insert_password(self, sitename, username, password, encrypted, owner):
        password = self.encrypt_handle.encrypt(password)
        sql_statement = f"""
                INSERT INTO Login ('sitename', 'username', 'password', 'encrypted', 'owner') 
                VALUES (?, ?, ?, ?, ?)
                """
        values = (sitename, username, password, encrypted, owner)
        self.database_handle.insert_record(sql_statement, values)

    def insert_note(self, title, content, owner):
        """function to prepare the sql statement and call the needed function"""
        content = self.encrypt_handle.encrypt(content)
        sql_statement = """
                INSERT INTO Notes ('title', 'content', 'owner') 
                VALUES (?, ?, ?)
                """
        values = (title, content, owner)
        self.database_handle.insert_record(sql_statement, values)

    def insert_payment(self, sitename, username, password, encrypted, owner):
        password = self.encrypt_handle.encrypt(password)
        sql_statement = f"""
                INSERT INTO Login ('sitename', 'username', 'password', 'encrypted', 'owner') 
                VALUES ('{sitename}', '{username}', '{password}', '{encrypted}', {owner})
                """
        self.database_handle.insert_record(sql_statement)

    # --------------------------------------------------------------------------------------
    # fetch section of our database utilities

    def fetch_data(self, table, owner):
        statement = f"""SELECT * FROM {table} WHERE owner={owner}"""
        values = self.database_handle.fetch_record(statement)
