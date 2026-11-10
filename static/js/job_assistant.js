const analyzeBtn = document.getElementById("analyzeJobBtn");
const jobDescription = document.getElementById("jobDescription");
const jobStatus = document.getElementById("jobStatus");
const resultsSection = document.getElementById("jobAnalysisResult");


analyzeBtn.addEventListener("click", async () => {

    const description = jobDescription.value.trim();

    if (!description) {
        jobStatus.textContent = "Please paste a job description first.";
        return;
    }

    if (description.length < 50) {
        jobStatus.textContent =
            "Please enter a more detailed description (at least 50 characters).";
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analysing...";
    jobStatus.textContent = "VoxPath is analysing the job description...";
    resultsSection.hidden = true;

    try {

        const response = await fetch("/api/analyze-job", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                description: description
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed.");
        }

        // Role Overview
        document.getElementById("roleOverview").textContent =
            data.role_overview;

        // Skills
        displayList("requiredSkills", data.required_skills);
        displayList("preferredSkills", data.preferred_skills);

        // Responsibilities
        displayList("responsibilities", data.responsibilities);

        // Qualifications
        displayList(
            "requiredQualifications",
            data.required_qualifications
        );

        displayList(
            "preferredQualifications",
            data.preferred_qualifications
        );

        // Preparation Recommendations
        displayList(
            "preparationSuggestions",
            data.preparation_suggestions
        );

        // Quality Score
        document.getElementById("qualityScore").textContent =
            data.quality_score;

        document.getElementById("qualityLabel").textContent =
            data.quality_label;

        displayScoreBreakdown(data.score_breakdown);

        resultsSection.hidden = false;

        jobStatus.textContent =
            "Job description analysed successfully!";

    } catch (error) {

        jobStatus.textContent = error.message;
        console.error("Job analysis error:", error);

    } finally {

        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyse Job Description →";

    }

});


function displayList(elementId, items) {

    const list = document.getElementById(elementId);

    list.innerHTML = "";

    items.forEach(item => {

        const li = document.createElement("li");

        li.textContent = item;

        list.appendChild(li);

    });

}


function displayScoreBreakdown(items) {

    const list = document.getElementById("scoreBreakdown");

    list.innerHTML = "";

    items.forEach(item => {

        const li = document.createElement("li");

        li.textContent =
            `${item.criterion}: ${item.points}/${item.maximum}`;

        list.appendChild(li);

    });

}