import streamlit as st
import duckdb
import os

st.title("📱 24시간 꺼지지 않는 마당서점")

# 1. DB 연결 (IP 주소 대신 파일을 사용합니다!)
# GitHub에 'madang.duckdb' 파일을 꼭 같이 올려야 작동합니다.
if os.path.exists('madang.duckdb'):
    # read_only=True로 해서 안전하게 파일만 읽습니다.
    con = duckdb.connect(database='madang.duckdb', read_only=True)
else:
    st.error("🚨 중요: 'madang.duckdb' 파일이 없습니다! GitHub에 파일을 올렸는지 확인해주세요.")
    st.stop()

# 2. 검색 기능
name = st.text_input("고객명")

if name:
    # 파일 DB를 쓸 때는 테이블 앞에 'mysqldb.'을 붙이지 않습니다.
    sql = f"""
        SELECT c.name, b.bookname, o.orderdate, o.saleprice 
        FROM Customer c, Book b, Orders o 
        WHERE c.custid = o.custid 
        AND o.bookid = b.bookid 
        AND c.name = '{name}'
    """

    try:
        result = con.execute(sql).df()
        st.write(result)
    except Exception as e:
        st.error(f"오류: {e}")

# (보너스) 데이터가 잘 들어있나 확인하는 버튼
if st.checkbox("전체 책 목록 보기"):
    st.write(con.execute("SELECT * FROM Book").df())