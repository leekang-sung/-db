# export_db.py
import duckdb

# 1. DuckDB 연결
con = duckdb.connect('madang.duckdb') # 이 이름으로 파일이 생깁니다

# 2. 리눅스 MySQL 연결 (빨대 꽂기)
con.execute("INSTALL mysql; LOAD mysql;")
con.execute("ATTACH 'host=192.168.88.130 user=root1 password=1234 database=madang' AS mysqldb (TYPE MYSQL)")

# 3. 데이터 복사 (MySQL -> 내 컴퓨터 파일)
print("데이터 복사 중...")
con.execute("CREATE TABLE Customer AS SELECT * FROM mysqldb.Customer")
con.execute("CREATE TABLE Book AS SELECT * FROM mysqldb.Book")
con.execute("CREATE TABLE Orders AS SELECT * FROM mysqldb.Orders")

print("완료! madang.duckdb 파일이 생성되었습니다.")
con.close()