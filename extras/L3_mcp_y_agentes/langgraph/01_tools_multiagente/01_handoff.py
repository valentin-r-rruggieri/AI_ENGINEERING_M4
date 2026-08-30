# Este archivo forma parte del recorrido práctico de LangGraph.
# Lee la explicación, ejecuta el ejemplo y modifica una variable por vez.

"""Handoff explícito entre dos agentes representados como nodos.

GUÍA DOCENTE
CUÁNDO USAR: cuando dos especialidades participan en un orden conocido.
DIFERENCIA: el estado hace visible qué entrega el primer agente al segundo.
EN CLASE: comprobar que contextualizar no produce el resultado final.
"""

# Importa TypedDict y componentes de LangGraph.
from typing import TypedDict
from langgraph.graph import END, START, StateGraph

# Define los artefactos compartidos entre roles.
class Estado(TypedDict):
    original: str
    nuevo: str
    contexto: str
    cambio: str

# Simula el rol que construye el mapa contextual.
def contextualizar(estado: Estado) -> dict[str, str]:
    return {"contexto": "Ambos textos regulan la vigencia del contrato."}

# Simula el rol que extrae usando el contexto anterior.
def extraer(estado: Estado) -> dict[str, str]:
    return {"cambio": f"{estado['contexto']} El plazo cambia de 12 a 18 meses."}

# Conecta el handoff de manera auditable.
constructor = StateGraph(Estado)
constructor.add_node("contextualizador", contextualizar)
constructor.add_node("extractor", extraer)
constructor.add_edge(START, "contextualizador")
constructor.add_edge("contextualizador", "extractor")
constructor.add_edge("extractor", END)
grafo = constructor.compile()

estado = grafo.invoke({"original": "12 meses", "nuevo": "18 meses", "contexto": "", "cambio": ""})
print(estado)

# Resumen final: este ejercicio hace visible el handoff entre roles.
# Elimina contexto del estado y analiza qué información pierde el extractor.
