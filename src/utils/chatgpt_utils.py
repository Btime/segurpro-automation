from openai import OpenAI 
from src.config.configuration import API_KEY_GPT

class ChatGPT:
    def __init__(self) -> None:
        self.__api_chatgpt = API_KEY_GPT
    def prompt(self, texto: str, triagem: bool = False):
            self.client = OpenAI(api_key=self.__api_chatgpt)


            prompt_texto =  """
                                faça a analise com o que mandei de input e traga o texto que criou de resumo. 
                                Separe a análise em tópicos e traga o texto formatado em markdown. 
                                Tire "\n" e quebre a linha por cada tópico.
                            """. strip()
            
            prompt_triagem = """
                                Análise do Problema: Avaliar o conteúdo do texto recebido para identificar a natureza do problema com o equipamento ou sistema.
                                Condições de Resposta: Se o texto indicar que o problema pode ser diagnosticado ou resolvido remotamente (equipamento inoperante, offline, ou problemas de conectividade), devo retornar TRUE. Se o texto sugerir a necessidade de ações físicas como instalação, remanejamento, reposicionamento, ou presença física de um técnico, devo retornar FALSE.
                                Resultado da Análise: Retornar TRUE para situações que requerem triagem e possíveis soluções remotas. Retornar FALSE para situações que necessitam de ação direta de um técnico no local.
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
                    "content": texto
                }
            ])


            message = self.completion.choices[0].message.content

            if triagem:
                if message.lower() == "false":
                    return False
                else:
                    return True
            return message