import sys
from rapidfuzz import fuzz

ocr_engine = None

def scan(path, ocr):
    if ocr == 'Tesseract':
        if "pytesseract" not in sys.modules:
            import pytesseract

        text_detected = pytesseract.image_to_string(path)

    if ocr == 'EasyOCR':
        if "easyocr" not in sys.modules:
            import easyocr

        if "cv2" not in sys.modules:
            import cv2 as cv

        reader = easyocr.Reader(['en'])
        image = cv.imread(path)


        text_detected = reader.readtext(image)

    if ocr == 'PaddleOCR':
        global ocr_engine

        if "paddleocr" not in sys.modules:
            from paddleocr import PaddleOCR

        if ocr_engine is None:
            ocr_engine = PaddleOCR(
                use_textline_orientation=True,  # Detect rotated text
                lang="en",
                enable_mkldnn=False
            )

        result = ocr_engine.predict(path)
        text_detected = result[0]["rec_texts"]

    return text_detected
        