document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.querySelector("#nome").value;
  const profissao = document.querySelector("#profissao").value;
  const bio = document.querySelector("#bio").value;
  const cor = document.querySelector("#cor").value;

  const dados = { nome, profissao, bio, cor };

  // Envia para o backend
  try {
    const res = await fetch("http://127.0.0.1:5000/enviar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dados)
    });

    const resposta = await res.json();
    alert(resposta.message || resposta.error);
  } catch (error) {
    console.error("Erro ao enviar para o servidor:", error);
    alert("Erro ao enviar para o servidor.");
  }

  // Exibe o currículo visualmente para o cliente
  const siteGerado = document.querySelector("#site-gerado");
  siteGerado.innerHTML = `
    <div class="curriculo-container">
      <h2>Currículo de ${nome}</h2>
      <div class="info">
        <p><strong>Nome:</strong> ${nome}</p>
        <p><strong>Profissão:</strong> ${profissao}</p>
        <p><strong>Bio:</strong> ${bio}</p>
      </div>
      <div class="color-box" style="background-color: ${cor};"></div>
      <p><strong>Cor escolhida:</strong> ${cor}</p>
    </div>
  `;
});
