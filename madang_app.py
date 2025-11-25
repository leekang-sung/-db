import streamlit as st
import duckdb
import os

st.title("📱 24시간 꺼지지 않는 마당서점")

# 1. 데이터베이스 연결
if os.path.exists('madang.duckdb'):
    con = duckdb.connect(database='madang.duckdb', read_only=True)
else:
    st.error("🚨 'madang.duckdb' 파일이 없습니다! GitHub에 파일을 올렸는지 확인해주세요.")
    st.stop()

# 2. 검색창
name = st.text_input("고객명")

if name:
    # --- [첫 번째 결과] 고객 정보만 따로 조회 ---
    # f-string을 써서 입력한 이름의 정보를 가져옵니다.
    sql_user = f"SELECT * FROM Customer WHERE name = '{name}'"
    user_df = con.execute(sql_user).df()

    if user_df.empty:
        st.warning(f"'{name}' 고객님을 찾을 수 없습니다.")
    else:
        # 고객 정보가 있으면 화면에 출력
        st.subheader(f"📋 '{name}'님 회원 정보")
        st.table(user_df)  # 표 형태로 깔끔하게 보여줍니다.

        # --- [두 번째 결과] 주문 내역 조회 (JOIN 사용) ---
        st.subheader(f"📚 '{name}'님 구매 내역")

        sql_order = f"""
            SELECT b.bookname, o.orderdate, o.saleprice 
            FROM Customer c, Book b, Orders o 
            WHERE c.custid = o.custid 
            AND o.bookid = b.bookid 
            AND c.name = '{name}'
        """

        order_df = con.execute(sql_order).df()

        if order_df.empty:
            st.info("구매한 책이 없습니다.")
        else:
            st.dataframe(order_df)  # 스크롤 가능한 표로 보여줍니다.