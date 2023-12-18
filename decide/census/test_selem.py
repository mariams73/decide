from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from base.tests import BaseTestCase
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

class CensusTestCase(StaticLiveServerTestCase):

    def setUp(self):
        #Crea un usuario admin y otro no admin
        self.base = BaseTestCase()
        self.base.setUp()
	
        #Opciones de Chrome
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        User.objects.create_superuser('admin_census', 'admin@example.com', 'qwerty')
        # Inicio de sesión como admin
        self.driver.get(f'{self.live_server_url}/admin/')
        #Busca los elementos y “escribe”
        self.driver.find_element(By.ID,'id_username').send_keys("admin_census")
        self.driver.find_element(By.ID,'id_password').send_keys("qwerty",Keys.ENTER)
        
        #Verifica que nos hemos logado porque aparece la barra de herramientas superior
        self.assertTrue(len(self.driver.find_elements(By.ID, 'user-tools'))==1)

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def test_add_new_voters(self):      
       #Abre la ruta del navegador             
        self.driver.get(f'{self.live_server_url}/census/')
       #Busca los elementos y “escribe”
        self.driver.find_element(By.ID,'id_voting_id').send_keys("2")
        self.driver.find_element(By.ID,'id_voters').send_keys("1,2,3,4",Keys.ENTER)
        
       #Verifica que los votantes se han añadido correctamente
        self.assertTrue(len(self.driver.find_elements(By.ID, 'voters-list'))==4)
        
    def test_export_census_csv(self):
        self.driver.get(f'{self.live_server_url}/census/')
       #Busca los elementos y “escribe”
        self.driver.find_element(By.ID,'id_voting_id').send_keys("1")
        self.driver.find_element(By.ID,'id_voters').send_keys("1,2,3,4",Keys.ENTER)
    
        self.driver.get(f'{self.live_server_url}/census/export/1')
        self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, 'download')) > 0)

