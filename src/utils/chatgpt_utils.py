from openai import OpenAI 
from src.config.configuration import API_KEY_GPT

class ChatGPT:
    def __init__(self) -> None:
        self.__api_chatgpt = API_KEY_GPT
    def prompt(self, address, neiborhood, municipio, site_name, texto: str, triagem: bool = False):
            self.client = OpenAI(api_key=self.__api_chatgpt)



            prompt_texto =  f"""
                    Vou te enviar o conteúdo de um chamado. 
                    Você deve preencher as informações do template abaixo, com o conteúdo referente ao texto que te enviarei. \n\n
                    **Site:** site
                    **Endereço:** endereço, bairro - municipio.
                    **Equipamento com defeito:** descrição_do_equipamento
                    **Situação identificada:** descrição_da_situação
                    **Resumo do caso:**
                    Após descrição_da_ação_inicial, foi verificado que descrição_detalhada_do_problema, localizado(a) no endereço endereço_completo, bairro bairro, cidade - estado

                """. strip()
            
            prompt_triagem = """
                                Análise do Problema: Avaliar o conteúdo do texto recebido para identificar a natureza do problema com o equipamento ou sistema.
                                Condições de Resposta: Se o texto indicar que o problema pode ser diagnosticado ou resolvido remotamente (contém termos como offline, problemas de conectividade ou comunicação, ajustar configurações, reconfigurar, atualização de software ou firmware, ou outros termos semelhantes), devo retornar TRUE. 
                                Para todos outros casos retornar FALSE
                                Observação: A necessidade de acompanhamento implica ações presenciais, pois geralmente envolve instalação ou supervisão física.
                                Traga apenas o resultado TRUE ou FALSE, nenhum texto adicional pois vou utilizar api
                            """.strip()
            

            self.completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",

            messages=[
                {
                    "role": "system", 
                    "content": prompt_triagem if triagem else prompt_texto
                },
                {
                    "role": "user",
                    "content": f"""
                    Endereço: {address}, {neiborhood}, {municipio}
                    Motivo da abertura: {texto}
                    Site: {site_name}
                    """
                }, 
            ])


            message = self.completion.choices[0].message.content

            if triagem:
                if message.lower() == "false":
                    return False
                else:
                    return True
            return message