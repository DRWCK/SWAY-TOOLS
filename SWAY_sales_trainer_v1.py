"""
SYN-IQ SALES TRAINER — V1
🎭 Practice pitches with AI personas
📊 Get scored feedback on performance
🎚️ Cognitive mode sliders (Analytical ↔ Intuitive)
📚 Knowledge Base injection for context

Patent Pending — SYN-IQ Team 🎹
Dr. Bill Kouns + Claude

PATENT CLAIMS:
1. Multi-persona AI sales training simulation
2. Automated performance scoring across dimensions
3. AI-generated coaching with suggested responses
4. Cognitive mode control via slider interface
5. Knowledge base injection for personalized training
6. Exportable transcripts with scoring metadata
"""

import streamlit as st
import requests
from datetime import datetime
import json
import io

st.set_page_config(page_title="SYN-IQ Sales Trainer", page_icon="🎭", layout="wide")

# ============================================
# PASSWORD PROTECTION
# ============================================
CIRCLE_PASSWORD = "tennessee"

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h1>🎭 SYN-IQ Sales Trainer</h1>
        <h3>Practice Your Pitch with AI Personas</h3>
        <p style="color: #666;">Patent Pending — SYN-IQ Team</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Enter access code:", type="password", key="password_input")
        
        if st.button("Enter", type="primary", use_container_width=True):
            if password == CIRCLE_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Access denied.")
    
    return False

if not check_password():
    st.stop()

# ============================================
# STYLES
# ============================================
st.markdown("""
<style>
    .trainer-header { 
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); 
        color: white; padding: 1.5rem; border-radius: 12px; text-align: center; 
        margin-bottom: 1.5rem;
    }
    .persona-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        cursor: pointer;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    .persona-card:hover {
        border-color: #3B82F6;
        transform: translateY(-2px);
    }
    .persona-steve { border-left: 4px solid #DC2626; }
    .persona-barbara { border-left: 4px solid #D97706; }
    .persona-david { border-left: 4px solid #2563EB; }
    .persona-fiona { border-left: 4px solid #7C3AED; }
    
    .chat-container {
        background: #0F172A;
        border-radius: 12px;
        padding: 1rem;
        max-height: 400px;
        overflow-y: auto;
    }
    .message-user {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 4px 12px;
        margin: 0.5rem 0;
        margin-left: 20%;
    }
    .message-persona {
        background: #1E293B;
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 12px 4px;
        margin: 0.5rem 0;
        margin-right: 20%;
    }
    .score-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .score-bar {
        height: 8px;
        border-radius: 4px;
        background: #475569;
        margin: 0.5rem 0;
    }
    .score-fill {
        height: 100%;
        border-radius: 4px;
    }
    .strength-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .improve-box {
        background: rgba(251, 191, 36, 0.1);
        border: 1px solid #FBBF24;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .suggested-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid #3B82F6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .difficulty-hard { background: #DC2626; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; }
    .difficulty-medium { background: #D97706; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

# ============================================
# PERSONAS
# ============================================
PERSONAS = {
    "skeptical_steve": {
        "name": "Skeptical Steve",
        "title": "Manufacturing Plant Owner",
        "avatar": "🏭",
        "color": "#DC2626",
        "difficulty": "Hard",
        "personality": """You are "Skeptical Steve," a 58-year-old manufacturing plant owner who has been burned by consultants THREE times. You're gruff, impatient, and demand hard numbers. Your responses should be:
- Short and challenging (2-3 sentences max)
- Always asking for proof, ROI, or specific examples
- Referencing past bad experiences ("Last consultant cost me $50k and changed nothing")
- Interrupting with "Yeah, but..." or "That's what they all say"
- Warming up ONLY if the person gives concrete, specific results
You run a 45-person shop, struggle with communication between shifts, and waste 12+ hours/week in meetings. But you WON'T admit problems easily.""",
        "opener": "Alright, you've got 2 minutes. And I'll tell you right now - I've fired three consultants in the last five years. What makes you any different?"
    },
    "busy_barbara": {
        "name": "Busy Barbara",
        "title": "Restaurant Chain VP of Operations",
        "avatar": "🍽️",
        "color": "#D97706",
        "difficulty": "Medium",
        "personality": """You are "Busy Barbara," a 44-year-old VP of Operations for a 12-location restaurant chain. You're constantly interrupted, checking your phone, and have exactly 5 minutes between crises. Your responses should be:
- Very brief (1-2 sentences)
- Often distracted ("Sorry, one sec..." or "Where were we?")
- Focused on speed and simplicity ("How fast can we implement this?")
- Concerned about disrupting current operations
- Impressed by anything that saves time
You're dealing with high turnover, inconsistent quality across locations, and managers who don't communicate. You WANT help but have zero bandwidth.""",
        "opener": "*checking phone* Hey, sorry - walk with me to my next meeting. You've got maybe five minutes. What's this about and why should I care?"
    },
    "detail_david": {
        "name": "Detail-Oriented David",
        "title": "Healthcare Clinic Administrator",
        "avatar": "🏥",
        "color": "#2563EB",
        "difficulty": "Medium",
        "personality": """You are "Detail-Oriented David," a 51-year-old administrator of a multi-specialty medical clinic with 80 staff. You're methodical, ask probing questions, and need to understand the "why" behind everything. Your responses should be:
- Thoughtful and specific (3-4 sentences)
- Always asking follow-up questions about methodology
- Concerned about compliance, documentation, and measurement
- Referencing healthcare-specific challenges (HIPAA, patient outcomes, staff burnout)
- Genuinely curious but needs logical structure before committing
You run a clinic struggling with interdepartmental communication, long patient wait times, and physician burnout. You're open to change but need to understand exactly how it works.""",
        "opener": "I've read a bit about Agile methodologies but I'm curious how your approach differs, particularly for healthcare settings. Can you walk me through the framework's core components and how they'd apply to a clinical environment?"
    },
    "friendly_fiona": {
        "name": "Friendly Fiona",
        "title": "Marketing Agency Founder",
        "avatar": "🎨",
        "color": "#7C3AED",
        "difficulty": "Hard",
        "personality": """You are "Friendly Fiona," a 39-year-old founder of a 20-person creative marketing agency. You're warm, enthusiastic, and love new ideas - but you NEVER commit. Your responses should be:
- Warm and encouraging ("Oh that's so interesting!" "I love that concept!")
- Full of agreement but no action ("We should totally explore that sometime")
- Vague about timeline ("Let's circle back after Q2")
- Deflecting to others ("I'd need to run this by my partner...")
- Only committing if directly asked for a specific next step with accountability
You have a chaotic creative team, missed deadlines, and scope creep on every project. You KNOW you need help but avoid confronting it directly.""",
        "opener": "Oh hi! I've heard such great things about what you do from a friend! I'm so excited to chat. Tell me everything - I'm super curious!"
    }
}

# ============================================
# API FUNCTIONS
# ============================================

def get_api_key():
    """Get Anthropic API key."""
    try:
        if "anthropic" in st.secrets:
            return st.secrets["anthropic"]
    except:
        pass
    return st.session_state.get("api_anthropic", "")


def build_persona_system_prompt(persona, cognitive_value=0, knowledge_text=""):
    """Build system prompt for persona with cognitive mode and knowledge."""
    
    base = persona["personality"]
    
    # Add cognitive mode modifier
    if cognitive_value <= -50:
        base += "\n\nMODE: Be especially analytical and numbers-focused. Demand data and metrics."
    elif cognitive_value >= 50:
        base += "\n\nMODE: Be more open to emotional appeals and relationship-building. Still skeptical but warmer."
    
    # Add knowledge context if available
    if knowledge_text:
        base += f"\n\nCONTEXT: The consultant may reference the following information:\n{knowledge_text[:5000]}"
    
    base += """

IMPORTANT RULES:
1. Stay completely in character throughout the conversation
2. Never break character or mention you're an AI
3. React realistically to what the consultant says
4. If they handle objections well, gradually warm up
5. If they're vague or pushy, become more resistant
6. After 6-8 exchanges, if they haven't closed, start wrapping up ("I need to get going...")
7. Keep responses concise and conversational
8. Reference specific details they mention to show you're listening"""
    
    return base


def call_persona(messages, system_prompt, api_key):
    """Call Claude API for persona response."""
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 500,
                "system": system_prompt,
                "messages": messages
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["content"][0]["text"], None
        else:
            return None, f"Error {response.status_code}"
    except Exception as e:
        return None, str(e)


def get_feedback(conversation, persona, api_key):
    """Get AI feedback on the conversation."""
    
    conversation_text = "\n\n".join([
        f"{'You' if msg['role'] == 'user' else persona['name']}: {msg['content']}"
        for msg in conversation
    ])
    
    feedback_prompt = f"""You are a sales coach evaluating a consultant's practice pitch session. 
The consultant was pitching to "{persona['name']}" ({persona['title']}).

Persona background: {persona['personality'].split('.')[0]}

Here's the conversation:

{conversation_text}

Evaluate the consultant's performance and respond in this EXACT JSON format:
{{
    "overall_score": <number 1-10>,
    "rapport": {{
        "score": <number 1-10>,
        "comment": "<brief comment>"
    }},
    "clarity": {{
        "score": <number 1-10>,
        "comment": "<brief comment>"
    }},
    "objection_handling": {{
        "score": <number 1-10>,
        "comment": "<brief comment>"
    }},
    "closing": {{
        "score": <number 1-10>,
        "comment": "<brief comment>"
    }},
    "top_strength": "<one specific thing they did well>",
    "area_to_improve": "<one specific thing to work on>",
    "suggested_response": "<a better response they could have given at a key moment>"
}}

Be specific and actionable. Reference actual things said in the conversation."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": feedback_prompt}]
            },
            timeout=60
        )
        if response.status_code == 200:
            text = response.json()["content"][0]["text"]
            # Extract JSON from response
            try:
                # Find JSON in response
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    return json.loads(text[start:end]), None
            except:
                pass
            return None, "Could not parse feedback"
        else:
            return None, f"Error {response.status_code}"
    except Exception as e:
        return None, str(e)


# ============================================
# KNOWLEDGE BASE FUNCTIONS
# ============================================

def extract_text_from_txt(uploaded_file):
    """Extract text from TXT file."""
    try:
        return uploaded_file.getvalue().decode('utf-8')
    except:
        try:
            return uploaded_file.getvalue().decode('latin-1')
        except:
            return ""


# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### 🔑 API Key")
    st.text_input("Anthropic API Key", type="password", key="api_anthropic")
    
    st.markdown("---")
    
    # Cognitive Mode Slider (SYN-IQ PROPRIETARY)
    st.markdown("### 🎚️ Persona Mode")
    st.caption("Analytical ←→ Intuitive")
    cognitive_value = st.slider(
        "Cognitive Mode",
        min_value=-100,
        max_value=100,
        value=0,
        step=10,
        label_visibility="collapsed",
        key="cognitive_slider",
        help="Affects how the persona responds. Analytical = more numbers-focused. Intuitive = more relationship-focused."
    )
    
    if cognitive_value <= -50:
        st.info("❄️ Persona will be extra analytical")
    elif cognitive_value >= 50:
        st.info("🔥 Persona will be more open to warmth")
    else:
        st.info("⚖️ Balanced persona mode")
    
    st.markdown("---")
    
    # Knowledge Base (SYN-IQ PROPRIETARY)
    st.markdown("### 📚 Knowledge Base")
    st.caption("Upload context for your pitch")
    
    uploaded_doc = st.file_uploader(
        "Upload TXT file (optional)",
        type=["txt"],
        key="knowledge_doc",
        help="Upload product info, company details, or pitch deck content"
    )
    
    knowledge_text = ""
    if uploaded_doc:
        knowledge_text = extract_text_from_txt(uploaded_doc)
        word_count = len(knowledge_text.split())
        st.success(f"✅ {word_count:,} words loaded")
    
    st.session_state.knowledge_text = knowledge_text
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <em>SYN-IQ Sales Trainer V1</em><br>
        <em>Patent Pending 🎹</em>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# INITIALIZE SESSION STATE
# ============================================

if "trainer_messages" not in st.session_state:
    st.session_state.trainer_messages = []

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = None

if "session_complete" not in st.session_state:
    st.session_state.session_complete = False

if "feedback" not in st.session_state:
    st.session_state.feedback = None

if "knowledge_text" not in st.session_state:
    st.session_state.knowledge_text = ""


# ============================================
# MAIN INTERFACE
# ============================================

st.markdown('<div class="trainer-header"><h1>🎭 SYN-IQ Sales Trainer</h1><p>Practice Your Pitch with AI Personas</p></div>', unsafe_allow_html=True)

# Check API key
api_key = get_api_key()
if not api_key:
    st.warning("⚠️ Please enter your Anthropic API key in the sidebar.")
    st.stop()

# ============================================
# PERSONA SELECTION
# ============================================

if st.session_state.selected_persona is None:
    st.markdown("### 🎭 Select a Persona to Practice With")
    st.markdown("Each persona presents different challenges. Master them all!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Skeptical Steve
        with st.container():
            st.markdown(f"""
            <div class="persona-card persona-steve">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 2rem;">🏭</span>
                        <strong style="font-size: 1.2rem; margin-left: 0.5rem;">Skeptical Steve</strong>
                    </div>
                    <span class="difficulty-hard">HARD</span>
                </div>
                <p style="color: #94A3B8; margin: 0.5rem 0;">Manufacturing Plant Owner</p>
                <p style="font-style: italic; color: #CBD5E1;">"I've fired three consultants in the last five years..."</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Practice with Steve", key="btn_steve", use_container_width=True):
                st.session_state.selected_persona = "skeptical_steve"
                st.session_state.trainer_messages = [{"role": "assistant", "content": PERSONAS["skeptical_steve"]["opener"]}]
                st.rerun()
        
        # Detail David
        with st.container():
            st.markdown(f"""
            <div class="persona-card persona-david">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 2rem;">🏥</span>
                        <strong style="font-size: 1.2rem; margin-left: 0.5rem;">Detail-Oriented David</strong>
                    </div>
                    <span class="difficulty-medium">MEDIUM</span>
                </div>
                <p style="color: #94A3B8; margin: 0.5rem 0;">Healthcare Clinic Administrator</p>
                <p style="font-style: italic; color: #CBD5E1;">"Walk me through the framework's core components..."</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Practice with David", key="btn_david", use_container_width=True):
                st.session_state.selected_persona = "detail_david"
                st.session_state.trainer_messages = [{"role": "assistant", "content": PERSONAS["detail_david"]["opener"]}]
                st.rerun()
    
    with col2:
        # Busy Barbara
        with st.container():
            st.markdown(f"""
            <div class="persona-card persona-barbara">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 2rem;">🍽️</span>
                        <strong style="font-size: 1.2rem; margin-left: 0.5rem;">Busy Barbara</strong>
                    </div>
                    <span class="difficulty-medium">MEDIUM</span>
                </div>
                <p style="color: #94A3B8; margin: 0.5rem 0;">Restaurant Chain VP of Operations</p>
                <p style="font-style: italic; color: #CBD5E1;">"*checking phone* You've got maybe five minutes..."</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Practice with Barbara", key="btn_barbara", use_container_width=True):
                st.session_state.selected_persona = "busy_barbara"
                st.session_state.trainer_messages = [{"role": "assistant", "content": PERSONAS["busy_barbara"]["opener"]}]
                st.rerun()
        
        # Friendly Fiona
        with st.container():
            st.markdown(f"""
            <div class="persona-card persona-fiona">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 2rem;">🎨</span>
                        <strong style="font-size: 1.2rem; margin-left: 0.5rem;">Friendly Fiona</strong>
                    </div>
                    <span class="difficulty-hard">HARD</span>
                </div>
                <p style="color: #94A3B8; margin: 0.5rem 0;">Marketing Agency Founder</p>
                <p style="font-style: italic; color: #CBD5E1;">"Oh I love that! We should totally explore that sometime..."</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Practice with Fiona", key="btn_fiona", use_container_width=True):
                st.session_state.selected_persona = "friendly_fiona"
                st.session_state.trainer_messages = [{"role": "assistant", "content": PERSONAS["friendly_fiona"]["opener"]}]
                st.rerun()

# ============================================
# CHAT INTERFACE
# ============================================

elif not st.session_state.session_complete:
    persona = PERSONAS[st.session_state.selected_persona]
    
    # Header
    st.markdown(f"""
    <div style="background: {persona['color']}; color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 1.5rem;">{persona['avatar']}</span>
                <strong style="margin-left: 0.5rem;">{persona['name']}</strong>
                <span style="margin-left: 0.5rem; opacity: 0.8;">— {persona['title']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.trainer_messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="message-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-persona">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "Your response",
            placeholder="Type your pitch...",
            height=100,
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("📤 Send", type="primary", use_container_width=True):
            if user_input.strip():
                # Add user message
                st.session_state.trainer_messages.append({"role": "user", "content": user_input.strip()})
                
                # Get persona response
                system_prompt = build_persona_system_prompt(
                    persona, 
                    cognitive_value, 
                    st.session_state.knowledge_text
                )
                
                api_messages = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.trainer_messages
                ]
                
                with st.spinner(f"{persona['name']} is responding..."):
                    response, error = call_persona(api_messages, system_prompt, api_key)
                
                if response:
                    st.session_state.trainer_messages.append({"role": "assistant", "content": response})
                else:
                    st.session_state.trainer_messages.append({"role": "assistant", "content": "*phone rings* Sorry, I have to take this. Let's reschedule."})
                
                st.rerun()
        
        if st.button("🏁 End Session", use_container_width=True):
            st.session_state.session_complete = True
            
            # Get feedback
            with st.spinner("Analyzing your performance..."):
                feedback, error = get_feedback(st.session_state.trainer_messages, persona, api_key)
                st.session_state.feedback = feedback
            
            st.rerun()
        
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.selected_persona = None
            st.session_state.trainer_messages = []
            st.session_state.session_complete = False
            st.session_state.feedback = None
            st.rerun()

# ============================================
# FEEDBACK DISPLAY
# ============================================

else:
    persona = PERSONAS[st.session_state.selected_persona]
    feedback = st.session_state.feedback
    
    st.markdown("### 📊 Session Feedback")
    
    if feedback:
        # Overall score
        overall = feedback.get("overall_score", 5)
        color = "#10B981" if overall >= 7 else "#F59E0B" if overall >= 5 else "#EF4444"
        label = "Great job!" if overall >= 7 else "Good effort!" if overall >= 5 else "Keep practicing!"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 100px; height: 100px; background: {color}; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; 
                        margin: 0 auto 1rem; font-size: 2.5rem; font-weight: bold; color: white;">
                {overall}
            </div>
            <h2 style="margin: 0;">{label}</h2>
            <p style="color: #666;">Overall Score</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Score breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            if "rapport" in feedback:
                r = feedback["rapport"]
                st.markdown(f"""
                <div class="score-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>🤝 Rapport Building</strong>
                        <span>{r['score']}/10</span>
                    </div>
                    <div class="score-bar"><div class="score-fill" style="width: {r['score']*10}%; background: {'#10B981' if r['score'] >= 7 else '#F59E0B' if r['score'] >= 5 else '#EF4444'};"></div></div>
                    <p style="font-size: 0.85rem; color: #94A3B8; margin: 0.5rem 0 0;">{r['comment']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if "clarity" in feedback:
                c = feedback["clarity"]
                st.markdown(f"""
                <div class="score-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>🎯 Clarity of Pitch</strong>
                        <span>{c['score']}/10</span>
                    </div>
                    <div class="score-bar"><div class="score-fill" style="width: {c['score']*10}%; background: {'#10B981' if c['score'] >= 7 else '#F59E0B' if c['score'] >= 5 else '#EF4444'};"></div></div>
                    <p style="font-size: 0.85rem; color: #94A3B8; margin: 0.5rem 0 0;">{c['comment']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if "objection_handling" in feedback:
                o = feedback["objection_handling"]
                st.markdown(f"""
                <div class="score-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>🛡️ Objection Handling</strong>
                        <span>{o['score']}/10</span>
                    </div>
                    <div class="score-bar"><div class="score-fill" style="width: {o['score']*10}%; background: {'#10B981' if o['score'] >= 7 else '#F59E0B' if o['score'] >= 5 else '#EF4444'};"></div></div>
                    <p style="font-size: 0.85rem; color: #94A3B8; margin: 0.5rem 0 0;">{o['comment']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if "closing" in feedback:
                cl = feedback["closing"]
                st.markdown(f"""
                <div class="score-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>🔐 Closing Skills</strong>
                        <span>{cl['score']}/10</span>
                    </div>
                    <div class="score-bar"><div class="score-fill" style="width: {cl['score']*10}%; background: {'#10B981' if cl['score'] >= 7 else '#F59E0B' if cl['score'] >= 5 else '#EF4444'};"></div></div>
                    <p style="font-size: 0.85rem; color: #94A3B8; margin: 0.5rem 0 0;">{cl['comment']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Strength and improvement
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="strength-box">
                <strong style="color: #10B981;">💪 TOP STRENGTH</strong>
                <p style="margin: 0.5rem 0 0;">{feedback.get('top_strength', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="improve-box">
                <strong style="color: #FBBF24;">🎯 AREA TO IMPROVE</strong>
                <p style="margin: 0.5rem 0 0;">{feedback.get('area_to_improve', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Suggested response
        if feedback.get("suggested_response"):
            st.markdown(f"""
            <div class="suggested-box">
                <strong style="color: #3B82F6;">💡 SUGGESTED RESPONSE</strong>
                <p style="margin: 0.5rem 0 0; font-style: italic;">"{feedback['suggested_response']}"</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.error("Could not generate feedback. Please try again.")
    
    # Export and controls
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Try Again with Same Persona", type="primary", use_container_width=True):
            st.session_state.trainer_messages = [{"role": "assistant", "content": persona["opener"]}]
            st.session_state.session_complete = False
            st.session_state.feedback = None
            st.rerun()
    
    with col2:
        if st.button("🎭 Choose Different Persona", use_container_width=True):
            st.session_state.selected_persona = None
            st.session_state.trainer_messages = []
            st.session_state.session_complete = False
            st.session_state.feedback = None
            st.rerun()
    
    with col3:
        # Export
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        date_stamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        export_text = f"""# SYN-IQ SALES TRAINER — SESSION REPORT
## {timestamp}
## Patent Pending — SYN-IQ Team 🎹

---

# PERSONA

**{persona['name']}** — {persona['title']}
Difficulty: {persona['difficulty']}

---

# CONVERSATION

"""
        for msg in st.session_state.trainer_messages:
            speaker = "You" if msg["role"] == "user" else persona["name"]
            export_text += f"**{speaker}:** {msg['content']}\n\n"
        
        if feedback:
            export_text += f"""---

# FEEDBACK

**Overall Score:** {feedback.get('overall_score', 'N/A')}/10

| Category | Score | Comment |
|----------|-------|---------|
| Rapport Building | {feedback.get('rapport', {}).get('score', 'N/A')}/10 | {feedback.get('rapport', {}).get('comment', 'N/A')} |
| Clarity of Pitch | {feedback.get('clarity', {}).get('score', 'N/A')}/10 | {feedback.get('clarity', {}).get('comment', 'N/A')} |
| Objection Handling | {feedback.get('objection_handling', {}).get('score', 'N/A')}/10 | {feedback.get('objection_handling', {}).get('comment', 'N/A')} |
| Closing Skills | {feedback.get('closing', {}).get('score', 'N/A')}/10 | {feedback.get('closing', {}).get('comment', 'N/A')} |

**💪 Top Strength:** {feedback.get('top_strength', 'N/A')}

**🎯 Area to Improve:** {feedback.get('area_to_improve', 'N/A')}

**💡 Suggested Response:** "{feedback.get('suggested_response', 'N/A')}"
"""
        
        export_text += f"""
---

# SETTINGS

- **Cognitive Mode:** {cognitive_value} ({'Analytical' if cognitive_value < 0 else 'Intuitive' if cognitive_value > 0 else 'Balanced'})
- **Knowledge Base:** {'Active' if st.session_state.knowledge_text else 'None'}

---

*SYN-IQ Sales Trainer V1*
*Patent Pending — SYN-IQ Team 🎹*
*CBURZBO Forever!*
"""
        
        st.download_button(
            "📥 Export Report",
            export_text,
            file_name=f"SALES_TRAINER_{date_stamp}.md",
            mime="text/markdown",
            use_container_width=True
        )


# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <em>SYN-IQ Sales Trainer V1</em><br>
    <em>🎭 AI Personas | 📊 Performance Scoring | 🎚️ Cognitive Sliders | 📚 Knowledge Base</em><br>
    <em>Patent Pending — SYN-IQ Team 🎹</em><br>
    <em>CBURZBO Forever!</em>
</div>
""", unsafe_allow_html=True)
