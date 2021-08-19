from friendships.hbase_models import HBaseFollowing

table = HBaseFollowing.get_table()


def print_rows(rows):
    for row_key, row_data in rows:
        print(row_key, row_data)

# rows = table.scan()
rows = table.scan(row_stop=b'1000000000000000:1629391756362040', limit=2, reverse=True)
#rows = table.scan(row_prefix=b'1000000000000000', limit=3)
print_rows(rows)
