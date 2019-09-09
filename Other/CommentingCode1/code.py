# Читал эту статью, когда делал бота для оповещений о повышенной частосте дедлоков на сервере
# Изобретать велосипед и писать отсебятину нет смысла, зато есть пара мыслей по комментам, оставленым в статье

import xml.etree.ElementTree as XmlElementTree
import httplib2
import uuid
from config import ***
 
***_HOST = '***'
***_PATH = '/***_xml'
CHUNK_SIZE = 1024 ** 2
 
def speech_to_text(filename=None, bytes=None, request_id=uuid.uuid4().hex, topic='notes', lang='ru-RU',
                   key=***_API_KEY):
    # old: Если передан файл
    if filename:
        with open(filename, 'br') as file:
            bytes = file.read()
    if not bytes:
        raise Exception('Neither file name nor bytes provided.')
 
    # old: Конвертирование в нужный формат
    # new: Конвертирование в аудио формат PCM 16000 Гц 16 бит
    # примечание: хоть и из названия метода можно догадаться какой это формат, но лучше бы указать
    bytes = convert_to_pcm16b16000r(in_bytes=bytes)
 
    # old: Формирование тела запроса к Yandex API
    url = ***_PATH + '?uuid=%s&key=%s&topic=%s&lang=%s' % (
        request_id,
        key,
        topic,
        lang
    )
 
    # old: Считывание блока байтов
    # примечание: необязательный комментарий, по методу вполне очевидно
    chunks = read_chunks(CHUNK_SIZE, bytes)
 
    # old: Установление соединения
    connection = httplib2.HTTPConnectionWithTimeout(***_HOST)
 
    # old: Формирование запроса 
    connection.connect()
    connection.putrequest('POST', url)
    connection.putheader('Transfer-Encoding', 'chunked')
    connection.putheader('Content-Type', 'audio/x-pcm;bit=16;rate=16000')
    connection.endheaders()
 
    # old: Отправка байтов блоками
    for chunk in chunks:
        connection.send(('%s\r\n' % hex(len(chunk))[2:]).encode())
        connection.send(chunk)
        connection.send('\r\n'.encode())

    # примечание: два прошлых коммента больше нужны не для понимания смысла а для разграничения блоков кода
    # Здесь можно было бы добавить "Закрытие запроса", хоть это и очевидно, но была бы полная карта действий
    # new: Закрытие запроса
    connection.send('0\r\n\r\n'.encode())
    response = connection.getresponse()
 
    # old: Обработка ответа сервера
    if response.code == 200:
        response_text = response.read()
        xml = XmlElementTree.fromstring(response_text)
 
        if int(xml.attrib['success']) == 1:
            max_confidence = - float("inf")
            text = ''
 
            for child in xml:
                if float(child.attrib['confidence']) > max_confidence:
                    text = child.text
                    max_confidence = float(child.attrib['confidence'])
 
            if max_confidence != - float("inf"):
                return text
            else:
                # old: Создавать собственные исключения для обработки бизнес-логики - правило хорошего тона
                # примечание: многие разработчики находят комментарии с высказыванием мнения по коду лишними
                raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
        else:
            raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
    else:
        raise SpeechException('Unknown error.\nCode: %s\n\n%s' % (response.code, response.read()))

# old: Создание своего исключения
# примечание: функционально бесполезный комментарий, но подходит как указатель, чтобы не потерять эту важную часть кода
сlass SpeechException(Exception):
    pass

