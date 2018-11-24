let erroUsername = false, erroEmail = false, erroSenha = false;
$("#username").focusout(function(){
  var username = $(this).val();
  if (username != "") {
    $.ajax({
      url: '/validaCadastro/',
      data: {
        'username': username
      },
      dataType: 'json',
      success: function(data) {
        if (data.result) {
          document.getElementById('erroUsername').style.display = "";
          document.getElementById('erroUsername').innerHTML = "Usuário já existe!";
          erroUsername = true;
        }
        else if (data.tem_espaco){
          document.getElementById('erroUsername').style.display = "";
          document.getElementById('erroUsername').innerHTML = "Não é permitido o uso de espaço no nome!";
          erroUsername = true;
        } else {
          erroUsername = false;
          document.getElementById('erroUsername').style.display = "none"
        }
      }
    })
  }
  else{
    alert('Todos os campos precisam ser preenchidos');
  }
});
$("#confPass").change(function(){
  var confPass = $(this).val();
  var password = document.getElementById('password').value;
  if(password != confPass){
    document.getElementById('erroSenha').style.display = "";
    document.getElementById('erroSenha').innerHTML = "Senhas estão diferentes!"
    erroSenha = true;
  }
  else{
    document.getElementById('erroSenha').style.display = "none"
    erroSenha = false;
  }
});
$("#email").focusout(function(){
  var email = $(this).val();
  if (email != "") {
    $.ajax({
      url: '/validaCadastro/',
      data: {
        'email': email
      },
      dataType: 'json',
      success: function(data) {
        if (data.result) {
          document.getElementById('erroEmail').style.display = "";
          document.getElementById('erroEmail').innerHTML = "E-mail inválido ou já em uso!";
          erroEmail = true;
        }
        else{
          document.getElementById('erroEmail').style.display = "none";
          erroEmail = false;
        }
      }
    })
  }
  else{
    document.getElementById('erroEmail').style.display = "";
    document.getElementById('erroEmail').innerHTML = "Todos os campos precisam ser preenchidos!";
    erroEmail = true;
  }
});
$("#btnCadastrar").click(function(){
  if(erroUsername == false && erroSenha == false && erroEmail == 0){
        document.getElementById('btnCadastrar').type = "submit";
        $("#btnCadastrar").click();
  }
  else{
    alert("Corrija os erros");
  }
});
