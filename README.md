# 🤖 AutoAgent — Agente IA Empresarial

> Agente de inteligencia artificial que **piensa, decide y actúa** de forma autónoma. Le das un objetivo y él decide qué herramientas usar para completarlo.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.1-f55036)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker)

---

## ¿Qué diferencia a un Agente de un Chatbot?

| Chatbot (SmartChat) | Agente (AutoAgent) |
|---|---|
| Responde preguntas | Completa tareas |
| Usa documentos pasivamente | Decide qué herramientas usar |
| Un solo paso | Múltiples pasos encadenados |
| Recupera información | Actúa: busca, envía, analiza |

---

## ✨ Herramientas disponibles

| Herramienta | Descripción |
|---|---|
| 🔍 `search_docs` | Busca en documentos internos (ChromaDB) |
| 🌐 `web_search` | Busca en internet con DuckDuckGo (gratis) |
| 📧 `send_email` | Envía emails via Gmail SMTP |
| 📄 `read_pdf` | Lee y analiza archivos PDF |
| ✂️ `summarize` | Resume textos largos |

---

## 🚀 Inicio rápido

```bash
# 1. Clonar
git clone https://github.com/tuusuario/autoagent.git
cd autoagent/backend

# 2. Configurar entorno
cp .env.example .env
# Edita .env con tu GROQ_API_KEY

# 3. Instalar
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 4. Arrancar
uvicorn main:app --reload --port 8000
```

Abre `frontend/index.html` en el navegador.

---

## 🐳 Docker

```bash
cp backend/.env.example backend/.env
# Edita backend/.env

docker compose up --build
```

---

## 💡 Ejemplos de tareas

```
"Busca información sobre seguros de hogar en los documentos"
"Busca en internet el precio medio de seguros de auto en España"
"Resume los documentos subidos y envía el resumen a cliente@email.com"
"¿Qué diferencia hay entre seguro a terceros y todo riesgo?"
```

---

## 🏗️ Arquitectura

```
Usuario → objetivo
    ↓
Agent Engine (LangChain ReAct)
    ↓
LLM decide plan (Groq LLaMA 3.1)
    ↓
Ejecuta herramientas en orden
    ↓
Razona sobre resultados
    ↓
Respuesta final + pasos visibles
```

---

## 📁 Estructura

```
autoagent/
├── backend/
│   ├── main.py
│   ├── app/
│   │   ├── api/          # Endpoints FastAPI
│   │   ├── core/         # Config / settings
│   │   ├── models/       # Schemas Pydantic
│   │   ├── services/     # Agent engine + memoria
│   │   └── tools/        # Herramientas del agente
│   └── data/
└── frontend/
    └── index.html
```

---

## 🔗 Relación con SmartChat

AutoAgent comparte la misma base vectorial que [SmartChat](https://github.com/tuusuario/smartchat). Puedes indexar documentos en SmartChat y el agente los usará automáticamente con la herramienta `search_docs`.

---

*Stack: FastAPI · LangChain · Groq · ChromaDB · DuckDuckGo · Docker*
