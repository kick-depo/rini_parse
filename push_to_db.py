import pymysql
from parsing import array
try:
    connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password= '',
    database= 'db_python',
    cursorclass=pymysql.cursors.DictCursor,
)
    print('Подключение успешно!')
    print('#' * 20)
    try:
        with connection.cursor() as cursor:
            sql = f"""INSERT INTO `wp_posts`(post_author, post_content, post_title, post_excerpt, comment_status, ping_status, post_name, to_ping, pinged, post_content_filtered, post_parent, guid, menu_order, post_type) 
            VALUES (1, '', {name}, '', 'closed', 'closed', {slug}, '', '',))"""
            cursor.execute(sql, (title, slug))

            guid = f'http://your-domain.com/?p={post_id}'
            sql = "UPDATE wp_posts SET guid=%s WHERE ID=%s"
            cursor.execute(sql, (guid, post_id))
    finally:
        connection.close()
except Exception as ex:
    print('Соединение не удалось :c')
    print(ex)
