const form = document.getElementById("resume-form");
const statusCard = document.getElementById("status-card");
const result = document.getElementById("result");
const generateButton = document.getElementById("generate-btn");

const apiBase = "http://localhost:8000";

const setStatus = (title, message) => {
  statusCard.querySelector("h2").textContent = title;
  statusCard.querySelector("p").textContent = message;
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const jobTitle = document.getElementById("job-title").value.trim();
  const jobDescription = document.getElementById("job-description").value.trim();
  setStatus("Generating...", "Tailoring your resume. Please wait.");
  generateButton.disabled = true;
  generateButton.textContent = "Generating...";

  try {
    const response = await fetch(`${apiBase}/api/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        job_title: jobTitle,
        job_description: jobDescription,
      }),
    });

    if (!response.ok) {
      let detail = "Generation failed.";
      try {
        const payload = await response.json();
        if (payload && payload.detail) {
          detail = payload.detail;
        }
      } catch (parseError) {
        // Ignore JSON parse errors and fall back to default message.
      }
      throw new Error(detail);
    }

    const payload = await response.json();
    result.querySelector("p").textContent = payload.message || "Processing complete.";
    setStatus("Ready", "Request completed successfully.");
  } catch (error) {
    setStatus("Error", error.message || "Could not generate a resume.");
    result.querySelector("p").textContent =
      error.message || "Generation failed. Try again.";
  } finally {
    generateButton.disabled = false;
    generateButton.textContent = "Generate resume";
  }
});
