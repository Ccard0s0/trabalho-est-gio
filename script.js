document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.querySelector("#nome").value;
  const profissao = document.querySelector("#profissao").value;
  const bio = document.querySelector("#bio").value;
  const cor = document.querySelector("#cor").value;
  const competencias = document.querySelector("#competencias").value;
  const experiencia = document.querySelector("#experiencia").value;
  const formacao = document.querySelector("#formacao").value;
  const projectos = document.querySelector("#projectos").value;
  const contactos = document.querySelector("#contactos").value;
  const idiomas = document.querySelector("#idiomas").value;
  const redes = document.querySelector("#redes").value;

  const formData = new FormData();
  formData.append("nome", nome);
  formData.append("profissao", profissao);
  formData.append("bio", bio);
  formData.append("cor", cor);
  formData.append("competencias", competencias);
  formData.append("experiencia", experiencia);
  formData.append("formacao", formacao);
  formData.append("projectos", projectos);
  formData.append("contactos", contactos);
  formData.append("idiomas", idiomas);
  formData.append("redes", redes);

  const fotoFile = document.querySelector("#foto").files[0];
  let foto_base64 = "";

  if (fotoFile) {
    const reader = new FileReader();
    reader.onload = () => {
      foto_base64 = reader.result;
      gerarCurriculo();
    };
    reader.readAsDataURL(fotoFile);
  } else {
    gerarCurriculo();
  }

  async function gerarCurriculo() {
    const siteGerado = document.querySelector("#site-gerado");
    const fotoHTML = foto_base64
      ? `<img src="${foto_base64}" alt="Foto" />`
      : "";

    siteGerado.innerHTML = `
      <div class="cv-preview">
        <div class="left-column" style="background-color: ${cor};">
          ${fotoHTML}
          <h1>${nome}</h1>
          <p>${profissao}</p>

          <div class="section">
            <h2>Contactos</h2>
            <ul>${contactos.split("\n").map(l => `<li>${l}</li>`).join("")}</ul>
          </div>

          <div class="section">
            <h2>Redes Sociais</h2>
            <ul>${redes.split("\n").map(l => `<li>${l}</li>`).join("")}</ul>
          </div>

          <div class="section">
            <h2>Competências</h2>
            <ul>${competencias.split(",").map(l => `<li>${l.trim()}</li>`).join("")}</ul>
          </div>

          <div class="section">
            <h2>Idiomas</h2>
            <ul>${idiomas.split("\n").map(l => `<li>${l}</li>`).join("")}</ul>
          </div>
        </div>

        <div class="right-column">
          <div class="section">
            <h2>Sobre mim</h2>
            <p>${bio.replace(/\n/g, "<br>")}</p>
          </div>

          <div class="section">
            <h2>Experiência</h2>
            <p>${experiencia.replace(/\n/g, "<br>")}</p>
          </div>

          <div class="section">
            <h2>Formação</h2>
            <p>${formacao.replace(/\n/g, "<br>")}</p>
          </div>

          <div class="section">
            <h2>Projetos</h2>
            <p>${projectos.replace(/\n/g, "<br>")}</p>
          </div>
        </div>
      </div>
    `;

    // Adiciona o HTML gerado ao formData
    formData.append("curriculo_html", siteGerado.innerHTML);

    // Enviar para backend
    try {
      const res = await fetch("http://127.0.0.1:5000/enviar", {
        method: "POST",
        body: formData,
      });

      const resposta = await res.json();
      alert(resposta.message || resposta.error);
    } catch (error) {
      console.error("Erro ao enviar para o servidor:", error);
      alert("Erro ao enviar para o servidor.");
    }

    // Evento do botão de guardar imagem
    const botaoImagem = document.querySelector("#guardar-imagem");
    if (botaoImagem) {
      botaoImagem.addEventListener("click", () => {
        html2canvas(siteGerado).then((canvas) => {
          const link = document.createElement("a");
          link.download = "curriculo.png";
          link.href = canvas.toDataURL("image/png");
          link.click();
        });
      });
    }
  }
});
