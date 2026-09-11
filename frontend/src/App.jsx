import { useEffect, useMemo, useState } from "react";
import { getModelInfo, requestPrediction } from "./api";
import {
  EXAMPLE_PATIENT,
  FEATURE_CONFIG,
} from "./featureConfig";
import "./App.css";

const FORM_SECTIONS = [
  {
    title: "Basic information",
    description: "General health and body information",
    keys: [
      "Age (yrs)",
      "BMI",
      "Pregnant(Y/N)",
      "No. of aborptions",
    ],
  },
  {
    title: "Menstrual health",
    description: "Information about your menstrual cycle",
    keys: [
      "Cycle(R/I)",
      "Cycle length(days)",
    ],
  },
  {
    title: "Symptoms and lifestyle",
    description: "Select Yes or No for each item",
    keys: [
      "Weight gain(Y/N)",
      "hair growth(Y/N)",
      "Skin darkening (Y/N)",
      "Hair loss(Y/N)",
      "Pimples(Y/N)",
      "Fast food (Y/N)",
      "Reg.Exercise(Y/N)",
    ],
  },
  {
    title: "Basic measurements",
    description: "Enter recent measurements where available",
    keys: [
      "Pulse rate(bpm)",
      "RR (breaths/min)",
      "Hb(g/dl)",
      "BP _Systolic (mmHg)",
      "BP _Diastolic (mmHg)",
    ],
  },
];

function App() {
  const [modelFeatures, setModelFeatures] = useState([]);
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendLoading, setBackendLoading] = useState(true);

  useEffect(() => {
    async function loadFeatures() {
      try {
        const modelInfo = await getModelInfo();
        setModelFeatures(modelInfo.features);
      } catch (err) {
        setError(err.message);
      } finally {
        setBackendLoading(false);
      }
    }

    loadFeatures();
  }, []);

  const configuredSections = useMemo(() => {
    return FORM_SECTIONS.map((section) => ({
      ...section,
      features: section.keys
        .filter((key) => modelFeatures.includes(key))
        .map((key) => ({
          key,
          ...FEATURE_CONFIG[key],
        })),
    })).filter((section) => section.features.length > 0);
  }, [modelFeatures]);

  function handleChange(featureKey, value) {
    setFormData((current) => ({
      ...current,
      [featureKey]: value === "" ? "" : Number(value),
    }));

    setResult(null);
    setError("");
  }

  function loadExamplePatient() {
    setFormData({ ...EXAMPLE_PATIENT });
    setResult(null);
    setError("");
  }

  function resetForm() {
    setFormData({});
    setResult(null);
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const prediction = await requestPrediction(formData);
      setResult(prediction);

      setTimeout(() => {
        document
          .getElementById("screening-result")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
      }, 100);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const completedInputs = modelFeatures.filter(
    (feature) =>
      formData[feature] !== undefined &&
      formData[feature] !== ""
  ).length;

  const formComplete =
    modelFeatures.length === 18 &&
    completedInputs === modelFeatures.length;

  const progress = modelFeatures.length
    ? Math.round(
        (completedInputs / modelFeatures.length) * 100
      )
    : 0;

  function renderInput(feature) {
    const value = formData[feature.key] ?? "";

    if (feature.type === "yesNo") {
      return (
        <select
          value={value}
          onChange={(event) =>
            handleChange(feature.key, event.target.value)
          }
          required
        >
          <option value="">Select an option</option>
          <option value="1">Yes</option>
          <option value="0">No</option>
        </select>
      );
    }

    if (feature.type === "select") {
      return (
        <select
          value={value}
          onChange={(event) =>
            handleChange(feature.key, event.target.value)
          }
          required
        >
          <option value="">Select an option</option>

          {feature.options.map((option) => (
            <option
              key={option.value}
              value={option.value}
            >
              {option.label}
            </option>
          ))}
        </select>
      );
    }

    return (
      <input
        type="number"
        min={feature.min}
        max={feature.max}
        step={feature.step}
        value={value}
        placeholder={feature.placeholder}
        onChange={(event) =>
          handleChange(feature.key, event.target.value)
        }
        required
      />
    );
  }

  return (
    <main className="app">
      <header className="hero">
        <span className="eyebrow">
          AI-powered educational screening
        </span>

        <h1>
          Understand your PCOS screening likelihood
        </h1>

        <p>
          Complete a short health questionnaire to receive
          an educational machine-learning screening result.
        </p>
      </header>

      <section className="screening-card">
        <div className="section-heading">
          <div>
            <span>PCOSense screening</span>
            <h2>Patient information</h2>
          </div>

          <strong>
            {completedInputs}/{modelFeatures.length || 18} completed
          </strong>
        </div>

        <div className="progress-track">
          <div
            className="progress-value"
            style={{ width: `${progress}%` }}
          />
        </div>

        {backendLoading && (
          <div className="message">
            Connecting to the screening model...
          </div>
        )}

        {error && (
          <div className="message error" role="alert">
            {error}
          </div>
        )}

        {!backendLoading && modelFeatures.length > 0 && (
          <form onSubmit={handleSubmit}>
            {configuredSections.map((section) => (
              <section
                className="form-section"
                key={section.title}
              >
                <div className="form-section-heading">
                  <h3>{section.title}</h3>
                  <p>{section.description}</p>
                </div>

                <div className="form-grid">
                  {section.features.map((feature) => (
                    <label
                      key={feature.key}
                      className="field"
                    >
                      <span>
                        {feature.label}

                        {feature.unit && (
                          <small> ({feature.unit})</small>
                        )}
                      </span>

                      {renderInput(feature)}
                    </label>
                  ))}
                </div>
              </section>
            ))}

            <div className="form-actions">
              <button
                type="button"
                className="example-button"
                onClick={loadExamplePatient}
              >
                Fill with example data
              </button>

              <button
                type="button"
                className="reset-button"
                onClick={resetForm}
              >
                Clear form
              </button>

              <button
                type="submit"
                className="submit-button"
                disabled={!formComplete || loading}
              >
                {loading
                  ? "Analysing..."
                  : "Check screening likelihood"}
              </button>
            </div>
          </form>
        )}

        {result && (
          <section
            id="screening-result"
            className={`result ${
              result.prediction === 1
                ? "higher"
                : "lower"
            }`}
            aria-live="polite"
          >
            <span className="result-label">
              Screening result
            </span>

            <h2>{result.label}</h2>

            <strong>
              {(result.probability * 100).toFixed(1)}%
            </strong>

            <p>Estimated model probability</p>

            <div className="probability-track">
              <div
                className="probability-value"
                style={{
                  width: `${result.probability * 100}%`,
                }}
              />
            </div>

            <small>{result.disclaimer}</small>
          </section>
        )}
      </section>

      <footer className="footer">
        <p>
          PCOSense is an educational machine-learning
          project and does not provide medical diagnosis.
        </p>
      </footer>
    </main>
  );
}

export default App;