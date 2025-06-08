# API de Pedidos - Documentação

## Endpoints Disponíveis

### Base URL
```
http://localhost:8000/pedidos/api/
```

### Autenticação
Todos os endpoints requerem autenticação via JWT Token.
```
Authorization: Bearer <seu_token_jwt>
```

## Endpoints de Pedidos

### 1. Listar Pedidos do Usuário
```
GET /pedidos/
```

**Resposta:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "usuario": 1,
      "usuario_nome": "João Silva",
      "status": "pendente",
      "status_display": "Pendente",
      "total": "299.99",
      "quantidade_total_items": 3,
      "forma_pagamento": "cartao_credito",
      "forma_pagamento_display": "Cartão de Crédito",
      "criado_em": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 2. Criar Novo Pedido
```
POST /pedidos/
```

**Payload:**
```json
{
  "endereco_entrega": "Rua das Flores, 123, Centro, São Paulo - SP",
  "forma_pagamento": "cartao_credito",
  "observacoes": "Entregar no período da manhã",
  "items": [
    {
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": "99.99"
    },
    {
      "produto_id": 3,
      "quantidade": 1,
      "preco_unitario": "199.99"
    }
  ]
}
```

**Resposta (201 Created):**
```json
{
  "id": 1,
  "usuario": 1,
  "usuario_nome": "João Silva",
  "status": "pendente",
  "status_display": "Pendente",
  "total": "399.97",
  "endereco_entrega": "Rua das Flores, 123, Centro, São Paulo - SP",
  "forma_pagamento": "cartao_credito",
  "forma_pagamento_display": "Cartão de Crédito",
  "observacoes": "Entregar no período da manhã",
  "itens": [
    {
      "id": 1,
      "produto": 1,
      "produto_nome": "Smartphone Galaxy S23",
      "produto_detalhes": {
        "id": 1,
        "nome": "Smartphone Galaxy S23",
        "slug": "smartphone-galaxy-s23",
        "preco": "99.99",
        "preco_promocional": null,
        "imagem": "/media/produtos/smartphone.jpg",
        "categoria": 1,
        "categoria_nome": "Eletrônicos",
        "ativo": true,
        "destaque": true,
        "estoque": 13
      },
      "quantidade": 2,
      "preco_unitario": "99.99",
      "subtotal": "199.98"
    }
  ],
  "quantidade_total_items": 3,
  "criado_em": "2024-01-15T10:30:00Z",
  "modificado_em": "2024-01-15T10:30:00Z"
}
```

### 3. Detalhes de um Pedido
```
GET /pedidos/{id}/
```

### 4. Atualizar Pedido
```
PATCH /pedidos/{id}/
```

**Payload (campos opcionais):**
```json
{
  "status": "confirmado",
  "endereco_entrega": "Novo endereço",
  "forma_pagamento": "pix",
  "observacoes": "Novas observações"
}
```

### 5. Cancelar Pedido
```
PATCH /pedidos/{id}/cancelar/
```

**Resposta:** Retorna o pedido com status "cancelado" e restaura o estoque dos produtos.

### 6. Meus Pedidos (mesmo que listar)
```
GET /pedidos/meus_pedidos/
```

### 7. Estatísticas do Usuário
```
GET /pedidos/estatisticas/
```

**Resposta:**
```json
{
  "total_pedidos": 5,
  "total_gasto": "1299.95",
  "pedidos_por_status": {
    "pendente": 2,
    "confirmado": 1,
    "enviado": 1,
    "entregue": 1,
    "cancelado": 0
  }
}
```

## Filtros e Ordenação

### Filtros Disponíveis
- `status`: Filtra por status do pedido
- `forma_pagamento`: Filtra por forma de pagamento
- `search`: Busca por ID ou endereço de entrega

### Ordenação
- `ordering`: Ordena por campos como `criado_em`, `total`, `status`

**Exemplos:**
```
GET /pedidos/?status=pendente
GET /pedidos/?forma_pagamento=cartao_credito
GET /pedidos/?search=123
GET /pedidos/?ordering=-criado_em
```

## Status de Pedidos

- `pendente`: Pedido criado, aguardando confirmação
- `confirmado`: Pedido confirmado, sendo preparado
- `enviado`: Pedido enviado para entrega
- `entregue`: Pedido entregue ao cliente
- `cancelado`: Pedido cancelado

## Formas de Pagamento

- `dinheiro`: Dinheiro
- `cartao_credito`: Cartão de Crédito
- `cartao_debito`: Cartão de Débito
- `pix`: PIX

## Códigos de Erro

- `400 Bad Request`: Dados inválidos ou estoque insuficiente
- `401 Unauthorized`: Token de autenticação inválido
- `403 Forbidden`: Sem permissão para acessar o recurso
- `404 Not Found`: Pedido não encontrado

## Exemplo de Uso no Frontend

```javascript
// Criar pedido
const criarPedido = async (dadosPedido) => {
  const response = await fetch('http://localhost:8000/pedidos/api/pedidos/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(dadosPedido)
  });
  
  return response.json();
};

// Listar pedidos
const listarPedidos = async () => {
  const response = await fetch('http://localhost:8000/pedidos/api/pedidos/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.json();
};
``` 