"""
Module de détection des conflits 

"""
from backend.db_connection import db

class ConflictDetector:
    """Classe pour détecter les conflits dans les emplois du temps"""
    
    def __init__(self):
        """Initialiser le détecteur"""
        pass
    
    def detect_all_conflicts(self):
        """
        Détecter tous les types de conflits
        
        Returns:
            dict: Dictionnaire avec tous les conflits détectés
        """
        return {
            'etudiants': self.detect_student_conflicts(),
            'professeurs': self.detect_professor_conflicts(),
            'salles': self.detect_room_conflicts(),
            'chevauchements': self.detect_time_overlaps()
        }
    
    def detect_student_conflicts(self):
        """
      
        Un conflit = PLUS D'1 EXAMEN PAR JOUR
        
        CORRECTION CRITIQUE:
        - ex.groupe_id = e.groupe_id (vérifier que l'examen est pour SON groupe)
        
        Returns:
            list: Liste des conflits étudiants
        """
        query = """
        SELECT 
            e.id as etudiant_id,
            e.matricule,
            CONCAT(e.prenom, ' ', e.nom) as etudiant,
            f.nom as formation,
            g.nom as groupe,
            DATE(ex.date_heure) as jour,
            COUNT(DISTINCT ex.id) as nb_examens,
            GROUP_CONCAT(
                DISTINCT CONCAT(TIME(ex.date_heure), ' - ', m.nom) 
                ORDER BY ex.date_heure 
                SEPARATOR ' | '
            ) as modules_detail
        FROM etudiants e
        JOIN formations f ON e.formation_id = f.id
        JOIN groupes g ON e.groupe_id = g.id
        JOIN inscriptions i ON e.id = i.etudiant_id
        JOIN modules m ON i.module_id = m.id
        JOIN examens ex ON m.id = ex.module_id 
            AND ex.groupe_id = e.groupe_id
        WHERE ex.statut = 'planifie'
        GROUP BY 
            e.id, 
            e.matricule, 
            e.prenom, 
            e.nom, 
            f.nom, 
            g.nom,
            DATE(ex.date_heure)
        HAVING COUNT(DISTINCT ex.id) > 1
        ORDER BY jour, nb_examens DESC, e.nom
        """
        
        result = db.execute_query(query)
        return result if result else []
    
    def detect_same_time_conflicts(self):
        """
         Détecter les conflits au MÊME CRÉNEAU HORAIRE (même heure)
        CRITIQUE: ex.groupe_id = e.groupe_id
        
        Returns:
            list: Liste des conflits au même créneau
        """
        query = """
        SELECT 
            e.id as etudiant_id,
            e.matricule,
            CONCAT(e.prenom, ' ', e.nom) as etudiant,
            f.nom as formation,
            g.nom as groupe,
            ex.date_heure as creneau_conflit,
            COUNT(DISTINCT ex.id) as nb_examens_simultanes,
            GROUP_CONCAT(DISTINCT m.nom ORDER BY m.nom SEPARATOR ' | ') as modules
        FROM etudiants e
        JOIN formations f ON e.formation_id = f.id
        JOIN groupes g ON e.groupe_id = g.id
        JOIN inscriptions i ON e.id = i.etudiant_id
        JOIN modules m ON i.module_id = m.id
        JOIN examens ex ON m.id = ex.module_id 
            AND ex.groupe_id = e.groupe_id
        WHERE ex.statut = 'planifie'
        GROUP BY 
            e.id, 
            e.matricule, 
            e.prenom, 
            e.nom, 
            f.nom,
            g.nom,
            ex.date_heure
        HAVING COUNT(DISTINCT ex.id) > 1
        ORDER BY nb_examens_simultanes DESC, creneau_conflit
        """
        
        result = db.execute_query(query)
        return result if result else []
    
    def detect_professor_conflicts(self):
        """
        Détecter les conflits professeurs (plus de 3 surveillances/jour)
        
        Returns:
            list: Liste des conflits professeurs
        """
        query = """
        SELECT 
            p.id as professeur_id,
            p.nom,
            p.prenom,
            d.nom as departement,
            DATE(ex.date_heure) as date_surveillance,
            COUNT(DISTINCT ex.id) as nb_surveillances,
            GROUP_CONCAT(
                DISTINCT CONCAT(TIME(ex.date_heure), ' - ', m.nom)
                ORDER BY ex.date_heure 
                SEPARATOR ' | '
            ) as horaires_detail
        FROM professeurs p
        JOIN departements d ON p.dept_id = d.id
        JOIN examens ex ON p.id = ex.prof_id
        JOIN modules m ON ex.module_id = m.id
        WHERE ex.statut = 'planifie'
        GROUP BY p.id, p.nom, p.prenom, d.nom, DATE(ex.date_heure)
        HAVING COUNT(DISTINCT ex.id) > 3
        ORDER BY date_surveillance, nb_surveillances DESC, p.nom
        """
        
        result = db.execute_query(query)
        return result if result else []
    
    def detect_room_conflicts(self):
        """
        Détecter les conflits de salles (capacité dépassée)
        
        Returns:
            list: Liste des conflits de salles
        """
        query = """
        SELECT 
            s.id as salle_id,
            s.nom as salle_nom,
            s.capacite,
            s.type as salle_type,
            ex.id as examen_id,
            m.nom as module_nom,
            g.nom as groupe_nom,
            ex.nb_etudiants,
            ex.date_heure,
            (ex.nb_etudiants - s.capacite) as depassement,
            CONCAT(
                'Il y a ', ex.nb_etudiants, ' étudiants pour ', 
                s.capacite, ' places (', (ex.nb_etudiants - s.capacite), ' en trop)'
            ) as message
        FROM salles s
        JOIN examens ex ON s.id = ex.salle_id
        JOIN modules m ON ex.module_id = m.id
        LEFT JOIN groupes g ON ex.groupe_id = g.id
        WHERE ex.statut = 'planifie'
          AND ex.nb_etudiants > s.capacite
        ORDER BY depassement DESC, ex.date_heure
        """
        
        result = db.execute_query(query)
        return result if result else []
    
    def detect_time_overlaps(self):
        """
        Détecter les chevauchements horaires dans les salles (même créneau, même salle)
        
        Returns:
            list: Liste des chevauchements
        """
        query = """
        SELECT 
            e1.id as examen1_id,
            e2.id as examen2_id,
            e1.salle_id,
            s.nom as salle_nom,
            s.type as salle_type,
            e1.date_heure as debut1,
            e2.date_heure as debut2,
            m1.nom as module1,
            m2.nom as module2,
            g1.nom as groupe1,
            g2.nom as groupe2,
            CONCAT(
                'Salle ', s.nom, ' occupée par ', m1.nom, 
                ' et ', m2.nom, ' au même moment'
            ) as message
        FROM examens e1
        JOIN examens e2 ON e1.salle_id = e2.salle_id 
            AND e1.id < e2.id
            AND e1.date_heure = e2.date_heure
        JOIN salles s ON e1.salle_id = s.id
        JOIN modules m1 ON e1.module_id = m1.id
        JOIN modules m2 ON e2.module_id = m2.id
        LEFT JOIN groupes g1 ON e1.groupe_id = g1.id
        LEFT JOIN groupes g2 ON e2.groupe_id = g2.id
        WHERE 
            e1.statut = 'planifie' 
            AND e2.statut = 'planifie'
        ORDER BY e1.date_heure
        """
        
        result = db.execute_query(query)
        return result if result else []
    
    def check_professor_balance(self):
        """
        Vérifier l'équilibrage des surveillances entre professeurs
        
        Returns:
            dict: Statistiques sur l'équilibrage
        """
        query = """
        SELECT 
            p.id,
            p.nom,
            p.prenom,
            d.nom as departement,
            COUNT(DISTINCT ex.id) as nb_surveillances,
            GROUP_CONCAT(
                DISTINCT DATE_FORMAT(ex.date_heure, '%d/%m/%Y')
                ORDER BY ex.date_heure
                SEPARATOR ', '
            ) as dates_surveillances
        FROM professeurs p
        JOIN departements d ON p.dept_id = d.id
        LEFT JOIN examens ex ON p.id = ex.prof_id AND ex.statut = 'planifie'
        GROUP BY p.id, p.nom, p.prenom, d.nom
        ORDER BY nb_surveillances DESC, p.nom
        """
        
        result = db.execute_query(query)
        
        if not result:
            return {'balanced': True, 'stats': []}
        
        surveillances = [r['nb_surveillances'] for r in result]
        max_surv = max(surveillances) if surveillances else 0
        min_surv = min(surveillances) if surveillances else 0
        diff = max_surv - min_surv
        
        return {
            'balanced': diff <= 2,
            'difference': diff,
            'max': max_surv,
            'min': min_surv,
            'avg': sum(surveillances) / len(surveillances) if surveillances else 0,
            'stats': result
        }
    
    def get_conflicts_summary(self):
        """
        Obtenir un résumé de tous les conflits
        
        Returns:
            dict: Résumé des conflits
        """
        conflicts = self.detect_all_conflicts()
        same_time = self.detect_same_time_conflicts()
        
        return {
            'total_etudiants': len(conflicts['etudiants']),
            'total_etudiants_meme_heure': len(same_time),
            'total_professeurs': len(conflicts['professeurs']),
            'total_salles': len(conflicts['salles']),
            'total_chevauchements': len(conflicts['chevauchements']),
            'has_conflicts': any([
                conflicts['etudiants'],
                conflicts['professeurs'],
                conflicts['salles'],
                conflicts['chevauchements'],
                same_time
            ])
        }
    
    def get_detailed_report(self):
        """
        Générer un rapport détaillé des conflits
        
        Returns:
            dict: Rapport complet
        """
        conflicts = self.detect_all_conflicts()
        summary = self.get_conflicts_summary()
        balance = self.check_professor_balance()
        same_time_conflicts = self.detect_same_time_conflicts()
        
        return {
            'summary': summary,
            'conflicts': conflicts,
            'same_time_conflicts': same_time_conflicts,
            'professor_balance': balance,
            'recommendations': self._generate_recommendations(summary, balance)
        }
    
    def _generate_recommendations(self, summary, balance):
        """
        Générer des recommandations pour résoudre les conflits
        
        Args:
            summary: Résumé des conflits
            balance: Équilibrage des professeurs
            
        Returns:
            list: Liste de recommandations
        """
        recommendations = []
        
        if summary['total_etudiants_meme_heure'] > 0:
            recommendations.append({
                'type': 'etudiants_meme_heure',
                'priority': 'CRITICAL',
                'message': f"🔴 {summary['total_etudiants_meme_heure']} conflit(s) CRITIQUES - Étudiants avec examens au MÊME CRÉNEAU HORAIRE",
                'action': "URGENT: Décaler immédiatement ces examens - conflit impossible à résoudre autrement"
            })
        
        if summary['total_etudiants'] > 0:
            recommendations.append({
                'type': 'etudiants',
                'priority': 'HIGH',
                'message': f"🟠 {summary['total_etudiants']} conflit(s) - Étudiants avec PLUSIEURS EXAMENS LE MÊME JOUR",
                'action': "Décaler les examens sur des jours différents pour respecter la contrainte '1 examen/jour'"
            })
        
        if summary['total_professeurs'] > 0:
            recommendations.append({
                'type': 'professeurs',
                'priority': 'MEDIUM',
                'message': f"🟡 {summary['total_professeurs']} professeur(s) ont plus de 3 surveillances/jour",
                'action': "Réduire le nombre de surveillances ou recruter des surveillants supplémentaires"
            })
        
        if summary['total_salles'] > 0:
            recommendations.append({
                'type': 'salles',
                'priority': 'HIGH',
                'message': f"🟠 {summary['total_salles']} salle(s) dépassent leur capacité",
                'action': "Utiliser des salles plus grandes, diviser les groupes, ou utiliser plusieurs salles"
            })
        
        if summary['total_chevauchements'] > 0:
            recommendations.append({
                'type': 'chevauchements',
                'priority': 'CRITICAL',
                'message': f"🔴 {summary['total_chevauchements']} chevauchement(s) - Même salle occupée par 2 examens simultanément",
                'action': "URGENT: Décaler les horaires ou changer de salle"
            })
        
        if not balance['balanced']:
            recommendations.append({
                'type': 'equilibrage',
                'priority': 'LOW',
                'message': f"🔵 Déséquilibre des surveillances (écart de {balance['difference']} entre min et max)",
                'action': "Mieux répartir les surveillances entre les professeurs pour plus d'équité"
            })
        
        if not recommendations:
            recommendations.append({
                'type': 'success',
                'priority': 'SUCCESS',
                'message': "✅ AUCUN CONFLIT DÉTECTÉ - Planning optimal !",
                'action': "Le planning respecte toutes les contraintes. Prêt pour validation."
            })
        
        return recommendations
    
    def export_conflicts_to_csv(self, filepath='conflicts_report.csv'):
        """
        🆕 Exporter les conflits dans un fichier CSV
        
        Args:
            filepath: Chemin du fichier de sortie
            
        Returns:
            bool: True si succès
        """
        try:
            import pandas as pd
            from datetime import datetime
            
            conflicts = self.detect_all_conflicts()
            all_conflicts = []
            
            for c in conflicts['etudiants']:
                all_conflicts.append({
                    'Type': 'ÉTUDIANT - Plusieurs examens/jour',
                    'Priorité': 'HIGH',
                    'Détail': f"{c['etudiant']} ({c['matricule']}) - {c['nb_examens']} examens le {c['jour']}",
                    'Modules': c.get('modules_detail', 'N/A'),
                    'Date': c['jour']
                })
            
            for c in conflicts['professeurs']:
                all_conflicts.append({
                    'Type': 'PROFESSEUR - Trop de surveillances',
                    'Priorité': 'MEDIUM',
                    'Détail': f"{c['prenom']} {c['nom']} - {c['nb_surveillances']} surveillances le {c['date_surveillance']}",
                    'Modules': c.get('horaires_detail', 'N/A'),
                    'Date': c['date_surveillance']
                })
            
            for c in conflicts['salles']:
                all_conflicts.append({
                    'Type': 'SALLE - Capacité dépassée',
                    'Priorité': 'HIGH',
                    'Détail': c.get('message', f"{c['salle_nom']} - {c['nb_etudiants']}/{c['capacite']} places"),
                    'Modules': c['module_nom'],
                    'Date': c['date_heure']
                })
            
            for c in conflicts['chevauchements']:
                all_conflicts.append({
                    'Type': 'CHEVAUCHEMENT - Même salle/créneau',
                    'Priorité': 'CRITICAL',
                    'Détail': c.get('message', f"Salle {c['salle_nom']} occupée 2 fois"),
                    'Modules': f"{c['module1']} / {c['module2']}",
                    'Date': c['debut1']
                })
            
            if all_conflicts:
                df = pd.DataFrame(all_conflicts)
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                print(f"✅ Rapport exporté: {filepath}")
                return True
            else:
                print("✅ Aucun conflit à exporter")
                return True
                
        except Exception as e:
            print(f"❌ Erreur export CSV: {e}")
            return False
    
    def print_detailed_conflicts(self):
        """
        🆕 Afficher un rapport détaillé dans la console
        """
        print("\n" + "="*80)
        print("📊 RAPPORT DÉTAILLÉ DES CONFLITS")
        print("="*80)
        
        report = self.get_detailed_report()
        summary = report['summary']
        
        print(f"\n📈 RÉSUMÉ:")
        print(f"   🔴 Conflits critiques (même créneau): {summary['total_etudiants_meme_heure']}")
        print(f"   🟠 Conflits étudiants (même jour): {summary['total_etudiants']}")
        print(f"   🟡 Conflits professeurs: {summary['total_professeurs']}")
        print(f"   🟠 Conflits salles: {summary['total_salles']}")
        print(f"   🔴 Chevauchements: {summary['total_chevauchements']}")
        
        total_conflicts = (
            summary['total_etudiants_meme_heure'] +
            summary['total_etudiants'] +
            summary['total_professeurs'] +
            summary['total_salles'] +
            summary['total_chevauchements']
        )
        print(f"\n   📊 TOTAL: {total_conflicts} conflit(s)")
        
        print("\n" + "-"*80)
        print("💡 RECOMMANDATIONS:")
        for i, rec in enumerate(report['recommendations'], 1):
            emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🔵',
                'SUCCESS': '✅'
            }.get(rec['priority'], '⚪')
            
            print(f"\n{i}. [{emoji} {rec['priority']}] {rec['type'].upper()}")
            print(f"   {rec['message']}")
            print(f"   → Action: {rec['action']}")
        
        print("\n" + "="*80 + "\n")


# Instance globale
conflict_detector = ConflictDetector()
