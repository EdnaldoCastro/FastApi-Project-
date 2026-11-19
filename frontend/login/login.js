const form = document.getElementById('form-login');
const msg = document.getElementById('mensagem');

form.addEventListener('submit', async function(evento) {
    evento.preventDefault();

    const emailDigitado = document.getElementById("email").value;
    const senhaDigitado = document.getElementById("senha").value;
    
    const dadosLogin = {
        email: emailDigitado,
        senha: senhaDigitado
    }

    console.log(dadosLogin);

    const resposta = await fetch("/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(dadosLogin)
    });

    const dados = await resposta.json();

    if (!resposta.ok){
        msg.textContent = dados.detail;
        return; 
    }  


    sessionStorage.setItem("access-token", dados.access_token);
    window.location.href = "/front/pedidos/pedidos.html"
})