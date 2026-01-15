"""
Application principale - Plateforme Gestion Examens
"""
import streamlit as st
from backend.db_connection import db

st.set_page_config(
    page_title="Gestion Examens Universitaires",
    page_icon="platform.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
    }
    
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #7f8c8d;
        border-top: 1px solid #ecf0f1;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

def check_database_connection():
    try:
        conn = db.connect()
        if conn:
            return True, "Connexion établie avec succès"
        return False, "Impossible de se connecter à la base de données"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def main():
    st.markdown(
        '<div class="main-header"> Plateforme de Gestion des Examens Universitaires</div>',
        unsafe_allow_html=True
    )

    is_connected, message = check_database_connection()

    if not is_connected:
        st.error(f"❌ {message}")
        st.info("Vérifiez les Secrets Streamlit (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT).")
        st.stop()

    st.success(f"✅ {message}")

    # Sidebar
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown("---")

    user_role = st.sidebar.selectbox(
        "👤 Rôle utilisateur",
        ["Vice-Doyen/Doyen", "Administrateur Examens", "Chef de Département", "Étudiant", "Professeur"]
    )

    st.sidebar.markdown("---")

    if user_role in ["Vice-Doyen/Doyen", "Administrateur Examens"]:
        st.sidebar.info("✅ Accès complet au système")
    elif user_role == "Chef de Département":
        st.sidebar.info("✅ Accès département")
    else:
        st.sidebar.info("ℹ️ Consultation uniquement")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📄 Pages disponibles")
    st.sidebar.markdown("Utilisez le menu à gauche pour naviguer entre les différentes interfaces.")

    st.markdown("### 👋 Bienvenue sur la plateforme")

    st.markdown("""
    <div class="info-card">
        <h4>🎯 Objectif de la plateforme</h4>
        <p>Génération automatique d'emplois du temps d'examens optimisés.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        <p>📚 Plateforme de Gestion des Examens Universitaires</p>
        <p><small>Projet BDA 2024-2025</small></p>
    </div>
    """, unsafe_allow_html=True)

main()
