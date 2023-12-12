import glob
import fitz
import numpy
import pymysql
from conexion import miConexion

# pdf = r"C:\Test\pdfs\\FN51941\\COMPROBANTES\THALIA_ELIZABETH_VENEGAS_DE_LEON_686625.pdf"

mycursor = miConexion.cursor()


def minfun(pdf):
    documento = fitz.open(pdf)
    # print("numero de paginas ", documento.pageCount)
    # print("Mtadatos", documento.metadata)

    pagina = documento.loadPage(0)

    text = pagina.getText("texto")

    st = text.index('SOCIAL')
    RFC = text.index('RFC')
    FOLIO = text.index('FOLIO')
    FOLIO_FISCAL = text.index('FOLIO FISCAL')
    CERTIFICADO = text.index('No. CERTIFICADO')
    # print(RFC)
    # print(st)
    UUID = text[FOLIO_FISCAL + 12:CERTIFICADO]
    #print(UUID)
    FOLIO1 = text[FOLIO + 5:FOLIO_FISCAL]
    #print(FOLIO1)

    nombre = text[st + 6:RFC]
    # print(nombre)

    da = nombre.split(" ")
    print()
    srt = ''

    for k in range(2, len(da)):
        srt += da[k] + ' '

        nombre = srt
        nombre1 = nombre.split("\n")
        srt2 = ''
        for m in range(len(nombre1)):
            # o = nombre1[0] + ' ' + nombre1[1]
            srt2 += nombre1[m] + ' '
        nombre2 = srt2
        a_paterno = da[0]

        a_materno = da[1]

        sql = "UPDATE movsnomina SET uuid = %s WHERE folio_nomina = %s and a_paterno =%s and a_materno =%s and nombre =%s"

        val = (UUID.strip(), FOLIO1.strip(), a_paterno.strip(), a_materno.strip(), nombre2.strip())
        print(val)

        mycursor.execute(sql, val)

        miConexion.commit()

        print(mycursor.rowcount, "record(s) affected")


my_array = numpy.array(["FN50845",
                        "FN51237",
                        "FN51239",
                        "FN51819",
                        "FN51941"])
d = "\\"
for x in my_array:
    car = x + d
    # print(car)
    targetPattern = r'C:\Test\pdfs\\' + car + 'COMPROBANTES\\*.pdf'
    # print(targetPattern)
    datos = glob.glob(targetPattern)
    # print(datos)
    for j in datos:
        minfun(j)
