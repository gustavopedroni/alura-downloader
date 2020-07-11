import os

from src.helpers.logging import get_logger

logger = get_logger('Auth')


class AluraAuth:

    def __init__(self, driver, *args, **kwargs):

        self.driver = driver

        self.args = args
        self.kwargs = kwargs

    def login(self):
        logger.info('Authenticating on Alura')

        try:

            self.driver.get('https://cursos.alura.com.br/loginForm')

            user_input = self.driver.find_element_by_xpath('//*[@id="login-email"]')
            password_input = self.driver.find_element_by_xpath('//*[@id="password"]')

            user_input.clear()
            password_input.clear()

            user_input.send_keys(os.getenv('ALURA_USER'))
            password_input.send_keys(os.getenv('ALURA_PASS'))

            self.driver.find_element_by_class_name('btn-login').click()

            logger.info('Successful Authenticate')

        except Exception as e:
            logger.error(e)
            logger.error('Error trying authenticating')
