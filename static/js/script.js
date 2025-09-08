// Comando para buscar os dados do backend
document.addEventListener('DOMContentLoadeds'() => (
carregarJogadores();
carregarAgenda();
carregarDiretoria();
));

// Função para buscar jogadores
function carregarJogadores() {
  fetch("/api/jogadores")
    .then(res => res.json())
    .then(data => {
      let div = document.getElementById("listaJogadores");
      div.innerHTML = "";
      data.forEach(jogador => {
        div.innerHTML += `
          <div>
            <img src="img/players/leonelMessi.png ${jogador.foto}" width="100">
            <p>${jogador.nome}, ${jogador.idade} anos</p>
            <p>Nascido em: ${jogador.localNascimento}</p>
            <p>Jogou em: ${jogador.timesAnterior}</p>
          </div>
        `;
      });
    });
}

// Função para buscar agenda
function carregarAgenda() {
  fetch("/api/agenda")
    .then(res => res.json())
    .then(data => {
      let div = document.getElementById("listaAgenda");
      div.innerHTML = "";
      data.forEach(jogo => {
        div.innerHTML += `
          <p>${jogo.data} - ${jogo.horario} - ${jogo.local} vs ${jogo.adversario}</p>
        `;
      });
    });
}


// Função para buscar diretoria
function carregarDiretoria() {
  fetch("/api/diretoria")
    .then(res => res.json())
    .then(data => {
      let div = document.getElementById("listaDiretoria");
      div.innerHTML = "";
      data.forEach(pessoa => {
        div.innerHTML += `<p>${pessoa.cargo}: ${pessoa.nome}</p>`;
      });
    });
}