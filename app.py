import streamlit as st
import time
from agents import Agents
from queue_jobs import JobQueue
from stack_versions import VersionStack
from logs import Logs
from pipeline import Pipeline

st.set_page_config(page_title="GitHub CI/CD 💖", layout="wide")

# INICIALIZAR ESTADOS
if "agents" not in st.session_state:
    st.session_state.agents = Agents()
    st.session_state.jobs = JobQueue()
    st.session_state.versions = VersionStack()
    st.session_state.logs = Logs()
    st.session_state.pipeline = Pipeline()

    for stage in ["Checkout", "Dependencias", "Linter", "Tests", "Deploy"]:
        st.session_state.pipeline.add_stage(stage)

agents = st.session_state.agents
jobs = st.session_state.jobs
versions = st.session_state.versions
logs = st.session_state.logs
pipeline = st.session_state.pipeline

st.title("💖 GitHub Actions Simulator")
st.caption("CI/CD con estructuras de datos")

# RENDER PIPELINE
pipeline_container = st.empty()

def render_pipeline():
    cols = pipeline_container.columns(len(pipeline.get_stages()))
    for i, stage in enumerate(pipeline.get_stages()):
        with cols[i]:
            if stage.status == "success":
                st.success(f"✔ {stage.stage}")
            elif stage.status == "running":
                st.warning(f"⏳ {stage.stage}")
            else:
                st.info(f"• {stage.stage}")

render_pipeline()

# INPUT NUEVO JOB
job = st.text_input("Nuevo Job")

if st.button("Agregar Job"):
    if job:
        jobs.add_job(job)
        logs.add(f"[QUEUE] {job}")

# EJECUTAR PIPELINE
if st.button("Ejecutar Pipeline"):
    job = jobs.get_job()

    if job:
        agent = agents.assign(job)

        if agent:
            logs.add(f"[RUNNING] {job} en {agent}")

            stages = pipeline.get_stages()
            progress = st.progress(0)

            
            pipeline.reset()

            for i, stage in enumerate(stages):
                stage.status = "running"
                render_pipeline()

                logs.add(f"[RUNNING] {stage.stage}")
                time.sleep(1)

                stage.status = "success"
                render_pipeline()

                logs.add(f"[SUCCESS] {stage.stage}")
                progress.progress((i+1)/len(stages))

            
            version = f"v{len(versions.get_all())+1}"
            versions.push(version)

            logs.add(f"[DEPLOY] {version}")
            st.success("🚀 Pipeline completado")

            agents.release(agent)

        else:
            logs.add("[ERROR] No hay agentes disponibles")

#---------------------------
st.subheader("Cola")
st.write(jobs.list_jobs())

#---------------------------
st.subheader("Versiones")
st.write(versions.get_all())

if st.button("Rollback"):
    removed = versions.rollback()
    if removed:
        logs.add(f"[ROLLBACK] {removed}")

# ---------------- LOGS ----------------
st.subheader("Logs")
for log in logs.get_logs():
    st.code(log)