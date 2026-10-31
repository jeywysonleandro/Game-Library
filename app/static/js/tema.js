
// ELEMENTOS DA PÁGINA

const botaoTema = document.getElementById("interruptor-tema");
const descricaoTema = document.getElementById("descricao-tema");
const corpoPagina = document.body;


// FUNÇÃO PARA APLICAR O TEMA

function aplicarTema(tema) {

    // Define o tema no corpo da página
    corpoPagina.dataset.tema = tema;

    // Verifica se o tema claro está ativo
    const temaClaroAtivo = tema === "claro";

    // Atualiza a aparência do interruptor
    if (botaoTema) {
        botaoTema.classList.toggle("ativo", temaClaroAtivo);

        // Atualiza o estado acessível do botão
        botaoTema.setAttribute("aria-pressed", String(temaClaroAtivo));
    }

    // Atualiza a descrição do tema
    if (descricaoTema) {
        descricaoTema.textContent = temaClaroAtivo
            ? "Tema claro ativado."
            : "Tema escuro ativado.";
    }
}


// RECUPERAR O TEMA SALVO

const temaSalvo = localStorage.getItem("tema");

// Verifica se existe um tema válido salvo
const temaInicial =
    temaSalvo === "claro" || temaSalvo === "escuro"
        ? temaSalvo
        : "escuro";

// Aplica o tema ao carregar a página
aplicarTema(temaInicial);


// ALTERNAR E SALVAR O TEMA

if (botaoTema) {

    botaoTema.addEventListener("click", function () {

        // Identifica o tema atual
        const temaAtual = corpoPagina.dataset.tema;

        // Define o próximo tema
        const novoTema = temaAtual === "escuro" ? "claro" : "escuro";

        // Aplica o novo tema
        aplicarTema(novoTema);

        // Salva a preferência no navegador
        localStorage.setItem("tema", novoTema);

    });

}
