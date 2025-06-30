document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.querySelector("#nome").value;
  const profissao = document.querySelector("#profissao").value;
  const bio = document.querySelector("#bio").value;
  const cor = document.querySelector("#cor").value;

  // Adicionando os outros campos
  const competencias = document.querySelector("#competencias").value;
  const experiencia = document.querySelector("#experiencia").value;
  const contactos = document.querySelector("#contactos").value;
  const redes = document.querySelector("#redes").value;

  // Criando FormData para enviar todos os dados, incluindo o arquivo de foto
  const formData = new FormData();
  formData.append("nome", nome);
  formData.append("profissao", profissao);
  formData.append("bio", bio);
  formData.append("cor", cor);
  formData.append("competencias", competencias);
  formData.append("experiencia", experiencia);
  formData.append("contactos", contactos);
  formData.append("redes", redes);
  formData.append("foto", document.querySelector("#foto").files[0]);

  try {
    const res = await fetch("http://127.0.0.1:5000/enviar", {
      method: "POST",
      body: formData
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
