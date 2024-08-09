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
        Entre las etiquetas a siempre utilizaras se encuentran: 'Base de Datos' y 'Documento'.
        A continuación, te proporciono el prompt para clasificar:

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
            Tu respuesta final debe ser un un script SQL limpio y sin caracteres no permitidos por SQL Server.                
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
