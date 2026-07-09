from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import DocumentModel

DocumentModel.metadata.create_all(bind=engine)

app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class DocumentCreate(BaseModel):
    title: str
    subject: str
    document_type: str
    file_url: str



@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(DocumentModel).all()

    return {
        "message": "Lấy danh sách tài liệu thành công",
        "data": documents
    }


@app.post("/documents")
def create_document(document: DocumentCreate,
                    db: Session = Depends(get_db)):

    new_document = DocumentModel(
        title=document.title,
        subject=document.subject,
        document_type=document.document_type,
        file_url=document.file_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Thêm tài liệu thành công",
        "data": new_document
    }


def delete_document_service(db: Session, document_id: int):

    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài liệu"
        )

    result = {
        "id": document.id,
        "title": document.title,
        "subject": document.subject,
        "document_type": document.document_type,
        "file_url": document.file_url
    }

    db.delete(document)
    db.commit()


@app.delete("/documents/{document_id}")
def delete_document(document_id: int,
                    db: Session = Depends(get_db)):

    document = delete_document_service(db, document_id)

    return {
        "message": "Xóa tài liệu thành công",
        "data": document
    }