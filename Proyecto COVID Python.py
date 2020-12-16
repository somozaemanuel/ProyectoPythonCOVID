import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from datetime import datetime as dt

warnings.filterwarnings("ignore", message="Boolean series")
warnings.filterwarnings("ignore", message="Adding an axes")

comando=""

datos_paises = pd.read_csv('full_data.csv')
datos_paises_a_dic = datos_paises.to_dict('list')

def validate_date(d):
    try:
        if len(d) == 10: 
            dt.strptime(d, '%Y-%m-%d')
            return True
        else: return False

    except ValueError:
        return False


def detectar_puntos(paisA, paisB, dato_interes, grafico):
    diccionario = {}

    lider = ""
    contador = 1
    for (pA, pB) in zip(paisA[dato_interes], paisB[dato_interes]):
        if(pA == pB):
           diccionario[contador] = pA
        if(pA > pB):
            if(lider == ""):
                lider = 'A'
            if(lider == 'B'):
                diccionario[contador] = pB
                lider = 'A'
        if(pA < pB):
            if(lider == ""):
                lider = 'B'
            if(lider == 'A'):
                diccionario[contador] = pA
                lider = 'B'
        contador += 1

    plt.subplot(1,2,grafico)
    plt.plot(diccionario.keys(),diccionario.values(),'bo',label='Puntos interseccion')
    plt.legend()

def calcular_intersecciones(pais_uno,pais_dos,datos_deseados,dato_interes,grafico):
    datos_deseados_1 = datos_deseados[(datos_deseados['location'] == pais_uno) & (np.isnan(datos_deseados[dato_interes])!=True)]
    datos_deseados_2 = datos_deseados[(datos_deseados['location'] == pais_dos) & (np.isnan(datos_deseados[dato_interes])!=True)]
    detectar_puntos(datos_deseados_1,datos_deseados_2,dato_interes,grafico)

def graficar_pais(pais_deseado,datos_deseados):
    datos_deseados = datos_deseados[(datos_deseados['location'] == pais_deseado) & (np.isnan(datos_deseados['total_cases'])!=True)]
    datos_deseados_dic = datos_deseados.to_dict('list')
    cantidad_puntos = np.linspace(1,len(datos_deseados_dic.get('location')),len(datos_deseados_dic.get('location')))
    plt.plot(cantidad_puntos,datos_deseados_dic.get('total_cases'),label=pais_deseado+' casos')

def graficar_pais_2(pais_deseado,datos_deseados):
    datos_deseados = datos_deseados[(datos_deseados['location'] == pais_deseado) & (np.isnan(datos_deseados['total_deaths'])!=True)]
    datos_deseados_dic = datos_deseados.to_dict('list')
    cantidad_puntos = np.linspace(1,len(datos_deseados_dic.get('location')),len(datos_deseados_dic.get('location')))
    plt.plot(cantidad_puntos,datos_deseados_dic.get('total_deaths'),label=pais_deseado+' muertes')

def graficar_pais_3(pais_deseado,datos_deseados):
    datos_deseados_1 = datos_deseados[(datos_deseados['location'] == pais_deseado) & (np.isnan(datos_deseados['total_cases'])!=True)]
    datos_deseados_dic_1 = datos_deseados_1.to_dict('list')
    cantidad_puntos = np.linspace(1,len(datos_deseados_dic_1.get('location')),len(datos_deseados_dic_1.get('location')))
    plt.subplot(1, 2, 1)
    plt.plot(cantidad_puntos,datos_deseados_dic_1.get('total_cases'),label=pais_deseado+' casos')
    plt.xlabel('Dias transcurridos')
    plt.ylabel('Cantidad de casos totales')
    plt.yscale('log')
    plt.title('Comparación de casos positivos totales')
    plt.legend()

    datos_deseados_2 = datos_deseados[(datos_deseados['location'] == pais_deseado) & (np.isnan(datos_deseados['total_deaths'])!=True)]
    datos_deseados_dic_2 = datos_deseados_2.to_dict('list')
    cantidad_puntos = np.linspace(1,len(datos_deseados_dic_2.get('location')),len(datos_deseados_dic_2.get('location')))
    plt.subplot(1, 2, 2)
    plt.plot(cantidad_puntos,datos_deseados_dic_2.get('total_deaths'),label=pais_deseado+' muertes')
    plt.xlabel('Dias transcurridos')
    plt.ylabel('Cantidad de muertes totales')
    plt.title('Comparación de fallecimientos totales')
    plt.yscale('log')
    plt.legend()
   



def operacion1():
    pais_encontrado = False
    pais_deseado=""

    while (not pais_encontrado):
        pais_deseado = input('Ingrese el pais que desea consultar: ')
        pais_encontrado = pais_deseado in datos_paises_a_dic.get('location')
        if (not pais_encontrado):
            print('Error: El país ingresado no es válido o no se encuentra disponible a consultar. Por favor, intente de nuevo.')

    graficar_pais(pais_deseado,datos_paises)
    graficar_pais_2(pais_deseado,datos_paises)
    plt.xlabel('Dias transcurridos')
    plt.ylabel('Cantidad de casos totales')
    plt.yscale('log')
    plt.legend()
    plt.show()

def operacion2():
    paises_deseados = []
    paises_encontrados = False
    fechas_validas = False

    while (not paises_encontrados):
        paises_deseados = (input('Ingrese los paises que desea consultar, separados por comas: ')).split(',')
        paises_comun = set(paises_deseados) & set(datos_paises_a_dic.get('location'))
        paises_no_validos = set(paises_deseados) - paises_comun
        paises_nv = []
        for x in paises_no_validos:
            paises_nv.append(x)
        
        if (paises_no_validos):
            print('Error: Los siguientes países no son válidos:',paises_nv, '. Intente nuevamente.')
        else:
            paises_encontrados= True


    print("Ahora por favor ingrese de qué fecha a qué fecha desea visualizar la cantidad de casos totales y fallecimientos.")        

    while (not fechas_validas):
        fecha_ini = input('Ingrese la fecha inicial en formato AÑO-MES-DÍA (por ejemplo 2018-12-01): ')
        fecha_fin = input('Ingrese la fecha final en formato AÑO-MES-DÍA (por ejemplo 2018-12-01): ')
        fechas_validas = fecha_ini < fecha_fin and validate_date(fecha_ini) and validate_date(fecha_fin)
        if (not fechas_validas):
            print('Error: Las fechas ingresadas son inválidas. Asegúrese de respeter el formato. La fecha inicial debe ser anterior a la final. Intente nuevamente.')
        
    datos_deseados = datos_paises[(datos_paises['date'] >= fecha_ini) & (datos_paises['date'] <= fecha_fin)]

    for pais in paises_deseados:
        graficar_pais(pais,datos_deseados)
    
    plt.xlabel('Dias transcurridos')
    plt.ylabel('Cantidad de casos totales')
    plt.legend()
    plt.yscale('log')
    plt.savefig('Limitrofes.png')
    plt.show()

def operacion3():
    pais_deseado_1 = ''
    pais_deseado_2 = ''
    paises_encontrados = False
    fechas_validas = False

    while (not paises_encontrados):
        pais_deseado_1 = input('Ingrese el primer país por el que desea consultar: ')
        pais_deseado_2 = input('Ingrese el segundo país por el que desea consultar: ')
        paises_encontrados = pais_deseado_1 in datos_paises_a_dic.get('location')
        if (not paises_encontrados):
            print('El país ',pais_deseado_1,'no se encuentra disponible a consultar. Por favor, reintente con otro pais.')
        else:
            paises_encontrados = pais_deseado_2 in datos_paises_a_dic.get('location')
            if (not paises_encontrados):
                print('El país ',pais_deseado_2,' no se encuentra disponible a consultar. Por favor, reintente con otro país.')



    while (not fechas_validas):
        fecha_ini = input('Ingrese la fecha inicial en formato AÑO-MES-DÍA (por ejemplo 2018-12-01): ')
        fecha_fin = input('Ingrese la fecha final en formato AÑO-MES-DÍA (por ejemplo 2018-12-01): ')
        fechas_validas = fecha_ini < fecha_fin and validate_date(fecha_ini) and validate_date(fecha_fin)
        if (not fechas_validas):
            print('Error: Las fechas ingresadas son inválidas. Asegúrese de respeter el formato. La fecha inicial debe ser anterior a la final. Intente nuevamente.')
    

    datos_deseados = datos_paises[(datos_paises['date'] >= fecha_ini) & (datos_paises['date'] <= fecha_fin)]
    graficar_pais_3(pais_deseado_1,datos_deseados)
    graficar_pais_3(pais_deseado_2,datos_deseados)
    calcular_intersecciones(pais_deseado_1,pais_deseado_2,datos_deseados,'total_cases',1)
    calcular_intersecciones(pais_deseado_1,pais_deseado_2,datos_deseados,'total_deaths',2)
    plt.show()
    


print('Bienvenido al graficador de casos de COVID.')
while (comando!='salida'):
    comando = input('Ingrese la operación que desea realizar o teclee "ayuda" y presione enter para ver las funciones disponibles: ')

    if (comando=='ayuda'):
        print('')
        print('Ingrese "1" si desea conocer la cantidad total de casos y fallecimientos por COVID de un país')
        print('Ingrese "2" si desea comparar la cantidad de casos de COVID en diferentes países en un intervalo de tiempo ')
        print('Ingrese "3" si desea comparar la cantidad de casos totales y fallecimientos por COVID en dos países en un intervalo de tiempo')
        print('Ingrese "salida" si desea terminar la ejecución del programa.')
        print('')

    if (comando=='1'):
        operacion1()
    elif (comando=='2'):
        operacion2()
    elif (comando=='3'):
        operacion3()
    

        