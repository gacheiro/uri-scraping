'''Script para fazer login no URI Online Judge.'''


import asyncio
import aiohttp
from bs4 import BeautifulSoup


BASE_URL = 'https://www.urionlinejudge.com.br'
LOGIN = BASE_URL + '/judge/pt/login'
DASHBOARD = BASE_URL + '/judge/pt'


form_data = {
    'email': 'usuario@email.com',
    'password': 'senha',
    'remember_me': 0,
    '_csrfToken': '', 
    '_Token[fields]': '40aa819a1f388146da80ca67cdaf803b21ac5e01%3A',
    '_Token[unlocked]': '',
}


def get_csrfToken(soup):
    '''Retorna o token no formulário de login.'''
    return soup.form.find_all('input')[1].get('value')


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

        
async def main():
    async with aiohttp.ClientSession() as session:
        
        login_page = await fetch(session, LOGIN)
        soup = BeautifulSoup(login_page, 'html.parser')
        
        # pega o token na página de login
        csrf = get_csrfToken(soup)
        print('Token do formulário: {}'.format(csrf))
        form_data['_csrfToken'] = csrf
        
        # faz login no uri
        await session.post(LOGIN, data=form_data)
        
        # acessa o Dashboard
        dashboard = await fetch(session, DASHBOARD)
        
        if '/judge/pt/logout' in dashboard:
            print('Login realizado com sucesso.')
        else:
            print('Parece que o login falhou.')
        
    #    with open('dashboard.html', 'w') as f:
    #        f.write(dashboard)
        

if __name__ == '__main__':
    asyncio.run(main())
