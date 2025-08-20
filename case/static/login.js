document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("togBtn");
  const title = document.querySelector("title");
  const heading = document.querySelector("h1");

  toggle.addEventListener("change", () => {
    if (toggle.checked) {

      title.textContent = "Bem vindo, gerente";
      heading.textContent = "Login (Admin)";
    } else {

      title.textContent = "Faça seu Login, usuário";
      heading.textContent = "Login";
    }
  });
});

