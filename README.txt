mysql -h localhost -u root lab6_database < create_tables.sql -p

alembic revision -m "add models" --autogenerate

alembic upgrade head