from openai import OpenAI 
from src.config.configuration import API_KEY_GPT

class ChatGPT:
    def __init__(self) -> None:
        self.__api_chatgpt = API_KEY_GPT
    def prompt(self, address, neighborhood, city, site_name, recused_reason, opening_reason: str, triagem: bool = False):
            self.client = OpenAI(api_key=self.__api_chatgpt)

            prompt_texto =  f"""
                                Vou te enviar o conteúdo de um chamado. 
                                Você deve considerar o motivo de recusa para análise.
                                AND
                                Você deve considerar o motivo de abertura para análise.
                                Você deve preencher as informações do template abaixo, com o conteúdo referente ao texto que te enviarei. \n\n
                                **Site:** site
                                **Endereço:** endereço, bairro - municipio.
                                **Equipamento com defeito:** descrição_do_equipamento
                                **Situação identificada:** descrição_da_situação
                                **Motivo de recusa:** motivo_da_recusa
                                **Resumo do caso:**
                                Após descrição_da_ação_inicial, foi verificado que descrição_detalhada_do_problema, localizado(a) no endereço endereço_completo, bairro bairro, cidade - estado
                                OBSERVAÇÃO: SE O MOTIVO DA RECUSA VIER COMO "MOTIVO DA RECUSA: -" APENAS IGNORAR E NÃO COLOCAR O MOTIVO DA RECUSA NA DESCRIÇÃO
                """. strip()

            prompt_triagem = f"""
                                Análise do Problema: Avaliar o conteúdo do texto recebido para identificar a natureza do problema com o equipamento ou sistema.
                                Se o texto indicar que o problema pode ser diagnosticado ou resolvido remotamente (contém termos como offline, problemas de conectividade ou comunicação, ajustar configurações, reconfigurar, atualização de software ou firmware, orçamentos ou outros termos semelhantes), devo retornar TRUE.
                                Se o motivo da reprova ou o motivo da abertura indicar que o problema exige a necessidade de troca, ,efetuar troca de alguma coisa, substituição de equipamentos físico, manutenção presencial, retorno ou visita técnica, problemas com fechadura, fechadura com problema de conectividade, problemas com portas, ou qualquer termo semelhante, retornar FALSE
                                Observação: A necessidade de acompanhamento implica ações presenciais, pois geralmente envolve instalação ou supervisão física. Leve em conta que "Site" mencionado tem o significado de "local", logo não é remoto.
                                Sempre considerar primeiro o campo motivo de recusa.
                                Traga apenas o resultado TRUE ou FALSE, nenhum texto adicional pois vou utilizar api.
                            """.strip()

            # prompt_triagem = f"""
            #             Analise o chamado e determine se é possível resolver o problema remotamente. Considere os detalhes fornecidos sobre a natureza da solicitação e avalie se uma solução pode ser implementada sem a necessidade de intervenção física no local. Retorne TRUE se o chamado puder ser resolvido remotamente e FALSE caso contrário. Considere o motivo_da_abertura e o motivo_da_recusa na análise.
            #             Traga apenas o resultado TRUE ou FALSE, nenhum texto adicional pois vou utilizar api.
            #     """.strip()

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
                    Endereço: {address}, {neighborhood}, {city}
                    Motivo da abertura: {opening_reason}
                    Site: {site_name}
                    Motivo da recusa: {recused_reason}
                    """
                }, 
            ])


            message = self.completion.choices[0].message.content

            if triagem:
                # print(message)
                if message.lower() == "false":
                    return False
                else:
                    return True
            return message
    
    # "FALSE" "TRUE"