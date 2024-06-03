import csv
import openpyxl
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from datetime import datetime


# Fonction pour lire les données de la feuille XLSX
def read_xlsx(sheet):
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(list(row))
    return data


# Fonction pour lire les données de la feuille ODS
def read_ods(sheet):
    data = []
    for row in sheet.getElementsByType(TableRow):
        row_data = []
        for cell in row.getElementsByType(TableCell):
            cell_text = "".join(str(text) for text in cell.getElementsByType(P))
            row_data.append(cell_text)
        data.append(row_data)
    return data


# Fonction pour formater les dates
def format_date_to_clean(date_str):
    if isinstance(date_str, datetime):
        return date_str.strftime("%d/%m/%Y")
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
    except ValueError:
        return date_str  # Retourner la date originale si le format ne correspond pas


def format_date_from_ods(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return date_str  # Retourner la date originale si le format ne correspond pas


# Lire le fichier XLSX (fichier1)
wb1 = openpyxl.load_workbook("fichier1.xlsx")
sheet1 = wb1.active

# Lire le fichier ODS (fichier2)
ods = load("fichier2.ods")
sheet2 = ods.spreadsheet.getElementsByType(Table)[0]

data1 = read_xlsx(sheet1)
data2 = read_ods(sheet2)

# Afficher les en-têtes pour débogage
print("Headers from fichier1.xlsx:", data1[0])
print("Headers from fichier2.ods:", data2[0])

# Extraire les en-têtes
headers1 = data1[0]
headers2 = data2[0]

# Vérifier la présence de "MATRICULE" dans les en-têtes et corriger si nécessaire
matricule_header_ods = "N° de matricule"  # Nom correct de la colonne dans le fichier ODS

if "MATRICULE" not in headers1:
    raise ValueError("'MATRICULE' is not in the headers of fichier1.xlsx")
if matricule_header_ods not in headers2:
    raise ValueError(f"'{matricule_header_ods}' is not in the headers of fichier2.ods")

# Renommer "N° de matricule" en "MATRICULE" dans les données ODS
headers2 = ["MATRICULE" if h == matricule_header_ods else h for h in headers2]
data2[0] = headers2

# Créer un dictionnaire pour un accès facile par MATRICULE et NO_COMPTEUR pour fichier 1
index1 = headers1.index("MATRICULE")
index2 = headers2.index("MATRICULE")
data1_dict = {(row[index1], row[headers1.index("NO_COMPTEUR")]): row for row in data1[1:]}

# Définir la correspondance des colonnes
correspondance_colonnes = {
    "NOUVEL_INDEX": "Index du compteur",
    "CONSOMMATION": "Consommation",
    "DATE_RELEVE": "Date",
    "TYPE_CONSOMMATION": "Consommation non-ordinnaire",
    "NOM": "Nom",
    "PRENOM": "Prénom",
    "ANCIEN_INDEX": "Index précédent",
    "DATE_ANCIEN_RELEVE": "Date du précédent relevé",
}

# Créer une liste pour stocker les données mises à jour
updated_data1 = [headers1]
clean_data = [headers1]

# Mettre à jour les valeurs dans data1 avec les valeurs correspondantes de data2
for row2 in data2[1:]:
    matricule2 = row2[index2]
    no_compteur2 = row2[headers2.index("N° de compteur")]
    if (matricule2, no_compteur2) in data1_dict:
        row1 = data1_dict[(matricule2, no_compteur2)]
        row_modified = False
        for col_name1, col_name2 in correspondance_colonnes.items():
            if col_name2 in headers2:
                idx1 = headers1.index(col_name1)
                idx2 = headers2.index(col_name2)
                if row2[idx2]:
                    if col_name1 in [
                        "DATE_RELEVE",
                        "DATE_ANCIEN_RELEVE",
                    ]:  # Si la colonne est une date, formater la date
                        formatted_date = format_date_from_ods(row2[idx2])
                        row1[idx1] = formatted_date
                    else:
                        row1[idx1] = row2[idx2]
                    row_modified = True
        if row_modified:
            clean_row = [
                format_date_to_clean(item) if headers1[i] in ["DATE_RELEVE", "DATE_ANCIEN_RELEVE"] else item
                for i, item in enumerate(row1)
            ]
            clean_data.append(clean_row)
        updated_data1.append(row1)
    else:
        new_row = [""] * len(headers1)
        new_row[index1] = matricule2
        new_row[headers1.index("NO_COMPTEUR")] = no_compteur2
        for col_name1, col_name2 in correspondance_colonnes.items():
            if col_name2 in headers2:
                idx1 = headers1.index(col_name1)
                idx2 = headers2.index(col_name2)
                if row2[idx2]:
                    if col_name1 in [
                        "DATE_RELEVE",
                        "DATE_ANCIEN_RELEVE",
                    ]:  # Si la colonne est une date, formater la date
                        formatted_date = format_date_from_ods(row2[idx2])
                        new_row[idx1] = formatted_date
                    else:
                        new_row[idx1] = row2[idx2]
        clean_row = [
            format_date_to_clean(item) if headers1[i] in ["DATE_RELEVE", "DATE_ANCIEN_RELEVE"] else item
            for i, item in enumerate(new_row)
        ]
        clean_data.append(clean_row)
        updated_data1.append(new_row)

# Ajouter les lignes de data1 qui ne sont pas dans data2
for key in data1_dict:
    matricule1, no_compteur1 = key
    if key not in [(row[index2], row[headers2.index("N° de compteur")]) for row in data2[1:]]:
        updated_data1.append(data1_dict[key])

# Écrire les données mises à jour dans un nouveau fichier XLSX
wb_out = openpyxl.Workbook()
sheet_out = wb_out.active

for row in updated_data1:
    sheet_out.append(row)

wb_out.save("fichier_merge.xlsx")

# Écrire les données modifiées dans un nouveau fichier "clean"
if clean_data:
    wb_clean = openpyxl.Workbook()
    sheet_clean = wb_clean.active

    for row in clean_data:
        sheet_clean.append(row)

    wb_clean.save("fichier_clean.xlsx")
else:
    print("Aucune donnée modifiée trouvée.")
