import re
import sys
import csv
from constraint import *





def main(argv):
    '''principal'''
    def sin_repetir(variable1, variable2):
        if variable1 != "-" and variable1 == variable2:
            return False
        return True

    def esta(*variables):
        # Obtener los valores únicos de todas las variables
        valores_variables = set(variables)

        # Verificar que al menos un valor de cada dominio esté presente
        for dominio_valor in valores:
            if dominio_valor not in valores_variables and dominio_valor != "-":
                return False

        return True

    def electricidad(variable):
        if variable[-1] == "C":
            return False
        return True

    def vehiculos_sin_interferencia(*variables):
        # Crear un diccionario para mapear las posiciones de los vehículos

        for i in range(0, filas):
            for j in range(0, columnas):
                var = variables[i*columnas+j]

                if var != '-':
                    id, tipo, nevera = var.split('-')
                    if tipo == 'TSU':
                        for u in range(j, columnas):
                            var_u = variables[i*columnas+u]

                            if var_u != '-':
                                id2, tipo2, nevera2 = var_u.split('-')
                                if tipo2 == 'TNU':
                                    return False
        return True

    def espacio_en_los_lados(*variables):
        for i in range(0, filas):
            for j in range(0, columnas):
                var = variables[i*columnas+j]
                if var != '-':
                    if i == 0:
                        var2 = variables[(i+1)*columnas+j]
                        if var2 != '-':
                            return False
                    elif i == filas-1:
                        var2 = variables[(i-1)*columnas+j]
                        if var2 != '-':
                            return False
                    else:
                        var2 = variables[(i+1)*columnas+j]
                        var3 = variables[(i-1)*columnas+j]
                        if var2 != '-' and var3 != '-':
                            return False
        return True
# ------------------------------------------------------

    with open(argv[1], 'r') as f:
        archivo = f.read()
        f.close()
    lines = archivo.split('\n')
    matriz = lines[0].split('x')
    filas = int(matriz[0])
    columnas = int(matriz[1])
    valores = []
    for linea in lines[2:]:
        if linea != '':
            valores.append(linea)

    valores.append("-")

    problem = Problem()
    variables = []
    for i in range(1, filas+1):
        for j in range(1, columnas+1):
            problem.addVariable(str(i)+str(j), valores)
            variables.append(str(i)+str(j))


#restriccion 1.1
    problem.addConstraint(esta, tuple(variables))

#restriccion 1.2
    for i in range(1, filas+1):
        for j in range(1, columnas+1):
            for k in range(1, filas+1):
                for l in range(1, columnas+1):
                    if int(str(i) + str(j)) < int(str(k) + str(l)):
                        problem.addConstraint(sin_repetir, (str(i) + str(j), str(k) + str(l)))


#restriccion 3
    valores_pe = re.findall(r'\((.*?)\)', lines[1])
    lista_valores_pe = [valor.replace(',', '') for valor in valores_pe]
    for i in variables:
        if i not in lista_valores_pe:
            problem.addConstraint(electricidad, (i,))

#restriccion 4

    problem.addConstraint(vehiculos_sin_interferencia, tuple(variables))

#restriccion 5
    problem.addConstraint(espacio_en_los_lados, variables)

#solucion
    num_sol = len(problem.getSolutions())
    solucion = problem.getSolution()

    data = []
    soluciones_csv = ["N. Sol: ", num_sol]
    data.append(soluciones_csv)
    if solucion != None:
        for i in range(1, filas+1):
            fila = []
            for j in range(1, columnas+1):
               fila.append(solucion[str(i)+str(j)])
            data.append(fila)

    nombre_archivo = argv[1].split("/")[-1]
    nombre_archivo = nombre_archivo.split('.')[0]

    with open("./CSP-tests/"+nombre_archivo + '.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)




if __name__ == "__main__":
    main(sys.argv)
