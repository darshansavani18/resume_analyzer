import { useLocation, useNavigate } from "react-router-dom";
import "./App.css";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();

  const data = location.state;

  if (!data) {
    return (
      <div className="main-container">
        <h2>No result found</h2>
        <button onClick={() => navigate("/")}>Go Back</button>
      </div>
    );
  }

  const aiResult = data.ai_result;

  return (
    <div className="main-container">
      <div className="score-card">
        <h2>AI Resume Score</h2>

        <div className="circle">
          <span>{aiResult.overall_score}</span>
        </div>

        <p className="score-text">
          {aiResult.overall_score >= 80
            ? "Excellent Resume"
            : aiResult.overall_score >= 60
            ? "Good Resume"
            : "Needs Improvement"}
        </p>
      </div>

      <div className="details-card">
        <h2>Score Breakdown</h2>
        <p>Skills: {aiResult.skills_score}/25</p>
        <p>Projects: {aiResult.projects_score}/25</p>
        <p>Experience: {aiResult.experience_score}/20</p>
        <p>Education: {aiResult.education_score}/10</p>
        <p>Structure: {aiResult.structure_score}/20</p>

        <h3>Strengths</h3>
        <ul>
          {aiResult.strengths.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        <h3>Improvements</h3>
        <ul>
          {aiResult.improvements.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        <button onClick={() => navigate("/")}>Upload Another Resume</button>
      </div>
    </div>
  );
}

export default Result;