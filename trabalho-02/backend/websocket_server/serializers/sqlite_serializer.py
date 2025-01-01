class SqliteSerializer():

    def to_dict(self, curson, row):
        fields = [col[0] for col in curson.description]
        return {fields[idx]: row[idx] for idx in range(len(fields))}