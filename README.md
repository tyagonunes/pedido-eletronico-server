# Pedido Eletrônico Server

Pedido Eletrônico Server é uma API backend desenvolvida em Django, responsável por gerenciar autenticação e contas para o ecossistema Pedido Eletrônico.

## Tecnologias Utilizadas
- Python 3.11+
- Django
- Django REST Framework

## Estrutura do Projeto
```
pedido_eletronico_server/
├── apps/
│   ├── core/      # Funcionalidades compartilhadas
│   └── contas/       # Módulo de usuários
├── config/           # Configurações do Django
├── manage.py         # Script de gerenciamento
├── requirements.txt  # Dependências do projeto
```

## Instalação
1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd pedido_eletronico_server
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Realize as migrações:
   ```bash
   python manage.py migrate
   ```
5. Crie um superusuário (opcional):
   ```bash
   python manage.py createsuperuser
   ```
6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Uso
Acesse `http://localhost:8000/` para utilizar a API. As rotas principais estão documentadas via Django REST Framework.

## Contribuição
Pull requests são bem-vindos! Para contribuir:
1. Crie um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b minha-feature`)
3. Commit suas alterações (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin minha-feature`)
5. Abra um Pull Request

## Licença
Este projeto está sob a licença MIT.
