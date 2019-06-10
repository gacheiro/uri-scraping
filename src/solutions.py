'''Script para extrair soluções de um perfil.'''

import asyncio
import aiohttp
from bs4 import BeautifulSoup


BASE_URL = 'https://www.urionlinejudge.com.br'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
        
    
def solutions(soup):
    '''Gera as soluções encontradas na página do perfil do usuário.'''
        
    # os dados das soluções ficam entre tags <tr>
    for tr in soup.tbody.find_all('tr'):
        
        lines = tr.get_text().split('\n')
        
        # esse 'if l' no final remove as strings vazias '' que ficam
        sol = tuple(l.strip() for l in lines if l)
       
        # pra não gerar linhas vazias se o usuário
        # não tiver a tabela de soluções completa
        if sol:
            yield sol
                

async def latest_solutions(session, id):
    '''Retorna até 30 soluções mais recentes do usuário.'''
    
    url = f'{BASE_URL}/judge/pt/profile/{id}?sort=Ranks.created&direction=desc'
    
    profile = await fetch(session, url)
    soup = BeautifulSoup(profile, 'html.parser')    
    return solutions(soup)       


async def main():
    
    # Aqui não precisa da aiohttp, já que é só um usuário
    # mas a ideia é ter uma lista de vários perfis
    # e requisitar todos de uma vez só
    async with aiohttp.ClientSession() as session:        
        
        sols = await latest_solutions(session, id=1)
        print("1's solutions:")
        print('\n'.join(str(s) for s in sols))
        

if __name__ == '__main__':
    asyncio.run(main())
