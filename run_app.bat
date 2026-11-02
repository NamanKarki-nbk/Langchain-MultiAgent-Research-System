@echo off
title NexusAgent Multi-Agent Research System
echo =======================================================
echo  Launching LangChain Multi-Agent Research System UI...
echo =======================================================
if exist "D:\conda_envs\aii_agents\python.exe" (
    "D:\conda_envs\aii_agents\python.exe" -m streamlit run app.py
) else (
    streamlit run app.py
)
pause
