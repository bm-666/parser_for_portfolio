from loguru import logger
from Parser import Parser
import settings


logger.add('parser.log')

if __name__ == '__main__':
    try:
        logger.info('start parser')
        parser = Parser()
        parser.start()
    except Exception as error:
        msg: str = f'{error.__class__}: {error}'
        logger.error(f'Парсер упал: {msg}')
