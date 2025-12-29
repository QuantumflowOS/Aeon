# dashboard.py
"""
Enhanced Streamlit dashboard with real-time monitoring and visualization.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="ÆEON Control Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = st.sidebar.text_input("API URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 ÆEON Control Center</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Settings")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Context Control", "Memory Explorer", "Protocol Manager", "Analytics"]
)


def get_system_health():
    """Fetch system health from API."""
    try:
        response = requests.get(f"{API_URL}/system/health", timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


def get_memory():
    """Fetch memory from API."""
    try:
        response = requests.get(f"{API_URL}/memory", timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


# ============================================
# DASHBOARD PAGE
# ============================================
if page == "Dashboard":
    st.header("📊 System Overview")
    
    # Real-time metrics
    col1, col2, col3, col4 = st.columns(4)
    
    health = get_system_health()
    
    if health:
        with col1:
            st.metric("Status", "🟢 Healthy", "Online")
        with col2:
            st.metric("Protocols", health.get("protocol_count", 0))
        with col3:
            st.metric("Memory Items", health.get("memory_items", 0))
        with col4:
            context = health.get("context", {})
            st.metric("Current Emotion", context.get("emotion", "N/A"))
        
        # Current Context
        st.subheader("🎯 Current Context")
        context_df = pd.DataFrame([context])
        st.dataframe(context_df, use_container_width=True)
        
        # Protocol Performance
        st.subheader("📈 Protocol Performance")
        protocols = health.get("protocols", [])
        
        if protocols:
            df = pd.DataFrame(protocols)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Reward bar chart
                fig = px.bar(
                    df, 
                    x="name", 
                    y="reward",
                    title="Protocol Rewards",
                    color="reward",
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Execution pie chart
                fig = px.pie(
                    df,
                    values="executions",
                    names="name",
                    title="Protocol Execution Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Cannot connect to AEON API. Make sure the server is running.")


# ============================================
# CONTEXT CONTROL PAGE
# ============================================
elif page == "Context Control":
    st.header("🎮 Context Control")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Update Context")
        
        emotion = st.selectbox(
            "Emotion",
            ["neutral", "happy", "sad", "angry", "excited", "anxious", "calm"]
        )
        
        intent = st.selectbox(
            "Intent",
            ["none", "work", "rest", "create", "learn", "social", "focus"]
        )
        
        environment = st.text_input("Environment", "default")
        
        if st.button("🚀 Update Context", use_container_width=True):
            try:
                response = requests.post(
                    f"{API_URL}/context/update",
                    json={
                        "emotion": emotion,
                        "intent": intent,
                        "environment": environment
                    }
                )
                if response.status_code == 200:
                    st.success("✅ Context updated successfully!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")
        
        st.divider()
        
        st.subheader("Execute Agent")
        
        if st.button("▶️ Run Agent", use_container_width=True):
            with st.spinner("Running agent..."):
                try:
                    response = requests.post(f"{API_URL}/agent/run")
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Agent executed successfully!")
                        
                        # Display results
                        agent_result = result.get("result", {})
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Protocol Used", agent_result.get("protocol", "N/A"))
                        with col_b:
                            st.metric("Reward", agent_result.get("reward", "N/A"))
                        
                        st.info(f"💭 **Thought**: {agent_result.get('thought', 'N/A')}")
                        st.success(f"⚡ **Action**: {agent_result.get('action', 'N/A')}")
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection error: {e}")
    
    with col2:
        st.subheader("Quick Actions")
        
        if st.button("😊 Happy Mode", use_container_width=True):
            requests.post(f"{API_URL}/context/update", 
                         json={"emotion": "happy", "intent": "create"})
            st.success("Switched to Happy Mode")
        
        if st.button("🎯 Focus Mode", use_container_width=True):
            requests.post(f"{API_URL}/context/update",
                         json={"emotion": "neutral", "intent": "work"})
            st.success("Switched to Focus Mode")
        
        if st.button("😔 Support Mode", use_container_width=True):
            requests.post(f"{API_URL}/context/update",
                         json={"emotion": "sad", "intent": "rest"})
            st.success("Switched to Support Mode")
        
        if st.button("💤 Rest Mode", use_container_width=True):
            requests.post(f"{API_URL}/context/update",
                         json={"emotion": "calm", "intent": "rest"})
            st.success("Switched to Rest Mode")


# ============================================
# MEMORY EXPLORER PAGE
# ============================================
elif page == "Memory Explorer":
    st.header("🧠 Memory Explorer")
    
    memory_data = get_memory()
    
    if memory_data and memory_data.get("status") == "success":
        memory = memory_data.get("memory", {})
        
        # Tabs for different memory types
        tab1, tab2, tab3 = st.tabs(["Semantic", "Episodic", "Statistics"])
        
        with tab1:
            st.subheader("Semantic Memory")
            semantic = memory.get("semantic", [])
            if semantic:
                st.write(f"Total items: {len(semantic)}")
                for item in semantic[-10:]:  # Show last 10
                    st.text(f"• {item}")
            else:
                st.info("No semantic memories yet")
        
        with tab2:
            st.subheader("Episodic Memory")
            episodic = memory.get("episodic", [])
            if episodic:
                st.write(f"Total events: {len(episodic)}")
                
                # Create dataframe
                events = []
                for event in episodic[-20:]:  # Show last 20
                    events.append({
                        "Time": event.get("timestamp", "N/A"),
                        "Emotion": event.get("context", {}).get("emotion", "N/A"),
                        "Intent": event.get("context", {}).get("intent", "N/A"),
                        "Action": event.get("action", "N/A")[:50] + "..."
                    })
                
                df = pd.DataFrame(events)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No episodic memories yet")
        
        with tab3:
            st.subheader("Memory Statistics")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Semantic Items", len(memory.get("semantic", [])))
            with col2:
                st.metric("Episodic Events", len(memory.get("episodic", [])))
    else:
        st.warning("⚠️ No memory data available")


# ============================================
# PROTOCOL MANAGER PAGE
# ============================================
elif page == "Protocol Manager":
    st.header("🔧 Protocol Manager")
    
    try:
        response = requests.get(f"{API_URL}/protocols")
        if response.status_code == 200:
            data = response.json()
            protocols = data.get("protocols", [])
            
            if protocols:
                df = pd.DataFrame(protocols)
                
                st.subheader("Protocol Overview")
                st.dataframe(df, use_container_width=True)
                
                st.subheader("Protocol Analysis")
                
                # Performance ranking
                df_sorted = df.sort_values("reward", ascending=False)
                fig = px.bar(
                    df_sorted,
                    x="name",
                    y="reward",
                    color="executions",
                    title="Protocol Performance Ranking",
                    labels={"reward": "Reward Score", "executions": "Times Executed"}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Execution timeline
                st.subheader("Execution Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Protocols", len(protocols))
                with col2:
                    st.metric("Avg Reward", f"{df['reward'].mean():.2f}")
                with col3:
                    st.metric("Total Executions", int(df["executions"].sum()))
            else:
                st.info("No protocols registered yet")
        else:
            st.error(f"❌ Error fetching protocols: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Connection error: {e}")


# ============================================
# ANALYTICS PAGE
# ============================================
elif page == "Analytics":
    st.header("📊 Advanced Analytics")
    
    st.info("🚧 Advanced analytics coming soon! This will include:")
    st.write("- Real-time performance trends")
    st.write("- Protocol evolution tracking")
    st.write("- Context pattern analysis")
    st.write("- Predictive modeling")
    st.write("- A/B testing results")


# Footer
st.sidebar.divider()
st.sidebar.caption("ÆEON v0.1.0")
st.sidebar.caption("Autonomous Evolving Orchestration Network")

# Auto-refresh option
if st.sidebar.checkbox("Auto-refresh (5s)"):
    time.sleep(5)
    st.rerun()
