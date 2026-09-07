import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
import os

wb = openpyxl.Workbook()

# ============================================================
# FEUILLE 1 : MODELE VIDE (a envoyer au secretariat)
# ============================================================
ws = wb.active
ws.title = "MODELE_VIDE"

# Styles
header_font = Font(name='Arial', bold=True, size=11, color='FFFFFF')
header_fill = PatternFill(start_color='1E40AF', end_color='1E40AF', fill_type='solid')
cat_a_fill = PatternFill(start_color='DBEAFE', end_color='DBEAFE', fill_type='solid')
cat_b_fill = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
center = Alignment(horizontal='center', vertical='center', wrap_text=True)
left = Alignment(horizontal='left', vertical='center', wrap_text=True)

# Titre du document
ws.merge_cells('A1:I1')
title_cell = ws['A1']
title_cell.value = 'ISP-GOMBE — INSTITUT SUPERIEUR PEDAGOGIQUE DE LA GOMBE'
title_cell.font = Font(name='Arial', bold=True, size=14, color='1E40AF')
title_cell.alignment = Alignment(horizontal='center', vertical='center')

ws.merge_cells('A2:I2')
subtitle = ws['A2']
subtitle.value = 'TEMPLATE D\'IMPORT DES NOTES — Année Académique'
subtitle.font = Font(name='Arial', bold=True, size=12, color='475569')
subtitle.alignment = Alignment(horizontal='center', vertical='center')

ws.merge_cells('A3:I3')
instructions = ws['A3']
instructions.value = 'Instructions : Remplissez ce fichier avec les données des étudiants. Une ligne = 1 BCI dans 1 UE. Puis importez-le via l\'interface admin.'
instructions.font = Font(name='Arial', italic=True, size=10, color='64748B')
instructions.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
ws.row_dimensions[3].height = 30

# Headers
headers = [
    ('Matricule', 16),
    ('Nom Complet', 28),
    ('Code_UE', 14),
    ('Intitule_UE', 30),
    ('BCI', 30),
    ('Categorie', 12),
    ('Credits', 10),
    ('Note', 8),
    ('Session', 14),
    ('Annee_Academique', 18),
    ('Promotion', 14),
    ('Option', 28),
    ('Section', 24),
]

for col_idx, (header, width) in enumerate(headers, 1):
    cell = ws.cell(row=5, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = center
    cell.border = thin_border
    ws.column_dimensions[get_column_letter(col_idx)].width = width

# Exemple pre-rempli (MPUTU NGOLA LE VIEUX)
example_data = [
    ['222546', 'MPUTU NGOLA LE VIEUX', 'MAT121', 'MATHEMATIQUES APPLIQUEES', 'Mathematiques Generales', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'MAT121', 'MATHEMATIQUES APPLIQUEES', 'Mathematiques Financieres', 'A', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'BUS111', 'INTRODUCTION A LA GESTION', 'Principes de Management', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'BUS111', 'INTRODUCTION A LA GESTION', 'Organisation des Entreprises', 'A', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'LAN121', 'ANGLAIS APPLIQUE', 'Anglais General', 'B', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'LAN121', 'ANGLAIS APPLIQUE', 'Anglais des Affaires', 'B', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'INF101', 'INITIATION A L\'INFORMATIQUE', 'Systeme d\'exploitation', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'INF101', 'INITIATION A L\'INFORMATIQUE', 'Traitement de texte', 'B', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'ECO101', 'ECONOMIE GENERALE', 'Microeconomie', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'ECO101', 'ECONOMIE GENERALE', 'Macroéconomie', 'A', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'DRO101', 'DROIT GENERAL', 'Droit Civil', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'DRO101', 'DROIT GENERAL', 'Droit Constitutionnel', 'B', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'COM101', 'COMPTABILITE GENERALE', 'Comptabilite Base', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'COM101', 'COMPTABILITE GENERALE', 'Balance generale', 'A', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'MAT122', 'MATHEMATIQUES FINANCIERES', 'Interets simples', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'MAT122', 'MATHEMATIQUES FINANCIERES', 'Interets composes', 'A', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'STA101', 'STATISTIQUES DESCRIPTIVES', 'Statistiques univariees', 'A', 2, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
    ['222546', 'MPUTU NGOLA LE VIEUX', 'STA101', 'STATISTIQUES DESCRIPTIVES', 'Diagrams et tableaux', 'B', 1, None, 'Normal', '2023-2024', 'L1', 'Informatique de Gestion', 'Sciences Commerciales & Informatique'],
]

for row_idx, row_data in enumerate(example_data, 6):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = center if col_idx in (1, 3, 6, 7, 8, 9, 10, 11) else left
        # Coloration par categorie
        if col_idx == 6:
            if value == 'A':
                cell.fill = cat_a_fill
            elif value == 'B':
                cell.fill = cat_b_fill

# ============================================================
# FEUILLE 2 : GUIDE DES CATEGORIES A/B
# ============================================================
ws2 = wb.create_sheet("GUIDE_CATEGORIES")

ws2.merge_cells('A1:D1')
ws2['A1'].value = 'GUIDE DES CATEGORIES A ET B — Systeme LMD ISP-GOMBE'
ws2['A1'].font = Font(name='Arial', bold=True, size=14, color='1E40AF')
ws2['A1'].alignment = Alignment(horizontal='center')

guide_headers = ['Categorie', 'Description', 'Exemples de BCI', 'Poids dans la Moyenne']
for col_idx, h in enumerate(guide_headers, 1):
    cell = ws2.cell(row=3, column=col_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = center
    cell.border = thin_border

guide_data = [
    ['A', 'Matières fondamentales / disciplines principales de la filière', 'Mathématiques Générales, Principes de Management, Comptabilité Base, Microéconomie, Droit Civil', 'Pondérée — Majoritaire'],
    ['B', 'Matières complémentaires / outils / langues', 'Anglais Général, Traitement de texte, Anglais des Affaires, Diagrammes', 'Pondérée — Mineur'],
]
for row_idx, row_data in enumerate(guide_data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws2.row_dimensions[row_idx].height = 45
    if row_data[0] == 'A':
        for col_idx in range(1, 5):
            ws2.cell(row=row_idx, column=col_idx).fill = cat_a_fill
    else:
        for col_idx in range(1, 5):
            ws2.cell(row=row_idx, column=col_idx).fill = cat_b_fill

# Formules
ws2.merge_cells('A7:D7')
ws2['A7'].value = 'FORMULES DE CALCUL'
ws2['A7'].font = Font(name='Arial', bold=True, size=12, color='1E40AF')

formules = [
    ['Note Pondérée', 'Note × Crédits du BCI', '7 × 3 = 21'],
    ['Moyenne Catégorie A', 'Σ(Notes pondérées A) / Σ(Crédits A)', '271 / 60 = 4.52'],
    ['Moyenne Catégorie B', 'Σ(Notes pondérées B) / Σ(Crédits B)', '—'],
    ['Moyenne Annuelle', 'Σ(Notes pondérées Toutes) / Σ(Crédits Tous)', '271 / 60 = 4.52'],
    ['Décision', 'Moyenne ≥ 10 → ADMIS | < 10 → AJOURNÉ', 'ADMIS'],
    ['Mention', '≥ 16 TRÈS BIEN | ≥ 14 BIEN | ≥ 12 ASSEZ BIEN | ≥ 10 PASSABLE', 'PASSABLE'],
    ['Crédits Capitalisés', 'Si ADMIS → 60 | Si AJOURNÉ → Crédits validés (note ≥ 10)', '60'],
]

for col_idx, h in enumerate(['Terme', 'Formule', 'Exemple'], 1):
    cell = ws2.cell(row=8, column=col_idx, value=h)
    cell.font = Font(name='Arial', bold=True, size=10, color='FFFFFF')
    cell.fill = PatternFill(start_color='334155', end_color='334155', fill_type='solid')
    cell.alignment = center
    cell.border = thin_border

for row_idx, row_data in enumerate(formules, 9):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)

ws2.column_dimensions['A'].width = 22
ws2.column_dimensions['B'].width = 50
ws2.column_dimensions['C'].width = 40
ws2.column_dimensions['D'].width = 25

# ============================================================
# FEUILLE 3 : STRUCTURE DES SESSIONS
# ============================================================
ws3 = wb.create_sheet("SESSIONS")

ws3.merge_cells('A1:C1')
ws3['A1'].value = 'TYPES DE SESSIONS'
ws3['A1'].font = Font(name='Arial', bold=True, size=14, color='1E40AF')
ws3['A1'].alignment = Alignment(horizontal='center')

for col_idx, h in enumerate(['Session', 'Description', 'Quand'], 1):
    cell = ws3.cell(row=3, column=col_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = center
    cell.border = thin_border

sessions = [
    ['Normal', 'Session principale — notes finales', 'Fin de semestre'],
    ['RATTRAPAGE', 'Session de rattrapage — les notes remplacent les échecs', 'Après délibération'],
    ['Session Spéciale', 'Pour les étudiants en situation d\'arriéré', 'Exceptionnel'],
]
for row_idx, row_data in enumerate(sessions, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws3.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)

ws3.column_dimensions['A'].width = 20
ws3.column_dimensions['B'].width = 50
ws3.column_dimensions['C'].width = 30

# ============================================================
# FEUILLE 4 : EXEMPLE COMPLET PRE-REMPLI (Bulletin)
# ============================================================
ws4 = wb.create_sheet("EXEMPLE_BULLETIN")

ws4.merge_cells('A1:I1')
ws4['A1'].value = 'BULLETIN DE NOTES — Exemple complet avec calculs automatiques'
ws4['A1'].font = Font(name='Arial', bold=True, size=13, color='1E40AF')
ws4['A1'].alignment = Alignment(horizontal='center')

ws4.merge_cells('A2:I2')
ws4['A2'].value = 'MPUTU NGOLA LE VIEUX | Matricule: 222546 | L1 — Informatique de Gestion | 2023-2024'
ws4['A2'].font = Font(name='Arial', bold=True, size=11, color='475569')
ws4['A2'].alignment = Alignment(horizontal='center')

bulletin_headers = ['Code UE', 'Intitulé UE', 'BCI', 'Cat.', 'Crédits', 'Note', 'Note Pond.', 'Moy. UE', 'Décision BCI']
for col_idx, h in enumerate(bulletin_headers, 1):
    cell = ws4.cell(row=4, column=col_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = center
    cell.border = thin_border

# Bulletin data avec notes
bulletin_data = [
    ['MAT121', 'MATHÉMATIQUES APPLIQUÉES', 'Mathématiques Générales', 'A', 2, 7, 14, None, None],
    ['MAT121', '', 'Mathématiques Financières', 'A', 1, 5, 5, 19, 'ADMIS'],
    ['BUS111', 'INTRODUCTION À LA GESTION', 'Principes de Management', 'A', 2, 8, 16, None, None],
    ['BUS111', '', 'Organisation des Entreprises', 'A', 1, 6, 6, 22, 'ADMIS'],
    ['LAN121', 'ANGLAIS APPLIQUÉ', 'Anglais Général', 'B', 2, 6, 12, None, None],
    ['LAN121', '', 'Anglais des Affaires', 'B', 1, 4, 4, 16, 'ADMIS'],
    ['INF101', 'INITIATION À L\'INFORMATIQUE', 'Système d\'exploitation', 'A', 2, 9, 18, None, None],
    ['INF101', '', 'Traitement de texte', 'B', 1, 8, 8, 26, 'ADMIS'],
    ['ECO101', 'ÉCONOMIE GÉNÉRALE', 'Microéconomie', 'A', 2, 5, 10, None, None],
    ['ECO101', '', 'Macroéconomie', 'A', 1, 4, 4, 14, 'ADMIS'],
    ['DRO101', 'DROIT GÉNÉRAL', 'Droit Civil', 'A', 2, 6, 12, None, None],
    ['DRO101', '', 'Droit Constitutionnel', 'B', 1, 5, 5, 17, 'ADMIS'],
    ['COM101', 'COMPTABILITÉ GÉNÉRALE', 'Comptabilité Base', 'A', 2, 7, 14, None, None],
    ['COM101', '', 'Balance générale', 'A', 1, 6, 6, 20, 'ADMIS'],
    ['MAT122', 'MATHÉMATIQUES FINANCIÈRES', 'Intérêts simples', 'A', 2, 5, 10, None, None],
    ['MAT122', '', 'Intérêts composés', 'A', 1, 4, 4, 14, 'ADMIS'],
    ['STA101', 'STATISTIQUES DESCRIPTIVES', 'Statistiques univariées', 'A', 2, 6, 12, None, None],
    ['STA101', '', 'Diagrams et tableaux', 'B', 1, 5, 5, 17, 'ADMIS'],
]

for row_idx, row_data in enumerate(bulletin_data, 5):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws4.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = center if col_idx in (1, 4, 5, 6, 7, 8, 9) else left
        if col_idx == 4:
            cell.fill = cat_a_fill if value == 'A' else cat_b_fill
        if col_idx == 9:
            if value == 'ADMIS':
                cell.font = Font(name='Arial', bold=True, color='059669')
            elif value == 'ÉCHOUÉ':
                cell.font = Font(name='Arial', bold=True, color='EF4444')

# Totaux
total_row = 5 + len(bulletin_data) + 1
ws4.merge_cells(f'A{total_row}:D{total_row}')
ws4.cell(row=total_row, column=1, value='TOTAUX').font = Font(name='Arial', bold=True, size=11)
ws4.cell(row=total_row, column=1).alignment = center
ws4.cell(row=total_row, column=1).border = thin_border
ws4.cell(row=total_row, column=5, value=60).font = Font(name='Arial', bold=True)
ws4.cell(row=total_row, column=5).alignment = center
ws4.cell(row=total_row, column=5).border = thin_border
total_pondere = sum(r[5] * r[4] for r in bulletin_data)
ws4.cell(row=total_row, column=7, value=total_pondere).font = Font(name='Arial', bold=True)
ws4.cell(row=total_row, column=7).alignment = center
ws4.cell(row=total_row, column=7).border = thin_border

# Moyennes
moy_row = total_row + 2
ws4.merge_cells(f'A{moy_row}:C{moy_row}')
ws4.cell(row=moy_row, column=1, value='MOYENNE ANNUELLE').font = Font(name='Arial', bold=True, size=12, color='1E40AF')
moy = total_pondere / 60
ws4.cell(row=moy_row, column=4, value=round(moy, 2)).font = Font(name='Arial', bold=True, size=14, color='1E40AF')
ws4.cell(row=moy_row, column=4).alignment = center

decision_row = moy_row + 1
ws4.merge_cells(f'A{decision_row}:C{decision_row}')
ws4.cell(row=decision_row, column=1, value='DÉCISION').font = Font(name='Arial', bold=True, size=12)
decision = 'ADMIS' if moy >= 10 else 'AJOURNÉ'
dec_color = '059669' if moy >= 10 else 'EF4444'
ws4.cell(row=decision_row, column=4, value=decision).font = Font(name='Arial', bold=True, size=14, color=dec_color)
ws4.cell(row=decision_row, column=4).alignment = center

mention_row = decision_row + 1
ws4.merge_cells(f'A{mention_row}:C{mention_row}')
ws4.cell(row=mention_row, column=1, value='MENTION').font = Font(name='Arial', bold=True, size=12)
if moy >= 16: mention = 'TRÈS BIEN'
elif moy >= 14: mention = 'BIEN'
elif moy >= 12: mention = 'ASSEZ BIEN'
elif moy >= 10: mention = 'PASSABLE'
else: mention = '—'
ws4.cell(row=mention_row, column=4, value=mention).font = Font(name='Arial', bold=True, size=12, color='1E40AF')
ws4.cell(row=mention_row, column=4).alignment = center

# Column widths
ws4.column_dimensions['A'].width = 14
ws4.column_dimensions['B'].width = 28
ws4.column_dimensions['C'].width = 28
ws4.column_dimensions['D'].width = 8
ws4.column_dimensions['E'].width = 10
ws4.column_dimensions['F'].width = 8
ws4.column_dimensions['G'].width = 12
ws4.column_dimensions['H'].width = 10
ws4.column_dimensions['I'].width = 14

# Save
output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, 'ISP_GOMBE_Import_Notes_Template.xlsx')
wb.save(output_path)
print(f'Template sauvegarde: {output_path}')
