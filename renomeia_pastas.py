import os
import re
from unicodedata import normalize

# Remove caracteres especiais
def normaliza(txt):
    """
    Devolve cópia de uma str substituindo os caracteres
    acentuados pelos seus equivalentes não acentuados.

    Remove também espaços anteriores, posteriores e duplicados.

    ATENÇÃO: caracteres gráficos não ASCII e não alfa-numéricos,
    tais como bullets, travessões, aspas assimétricas, etc.
    são simplesmente removidos!

        >>> normaliza('[ACENTUAÇÃO] ç: áàãâä! éèêë? íìîï, óòõôö; úùûü.')
        '[ACENTUACAO] c: aaaaa! eeee? iiii, ooooo; uuuu.'
    """
    if not txt:
        return ''
    result = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    result.strip()
    result = re.sub(r'\s{2,}', ' ', result)
    return result

def edita_nome(nome_pasta):
    '''Normaliza o nome da pasta, substituindo os espaços por '_'.'''
    dst = normaliza(nome_pasta).upper()
    dst = re.sub(r'\s', '_', dst)
    return dst

# Extrai os nomes das pastas em sequência de subpastas
print('Obtendo dados...')
folders = []
for root, subdirs, files in os.walk(os.getcwd()):
    for d in subdirs:
        folders.append(os.path.join(root, d))

# Renomeia as subpastas, na ordem das mais internas para as mais externas
print('Renomeando pastas...\n')
for folder in folders[::-1]:
    base_name = os.path.basename(folder)
    par_dir = os.path.dirname(folder)
    dst = edita_nome(base_name)
    os.rename(folder, os.path.join(par_dir, dst))
    print(f'{folder} ===> {os.path.join(par_dir, dst)}')

input('\nConcluído! Pressione qualquer tecla para sair...')
