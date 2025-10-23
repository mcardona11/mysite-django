from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User

class PollsSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configuració del navegador en mode headless
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # Crear superusuari per al test
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_view_site_and_create_question(self):
        # Entrar a l'admin
        self.selenium.get(f'{self.live_server_url}/admin/')
        self.selenium.find_element(By.NAME, "username").send_keys("isard")
        self.selenium.find_element(By.NAME, "password").send_keys("pirineus")
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()

        # Clicar al botó "View site"
	self.selenium.find_element(By.XPATH, "//a[text()='View site']").click()

        # Tornar a admin per crear una Question
        self.selenium.get(f'{self.live_server_url}/admin/polls/question/add/')
        self.selenium.find_element(By.NAME, "question_text").send_keys("Quina és la teva fruita preferida?")
        self.selenium.find_element(By.NAME, "pub_date").send_keys("2025-10-20 17:00:00")
        self.selenium.find_element(By.NAME, "_save").click()

        # Afegir una Choice a la Question creada
        self.selenium.get(f'{self.live_server_url}/admin/polls/choice/add/')
        question_field = self.selenium.find_element(By.NAME, "question")
        question_field.send_keys("Quina és la teva fruita preferida?")
        self.selenium.find_element(By.NAME, "choice_text").send_keys("Poma")
        self.selenium.find_element(By.NAME, "votes").send_keys("0")
        self.selenium.find_element(By.NAME, "_save").click()
