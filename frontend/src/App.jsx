import { useState } from "react";
import axios from "axios";
import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
  useLocation,
} from "react-router-dom";
import "./App.css";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please choose a resume file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setMessage("Analyzing resume with AI...");

      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload-resume/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      navigate("/result", { state: response.data });
    } catch (error) {
      console.error(error.response?.data || error.message || error);
      setMessage(
        error.response?.data?.error ||
          "Upload failed. Check backend terminal."
      );
    }
  };

  return (
    <div className="main-container">
      <div className="upload-card">
        <h1>Resume Analyzer</h1>
        <p>Upload your resume PDF or DOCX file</p>

        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileChange}
        />

        <button onClick={handleUpload}>Upload Resume</button>

        <h3>{message}</h3>
      </div>
    </div>
  );
}

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const data = location.state;

  if (!data) {
    return (
      <div className="main-container">
        <div className="upload-card">
          <h2>No result found</h2>
          <button onClick={() => navigate("/")}>Go Back</button>
        </div>
      </div>
    );
  }

  const aiResult = data.ai_result;
  const score = aiResult.overall_score;
  const jobRecommendations = data.job_recommendations;

  return (
    <div className="main-container">
      <div className="score-card">
        <h2>AI Resume Score</h2>

        <div className="circle">
          <span>{score}</span>
        </div>

        <p className="score-text">
          {score >= 80
            ? "Excellent Resume"
            : score >= 60
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

      {jobRecommendations?.jobs && (
        <div className="jobs-card">
          <h2>Recommended Jobs</h2>
          {jobRecommendations.jobs.map((job, index) => (
            <div key={index} className="job-item">
              <div className="job-header">
                <h3>{job.title}</h3>
                <span className="match-badge">{job.match_percentage}% Match</span>
              </div>
              <p className="company-name">{job.company}</p>
              <p className="job-description">{job.description}</p>
              <div className="job-skills">
                <strong>Required Skills:</strong>
                <div className="skills-tags">
                  {job.required_skills.map((skill, idx) => (
                    <span key={idx} className="skill-tag">{skill}</span>
                  ))}
                </div>
              </div>
              <button className="apply-btn">Apply for this Job</button>
            </div>
          ))}
        </div>
      )}

      {data.extracted_text && (
        <div className="text-card">
          <h3>Extracted Resume Text</h3>
          <pre>{data.extracted_text}</pre>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;