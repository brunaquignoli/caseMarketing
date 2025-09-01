Instruções para a execução do projeto:

Por conta das importações feitas no back-end, é necessário fazer a instalação de algumas dependências e criar um ambiente virtual dentro do prompt de comando:

python -m venv venv
venv\Scripts\activate
pip install flask pandas

Depois disso o projeto poderá ser executado no próprio prompt de comando ou em algum software como o Visual Studio Code:

python main.py

Após o Flask iniciar, o site poderá ser acessado pelo navegador através do endereço:

http://127.0.0.1:5000

Na tela de login, o acesso pode ser feito como Admin ou como User.

Ao entrar no sistema, o usuário pode visualizar as tabelas com 10, 25, 50 ou até 100 dados por página e poderá filtrar as informações por menores e maiores valores e até pesquisar informações que queira.

## telas
> tela de login
<img width="1875" height="921" alt="image" src="https://github.com/user-attachments/assets/ae516cd5-2ccb-424e-a7b1-2b41e03f78ef" />

> tela principal
<img width="1857" height="916" alt="image" src="https://github.com/user-attachments/assets/df97675f-51fc-49eb-a664-f5f3f7226566" />

> tela principal com filtros por nome e pesquisa por empresa
<img width="1852" height="918" alt="image" src="https://github.com/user-attachments/assets/972f2d18-1b6d-49a6-a537-8d061d1548ec" />
