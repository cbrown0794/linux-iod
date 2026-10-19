# st-app.py
# launches a streamlit app for the dashboard with all graphs
from get_data import connect_to
import streamlit as st
import pandas as pd
import time

# class to hold server information
class ServerInfo:
	def __init__(self, name: str, addr: str, port: int, tab: st.delta_generator = None):
		self.name = name
		self.addr = addr
		self.port = port
		self.tab = tab

	def __str__(self):
		return f"name: {self.name}; address: {self.addr}:{self.port}"

# constants for server info
SERVERS = {
	"cb": ServerInfo("cbrown", "10.0.1.2", 6767),
	"sw": ServerInfo("sw-server", "10.0.2.2", 6767),
	"ah": ServerInfo("N/A", "10.0.3.2", 6767),
	"rm": ServerInfo("rmoses", "10.0.4.2", 6767),
}

METRICS = ["cpu", "vm", "disk", "io_r", "io_w"]


st.header("Linux Infrastructure Observabililty Dashboard", width="content")

# select options
col1, col2 = st.columns(2)

with col1:
	current_metrics = st.multiselect("Metrics:", METRICS, default="cpu")

with col2:
	history_len = st.number_input("History Length:", min_value=60, value=120)

# tabs for each server
SERVERS["cb"].tab, SERVERS["sw"].tab, SERVERS["ah"].tab, SERVERS["rm"].tab = st.tabs([
	SERVERS["cb"].name,
	SERVERS["sw"].name,
	SERVERS["ah"].name,
	SERVERS["rm"].name,
])

if "data" not in st.session_state:
	st.session_state["data"] = {
		server.addr: pd.DataFrame({"time": pd.Series(dtype=float), **{metric: pd.Series(dtype=float) for metric in METRICS}}) for server in SERVERS.values()
	}

# fetch data using connect_to() every 5 seconds
@st.fragment(run_every="5s")
def update_data(server):
	try: st.session_state["data"][server.addr] = pd.concat([st.session_state["data"][server.addr], pd.DataFrame([connect_to(server.addr, server.port)])])
	except RuntimeError as e: st.error(e)
	df = st.session_state["data"][server.addr]
	df = df[df["time"] > time.time() - history_len]
	df = df.assign(time=pd.to_datetime(df["time"], unit="s"))
	st.area_chart(df, x="time", y=current_metrics)

for server in SERVERS.values():
	with server.tab:
		update_data(server)
