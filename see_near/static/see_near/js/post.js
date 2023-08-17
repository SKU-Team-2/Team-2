document.addEventListener("DOMContentLoaded", function () {
  const submitButton = document.getElementById("submit-btn");

  submitButton.addEventListener("click", async function () {
    const title = document.querySelector("#title").value;
    const price = document.querySelector("#price").value;
    const category = document.querySelector("#category select").value;
    const description = document.querySelector(
      ".product-detail textarea"
    ).value;
    const imageInput = document.getElementById("product-detail-img");

    const formData = new FormData();
    formData.append("title", title);
    formData.append("price", price);
    formData.append("categories", category);
    formData.append("content", description);
    if (imageInput.files && imageInput.files[0]) {
      formData.append("images", imageInput.files[0]);
    }

    try {
      const response = await fetch("https://localhost:8000/posts/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to submit product");
      }

      const data = await response.json();
      console.log("Product submitted successfully:", data);
    } catch (error) {
      console.error("Error submitting product:", error);
    }
  });
});
