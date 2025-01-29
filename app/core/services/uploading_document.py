from fastapi import UploadFile, HTTPException

import os

upload_folder = "media"
os.makedirs(upload_folder, exist_ok=True)

async def upload_documents(file: UploadFile):
    file_path = os.path.join(upload_folder, file.filename)
    try:
        with open(file_path, "wb") as f:
            content_read = await file.read()
            f.write(content_read)
            return {"filename": file.filename, "message": "Документ успешно загружен"}
    except Exception as e: # Сделать отлов конкретных ошибок
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке файла: {e}")