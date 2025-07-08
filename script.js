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

    // Atualiza a cor do lado esquerdo do currículo
    siteGerado.style.setProperty('--cor-destaque', cor);

    siteGerado.innerHTML = `
      <div class="cv-preview">
        <div class="left-column">
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
    // Antes de enviar, aplica a cor de destaque inline na left-column e remove qualquer style da cv-preview
    const parser = new DOMParser();
    const doc = parser.parseFromString(siteGerado.innerHTML, 'text/html');
    const leftColumn = doc.querySelector('.left-column');
    if (leftColumn) {
      leftColumn.setAttribute('style', `background-color: ${cor} !important; color: #fff !important; width:35%; height:297mm; min-height:297mm; padding:30px; display:flex; flex-direction:column; justify-content:flex-start; align-items:center;`);
    }
    const rightColumn = doc.querySelector('.right-column');
    if (rightColumn) {
      rightColumn.setAttribute('style', 'background: #fff !important; color: #000 !important; width:65%; height:297mm; min-height:297mm; padding:30px; display:flex; flex-direction:column; justify-content:flex-start;');
      // Força o texto a ficar preto
      Array.from(rightColumn.querySelectorAll('*')).forEach(el => {
        el.setAttribute('style', (el.getAttribute('style') || '') + 'color:#000 !important;background:transparent !important;');
      });
    }
    const cvPreview = doc.querySelector('.cv-preview');
    if (cvPreview) {
      cvPreview.setAttribute('style', 'width:210mm; height:297mm; display:flex; box-shadow:none; overflow:hidden; page-break-after:always;');
    }
    // Garante que a foto aparece corretamente
    const img = doc.querySelector('.left-column img');
    if (img && foto_base64) {
      img.setAttribute('src', foto_base64);
      img.setAttribute('style', 'width:120px; height:120px; border-radius:50%; object-fit:cover; margin-bottom:20px; display:block;');
    }
    // Loga o HTML que será enviado ao backend para facilitar depuração
    console.log('HTML enviado ao backend (curriculo_html):', doc.body.innerHTML);
    formData.append("curriculo_html", doc.body.innerHTML);

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

  // Mostrar nome do ficheiro escolhido para foto
  const inputFoto = document.getElementById('foto');
  const nomeFicheiro = document.getElementById('nome-ficheiro');
  if (inputFoto && nomeFicheiro) {
    inputFoto.addEventListener('change', function() {
      const nome = this.files[0] ? this.files[0].name : '';
      nomeFicheiro.textContent = nome;
    });
  }

  // Botão de cor de destaque com cor dinâmica
  const inputCor = document.getElementById('cor');
  const labelCor = document.getElementById('label-cor');
  if (inputCor && labelCor) {
    function atualizarCorBotao() {
      labelCor.style.background = inputCor.value;
      // Ajusta a cor do texto para branco ou preto conforme contraste
      const cor = inputCor.value.replace('#', '');
      const r = parseInt(cor.substr(0,2),16);
      const g = parseInt(cor.substr(2,2),16);
      const b = parseInt(cor.substr(4,2),16);
      const luminancia = (0.299*r + 0.587*g + 0.114*b)/255;
      labelCor.style.color = luminancia > 0.5 ? '#000' : '#fff';
    }
    inputCor.addEventListener('input', atualizarCorBotao);
    atualizarCorBotao();
  }
});
