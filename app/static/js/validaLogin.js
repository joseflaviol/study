var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$("#btnLogin").click(function() {
  var username = document.getElementById('usernameLogin').value;
  var password = document.getElementById('passwordLogin').value;
  if (username != "" && password != "") {
    $.ajax({
      type: 'POST',
      url: '/validaLogin/',
      data: {
        'csrfmiddlewaretoken': csrftoken,
        'username': username,
        'password': password
      },
      dataType: 'json',
      success: function(data) {
        if (data.result) {
          $("#logar").click();
        }
        else {
          document.getElementById('erroLogin').style.display = "";
          document.getElementById('erroLogin').innerHTML = "Login não existe!"
        }
      }
    });
  }
  else {
    alert("Todos campos devem ser preenchidos");
  }
});
