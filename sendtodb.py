import mysql.connector

def add_post_and_meta(meta_value, credintial,host,user,password,database):
    # Database connection parameters
    db_config = {
        "host": host,
        "user": user,
        "password": password,
        "database": database
    }

    try:
        # Create a connection to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Define data to be inserted into 'wp_posts' table
        post_data = {
            "post_author": 1,
            "post_title": credintial,
            "post_status": "publish",
            "comment_status": "open",
            "ping_status": "open",
            "post_name": credintial,
            "post_type": "shop_coupon",
            "comment_count": 0
        }

        # Insert data into 'wp_posts' table
        insert_post_query = """
        INSERT INTO wp_posts (post_author, post_title, post_status, comment_status, ping_status, post_name, post_type, comment_count)
        VALUES (%(post_author)s, %(post_title)s, %(post_status)s, %(comment_status)s, %(ping_status)s, %(post_name)s, %(post_type)s, %(comment_count)s)
        """
        cursor.execute(insert_post_query, post_data)
        new_post_id = cursor.lastrowid

        # Define data to be inserted into 'wp_postmeta' table
        postmeta_data = {
            "post_id": new_post_id,
            "meta_key": "coupon_amount",
            "meta_value": meta_value
        }

        # Insert data into 'wp_postmeta' table
        insert_postmeta_query = """
        INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
        VALUES (%(post_id)s, %(meta_key)s, %(meta_value)s)
        """
        cursor.execute(insert_postmeta_query, postmeta_data)

        # Commit the changes to the database
        conn.commit()

        print(f"Successfully added post with ID {new_post_id} and meta_value {meta_value}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


