import os
from datetime import datetime
from elasticsearch import Elasticsearch

class SIEMLogger:
    def __init__(self):
        self.es = Elasticsearch(
            os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
        )
        self.index = "narmer-audit"

    def log(self, event: str, user: str, details: dict):
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "user": user,
            "details": details,
            "app": "narmer-pharaoh"
        }
        try:
            self.es.index(index=self.index, body=doc)
        except:
            pass  # فشل صامت إذا لم يكن Elasticsearch متاحًا

# استخدام
siem = SIEMLogger() 