"""
    colstudies application
"""

import json
import globalvars as g
import os


def getFileList(studyno):
    """

    get the files for a study from STAR
    no authentication required, local files or network drive

    parse result: 'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>


    """
    status_code = 0  # default
    text = ""

    # todo: read files from star
    # access star: C:\Users\moeltgen\Documents\python\colstudies_github\STAR_Files\Inventar\ZA100nn\ZA10002\Service
    # parse result: 'we need: <id> <file> <SN> <size> <type> <datapubl> <publ>
    lines = "44087;ZA0017_cdb.pdf;0017;118259;3;N;J; \r\n44088;ZA0017_cdb.pdf;0017;118259;3;N;J; \r\n"

    lines = ""
    count = 0

    studynodir = studyno[0:5] + "nn"

    filepath = os.path.join(
        g.starpath, studynodir, studyno, "Service"
    )  # Service folder for study
    print("filepath", filepath)

    if os.path.exists(filepath):
        files = os.listdir(filepath)

        for file in files:
            count += 1
            filecompletepath = os.path.join(filepath, file)
            filetype = str(GetMaterialtyp(file))
            filesize = str(os.path.getsize(filecompletepath))
            datapubl = ""
            publ = ""
            fileext = str(os.path.splitext(filecompletepath)[1])  # extension

            line = (
                "("
                + str(count)
                + ");"
                + file
                + ";"
                + studyno
                + ";"
                + filesize
                + ";"
                + filetype
                + ";"
                + datapubl
                + ";"
                + publ
                + "; \r\n"
            )
            lines += line

        status_code = 200  # ok
        print("Files found: " + str(count))

    else:
        status_code = 400  # not found
        text = "Path not found: " + filepath

    response = []
    if status_code == 200:
        return [status_code, lines]
    else:
        return [status_code, text]


def GetMaterialtyp(filename):
    # function from DBKEdit star.inc

    GetMtyp = 4  # Sonstiges

    filenameU = filename.upper()

    if "_CDB." in filenameU:
        GetMtyp = 3  # Codebuch
    if "_COD." in filenameU:
        GetMtyp = 3  # Codebuch

    if "_FB" in filenameU:
        GetMtyp = 1  # Fragebogen   #Achtung ohne Punkt wg. Erweiterungen
    if "_Q" in filenameU:
        GetMtyp = 1  # Fragebogen   #Achtung ohne Punkt wg. Erweiterungen
    if "_BQ" in filenameU:
        GetMtyp = 1  # Fragebogen   #Achtung ohne Punkt wg. Erweiterungen

    if "_MB." in filenameU:
        GetMtyp = 2  # Methodenbericht
    if "_MR." in filenameU:
        GetMtyp = 2  # Methodenbericht

    if ".POR" in filenameU:
        GetMtyp = 5  # Datensatz
    if ".SAV" in filenameU:
        GetMtyp = 5  # Datensatz
    if ".DTA" in filenameU:
        GetMtyp = 5  # Datensatz

    if "_B." in filenameU:
        GetMtyp = 6  # Datengeber-Bericht

    if "_CP." in filenameU:
        GetMtyp = 7  # Code-/Spaltenplan
    if "_SP." in filenameU:
        GetMtyp = 7  # Code-/Spaltenplan
    if "_CS." in filenameU:
        GetMtyp = 7  # Code-/Spaltenplan
    if "_CM." in filenameU:
        GetMtyp = 7  # Code-/Spaltenplan

    if "_ANM." in filenameU:
        GetMtyp = 8  # Anmerkungen

    if "_SB." in filenameU:
        GetMtyp = 9  # Studienbeschreibung
    if "_SD." in filenameU:
        GetMtyp = 9  # Studienbeschreibung

    if ".XLS" in filenameU:
        GetMtyp = 10  # Tabelle (ZHSF)

    if "_MFB." in filenameU:
        GetMtyp = 11  # Methodenfragebogen
    if "_MQ." in filenameU:
        GetMtyp = 11  # Methodenfragebogen

    if "_B." in filenameU:
        GetMtyp = 12  # Bericht #Achtung mit Punkt wg. _BQ
    if "_R." in filenameU:
        GetMtyp = 12  # Bericht

    if "_KS." in filenameU:
        GetMtyp = 13  # Kartenspiel/Listenheft
    if "_SC." in filenameU:
        GetMtyp = 13  # Kartenspiel/Listenheft
    if "_LH." in filenameU:
        GetMtyp = 13  # Kartenspiel/Listenheft

    # neu
    if ".XML" in filenameU:
        GetMtyp = 17  # DDI-C Codebook

    return GetMtyp
