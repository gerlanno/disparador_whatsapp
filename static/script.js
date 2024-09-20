document.getElementById('intervaloAleatorio').addEventListener('change', function () {
    const seletorIntervalo = document.getElementById('delayInterval');
    const orientacaoTexto = document.getElementById('orientacaoTexto');

    if (this.checked) {
        // Muda o foco para o seletor de intervalo
        seletorIntervalo.focus();

        // Exibe a mensagem de orientação
        orientacaoTexto.style.display = 'block';
    } else {
        // Esconde a mensagem de orientação se desmarcar
        orientacaoTexto.style.display = 'none';
    }
});





