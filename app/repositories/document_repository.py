from pathlib import Path
import json

class DocumentRepository:

    def __init__(self):

        self.metadata_file = Path(
            "document_metadata.json"
            )
        if not self.metadata_file.exists():
            self.metadata_file.write_text("[]")

    def get_all(self):

        return json.loads(
            self.metadata_file.read_text()
        )
    
    def get_all(self):

        return json.loads(
            self.metadata_file.read_text()
        )
    
    def save_all(self,documents):

        self.metadata_file.write_text(
            json.dumps(
                documents,
                indent=4
            )
        )