dic = {'P0000' : {
                    'Descricao'                 : "Acesso aos parametros",
                    'Faixa de valores'          : '0 a 9999',
                    'Ajuste de fabrica'         : 0,
                    'Ajuste do usuario'         : '',
                    'Propriedades'              : '',
                    'Grupos'                    : '',
                    'Pagina'                    : "5 - 2"
                },
       'P0001' : {
                    'Descricao'                 : "Referencia de velocidade",
                    'Faixa de valores'          : '0 a 65535',
                    'Ajuste de fabrica'         : '',
                    'Ajuste do usuario'         : '',
                    'Propriedades'              : "ro",
                    'Grupos'                    : "READ",
                    'Pagina'                    : '17 - 1'
                }
       }

for key, value in dic.items():                  # laço que percorre dicionario dic
    print(key, ':')                             # key é a chave para cada dicionario dentro do dicionario principal
    for chave, valor in value.items():          # laço que percorre dicionario value
        print("  ", chave , '->' ,valor)        


