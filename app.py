import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AI ERP System", page_icon="🎓", layout="wide")
st.title("🎓 AI-Powered Educational ERP System")
st.caption("Student, Attendance, Fees, Results and AI Performance Prediction")

DATA="data"
students=pd.read_csv(os.path.join(DATA,"students.csv"))
attendance=pd.read_csv(os.path.join(DATA,"attendance.csv"))
marks=pd.read_csv(os.path.join(DATA,"marks.csv"))
fees=pd.read_csv(os.path.join(DATA,"fees.csv"))

c1,c2,c3,c4=st.columns(4)
c1.metric("Students", len(students))
c2.metric("Avg Attendance", f"{attendance.attendance_percentage.mean():.1f}%")
c3.metric("Fees Pending", f"₹{fees.pending_fees.sum():,.0f}")
c4.metric("Avg Internal", f"{marks.internal.mean():.1f}")

st.subheader("Student Overview")
overview=students.merge(attendance,on="student_id").merge(marks,on="student_id").merge(fees,on="student_id")
st.dataframe(overview, use_container_width=True)

st.sidebar.header("ERP Modules")
module=st.sidebar.radio("Select Module",["Dashboard","Students","Attendance","Fees","Results","AI Prediction"])

if module=="Students":
    st.subheader("Student Management")
    st.dataframe(students, use_container_width=True)

elif module=="Attendance":
    st.subheader("Attendance Management")
    st.dataframe(attendance, use_container_width=True)
    st.warning(f"{(attendance.attendance_percentage < 75).sum()} student(s) have attendance below 75%.")

elif module=="Fees":
    st.subheader("Fees Management")
    st.dataframe(fees, use_container_width=True)

elif module=="Results":
    st.subheader("Result Management")
    st.dataframe(marks, use_container_width=True)

elif module=="AI Prediction":
    st.subheader("🤖 AI Student Performance Prediction")
    st.info("Demo prediction based on attendance, internal marks, assignment marks and previous CGPA.")
    sid=st.selectbox("Select Student", students.student_id.tolist())
    row=overview[overview.student_id==sid].iloc[0]
    score=(row.attendance_percentage*0.30)+(row.internal*0.30)+(row.assignment*0.20)+(row.previous_cgpa*10*0.20)
    if score >= 75:
        result="Good"
    elif score >= 60:
        result="Average"
    else:
        result="At Risk"
    st.metric("Predicted Performance", result)
    st.progress(min(int(score),100))
    st.write(f"Prediction score: **{score:.1f}/100**")
