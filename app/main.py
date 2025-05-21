from fastapi import FastAPI, UploadFile
from service import PhoneExtractor
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from middleware import catch_exceptions_middleware
from fastapi import Request

app = FastAPI()
app.middleware("http")(catch_exceptions_middleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/extract-phones/")
async def extract_phones(file: UploadFile):
    """
        Обрабатывает POST-запрос для извлечения телефонных номеров из загруженного текстового файла.

        Args:
            file (UploadFile): Загруженный файл, содержащий текст.

        Returns:
            dict: Список извлечённых телефонных номеров или сообщение об их отсутствии.

        Raises:
            HTTPException: Если файл пустой, не текстовый, или не в формате UTF-8.
     """
    content = await file.read()
    extractor = PhoneExtractor()
    numbers = extractor.extract_from_text(content, file.content_type)

    if not numbers:
        return {"message": "Телефонные номера не найдены."}

    return {"phones": numbers}


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    """
        Отображает HTML-форму для загрузки файла.

        Args:
            request (Request): Объект запроса.

        Returns:
            TemplateResponse: HTML-страница с формой загрузки.
    """
    return templates.TemplateResponse("form.html", {"request": request})
