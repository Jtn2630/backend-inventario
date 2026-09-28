import sqlite3


DATABASE = "database/inventory.db"


# ==========================================
# Estrutura da Base de Dados
# ==========================================

def column_exists(cursor, table, column):

    cursor.execute(
        f"PRAGMA table_info({table})"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    return column in columns


def add_column(
    cursor,
    table,
    column,
    definition
):

    if column_exists(
        cursor,
        table,
        column
    ):
        return

    cursor.execute(
        f"""
        ALTER TABLE {table}
        ADD COLUMN {column} {definition}
        """
    )


# ==========================================
# Atualização da Base de Dados
# ==========================================

def update_database():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    # ==========================================
    # Cônjuge
    # ==========================================

    add_column(
        cursor,
        "spouse",
        "marriage_date",
        "DATE"
    )

    add_column(
        cursor,
        "spouse",
        "participation_percentage",
        "NUMERIC"
    )


    # ==========================================
    # Bem
    # ==========================================

    add_column(
        cursor,
        "asset",
        "acquisition_date",
        "DATE"
    )

    add_column(
        cursor,
        "asset",
        "is_private",
        "BOOLEAN"
    )


    connection.commit()

    connection.close()

    print(
        "Database updated successfully."
    )


if __name__ == "__main__":
    update_database()