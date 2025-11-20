import streamlit as st
import duckdb
import pandas as pd

# 1. 화면 구성
st.title("📱 DuckDB 마당서점 검색")
name = st.text_input("고객명", "")  # 기본값을 빈 문자열로 설정

# 2. DuckDB 연결 및 MySQL 연동
# DuckDB를 메모리 모드로 실행
con = duckdb.connect(database=':memory:')

# MySQL 확장 기능 설치 및 로드 (최초 1회 필요)
con.execute("INSTALL mysql; LOAD mysql;")

# 3. 리눅스 MySQL 서버에 '빨대 꽂기' (ATTACH)
# 사용자가 주신 정보: user='root1', passwd='1234', host='192.168.88.130', db='madang'
try:
    con.execute(f"""
        ATTACH 'host=192.168.88.130 user=root1 password=1234 database=madang' 
        AS mysqldb (TYPE MYSQL);
    """)
except Exception as e:
    st.error(f"DB 연결 실패: {e}")
    st.stop()

# 4. 검색 및 결과 출력
if name:
    # SQL 쿼리 작성 (DuckDB에 연결된 'mysqldb'를 앞에 붙여야 합니다)
    # f-string을 사용하여 입력받은 이름을 쿼리에 넣습니다.
    sql = f"""
        SELECT c.name, b.bookname, o.orderdate, o.saleprice 
        FROM mysqldb.Customer c, mysqldb.Book b, mysqldb.Orders o 
        WHERE c.custid = o.custid 
        AND o.bookid = b.bookid 
        AND c.name = '{name}'
    """

    try:
        # DuckDB로 쿼리 실행 후 바로 데이터프레임(df)으로 변환
        df = con.execute(sql).df()

        if df.empty:
            st.warning("검색 결과가 없습니다.")
        else:
            st.write(df)

    except Exception as e:
        st.error(f"쿼리 오류: {e}")