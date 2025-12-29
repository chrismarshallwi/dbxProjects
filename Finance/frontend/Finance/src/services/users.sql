CREATE TABLE if not exists operations.utility.app_users (
  app_name STRING,
  user_id STRING,
  roles ARRAY<STRING>,
  metadata MAP<STRING, STRING>
);

INSERT INTO operations.utility.app_users (app_name, user_id, roles, metadata)
VALUES ('finance', 'chrismarshall.wi@icloud.com', array('admin'), NULL);



