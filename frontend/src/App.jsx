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
        <p>Upload your resume (PDF, DOCX, PNG, JPG, or JPEG)</p>

        <input
          type="file"
          accept=".pdf,.doc,.docx,.png,.jpg,.jpeg"
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
  const fieldAnalysis = data.field_analysis;
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
      </div>

      {fieldAnalysis && fieldAnalysis.field_scores && (
        <div className="field-scores-card">
          <h2>Resume Fit by Career Field</h2>
          <p className="versatility-score">
            Overall Versatility Score: {fieldAnalysis.overall_versatility_score}/100
          </p>

          {fieldAnalysis.best_fit_fields && fieldAnalysis.best_fit_fields.length > 0 && (
            <div className="best-fit-section">
              <h3>Best Fit Fields</h3>
              <div className="best-fit-tags">
                {fieldAnalysis.best_fit_fields.map((field, index) => (
                  <span key={index} className="best-fit-badge">{field}</span>
                ))}
              </div>
            </div>
          )}

          <div className="field-scores-grid">
            {Object.entries(fieldAnalysis.field_scores).map(([field, data], index) => (
              <div key={index} className="field-score-item">
                <div className="field-header">
                  <h4>{field}</h4>
                  <span className={`field-score ${data.score >= 70 ? "high" : data.score >= 50 ? "medium" : "low"}`}>
                    {data.score}
                  </span>
                </div>
                
                <div className="field-progress-bar">
                  <div 
                    className="field-progress-fill" 
                    style={{width: `${data.score}%`}}
                  ></div>
                </div>

                {data.strengths && data.strengths.length > 0 && (
                  <div className="field-strengths">
                    <strong>Strengths:</strong>
                    <ul>
                      {data.strengths.map((strength, idx) => (
                        <li key={idx}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {data.gaps && data.gaps.length > 0 && (
                  <div className="field-gaps">
                    <strong>Gaps:</strong>
                    <ul>
                      {data.gaps.map((gap, idx) => (
                        <li key={idx}>{gap}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="details-card">
        <button onClick={() => navigate("/")}>Upload Another Resume</button>
      </div>

      {jobRecommendations?.jobs && (
        <div className="jobs-card">
          <h2>Recommended Jobs</h2>
          {jobRecommendations.jobs.map((job, index) => (
            <div key={index} className="job-item">
              <div className="job-header">
                <h2>{job.title}</h2>
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