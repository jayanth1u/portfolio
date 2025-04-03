import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64
from datetime import date

# ✅ Set Streamlit Page Config
st.set_page_config(page_title="Portfolio", page_icon="📌", layout="wide")

# 🔄 **Initialize Session State**
if "profile_photo" not in st.session_state:
    st.session_state["profile_photo"] = None
if "skills" not in st.session_state:
    st.session_state["skills"] = {}
if "projects" not in st.session_state:
    st.session_state["projects"] = {}
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "title" not in st.session_state:
    st.session_state["title"] = ""
if "dob" not in st.session_state:
    st.session_state["dob"] = date.today()
if "email" not in st.session_state:
    st.session_state["email"] = ""
if "phone" not in st.session_state:
    st.session_state["phone"] = ""
if "location" not in st.session_state:
    st.session_state["location"] = ""

# 📄 **PDF Generation Function**
def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Profile Photo in the Right Corner (PDF)
    if st.session_state["profile_photo"]:
        img = ImageReader(BytesIO(st.session_state["profile_photo"]))
        c.drawImage(img, width - 150, height - 100, width=100, height=100, mask='auto')

    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 50, st.session_state["name"])
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 70, st.session_state["title"])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 110, "📬 Contact Information")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 130, f"✉️ Email: {st.session_state['email']}")
    c.drawString(50, height - 150, f"📞 Phone: {st.session_state['phone']}")
    c.drawString(50, height - 170, f"📍 Address: {st.session_state['location']}")

    # 🔹 Add Skills to PDF
    y_position = height - 200
    if st.session_state["skills"]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, "🚀 Skills:")
        y_position -= 20
        c.setFont("Helvetica", 10)
        for skill, details in st.session_state["skills"].items():
            c.drawString(50, y_position, f"🔹 {skill}: {', '.join(details)}")
            y_position -= 20

    # 🔹 Add Projects to PDF
    if st.session_state["projects"]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, "📂 Projects:")
        y_position -= 20
        c.setFont("Helvetica", 10)
        for project, description in st.session_state["projects"].items():
            c.drawString(50, y_position, f"🔹 {project}: {description}")
            y_position -= 20

    c.save()
    buffer.seek(0)
    return buffer

# 🔗 **Navbar**
st.markdown("<h1 style='text-align: center; color: white; background-color:#2c3e50; padding: 10px; border-radius: 8px;'>🚀 My Portfolio</h1>", unsafe_allow_html=True)

# 📍 **Navigation Bar**
page = st.radio("", ["🏠 Home", "💡 Skills", "📂 Projects", "📄 View Portfolio"], horizontal=True)

# 🏠 **Home Page**
if page == "🏠 Home":
    st.header("👤 Personal Details")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.session_state["name"] = st.text_input("📛 Name:", value=st.session_state["name"])
        st.session_state["title"] = st.text_input("🎓 Title:", value=st.session_state["title"])
        st.session_state["dob"] = st.date_input("📅 Date of Birth:", st.session_state["dob"])
        st.session_state["email"] = st.text_input("✉️ Email:", value=st.session_state["email"])
        st.session_state["phone"] = st.text_input("📞 Phone:", value=st.session_state["phone"])
        st.session_state["location"] = st.text_area("📍 Address:", value=st.session_state["location"])

    with col2:
        st.markdown("#### 📷 Upload Profile Photo")
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.session_state["profile_photo"] = uploaded_file.read()
        
        if st.session_state["profile_photo"]:
            encoded_image = base64.b64encode(st.session_state["profile_photo"]).decode()
            st.markdown(
                f"""
                <style>
                .profile-pic {{
                    border-radius: 50%;
                    width: 150px;
                    height: 150px;
                    object-fit: cover;
                    display: block;
                    margin: auto;
                }}
                </style>
                <img src="data:image/png;base64,{encoded_image}" class="profile-pic">
                """,
                unsafe_allow_html=True,
            )

# 💡 **Skills Page**
elif page == "💡 Skills":
    st.header("🚀 My Skills")
    skill_name = st.text_input("Skill Name:")
    skill_details = st.text_area("Skill Details (comma-separated):")

    if st.button("Add Skill"):
        if skill_name and skill_details:
            st.session_state["skills"][skill_name] = skill_details.split(", ")

    if st.session_state["skills"]:
        st.subheader("Existing Skills:")
        for skill, details in st.session_state["skills"].items():
            st.write(f"**{skill}:** {', '.join(details)}")

# 📂 **Projects Page**
elif page == "📂 Projects":
    st.header("📂 My Projects")
    
    # Input fields for new project
    project_name = st.text_input("Project Name:")
    project_description = st.text_area("Project Description:")
    
    if st.button("Add Project"):
        if project_name and project_description:
            st.session_state["projects"][project_name] = project_description
    
    # Display existing projects with title and description properly formatted
    if st.session_state["projects"]:
        st.subheader("Existing Projects:")
        for project, description in st.session_state["projects"].items():
            st.markdown(f"**{project}**\n\n{description}")  # ✅ Title on top, description below


# 📄 **View Portfolio Page**
elif page == "📄 View Portfolio":
    st.header("📄 My Portfolio")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("👤 Personal Details")
        st.write(f"**📛 Name:** {st.session_state['name']}")
        st.write(f"**🎓 Title:** {st.session_state['title']}")
        st.write(f"**📅 Date of Birth:** {st.session_state['dob']}")
        st.write(f"**✉️ Email:** {st.session_state['email']}")
        st.write(f"**📞 Phone:** {st.session_state['phone']}")
        st.write(f"**📍 Address:** {st.session_state['location']}")

        st.subheader("🚀 Skills")
        for skill, details in st.session_state["skills"].items():
            st.write(f"**{skill}:** {', '.join(details)}")

        st.subheader("📂 Projects")
        for project, description in st.session_state["projects"].items():
            st.markdown(f"**{project}**  \n{description}")  # ✅ Title on top, description below

        
    with col2:
        if st.session_state["profile_photo"]:
            encoded_image = base64.b64encode(st.session_state["profile_photo"]).decode()
            st.markdown(
                f"""
                <style>
                .profile-pic {{
                    border-radius: 50%;
                    width: 150px;
                    height: 150px;
                    object-fit: cover;
                    display: block;
                    margin: auto;
                    position: relative;
                    top: -65px; 
                }}
                </style>
                <img src="data:image/png;base64,{encoded_image}" class="profile-pic">
                """,
                unsafe_allow_html=True,
            )    
           

    st.sidebar.header("📥 Download Portfolio")
    if st.sidebar.button("Generate PDF"):
        pdf_file = generate_pdf()
        st.sidebar.download_button("📄 Download Portfolio", pdf_file, "Portfolio.pdf", "application/pdf")
