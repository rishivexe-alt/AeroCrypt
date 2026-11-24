from __future__ import annotations
import math, random, sys, time
from collections import deque
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from aerocrypt.protocol import parse_telemetry, parse_link_metrics, parse_security_status, TelemetryPacket
from aerocrypt.serial_reader import available_ports, open_receiver, read_available_lines

st.set_page_config(page_title="AeroCrypt | UAV Telemetry", page_icon="🛰️", layout="wide")
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#080d15}[data-testid="stSidebar"]{background:#0d1520;border-right:1px solid #1d2a39}
.block-container{padding-top:1.4rem;max-width:1500px}.hero{padding:1.3rem 1.5rem;border:1px solid #243346;border-radius:16px;background:linear-gradient(120deg,#101e30,#0c1420 65%,#111c2a);margin-bottom:1rem}
.hero h1{letter-spacing:.09em;font-size:2rem;margin:0;color:#e7eef8}.hero p{color:#8fa3ba;margin:.4rem 0 0}.metric-card{background:#101923;border:1px solid #233244;border-radius:13px;padding:1rem 1.1rem;min-height:105px;margin-bottom:.65rem}
.metric-label{color:#8294a9;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase}.metric-value{color:#e6edf6;font-size:1.65rem;font-weight:700;margin-top:.35rem}.metric-unit{color:#8193a8;font-size:.82rem;margin-left:.25rem}
.pill{display:inline-block;border-radius:30px;padding:.32rem .7rem;font-size:.76rem;font-weight:700}.ok{background:#103426;color:#42d392;border:1px solid #1c6748}.warn{background:#3a2b12;color:#f4c15e;border:1px solid #74531d}
.section-title{color:#dce6f2;letter-spacing:.1em;font-size:1rem;font-weight:750;padding-bottom:.55rem;border-bottom:1px solid #253243;margin:1.3rem 0 .9rem}
</style>""", unsafe_allow_html=True)

def init_state():
    defaults={"history":deque(maxlen=500),"serial":None,"mode":"Demo mode","security":{"verified":False,"status":"WAITING_FOR_PACKET"},"link":{"rssi_dbm":None,"snr_db":None},"accepted":0,"rejected":0,"paused":False,"demo_counter":2270}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v

def add_packet(packet):
    st.session_state.history.append(packet.to_dict()); st.session_state.accepted+=1

def consume_lines(lines):
    for line in lines:
        security=parse_security_status(line)
        if security:
            st.session_state.security=security
            if not security["verified"]: st.session_state.rejected+=1
            continue
        link=parse_link_metrics(line)
        if link:
            st.session_state.link={"rssi_dbm":link.rssi_dbm,"snr_db":link.snr_db}; continue
        prefix="STREAMLIT_TELEMETRY:"
        if line.startswith(prefix):
            try:
                add_packet(parse_telemetry(line[len(prefix):]))
                st.session_state.security={"verified":True,"status":"VERIFIED"}
            except ValueError: st.session_state.rejected+=1

def demo_tick():
    n=st.session_state.demo_counter; st.session_state.demo_counter+=1; phase=n/4
    packet=TelemetryPacket(n,28.4+.22*math.sin(phase/5),918+.4*math.cos(phase/7),
        .006+random.uniform(-.004,.004),.058+random.uniform(-.008,.008),1.009+random.uniform(-.012,.012),
        .42+random.uniform(-.08,.08),1.06+random.uniform(-.12,.12),.08+random.uniform(-.08,.08))
    packet.received_at=time.strftime("%Y-%m-%d %H:%M:%S"); add_packet(packet)
    st.session_state.security={"verified":True,"status":"DEMO_AUTHENTICATED"}
    st.session_state.link={"rssi_dbm":-43+random.randint(-3,2),"snr_db":round(5.2+random.uniform(-1.2,1.2),2)}

def metric(label,value,unit=""):
    u=f'<span class="metric-unit">{unit}</span>' if unit else ""
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}{u}</div></div>',unsafe_allow_html=True)

init_state()
with st.sidebar:
    st.markdown("## SYSTEM CONFIGURATION")
    mode=st.radio("Input source",["Demo mode","Serial mode"],index=0 if st.session_state.mode=="Demo mode" else 1)
    st.session_state.mode=mode
    if mode=="Serial mode":
        ports=available_ports(); selected=st.selectbox("Serial port",ports or ["No serial ports detected"]); baud=st.selectbox("Baud rate",[115200,57600,38400,19200,9600],index=0)
        a,b=st.columns(2)
        with a:
            if st.button("Connect",use_container_width=True,disabled=not ports):
                try:
                    if st.session_state.serial and st.session_state.serial.is_open: st.session_state.serial.close()
                    st.session_state.serial=open_receiver(selected,baud); st.success(f"Connected: {selected}")
                except Exception as exc: st.error(f"Serial connection failed: {exc}")
        with b:
            if st.button("Disconnect",use_container_width=True):
                if st.session_state.serial: st.session_state.serial.close()
                st.session_state.serial=None
        st.caption("ESP32 ground receiver · USB serial · 115200 baud")
    else: st.info("Demo mode streams representative values to preview the monitoring interface.")
    st.divider(); st.session_state.paused=st.checkbox("Pause live updates",value=st.session_state.paused)
    a,b=st.columns(2)
    with a:
        if st.button("Clear history",use_container_width=True):
            st.session_state.history.clear(); st.session_state.accepted=0; st.session_state.rejected=0
    with b:
        if st.button("Refresh",use_container_width=True): st.rerun()
    st.caption("AeroCrypt · Ground station console")

if not st.session_state.paused:
    if mode=="Demo mode": demo_tick()
    elif st.session_state.serial and st.session_state.serial.is_open:
        try: consume_lines(read_available_lines(st.session_state.serial))
        except Exception as exc: st.warning(f"Serial read interrupted: {exc}")

history=list(st.session_state.history); df=pd.DataFrame(history)
st.markdown('<div class="hero"><h1>AEROCRYPT</h1><p>AES-128-GCM secured long-range UAV telemetry · Ground station monitoring console</p></div>',unsafe_allow_html=True)
connected=mode=="Demo mode" or (st.session_state.serial is not None and st.session_state.serial.is_open)
security_ok=bool(st.session_state.security.get("verified"))
c1,c2,c3,c4=st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">RECEIVER</div><p><span class="pill {"ok" if connected else "warn"}">● {"CONNECTED" if connected else "DISCONNECTED"}</span></p></div>',unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">LORA LINK</div><div class="metric-value">{len(history)}</div><div>Packets accepted</div></div>',unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">ENCRYPTION</div><p><span class="pill {"ok" if security_ok else "warn"}">● {"AES-GCM VERIFIED" if security_ok else "WAITING FOR PACKET"}</span></p></div>',unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div class="metric-label">TELEMETRY</div><p><span class="pill {"ok" if history else "warn"}">● {"LIVE DATA" if history else "NO DATA"}</span></p></div>',unsafe_allow_html=True)
if not history: st.info("Waiting for telemetry. Connect the ESP32 ground receiver or switch to Demo mode.")
if history:
    latest=history[-1]; st.markdown('<div class="section-title">LATEST PACKET</div>',unsafe_allow_html=True)
    st.markdown(f"### PACKET #{latest['packet']} · `{latest['received_at']}`")
    cols=st.columns(4)
    cards=[("TEMPERATURE",f"{latest['temperature_c']:.2f}","°C"),("PRESSURE",f"{latest['pressure_hpa']:.2f}","hPa"),("ACCEL X",f"{latest['accel_x_g']:.3f}","g"),("ACCEL Y",f"{latest['accel_y_g']:.3f}","g"),("ACCEL Z",f"{latest['accel_z_g']:.3f}","g"),("GYRO X",f"{latest['gyro_x_dps']:.2f}","°/s"),("GYRO Y",f"{latest['gyro_y_dps']:.2f}","°/s"),("GYRO Z",f"{latest['gyro_z_dps']:.2f}","°/s"),("RSSI",str(st.session_state.link.get("rssi_dbm") if st.session_state.link.get("rssi_dbm") is not None else "—"),"dBm"),("SNR",str(st.session_state.link.get("snr_db") if st.session_state.link.get("snr_db") is not None else "—"),"dB")]
    for i,(label,value,unit) in enumerate(cards):
        with cols[i%4]: metric(label,value,unit)
    st.markdown('<div class="section-title">MOTION TELEMETRY</div>',unsafe_allow_html=True); plot_df=df.tail(200); left,right=st.columns(2)
    with left:
        fig=go.Figure()
        for key,label in [("gyro_x_dps","gyro_x"),("gyro_y_dps","gyro_y"),("gyro_z_dps","gyro_z")]: fig.add_trace(go.Scatter(x=plot_df.packet,y=plot_df[key],mode="lines",name=label))
        fig.update_layout(title="Gyroscope vs Packet",xaxis_title="Packet number",yaxis_title="Angular rate (°/s)",template="plotly_dark",height=330,margin=dict(l=10,r=10,t=45,b=10),legend=dict(orientation="h")); st.plotly_chart(fig,use_container_width=True)
    with right:
        fig=go.Figure()
        for key,label in [("accel_x_g","accel_x"),("accel_y_g","accel_y"),("accel_z_g","accel_z")]: fig.add_trace(go.Scatter(x=plot_df.packet,y=plot_df[key],mode="lines",name=label))
        fig.update_layout(title="Acceleration vs Packet",xaxis_title="Packet number",yaxis_title="Acceleration (g)",template="plotly_dark",height=330,margin=dict(l=10,r=10,t=45,b=10),legend=dict(orientation="h")); st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="section-title">GPS TELEMETRY</div>',unsafe_allow_html=True); a,b,c=st.columns(3); has_gps=latest.get("latitude") is not None
    with a: metric("LATITUDE",f"{latest['latitude']:.6f}" if has_gps else "—")
    with b: metric("LONGITUDE",f"{latest['longitude']:.6f}" if has_gps else "—")
    with c: metric("SATELLITES",str(latest["satellites"]) if has_gps else "—")
    if not has_gps: st.caption("GPS fields appear when the extended GPS telemetry schema is transmitted by the airborne node.")
    st.markdown('<div class="section-title">TELEMETRY HISTORY</div>',unsafe_allow_html=True)
    cols=["packet","temperature_c","pressure_hpa","accel_x_g","accel_y_g","accel_z_g","gyro_x_dps","gyro_y_dps","gyro_z_dps","received_at"]
    st.dataframe(df[cols].tail(100).iloc[::-1],use_container_width=True,hide_index=True)
    st.download_button("Download telemetry CSV",df.to_csv(index=False).encode("utf-8"),file_name="aerocrypt_telemetry.csv",mime="text/csv")
st.markdown('<div class="section-title">GROUND-STATION STATUS</div>',unsafe_allow_html=True)
a,b,c=st.columns(3)
with a: metric("PACKETS ACCEPTED",str(st.session_state.accepted))
with b: metric("PACKETS REJECTED",str(st.session_state.rejected))
with c: metric("LAST RSSI",f"{st.session_state.link.get('rssi_dbm')} dBm" if st.session_state.link.get("rssi_dbm") is not None else "—")
st.caption("AeroCrypt · Secure telemetry pipeline · ESP32 / SX1278 / AES-128-GCM")
if not st.session_state.paused: time.sleep(.7); st.rerun()
