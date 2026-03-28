import streamlit as st
from agents import Agents
from queue_jobs import JobQueue
from stack_versions import VersionStack
from logs import Logs
from pipeline import Pipeline

agents = Agents()
jobs = JobQueue()
versions = VersionStack()
logs = Logs()
pipeline = Pipeline()

for stage in ["Checkout", "Dependencias", "Linter", "Tests", "Deploy"]:
    pipeline.add_stage(stage)

st.title("Simulador CI/CD")

st.subheader("Agentes")
for k, v in agents.get_status().items():
    st.write(f"{k}: {v}")

job_name = st.text_input("Nuevo Job")

if st.button("Agregar Job"):
    if job_name:
        jobs.add_job(job_name)
        logs.add(f"Job agregado: {job_name}")

if st.button("Procesar Job"):
    for agent in agents.get_status():
        if agents.status[agent] == "Libre":
            job = jobs.get_job()
            if job:
                agents.status[agent] = f"Ocupado ({job})"
                logs.add(f"{job} en {agent}")
                version = f"v{len(versions.get_all())+1}"
                versions.push(version)
                logs.add(f"Deploy: {version}")
            break

if st.button("Rollback"):
    removed = versions.rollback()
    if removed:
        logs.add(f"Rollback: eliminado {removed}")
    else:
        logs.add("No hay rollback disponible")

st.subheader("Cola")
st.write(jobs.list_jobs())

st.subheader("Pipeline")
st.write(" -> ".join(pipeline.get_stages()))

st.subheader("Versiones")
st.write(versions.get_all())

st.subheader("Logs")
for log in logs.get_logs():
    st.text(log)
