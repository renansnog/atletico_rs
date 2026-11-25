const caminhoFotos = "/static/img/players/";
const formJogador = document.querySelector("#formJogador");
const formPartida = document.querySelector("#formPartida");
const botaoCancelar = document.querySelector("#cancelarEdicao");
const botaoSalvar = formJogador.querySelector('[type="submit"]');
const statusJogadores = document.querySelector("#statusJogadores");
const statusAgenda = document.querySelector("#statusAgenda");
const listaJogadores = document.querySelector("#listaJogadores");
let jogadorEmEdicao = null;

async function api(caminho, metodo = "GET", dados) {
  const resposta = await fetch("/api/" + caminho, {
    method: metodo,
    ...(dados && {
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    }),
  });
  if (!resposta.ok) {
    const resultado = await resposta.json().catch(() => ({}));
    throw new Error(resultado.erro || "Não foi possível concluir a operação.");
  }
  if (resposta.status !== 204) return resposta.json();
}

function elemento(tag, texto) {
  const item = document.createElement(tag);
  if (texto !== undefined) item.textContent = texto;
  return item;
}

async function carregar(caminho, lista, renderizar, vazio) {
  try {
    const dados = await api(caminho);
    lista.replaceChildren(...(dados.length ? dados.map(renderizar) : [elemento("p", vazio)]));
  } catch (erro) {
    lista.replaceChildren(elemento("p", erro.message));
  }
}

function cancelarEdicao() {
  jogadorEmEdicao = null;
  formJogador.reset();
  botaoSalvar.textContent = "Cadastrar jogador";
  botaoCancelar.hidden = true;
}

function editar(jogador) {
  jogadorEmEdicao = jogador.id;
  for (const campo of ["nome", "idade", "localNascimento", "timesAnterior", "foto"]) {
    formJogador.elements[campo].value = jogador[campo] ?? "";
  }
  botaoSalvar.textContent = "Salvar edição";
  botaoCancelar.hidden = false;
  statusJogadores.textContent = "Editando " + jogador.nome;
  formJogador.elements.nome.focus();
}

async function excluir(jogador, botao) {
  if (!window.confirm("Excluir " + jogador.nome + "?")) return;
  botao.disabled = true;
  try {
    await api("jogadores/" + jogador.id, "DELETE");
    if (jogadorEmEdicao === jogador.id) cancelarEdicao();
    statusJogadores.textContent = "Jogador excluído.";
    await carregarJogadores();
  } catch (erro) {
    statusJogadores.textContent = erro.message;
  } finally {
    botao.disabled = false;
  }
}

function cartaoJogador(jogador) {
  const cartao = elemento("article");
  if (jogador.foto) {
    const foto = elemento("img");
    foto.src = caminhoFotos + encodeURIComponent(jogador.foto);
    foto.alt = "";
    foto.width = 100;
    cartao.append(foto);
  }
  cartao.append(elemento("h3", jogador.nome || "Jogador"));
  if (jogador.idade !== null) cartao.append(elemento("p", jogador.idade + " anos"));
  if (jogador.localNascimento) {
    cartao.append(elemento("p", "Nascimento: " + jogador.localNascimento));
  }
  if (jogador.timesAnterior) {
    cartao.append(elemento("p", "Times anteriores: " + jogador.timesAnterior));
  }
  const acoes = elemento("div");
  acoes.className = "acoes";
  const botaoEditar = elemento("button", "Editar");
  const botaoExcluir = elemento("button", "Excluir");
  botaoEditar.addEventListener("click", () => editar(jogador));
  botaoExcluir.addEventListener("click", () => excluir(jogador, botaoExcluir));
  acoes.append(botaoEditar, botaoExcluir);
  cartao.append(acoes);
  return cartao;
}

function carregarJogadores() {
  return carregar("jogadores", listaJogadores, cartaoJogador, "Nenhum jogador cadastrado.");
}

function carregarAgenda() {
  return carregar("agenda", document.querySelector("#listaAgenda"), (jogo) => {
    const data = jogo.data?.split("-").reverse().join("/") || "Data a definir";
    const horario = jogo.horario?.slice(0, 5) || "Horário a definir";
    return elemento("p", data + " às " + horario + " · " + jogo.adversario + " · " + jogo.local);
  }, "Nenhuma partida cadastrada.");
}

formJogador.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formJogador));
  dados.idade = Number(dados.idade);
  const id = jogadorEmEdicao;
  botaoSalvar.disabled = true;
  botaoCancelar.disabled = true;
  listaJogadores.inert = true;
  try {
    await api(id ? "jogadores/" + id : "jogadores", id ? "PUT" : "POST", dados);
    cancelarEdicao();
    statusJogadores.textContent = id ? "Jogador atualizado." : "Jogador cadastrado.";
    await carregarJogadores();
  } catch (erro) {
    statusJogadores.textContent = erro.message;
  } finally {
    botaoSalvar.disabled = false;
    botaoCancelar.disabled = false;
    listaJogadores.inert = false;
  }
});

botaoCancelar.addEventListener("click", () => {
  cancelarEdicao();
  statusJogadores.textContent = "";
});

formPartida.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const botao = formPartida.querySelector("button");
  botao.disabled = true;
  try {
    await api("agenda", "POST", Object.fromEntries(new FormData(formPartida)));
    formPartida.reset();
    statusAgenda.textContent = "Partida cadastrada.";
    await carregarAgenda();
  } catch (erro) {
    statusAgenda.textContent = erro.message;
  } finally {
    botao.disabled = false;
  }
});

carregarJogadores();
carregarAgenda();
carregar("diretoria", document.querySelector("#listaDiretoria"),
  (pessoa) => elemento("p", pessoa.cargo + ": " + pessoa.nome),
  "Nenhum integrante cadastrado.");
