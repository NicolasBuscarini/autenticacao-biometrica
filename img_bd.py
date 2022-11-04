import sqlite3


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data


def insert_blob(nome, usuario, senha, img, acesso):
    global cursor, connection
    print("Inserting BLOB into Cadastro_Agentes table")
    try:
        connection = sqlite3.connect("db/Cadastros_Agentes.db")

        cursor = connection.cursor()
        sql_insert_blob_query = "INSERT INTO Cadastro_Agentes " \
                                "(nome, usuario, senha, imagem_biometria, acesso) " \
                                "VALUES (?, ?, ?, ?, ?)"

        binary_img = convert_to_binary_data(img)

        # Convert data into tuple format
        data_usuario = (nome, usuario, senha, binary_img, acesso)

        result = cursor.execute(sql_insert_blob_query, data_usuario)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into Cadastro_Agentes table", result)

    except sqlite3.Error as error:
        print("Failed inserting BLOB data into SQLite table {}".format(error))

    finally:
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


insert_blob("Nicolas", "nicolas", "nicolas123", "assets/images/fingerprint2.png", 3)
