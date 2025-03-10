import streamlit as st
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
import re
from collections import defaultdict

# Load Gemini API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# Backend Flask server URL
BASE_URL = "http://127.0.0.1:5000"

# Apply custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #f7f6f2;
            color: #333333;
        }
        .stApp {
            background-color: #fefefe;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: auto;
        }
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 8px;
        }
        .stButton>button {
            background-color: black;
            color: white;
            border-radius: 8px;
            padding: 8px 20px;
            border: none;
        }
        .stButton>button:hover {
            background-color: grey;
        }
        .task-row {
            padding: 10px;
            margin-bottom: 10px;
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            transition: all 0.3s ease-in-out;
        }
        .task-row:hover {
            background-color: #f1f1fc;
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

# Clear all tasks
def clear_all_tasks():
    try:
        requests.delete(f"{BASE_URL}/tasks")
    except Exception as e:
        st.error(f"❌ Failed to clear tasks: {e}")

# UI title
st.title("📚 AI Study Planner")

# Generate plan from Gemini
def generate_study_plan(goal_text):
    prompt = (
        f"Break down this study goal into a daily plan: '{goal_text}'. "
        "Give a numbered list (Day 1, Day 2...) with specific topics to study each day."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip().split("\n")
    except Exception as e:
        return [f"❌ Error: {str(e)}"]

# Fetch tasks from backend
def get_tasks():
    try:
        response = requests.get(f"{BASE_URL}/tasks")
        if response.status_code == 200:
            tasks = response.json()
            return sorted(tasks, key=lambda x: x['id'])  # Keep order
        else:
            return []
    except Exception:
        return []

# Add a task
def add_task(name):
    try:
        requests.post(f"{BASE_URL}/tasks", json={"name": name})
    except Exception as e:
        st.error(f"❌ Failed to add task: {e}")

# Update task completion
def update_task(task_id, completed):
    try:
        requests.put(f"{BASE_URL}/tasks/{task_id}", json={"completed": completed})
    except Exception as e:
        st.error(f"❌ Failed to update task: {e}")

# Delete a task
def delete_task(task_id):
    try:
        requests.delete(f"{BASE_URL}/tasks/{task_id}")
    except Exception as e:
        st.error(f"❌ Failed to delete task: {e}")

# Detect parent task
def is_parent_task(name):
    return bool(re.match(r"^(Month|Week|Year)\s*\d*", name, re.IGNORECASE))

# ✨ Generate AI Study Plan
goal = st.text_input("🎯 Describe your study goal (e.g., 'Prepare for DBMS external in 5 days')")
if st.button("✨ Generate Plan with AI"):
    if goal:
        plan = generate_study_plan(goal)
        if plan and plan[0].startswith("❌ Error"):
            st.error(plan[0])
        else:
            for day in plan:
                line = day.strip()
                if line and not line.startswith("###") and not line.startswith("- ["):
                    add_task(line)
            st.success("✅ Study plan generated and added to your task list!")
            st.rerun()
    else:
        st.warning("⚠️ Please enter a goal!")

# 📋 Show tasks
st.subheader("📌 Your Tasks")
tasks = get_tasks()

if not tasks:
    st.info("No tasks yet. Generate a plan or add manually!")

# Group child tasks under parents and auto-complete parents
from collections import defaultdict

parent_to_children = defaultdict(list)
parent_order = []
task_map = {t["id"]: t for t in tasks}
parent_id = None

for task in tasks:
    if is_parent_task(task["name"]):
        parent_id = task["id"]
        parent_order.append(parent_id)
    if parent_id:
        parent_to_children[parent_id].append(task)

# Auto-complete parents
for pid, group in parent_to_children.items():
    children = [t for t in group if t["id"] != pid]
    if children:
        if all(child["completed"] for child in children):
            if not task_map[pid]["completed"]:
                update_task(pid, True)
        else:
            if task_map[pid]["completed"]:
                update_task(pid, False)

# Render tasks in order with indentation
rendered_ids = set()

for task in tasks:
    if task["id"] in rendered_ids:
        continue

    is_parent = is_parent_task(task["name"])
    padding = "0px" if is_parent else "20px"
    weight = "bold" if is_parent else "normal"
    task_display = f"{'✅' if task['completed'] else '🔲'} {task['name']}"

    col1, col2, col3 = st.columns([6, 2, 2])
    with col1:
        st.markdown(
            f"<div class='task-row' style='padding-left: {padding}; font-weight: {weight};'>{task_display}</div>",
            unsafe_allow_html=True
        )

    with col2:
        if not is_parent and st.button("✔️", key=f"complete_{task['id']}"):
            update_task(task["id"], not task["completed"])
            st.rerun()

    with col3:
        if st.button("🗑️", key=f"delete_{task['id']}"):
            delete_task(task["id"])
            st.rerun()

    rendered_ids.add(task["id"])

# 🧹 Clear All Tasks
if tasks:
    st.markdown("---")
    if st.button("🧹 Clear All Tasks"):
        clear_all_tasks()
        st.rerun()

# ➕ Manual Task Input
st.markdown("---")
new_task = st.text_input("✍️ Add a task manually")
if st.button("Add Task"):
    if new_task:
        add_task(new_task)
        st.success("Task added!")
        st.rerun()

# 📄 PDF Export
def create_task_pdf(tasks):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 50
    line_height = 18

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, height - 50, "📚 AI Study Planner - Task List")
    c.setFont("Helvetica", 12)
    y = height - 80

    for task in tasks:
        indent = "    " if not is_parent_task(task["name"]) else ""
        status = "✅" if task['completed'] else "🔲"
        line = f"{indent}{status} {task['name']}"
        wrapped_lines = wrap(line, width=90)
        for wline in wrapped_lines:
            c.drawString(margin, y, wline)
            y -= line_height
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

# 🖨️ Download as PDF
if tasks:
    pdf_buffer = create_task_pdf(tasks)
    st.download_button(
        label="📄 Download Schedule as PDF",
        data=pdf_buffer,
        file_name="study_plan.pdf",
        mime="application/pdf"
    )
