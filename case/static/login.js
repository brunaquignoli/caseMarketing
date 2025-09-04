document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("togBtn");
  const title = document.querySelector("title");
  const heading = document.querySelector("h1");
  const roleInput = document.getElementById("roleInput");

  toggle.addEventListener("change", () => {
    if (toggle.checked) {
      title.textContent = "Bem vindo, gerente";
      heading.textContent = "Login (Admin)";
      roleInput.value = "admin";
    } else {
      title.textContent = "Faça seu Login, usuário";
      heading.textContent = "Login";
      roleInput.value = "user";
    }
  });
});

