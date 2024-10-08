import uiautomator2 as u2
import time
from faker import Faker
import random
import logging
import traceback


# Configuração básica do logging
logging.basicConfig(filename='automation_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class StartAuto:
    def __init__(self):
            # Conecte-se ao dispositivo
            self.device = u2.connect()
            self.device.implicitly_wait(2)  # tempo de espera em segundos
            global data_nascimento_str , name ,cell ,email
            fake = Faker()
           #fake = Faker('pt_BR') 
            name = fake.name()
            email = fake.email()
            cell = fake.phone_number()
            data_nascimento = fake.date_of_birth()
            data_nascimento_str = data_nascimento.strftime("%d/%m/%Y")
            logging.info(f'Dados de teste gerados: Nome - {name}, Email - {email}, Celular - {cell}, Nascimento - {data_nascimento_str}')
            
            try:
                self.inicio()
                #self.cadastro()
                #self.segmento()
                self.switch_acount()
                self.navegacao()
                
                
            except Exception as e:
                print(f"Erro na inicialização: {str(e)}")
    
    def wait_and_click(self, resource_type, identifier, timeout=4):
        try:    
            time.sleep(2)
            print(f"Aguardando e clicando no elemento {identifier} ({resource_type})")
            if resource_type == 'resourceId':
                time.sleep(2)
                self.device(resourceId=identifier).wait(timeout=timeout)
                self.device(resourceId=identifier).click()
            elif resource_type == 'text':
                time.sleep(2)
                self.device(text=identifier).wait(timeout=timeout)
                self.device(text=identifier).click()        
        except:
            print(f"Erro ao aguardar e clicar no elemento {identifier} ({resource_type}): {traceback.format_exc()}")
    def set_text_field(self, identifier_type, identifier_value, text):
        try:    
            time.sleep(2)
            if identifier_type == 'resourceId':
                elemento = self.device(resourceId=identifier_value)
            elif identifier_type == 'text':
                elemento = self.device(text=identifier_value)
            else:
                raise ValueError("Tipo de identificador inválido. Use 'resourceId' ou 'text'.")
            time.sleep(2)
            if elemento.exists:
                elemento.set_text(text)
                print(f"Texto '{text}' definido com sucesso no campo '{identifier_value}'.")
            else:
                print(f"Elemento com {identifier_type} '{identifier_value}' não encontrado.")
        except:
            print(f"Erro ao definir texto no campo '{identifier_value}': {traceback.format_exc()}")
    
    def sentimento_random(self):
        try:
            sentimentos_map = [ 
                'Amor',
                'Dor',
                'apego',
                'raiva'   
            ]

            lista = list(sentimentos_map)
            global sentimento
            sentimento = random.choice(lista)
            self.device(resourceId = 'br.com.olya.app:id/etSearch').set_text(sentimento)
            time.sleep(2)
            oleos = self.device(resourceId = 'br.com.olya.app:id/tvName')
            total_oleos = oleos.count
            if total_oleos == 0:
                print('Nenhum oleo encontrado!')
                return
            oleo_selecionado = random.randint(0, total_oleos - 1)
            oleo = oleos[oleo_selecionado]
            try:
                time.sleep(1)
                oleo.click()
                print(f'Oleo clicado com sucesso')
            except Exception as e:
                print(f"Erro ao clicar no Oleo: {str(e)}")
        except Exception as e:
            print(f"Erro no método sentimento_random: {str(e)}")
        
    def compartilhar(self):
        try:
            time.sleep(2)
            self.wait_and_click('text', 'Mensagens')
            print("Clicou em 'Mensagens'")
            self.wait_and_click('text', '21976873139')
            print("Clicou no número de telefone '21976873139'")
            self.wait_and_click('text', 'Avançar')
            print("Clicou em 'Avançar'")
            time.sleep(3)
            
            if self.device(resourceId='android:id/alertTitle').exists(timeout=5):
                self.wait_and_click('resourceId', 'android:id/aerr_close')
                print("Fechou o erro do app de mensagens")
            else:
                print("Nenhum erro encontrado no app de mensagens")
        except Exception as e:
            print(f"Erro no método compartilhar: {str(e)}")
            
               
    def escolher_bandeira_aleatoria(self, tentativas=3, delay_entre_tentativas=2):
        for tentativa in range(tentativas):
            try:
                self.wait_and_click('resourceId', 'br.com.olya.app:id/spinner_icon')  # Abre o spinner
                time.sleep(2)

                # Busca as bandeiras
                bandeiras = self.device(resourceId='br.com.olya.app:id/spinner_text')
                total_bandeiras = bandeiras.count

                logging.info(f'Total de bandeiras encontradas: {total_bandeiras}')

                if total_bandeiras == 0:
                    logging.warning("Nenhuma bandeira disponível para selecionar.")
                    if tentativa < tentativas - 1:
                        logging.info(f"Tentando novamente... ({tentativa + 1}/{tentativas})")
                        time.sleep(delay_entre_tentativas)
                        continue
                    return

                # Seleciona uma bandeira aleatória
                indice_selecionado = random.randint(0, total_bandeiras - 1)
                bandeira = bandeiras[indice_selecionado]

                # Obtém o nome da bandeira
                try:
                    nome_bandeira = bandeira.get_text()
                    logging.info(f'Nome da bandeira selecionada: {nome_bandeira}')
                except Exception as e:
                    logging.error(f"Erro ao obter o nome da bandeira: {str(e)}")
                    if tentativa < tentativas - 1:
                        logging.info(f"Tentando novamente... ({tentativa + 1}/{tentativas})")
                        time.sleep(delay_entre_tentativas)
                        continue
                    return

                # Tenta clicar na bandeira
                try:
                    time.sleep(1)
                    bandeira.click()
                    logging.info(f'Bandeira clicada com sucesso: {nome_bandeira}')
                    break  # Sai do loop se a bandeira for clicada com sucesso
                except Exception as e:
                    logging.error(f"Erro ao clicar na bandeira: {str(e)}")
                    if tentativa < tentativas - 1:
                        logging.info(f"Tentando novamente... ({tentativa + 1}/{tentativas})")
                        time.sleep(delay_entre_tentativas)
                    else:
                        return
            except Exception as e:
                logging.error(f"Erro durante a tentativa de selecionar uma bandeira: {str(e)}")
                if tentativa < tentativas - 1:
                    logging.info(f"Tentando novamente... ({tentativa + 1}/{tentativas})")
                    time.sleep(delay_entre_tentativas)
                else:
                    return

    def inicio(self):
        try:#Iniciar o aplicativo
            self.device.app_start('br.com.olya.app')
            self.wait_and_click('text', 'Vamos começar!')
            time.sleep(1)
            self.wait_and_click('text', 'Próximo')
            self.wait_and_click('text', 'Próximo')
        except Exception as e:
            print(f"Erro no método inicio: {str(e)}")
            
   
    def cadastro(self):
        #Faz fluxo do cadastro completo
        try:
            self.wait_and_click('text', 'Cadastrar')
            self.set_text_field('text', 'Escreva seu nome', name)
            time.sleep(1)
            self.escolher_bandeira_aleatoria()
            time.sleep(1)
            self.set_text_field('text', 'Escreva seu telefone', cell)
            time.sleep(1)
            self.set_text_field('text', 'Escreva seu e-mail', email)
            self.set_text_field('text', 'Escreva sua data de nascimento', data_nascimento_str)

            logging.info(f'Registrado: Nome - {name}, Telefone - {cell}, Email - {email}, Nascimento - {data_nascimento_str}')

            self.device(scrollable=True).scroll(steps=10)
            self.wait_and_click('text', 'Selecione seu gênero')
            self.wait_and_click('text', 'Prefiro não informar')
            peso = round(random.uniform(50, 150))
            peso = min(peso, 150)
            self.set_text_field('text', 'Seu peso', peso)
            altura = "{:.2f}".format(round(random.uniform(1.50, 2.00), 2))
            self.set_text_field('text', 'Sua altura', altura)

            logging.info(f'Peso: {peso}, Altura: {altura}')

            self.set_text_field('text', 'Escreva sua senha', '12345')
            self.set_text_field('text', 'Confirme sua senha', '12345')
            self.wait_and_click('resourceId','br.com.olya.app:id/cbAuthorization')
            time.sleep(5)
            self.device(scrollable=True).scroll(steps=10)
            time.sleep(5)
            self.wait_and_click('resourceId', 'br.com.olya.app:id/tvAuthorization')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/ivArrowBack') 
            self.wait_and_click('text', 'Cadastrar')
            time.sleep(2)
        except Exception as e:
            print(f'erro:{str(e)}')

    def segmento(self):
        try:   
            self.wait_and_click('text', 'Realizar primeira avaliação')
            if self.device(text='Apenas esta vez').exists(timeout=3):
                    self.wait_and_click('text', 'Apenas esta vez')
            else:
                print("Confirmação não apareceu, continuando...")
            self.wait_and_click('text', 'Fale Conosco')
            time.sleep(2)
            self.wait_and_click('text', 'Fechar')
            time.sleep(3)
        except Exception as e:
            print(f'erro:{str(e)}')
        
    
    def navegacao(self):
        try:
                    #Start navegação para Home
            self.wait_and_click('resourceId', 'br.com.olya.app:id/fragmentHome')
                    #segmento para oleos e compartilhar 
            self.wait_and_click('resourceId', 'br.com.olya.app:id/fragmentFollowUp')
            self.sentimento_random()
            self.wait_and_click('resourceId', 'br.com.olya.app:id/viewHeart')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/ivShare')
            self.compartilhar()
                    #Aba educação e diluição
            self.wait_and_click('resourceId', 'br.com.olya.app:id/fragmentWellBeing')
            self.wait_and_click('text', 'Diluição')
            time.sleep(3)
            self.set_text_field('text', 'Ex: 15', '25')
            time.sleep(2)
            self.set_text_field('text', 'Ex: 3', '5')
            self.wait_and_click('text', 'Calcular!')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/fragmentHome')
                    #Relatorio de bem-estar
            self.wait_and_click('resourceId', 'br.com.olya.app:id/clWellbeingReport')
                    #Afiliados
            self.wait_and_click('resourceId', 'br.com.olya.app:id/fragmentQueries')
                    #Perfil
            self.wait_and_click('resourceId', 'br.com.olya.app:id/fragmentProfile')
                    #confidar amigos    
            self.wait_and_click('resourceId', 'br.com.olya.app:id/clInviteFriends')
            self.compartilhar()
                    #edit Perfil
            self.wait_and_click('resourceId', 'br.com.olya.app:id/tvProfile')
            time.sleep(2)
            self.escolher_bandeira_aleatoria()
            time.sleep(2)
            self.device(resourceId = 'br.com.olya.app:id/etCellphone').clear_text()
            self.set_text_field('resourceId', 'br.com.olya.app:id/etCellphone', cell)
            time.sleep(3)
            self.device(scrollable=True).scroll(steps=5)
            time.sleep(2)
            self.device(resourceId = 'br.com.olya.app:id/etWeight').clear_text()
            peso = round(random.uniform(50, 150))
            peso = min(peso, 150)
            self.set_text_field('resourceId', 'br.com.olya.app:id/etWeight', peso)
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btUpdate')
                    #Edit senha
            self.wait_and_click('resourceId', 'br.com.olya.app:id/tvChangePassword')
            self.set_text_field('resourceId', 'br.com.olya.app:id/etPassword', '12345')
            self.set_text_field('resourceId', 'br.com.olya.app:id/etNewPassword', '12345')
            self.set_text_field('resourceId', 'br.com.olya.app:id/etConfirmPassword', '12345')
            self.wait_and_click('resourceId', 'android:id/input_method_nav_back')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btEdit')
                    #extrato            
            self.wait_and_click('resourceId', 'br.com.olya.app:id/tvBalance')
            time.sleep(3)
            self.device.press("back")
                    #mover Afiliados
            self.wait_and_click('resourceId', 'br.com.olya.app:id/tvMoveAffiliates')
            time.sleep(1)
            self.device.press("back")
                    #termos e condições
            self.wait_and_click('resourceId', 'br.com.olya.app:id/tvTerms')
            time.sleep(3)
            self.device(scrollable=True).scroll(steps=2)
            time.sleep(3)
            self.device.press('back')
                    #Logout
            self.wait_and_click('resourceId', 'br.com.olya.app:id/tvLogout')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/idLogout')
            time.sleep(3)
        except Exception as e:
            print(f"Erro no método navegacao: {str(e)}")

    def escolher_categoria_aleatoria(self):
            categorias = self.device(resourceId='br.com.olya.app:id/tvCategory')
            total_categorias = categorias.count

            if total_categorias < 4:
                logging.warning("Não há categorias suficientes para selecionar.")
                return

            indices_selecionados = random.sample(range(total_categorias), 4)
            categorias_escolhidas = []

            for indice in indices_selecionados:
                categoria = categorias[indice]
                categoria_nome = categoria.get_text()
                categorias_escolhidas.append(categoria_nome)
                categoria.click()
                time.sleep(3)

            logging.info(f'Categorias escolhidas: {categorias_escolhidas}')

    def switch_acount(self):
        try:
            self.wait_and_click('text', 'Login')
            time.sleep(3)
                    #Fluxo para entrar na conta                
            self.set_text_field('resourceId', 'br.com.olya.app:id/etEmailLogin', 'matheusQa')
            self.set_text_field('resourceId', 'br.com.olya.app:id/etPasswordLogin', '1234567')
            self.wait_and_click('resourceId', 'android:id/input_method_nav_back')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btLogin')
                    #começar bio Scanner
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btInviteUser')
            if self.device(text='Apenas esta vez').exists(timeout=5 ):
                self.device(text='Apenas esta vez').click()
            else:
                print("Confirmação não apareceu, continuando...")
            self.device(resourceId='br.com.olya.app:id/etName').wait(timeout=45)
            
            self.device(resourceId='br.com.olya.app:id/etName').set_text(name)
                    #dados do usuário para leitura
            peso = round(random.uniform(50, 150))
            peso = min(peso, 150)
            self.set_text_field('resourceId', 'br.com.olya.app:id/etWeight', peso)
            altura = "{:.2f}".format(round(random.uniform(1.50, 2.00), 2))
            self.set_text_field('resourceId', 'br.com.olya.app:id/etHeight', altura)
            logging.info(f'Login: Nome - {name}, Peso - {peso}, Altura - {altura}')
            self.wait_and_click('resourceId', 'android:id/input_method_nav_back')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btSend')
                    #preencher sentimentos
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btQuestions')
            time.sleep(3)
            self.escolher_categoria_aleatoria()
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btSend')
            time.sleep(2)
            self.escolher_categoria_aleatoria()
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btSend')
            time.sleep(2)
            self.escolher_categoria_aleatoria()
            self.wait_and_click('resourceId', 'br.com.olya.app:id/btSend')
            time.sleep(4)
                    #relatorio / compartilhar relatório
            self.device(scrollable=True).scroll(steps=2)
            time.sleep(2)
            self.wait_and_click('resourceId', '')
            self.wait_and_click('resourceId', 'br.com.olya.app:id/clShare')
            self.compartilhar()
            self.device.press('home')
            time.sleep(2)
            self.device.app_start('br.com.olya.app')
            time.sleep(2)
            self.navegacao()
            time.sleep(2)
            #self.wait_and_click('resourceId', 'br.com.olya.app:id/fragmentProfile')
            #self.wait_and_click('resourceId', 'br.com.olya.app:id/tvLogout')
            #self.wait_and_click('resourceId', 'br.com.olya.app:id/idLogout')
        except Exception as e:
            print(f"Erro no método switch_acount: {str(e)}")
        
if __name__ == "__main__":
    auto = StartAuto()
    auto.__init__()
