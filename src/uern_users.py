'''
    Um script para pegar o id e o nome dos estudantes da UERN no URI Online Judge.
'''


import asyncio
import aiohttp
from bs4 import BeautifulSoup


BASE_URL = 'https://www.urionlinejudge.com.br'
UERN = BASE_URL + '/judge/pt/users/university/uern'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
        
        
def users(soup):
    '''Gera tuplas (id, nome) dos usuários na página da universidade.'''
    
    # itera entre as diversas tags <tbody>
    for tbody in soup.find_all('tbody'):
        
        # os dados do usuário ficam entre tags <tr>
        for user in tbody.find_all('tr'):
        
            # pega a tag <a>
            # extrai o link e o texto
            # <a href="/judge/pt/profile/[id]"> Nome do Estudante </a>
            atag = user.find('a')
            
            try:
                # pega só o id no final  href="/judge/pt/profile/[id]"
                id = atag.get('href').split('/')[-1]
                name = atag.string
                yield id, name
                
            except AttributeError:
                # lista de usuários acabou
                return
            

async def main():
    async with aiohttp.ClientSession() as session:
    
        pages = asyncio.gather(
            fetch(session, UERN),
            fetch(session, UERN + '?page=2'),
            fetch(session, UERN + '?page=3'),
            fetch(session, UERN + '?page=4'))
        
        # junta todas as páginas em uma sopa só
        all_pages = ''.join(await pages)        
        soup = BeautifulSoup(all_pages, 'html.parser')
        
        # imprime os estudantes em ordem alfabética
        for id, name in sorted(users(soup), key=lambda u: u[1]):
            print('[{}] {}'.format(id, name))
        
           
if __name__ == '__main__':
    asyncio.run(main())
