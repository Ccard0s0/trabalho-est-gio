document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.querySelector("#nome").value;
  const bio = document.querySelector("#bio").value;
  const cor = document.querySelector("#cor").value;

  const dados = { nome, bio, cor };

  const res = await fetch("http://127.0.0.1:5000/enviar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(dados)
  });

  const resposta = await res.json();
  alert(resposta.message || resposta.error);
});
