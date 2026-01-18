"""
Application principale - Plateforme Gestion Examens
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


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
    """Vérifier la connexion à la base de données"""
    try:
        conn = db.connect()
        if conn:
            return True, "Connexion établie avec succès"
        return False, "Impossible de se connecter à la base de données"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def main():
    """Fonction principale"""
    
    # En-tête
    st.markdown('<div class="main-header"> Plateforme de Gestion des Examens Universitaires</div>', unsafe_allow_html=True)
    
    # Vérifier la connexion
    is_connected, message = check_database_connection()
    
    if not is_connected:
        st.error(f"❌ {message}")
        st.info("Vérifiez que MySQL est démarré et que le fichier .env est correctement configuré.")
        return
    
    st.success(f"✅ {message}")
    
    # Sidebar - Navigation
    st.sidebar.title("🧭Navigation")
    st.sidebar.markdown("---")
    
    # Informations utilisateur
    user_role = st.sidebar.selectbox(
        "👤 Rôle utilisateur",
        ["Vice-Doyen/Doyen", "Administrateur Examens", "Chef de Département", "Étudiant", "Professeur"]
    )
    
    st.sidebar.markdown("---")
    
    # Pages disponibles selon le rôle
    if user_role in ["Vice-Doyen/Doyen", "Administrateur Examens"]:
        st.sidebar.info("✅ Accès complet au système")
    elif user_role == "Chef de Département":
        st.sidebar.info("✅ Accès département")
    else:
        st.sidebar.info("ℹ️ Consultation uniquement")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📄 Pages disponibles")
    st.sidebar.markdown("Utilisez le menu à gauche pour naviguer entre les différentes interfaces de la plateforme.")
    
    # Contenu principal
    st.markdown("### 👋 Bienvenue sur la plateforme")
    
    st.markdown("""
    <div class="info-card">
        <h4>🎯 Objectif de la plateforme</h4>
        <p>
        Cette plateforme permet de générer automatiquement des emplois du temps d'examens optimisés 
        pour une université de plus de 13 000 étudiants, en respectant toutes les contraintes :
        </p>
        <ul>
            <li>✅ Maximum 1 examen par jour par étudiant</li>
            <li>✅ Maximum 3 surveillances par jour par professeur</li>
            <li>✅ Respect des capacités des salles et amphis</li>
            <li>✅ Équilibrage des surveillances entre professeurs</li>
            <li>✅ Priorisation des surveillances par département</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Fonctionnalités principales
    st.markdown("### ⚡ Fonctionnalités principales")
    
    features = {
        "🤖 Génération automatique": "Création d'emplois du temps optimisés en moins de 45 secondes",
        "🔍 Détection de conflits": "Identification automatique de tous les types de conflits",
        "📊 Tableaux de bord": "Visualisation en temps réel des KPIs et statistiques",
        "👥 Multi-utilisateurs": "Interfaces adaptées selon les rôles (doyen, chef dept, étudiant...)",
        "⚖️ Équilibrage": "Distribution équitable des surveillances entre professeurs",
        "📈 Analytics": "Analyse approfondie des données et de l'utilisation des ressources"
    }
    
    cols = st.columns(2)
    for idx, (feature, description) in enumerate(features.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="info-card">
                <strong>{feature}</strong><br>
                <small>{description}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>📚 Plateforme de Gestion des Examens Universitaires</p>
        <p><small>Projet BDA 2024-2025</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
