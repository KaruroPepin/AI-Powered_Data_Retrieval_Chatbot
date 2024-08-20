from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import HumanMessagePromptTemplate,SystemMessagePromptTemplate,ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Clasificador
def ContextClassifier(prompt_usuario, client):

    system_template = """
    #Rol: 
        Clasifica el prompt "{prompt_usuario}" basado en su contexto. 
        Genera una etiqueta descriptiva que catalogue el tipo de fuente de datos y el contexto general del prompt. 
        Asegúrate de que la etiqueta sea precisa, representativa del contenido y sobretodo no variable.
        Entre las etiquetas que siempre utilizaras se encuentran: 'Base de Datos', 'Documento' y 'Grafico'.
        A continuación, te proporciono ejemplos de prompts para clasificar:

        -Ejemplo 1: 
        Enunciado: Cuales tipo de propiedades se encuentran disponibles?.
	    Etiqueta: Base de Datos

        -Ejemplo 2: 
        Enunciado: Cual es la definicion de corporate information?.
	    Etiqueta: Documento      

        -Ejemplo 3: 
        Enunciado: Cual es el top 5 estados en los que se encuentran las propiedades?.
	    Etiqueta: Base de Datos

        -Ejemplo 4: 
        Enunciado: Dame un resumen de la seccion 3 del documento de modelos de datos.
	    Etiqueta: Documento

        -Ejemplo 5:
        Enunciado: Proporciona una lista de clientes que han realizado compras en el último mes.
        Etiqueta: Base de Datos 

        -Ejemplo 6:
        Enunciado: Cual es el propósito principal del documento de estrategia de ventas?
        Etiqueta: Documento

        -Ejemplo 7:
        Enunciado: Que define el término 'transformación digital' en el informe?
        Etiqueta: Documento


        -Ejemplo 8:
        Enunciado: Que registros de ventas están disponibles para el mes de julio?
        Etiqueta: Base de Datos

        -Ejemplo 9:
        Enunciado: Resume los puntos clave del informe de rendimiento anual.
        Etiqueta: Documento

        -Ejemplo 10:
        Enunciado: ¿Cuáles son los productos más vendidos en el último trimestre?
        Etiqueta: Base de Datos

        -Ejemplo 11:
        Enunciado: Dame una lista de clientes con facturas pendientes.
        Etiqueta: Base de Datos

        -Ejemplo 12:
        Enunciado: Que politicas se mencionan en el manual del empleado?
        Etiqueta: Documento

        -Ejemplo 13:
        Enunciado: Proporciona la definicion de los terminos en el glosario del informe técnico.
        Etiqueta: Documento

        -Ejemplo 14:
        Enunciado: Cual es la conclusion del analisis de mercado del informe financiero?
        Etiqueta: Documento

        -Ejemplo 15:
        Enunciado: Genera un grafico de barras que muestre el crecimiento de la poblacion en las ciudades principales del pais en los ultimos 10 años.
        Etiqueta: Grafico

        -Ejemplo 16:
        Enunciado: Quiero ver una comparacion visual de las ventas mensuales entre 2022 y 2023 en un grafico de lineas.
        Etiqueta: Grafico

        -Ejemplo 17:
        Enunciado: Crea un grafico circular que represente la distribucion de las ganancias por region en el ultimo trimestre.
        Etiqueta: Grafico

        -Ejemplo 18:
        Enunciado: Haz un diagrama de dispersion que muestre la relacion entre la inversion en publicidad y el incremento en las ventas.
        Etiqueta: Grafico

        -Ejemplo 19:
        Enunciado: Elaborar un grafico de columnas comparando las tasas de graduacion en diferentes universidades.
        Etiqueta: Grafico

        -Ejemplo 20:
        Enunciado: Quisiera ver un histograma que muestre la distribucion de edades de nuestros clientes.
        Etiqueta: Grafico

        -Ejemplo 21:
        Enunciado: Proporciona un grafico de area que ilustre la acumulacion de capital durante los ultimos 20 años.
        Etiqueta: Grafico

        -Ejemplo 22:
        Enunciado: Genera un grafico de radar que compare las caracteristicas clave de nuestros productos con los de la competencia.
        Etiqueta: Grafico
    
    #Resultado final: Como resultado final a tu respuesta esta siempre sera la Etiqueta. No debes responder con algo distinto a las etiquetas indicadas.

    """
    system_prompt = PromptTemplate(template=system_template,input_variables=["dbschema"])
    system_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

	#2. Humano
    human_template = """
	Pregunta:{prompt_usuario}\n
	Etiqueta:
	"""
    human_prompt = PromptTemplate(template=human_template,input_variables=["prompt_usuario"])
    human_prompt = HumanMessagePromptTemplate(prompt=human_prompt)

	#3. Chat
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    label = chat_prompt | client | StrOutputParser()
    label = label.invoke({"prompt_usuario":prompt_usuario})
    return label   

# Query Maker
def QueryMaker(prompt_usuario, client, dbschema):

    system_template = """
        # Rol:
            Eres un asistente de inteligencia artificial diseñado para ayudar al equipo de ingeniería de datos a realizar consultas en diversas fuentes de datos. 
            Tu tarea principal es responder a las preguntas de los usuarios proporcionando un scripts SQL a partir del esquema de base de datos entregado a continuacion: 
            
        #Este es el esquema de base de datos: 
            {dbschema}

        #Tarea:
            a. Solo debes dar como resultado el query/consulta sin ningun otro character como las comillas (```) o palabra.
            b. Es importante entregar la consulta en un formato ordenado y facil de entender.
            c. Como último paso en la elaboración de tus respuestas, siempre evalúas la coherencia y objetividad de las mismas.
            d. Creas consultas SQL los cuales poseen los siguientes criterios de aceptacion:

                ##Optimización del Rendimiento:
                    1. Utiliza SELECT con solo las columnas necesarias en lugar de SELECT * para reducir el consumo de recursos y el ancho de banda.
                    2. Asegúrate de que las columnas utilizadas en las condiciones WHERE, JOIN, ORDER BY, y GROUP BY tengan índices adecuados para mejorar la velocidad de la consulta.
                    3. Operaciones como funciones o cálculos en columnas indexadas pueden deshabilitar el uso del índice.
                    4. Para consultas que retornan grandes conjuntos de datos, utiliza LIMIT y OFFSET para paginar los resultados.

                ##Objetividad y Exactitud:
                    1. Asegúrate de que los datos utilizados sean precisos y estén actualizados.
                    2. Usa alias de tablas y columnas para evitar ambigüedades en la consulta, especialmente en consultas con múltiples tablas.
                    3. Define claramente las condiciones en la cláusula WHERE para asegurarte de que la consulta retorne los resultados esperados.

                ##Seguridad
                    1. Usa declaraciones preparadas y parámetros vinculados en lugar de concatenar cadenas para evitar inyecciones SQL.
                    2. Cifra los datos sensibles, como números de tarjetas de crédito o información personal.
                    3. Validación de Entrada: Valida y sanitiza todas las entradas del usuario para evitar la ejecución de consultas maliciosas.

                ##Legibilidad:
                    1. Usa convenciones de nombres consistentes para tablas, columnas, y alias.
                    2. Divide las consultas largas y complejas en subconsultas o vistas para facilitar la lectura y el mantenimiento.

        #Contexto:
            El equipo de ingeniería de datos necesita una herramienta de inteligencia artificial que genere consultas SQL optimizadas.

        #Ejemplos:
            - Ejemplo 1: 
                Pregunta: 
                    Top 3 Quaters con mayor ventas en los ultimos 10 años.
                Consulta:
                    SELECT TOP 3
                        DATEPART(YEAR, soh.OrderDate) AS Year, 
                        DATEPART(QUARTER, soh.OrderDate) AS Quarter, 
                        SUM(soh.TotalDue) AS TotalSales 
                    FROM 
                        SalesLT.SalesOrderHeader AS soh 
                    GROUP BY 
                        DATEPART(YEAR, soh.OrderDate), 
                        DATEPART(QUARTER, soh.OrderDate) 
                    ORDER BY 
                        TotalSales DESC;
        #Respuesta final:
            Tu respuesta final debe ser un un script SQL limpio y sin caracteres no permitidos por SQL Server como los es ```.                
    """
    system_prompt = PromptTemplate(template=system_template,input_variables=["dbschema"])
    system_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

	#2. Humano
    human_template = """
	Pregunta:{prompt_usuario}\n
	Query:
	"""
    human_prompt = PromptTemplate(template=human_template,input_variables=["prompt_usuario"])
    human_prompt = HumanMessagePromptTemplate(prompt=human_prompt)

	#3. Chat
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    llm_chain = chat_prompt | client | StrOutputParser()
    llm_chain = llm_chain.invoke({"prompt_usuario":prompt_usuario, "dbschema":dbschema})
    return llm_chain

def chart_type(prompt_usuario, client):

    system_template = """
    #Rol: 
        Clasifica el prompt "{prompt_usuario}" basado en su contexto y elabora un titulo descriptivo. 
        Genera una etiqueta descriptiva que catalogue el tipo de grafico mas cercano al enunciado y un titulo descriptivo que servira como encabezado. 
        Asegúrate de que el tipo de grafico sea precisa, representativa del contenido y asi mismo con el titulo descriptivo.
        Entre los tipos de graficos que utilizaras se encuentran: 'barras', 'lineas', 'circular', 'dispersion', 'histograma' y 'area'.
        A continuación, te proporciono ejemplos de prompts para clasificar:

        -Ejemplo 1: 
        Enunciado: ¿Cuál es la distribución de ventas por región en el último trimestre?
        Etiqueta: barras
        Titulo: Distribución de Ventas por Región en el Último Trimestre

        -Ejemplo 2: 
        Enunciado: Muestra la tendencia de crecimiento de usuarios durante los últimos 12 meses.
        Etiqueta: barras
        Titulo: Tendencia de Crecimiento de Usuarios en los Últimos 12 Meses

        -Ejemplo 3: 
        Enunciado: ¿Cómo se divide el presupuesto anual entre los diferentes departamentos?
        Etiqueta: circular
        Titulo: Distribución del Presupuesto Anual por Departamento
        
        -Ejemplo 4: 
        Enunciado: ¿Existe alguna correlación entre la edad de los clientes y el monto de sus compras?
        Etiqueta: barras
        Titulo: Correlación entre Edad de los Clientes y Monto de Compras
        
        -Ejemplo 5: 
        Enunciado: ¿Cómo se distribuyen las puntuaciones de los exámenes en la última prueba?
        Etiqueta: dispersion
        Titulo: Distribución de Puntuaciones en la Última Prueba
        
        -Ejemplo 6: 
        Enunciado: Muestra el cambio en la participación de mercado de las principales marcas durante los últimos cinco años.
        Etiqueta: area
        Titulo: Cambio en la Participación de Mercado de las Principales Marcas en los Últimos Cinco Años
        
        -Ejemplo 7:
        Enunciado: ¿Cuántos productos se vendieron en cada categoría el mes pasado?
        Etiqueta: barras
        Titulo: Ventas por Categoría en el Mes Pasado
        
        -Ejemplo 8:
        Enunciado: Comparación de ingresos por tienda en diferentes ciudades.
        Etiqueta: barras
        Titulo: Comparación de Ingresos por Tienda en Diferentes Ciudades

        
        -Ejemplo 9:
        Enunciado: ¿Cuál es el número de empleados por departamento?
        Etiqueta: barras
        Titulo: Número de Empleados por Departamento
        
        -Ejemplo 10:
        Enunciado: Muestra las ventas mensuales por producto.
        Etiqueta: barras
        Titulo: Ventas Mensuales por Producto

        -Ejemplo 11:
        Enunciado: Comparar el número de suscriptores nuevos en cada región.
        Etiqueta: barras
        Titulo: Comparación de Nuevos Suscriptores por Región
        
        -Ejemplo 12:
        Enunciado: ¿Cómo ha evolucionado el precio de las acciones en los últimos seis meses?
        Etiqueta: lineas
        Titulo: Evolución del Precio de las Acciones en los Últimos Seis Meses
        
        -Ejemplo 13:
        Enunciado: Muestra el crecimiento de ingresos anuales desde 2015.
        Etiqueta: lineas
        Titulo: Crecimiento de Ingresos Anuales desde 2015
        
        -Ejemplo 14
        Enunciado: Tendencia de consumo de energía en los últimos 24 meses.
        Etiqueta: lineas
        Titulo: Tendencia del Consumo de Energía en los Últimos 24 Meses
        
        -Ejemplo 15:
        Enunciado: Evolución del número de usuarios activos por mes en el último año.
        Etiqueta: lineas
        Titulo: Evolución del Número de Usuarios Activos por Mes en el Último Año
        
        -Ejemplo 16:
        Enunciado: ¿Cómo ha cambiado la temperatura promedio mensual en la última década?
        Etiqueta: lineas
        Titulo:
        
        -Ejemplo 17:
        Enunciado: Distribución del uso del tiempo en una jornada laboral típica.
        Etiqueta: circular
        Titulo: Distribución del Uso del Tiempo en una Jornada Laboral Típica
                
        -Ejemplo 18:
        Enunciado: ¿Cuál es la proporción de ventas de cada producto respecto al total?
        Etiqueta: circular
        Titulo: Proporción de Ventas por Producto respecto al Total

        -Ejemplo 19:
        Enunciado: Muestra la participación de cada segmento de clientes en las ventas totales.
        Etiqueta: circular
        Titulo: Participación de Segmentos de Clientes en las Ventas Totales
        
        -Ejemplo 20:
        Enunciado: ¿Hay una relación entre la experiencia laboral y el salario en la empresa?
        Etiqueta: dispersion
        Titulo: Relación entre Experiencia Laboral y Salario en la Empresa
        
        -Ejemplo 21:
        Enunciado: Analiza la correlación entre horas de estudio y calificaciones obtenidas.
        Etiqueta: dispersion
        Titulo: Correlación entre Horas de Estudio y Calificaciones Obtenidas
        
        -Ejemplo 22:
        Enunciado: ¿Existe alguna correlación entre la cantidad de ejercicio semanal y el índice de masa corporal?
        Etiqueta: dispersion
        Titulo: Relación entre Cantidad de Ejercicio Semanal e Índice de Masa Corporal
        
        -Ejemplo 23:
        Enunciado: Relación entre el tamaño de las casas y su precio de venta.
        Etiqueta: dispersion
        Titulo: Relación entre Tamaño de las Casas y Precio de Venta
        
        -Ejemplo 24:
        Enunciado: Muestra la distribución de edades de los clientes.
        Etiqueta: histograma
        Titulo: Distribución de Edades de los Clientes
        
        -Ejemplo 25:
        Enunciado: ¿Cómo se distribuyen los salarios entre los empleados?
        Etiqueta: histograma
        Titulo: Distribución de Salarios entre los Empleados
        
        -Ejemplo 26:
        Enunciado: Distribución de los tiempos de entrega de pedidos en los últimos meses.
        Etiqueta: histograma
        Titulo: Distribución de Tiempos de Entrega de Pedidos en los Últimos Meses
        
        -Ejemplo 27:
        Enunciado: Muestra el cambio en el número de empleados por año en los últimos 10 años.
        Etiqueta: area
        Titulo: Cambio en el Número de Empleados por Año en los Últimos 10 Años
        
        -Ejemplo 28:
        Enunciado: Evolución del tráfico web por canal a lo largo del año pasado.
        Etiqueta: area
        Titulo: Evolución del Tráfico Web por Canal en el Último Año
        
        -Ejemplo 29:
        Enunciado: Comparación del crecimiento de ingresos entre diferentes productos durante los últimos cinco años.
        Etiqueta: area
        Titulo: Comparación del Crecimiento de Ingresos entre Diferentes Productos en los Últimos Cinco Años
        

    #Resultado final: Como resultado final a tu respuesta, esta siempre sera la Etiqueta del tipo de grafico y el titulo para el grafico. No debes responder con algo distinto a las opciones indicadas.
    #Ejemplo del resultado final: 
        -Ejemplo: 
        Enunciado: Distribución de los tiempos de entrega de pedidos en los últimos meses.
        Etiqueta: histograma
        Titulo: Distribución de Tiempos de Entrega de Pedidos en los Últimos Meses
        Resultado final: histograma,Distribución de Tiempos de Entrega de Pedidos en los Últimos Meses

    """
    system_prompt = PromptTemplate(template=system_template,input_variables=["dbschema"])
    system_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

	#2. Humano
    human_template = """
	Pregunta:{prompt_usuario}\n
	Etiqueta:
	"""
    human_prompt = PromptTemplate(template=human_template,input_variables=["prompt_usuario"])
    human_prompt = HumanMessagePromptTemplate(prompt=human_prompt)

	#3. Chat
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    grhtype = chat_prompt | client | StrOutputParser()
    grhtype = grhtype.invoke({"prompt_usuario":prompt_usuario})
    return grhtype
