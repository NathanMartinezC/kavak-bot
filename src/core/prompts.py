from src.infrastructure.config import settings

def identify_intent_prompt(message: str) -> str:
    text = f"""
    Da un mensaje de bienvenida breve presentándote como asistente virtual de ventas de autos de Kavak 
    (si el mensaje aparenta ser continuación a una charla previa, omite la bienvenida)
    y dado este mensaje: "{message}", extrae los siguientes datos como JSON:
    - intent: 'recommendation', 'financing', 'company_info' (default en caso de no poder identificar)
    Si intent es 'recommendation':
    - preferences: 'make'(marca), 'model' (modelo), 'year' (año), 'price' (precio), 'km' (kilometraje), 'bluetooth' (bluetooth), 'car_play' (car play) (al menos uno de estos, caso contrario pedir más información)
    Si intent es 'financing':
    - preferences: 'initial_payment' (pago inicial o enganche) (más dos campos declarados en recommendation)
    Si intent es 'company_info':
    - preferences: null
    En todos los casos, si se infiere error de escritura en los campos de preferences, corregirlo (e.g. marca (evitar abreviaciones), modelo, etc).
    """
    return text

def company_info_prompt(message: str) -> str:
    text = f"""
    Dado este mensaje: "{message}", reacciona un como asistente virtual de ventas de autos de Kavak,
    si identificas que se solicita información específica, busca y extrae la información solicitada de este sitio web {settings.kavak_url}/blog/sedes-de-kavak-en-mexico
    en cualquier caso regresa un JSON:
    - response: (texto de infomación solicitada, en caso de no encontrar, sugiere este sitio web {settings.kavak_url} para más información)
    """
    return text