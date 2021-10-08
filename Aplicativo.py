# Análisis de sensibilidad
from docplex.mp.model import Model

'''
Un campesino planea cultivar  para su fabricación de acuerdo con la siguiente tabla.

          |   Hectárea   |    Fanegada  |  Kilometro cuadrado  
-------------------------------------------------------------
 cafe     | 2500 plantas | 500 plantas  | 250000 plantas 
 aguacate | 350 plantas  | 70 plantas   | 35000 plantas
 cacao    | 1000 plantas | 200 plantas  | 100000 plantas

El campesino dispone de 100'000.000 semillas de cafe, 50'000.000 semillas aguacate y 70'000.000 semillas de cacao para 
iniciar la producción. Considera que puede vender cada kilogramo de cafe en 18000 pesos, cada kilogramo de aguacate en 
5000 pesos y cada kilogramo de cacao en 8500 pesos y que puede colocar en el mercado toda su producción. Determina los 
niveles de producción para cada uno de sus productos a fin de obtener el mayor ingreso posible y adicionalmente se busca 
realizar el respectivo análisis de sensibilidad.

x = kilogramos de cafe producidos
y = kilogramos de aguacate producidos
z = kilogramos de cacao producidos

'''

# Se nombra el modelo
md2 = Model('Análisis de sensibilidad en cultivos')

# Se crean las variables
x = md2.continuous_var(name='x')
y = md2.continuous_var(name='y')
z = md2.continuous_var(name='z')

# Se introduce la funcion objetivo
md2.maximize(18000*x+5000*y+8500*z)

# Se introducen las restricciones
md2.add_constraint(2500*x+350*y+1000*z <= 100000000)
md2.add_constraint(500*x+70*y+200*z <= 50000000)
md2.add_constraint(250000*x+35000*y+100000*z <= 70000000)

# Se soluciona el sistema
solution2 = md2.solve(log_output=True)
print("\nSolucion del sistema\n")
print(solution2)

# Numero de restricciones
n_const2 = md2.number_of_constraints

# Restricciones en un arreglo
const2 = [md2.get_constraint_by_index(i) for i in range(n_const2)]

# Variable de holgura
h2 = md2.slack_values(const2)

# Impresion variables de holgura
print("Variables de holgura\n")
for n in range(n_const2):
    print("La variable de holgura de la restricción "+str(const2[n])+" es "+str(h2[n]))

# Impresion valor dual
print("\nValor dual\n")
valor_dual2 = md2.dual_values(const2)
for n in range(n_const2):
    print("El valor dual de la restricción "+str(const2[n])+" es "+str(valor_dual2[n]))

# Aplicacion analisis de sensibilidad
cpx2 = md2.get_engine().get_cplex()
of2 = cpx2.solution.sensitivity.objective()
b2 = cpx2.solution.sensitivity.rhs()
var_list2 = [md2.get_var_by_name('x'), md2.get_var_by_name('y'), md2.get_var_by_name('z')]

print("\nAnalisis\n")
for n in range(len(var_list2)):
    print("La variable "+str(var_list2[n])+" "+str(of2[n]))

print("\nAnalisis\n")
for n in range(n_const2):
    print("La restricción "+str(const2[n])+" "+str(b2[n]))
print("\n")
