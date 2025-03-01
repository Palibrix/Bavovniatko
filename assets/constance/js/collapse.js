document.addEventListener("DOMContentLoaded", function(event) {

    let coll = document.getElementsByClassName("collapsible");
    let i;

    for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
      this.classList.toggle("active");
      let content = this.nextElementSibling;
      let toggleIcon = this.querySelector(".toggle-icon");
      if (content.style.display === "block") {
        content.style.display = "none";
        toggleIcon.textContent = "+";
      } else {
          content.style.display = "block";
          toggleIcon.textContent = "-";
      }
    });
  }
});