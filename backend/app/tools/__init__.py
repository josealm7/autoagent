from app.tools.search_docs import search_docs
from app.tools.web_search import web_search
from app.tools.send_email import send_email
from app.tools.read_document import read_document
from app.tools.summarize import summarize

ALL_TOOLS = [search_docs, web_search, send_email, read_document, summarize]
TOOL_NAMES = [t.name for t in ALL_TOOLS]
