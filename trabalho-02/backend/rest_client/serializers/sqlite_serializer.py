class SqliteSerializer():
    @staticmethod
    def to_dict(cursor, row):
        fields = [col[0] for col in cursor.description]
        return {fields[idx]: row[idx] for idx in range(len(fields))}