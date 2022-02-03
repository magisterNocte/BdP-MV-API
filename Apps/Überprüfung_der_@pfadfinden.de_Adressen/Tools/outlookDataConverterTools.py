
import os
import pathlib

from openpyxl.utils import get_column_letter


class excelHandling():
    path = str(pathlib.Path(__file__).parent.resolve())

    def sort_outlook_ws(sourceWs, sortedWS):
        print("Sorting Data...")
        i = 1
        while sourceWs["A" + str(i)].value != None:
            rowValue = sourceWs["A" + str(i)].value.split(',')
            column = 1
            for x in rowValue:
                sortedWS[get_column_letter(
                    column) + str(i)] = rowValue[column-1]
                column += 1
            i += 1
        print("Data sorted.")

    def filter_outlook_ws(sourceWs, filteredWsPostfach, filteredWsWeiterleitung, exceptionWs):
        print("Filtering Data...")
        # LV Einträge werden als erstes aussortiert weil sie buggy sind
        i = 1
        lineInFilteredPostfach = 1
        lineInFilteredWeiterleitung = 1
        lineInNoPeople = 1
        while sourceWs["A" + str(i)].value != None:
            if "LV" in sourceWs["G" + str(i)].value:
                sourceWs.delete_rows(i)
                i -= 1
            elif "Landesversammlung" in sourceWs["G" + str(i)].value:
                exceptionWs["A" +
                            str(lineInNoPeople)] = sourceWs["G" + str(i)].value
                exceptionWs["B" +
                            str(lineInNoPeople)] = sourceWs["AF" + str(i)].value
                lineInNoPeople += 1

            elif sourceWs["I" + str(i)].value != "" and "Office 365 E2" in sourceWs["N" + str(i)].value:
                filteredWsPostfach["A" + str(lineInFilteredPostfach)
                                   ] = sourceWs["I" + str(i)].value
                filteredWsPostfach["B" +
                                   str(lineInFilteredPostfach)] = sourceWs["K" + str(i)].value
                filteredWsPostfach["C" +
                                   str(lineInFilteredPostfach)] = sourceWs["AF" + str(i)].value
                lineInFilteredPostfach += 1

            elif sourceWs["I" + str(i)].value != "":
                filteredWsPostfach["A" + str(lineInFilteredPostfach)
                                   ] = sourceWs["I" + str(i)].value
                filteredWsWeiterleitung["A" + str(
                    lineInFilteredWeiterleitung)] = sourceWs["I" + str(i)].value
                filteredWsWeiterleitung["B" + str(
                    lineInFilteredWeiterleitung)] = sourceWs["K" + str(i)].value
                filteredWsWeiterleitung["C" + str(
                    lineInFilteredWeiterleitung)] = sourceWs["AF" + str(i)].value
                lineInFilteredWeiterleitung += 1
            else:
                exceptionWs["A" +
                            str(lineInNoPeople)] = sourceWs["G" + str(i)].value
                exceptionWs["B" +
                            str(lineInNoPeople)] = sourceWs["AF" + str(i)].value
                lineInNoPeople += 1
            i += 1
        print("Data Filtered.")

    def save_new_file(wb, workbook_file_name):
        wb.save(workbook_file_name)
        saveFile = input("Datei" + workbook_file_name + " behalten? (y/n): ")
        if (saveFile) == "n":
            os.remove("test_excel_file.xlsx")
