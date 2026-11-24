const form = document.getElementById('form-login');
const mensagem = document.getElementById('mensagem');

form.addEventListener('submit', async function(evento) {
    evento.preventDefault();

    const emailDigitado = document.getElementById("email").value;
    const senhaDigitado = document.getElementById("senha").value;
    
    const dadosLogin = {
        email: emailDigitado,
        senha: senhaDigitado
    }

    try{
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(dadosLogin)
        });

        const dados = await response.json();

        if (response.status == 401){
            mensagem.textContent = "Email ou senha inválidos!"
            return; 
        }  

        if (response.status ==  500){
            mensagem.textContent = "Erro no servidor interno!"
            return; 
        }  

        if (!response.ok){
            mensagem.textContent = 'Não foi possível realizar o login!'
            return
        }

        sessionStorage.setItem("access-token", dados.access_token);
        window.location.replace("/front/pedidos/pedidos.html")
        

       } catch{
        mensagem.textContent = "Erro no servidor!"
    }
})