import re
from typing import List
from loguru import logger
from fastapi import HTTPException

class PhoneExtractor:
    """
        Класс для извлечения российских телефонных номеров из текста.

        Атрибуты:
            PHONE_REGEX (Pattern): Регулярное выражение для поиска номеров.
    """
    PHONE_REGEX = re.compile(
        r"(?:\+7|8)\s*[\(\-]?(\d{3})[\)\-]?\s*(\d{3})[\-\.\s]?(\d{2})[\-\.\s]?(\d{2})"
    )

    def extract_from_text(self, content: bytes, content_type: str) -> List[str]:
        """
            Извлекает телефонные номера из текстового содержимого.

            Args:
                content (bytes): Содержимое файла в байтах.
                content_type (str): MIME-тип загруженного файла.

            Returns:
                List[str]: Список уникальных телефонных номеров в формате +7(XXX)XXX-XX-XX.

            Raises:
                HTTPException: Если файл пустой, не текстовый или не в UTF-8.
        """
        if not content_type.startswith("text/"):
            logger.warning(f"Неподдерживаемый тип файла: {content_type}")
            raise HTTPException(status_code=400, detail="Формат файла должен быть текстовым.")

        if not content.strip():
            logger.warning("Загружен пустой файл.")
            raise HTTPException(status_code=400, detail="Файл пустой.")

        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            logger.exception("Не удалось декодировать файл.")
            raise HTTPException(status_code=400, detail="Файл не в формате UTF-8.")

        found_numbers = []
        seen = set()
        matches = self.PHONE_REGEX.finditer(text)
        for match in matches:
            formatted = f"+7({match[1]}){match[2]}-{match[3]}-{match[4]}"
            if formatted not in seen:
                seen.add(formatted)
                found_numbers.append(formatted)

        logger.info(f"Найдено номеров: {len(found_numbers)}")
        return found_numbers