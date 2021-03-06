# IBSngReport
- A simple django framework app.
- Fetch IBSng users list.
- It has a powerful datatable search.

### Steps to run:

1. Add this 4 views in IBSng db:
   - uname (UserNames)
   - ulock (User Lock)
   - ucomment (User Comments)
   - ullog (user last log id)

 code:
  
    CREATE VIEW uname AS
		SELECT user_attrs.user_id, user_attrs.attr_value AS uname
		FROM user_attrs
		WHERE (user_attrs.attr_name = 'uname'::text)
  
    CREATE VIEW ulock AS
		SELECT user_attrs.user_id, user_attrs.attr_value AS ulock
		FROM user_attrs
		WHERE (user_attrs.attr_name = 'ulock'::text)
    
    CREATE VIEW ucomment AS
		SELECT user_attrs.user_id, user_attrs.attr_value AS ucomment
		FROM user_attrs
		WHERE (user_attrs.attr_name = 'comment'::text)
     
    CREATE VIEW uname AS
		SELECT max(connection_log.connection_log_id) AS last_log_id, connection_log.user_id
		FROM connection_log
		GROUP BY connection_log.user_id

2. Fill config/database.ini with appropriate data.
3. Host app on your server.
