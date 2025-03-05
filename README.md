# Aplicação web frontend

Esta aplicação web é um painel de controle responsivo e interativo, ideal para gerenciar funcionalidades de um sistema. É um **painel de controle (dashboard)** desenvolvido usando o **Flask** (um microframework Python para desenvolvimento web) e **Bootstrap 5** para o design responsivo. A aplicação é composta por três painéis principais:

---

### **1. Painel 1: Mini-Sidebar (Barra Lateral Pequena)**
- **Descrição**: Uma barra lateral pequena e fixa, sempre visível, localizada no lado esquerdo da tela.
- **Funcionalidades**:
  - **Botão de Alternar (Toggle Button)**: Um ícone de hambúrguer (`bi-list`) que abre/fecha a barra lateral principal.
  - **Botão 1**: Um ícone de casa (`bi-house`) que, ao ser clicado, exibe links relacionados no painel principal.
  - **Botão 2**: Um ícone de engrenagem (`bi-gear`) que, ao ser clicado, exibe outros links ou funcionalidades no painel principal.
- **Design**: A barra lateral pequena tem um fundo escuro (`bg-dark`) e texto branco (`text-white`), com ícones que facilitam a navegação.

---

### **2. Painel 2: Main Sidebar (Barra Lateral Principal)**
- **Descrição**: Uma barra lateral maior que pode ser expandida ou recolhida. Ela é oculta por padrão e aparece quando o botão de alternar na mini-sidebar é clicado.
- **Funcionalidades**:
  - **Links**: Exibe uma lista de links (por exemplo, "Link 1.1" e "Link 1.2") que podem ser relacionados ao **Botão 1** ou **Botão 2**.
  - **Responsividade**: Em telas pequenas, a barra lateral principal desliza sobre o conteúdo principal. Em telas maiores, ela aparece ao lado da mini-sidebar.
- **Design**: A barra lateral principal também tem um fundo escuro e texto branco, com links organizados verticalmente.

---

### **3. Painel 3: Main Content (Conteúdo Principal)**
- **Descrição**: A área principal do painel, onde o conteúdo dinâmico é exibido.
- **Funcionalidades**:
  - **Conteúdo Inicial**: Exibe uma mensagem de boas-vindas e uma breve descrição.
  - **Responsividade**: O conteúdo principal se ajusta automaticamente ao tamanho da tela, deslocando-se para a direita quando a barra lateral principal é expandida.
- **Design**: O conteúdo principal tem um layout limpo, com padding (`p-4`) para espaçamento interno.

---

### **Funcionamento da Aplicação**
1. **Estado Inicial**:
   - A mini-sidebar está sempre visível.
   - A barra lateral principal está oculta.
   - O conteúdo principal é exibido ao lado da mini-sidebar.

2. **Interações**:
   - **Botão de Alternar**: Quando clicado, a barra lateral principal desliza da esquerda para a direita, sobrepondo-se ao conteúdo principal em telas pequenas ou empurrando o conteúdo principal para a direita em telas maiores.
   - **Botão 1 e Botão 2**: Esses botões controlam quais links são exibidos na barra lateral principal. Por exemplo, o **Botão 1** pode exibir links relacionados à "Home", enquanto o **Botão 2** pode exibir links relacionados a "Configurações".

3. **Responsividade**:
   - Em dispositivos móveis (telas pequenas), a barra lateral principal desliza sobre o conteúdo principal.
   - Em desktops (telas maiores), a barra lateral principal aparece ao lado da mini-sidebar, e o conteúdo principal se ajusta ao espaço disponível.

---

### **Tecnologias Utilizadas**
- **Flask**: Para o backend da aplicação, permitindo a renderização de templates HTML e o uso de `url_for` para vincular arquivos estáticos (CSS e JavaScript).
- **Bootstrap 5**: Para o design responsivo e componentes pré-construídos, como barras laterais e botões.
- **Bootstrap Icons**: Para ícones modernos e escaláveis, como o ícone de hambúrguer, casa e engrenagem.
- **JavaScript**: Para adicionar interatividade, como alternar a visibilidade da barra lateral e atualizar o conteúdo dinâmico.
- **CSS Personalizado**: Para estilos adicionais, como animações e ajustes de layout.

---
