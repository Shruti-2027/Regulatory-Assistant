import { useEffect, useId, useRef, useState } from 'react'
import Navbar from './components/Navbar'
import './App.css'
import {
  createDraft,
  validateDraft,
  reviseDraft,
  exportPDF,
} from "./api/api";

const STAGE_DELAY_MS = 750
const FINAL_MESSAGE = 'Final Regulatory Draft Ready for Submission'
const PREV_STAGE_MSG = 'Complete previous stage first'
const CONTENT_MSG = 'Add regulatory content first'

function getTheme() {
  if (typeof window === 'undefined') return 'light'
  const stored = localStorage.getItem('ra-theme')
  if (stored === 'light' || stored === 'dark') return stored
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function statusLabel(stage, ctx) {
  const {
    hasContent,
    draftRunning,
    draftComplete,
    validateRunning,
    validateComplete,
    finalRunning,
    finalComplete,
  } = ctx

  if (stage === 1) {
    if (!hasContent) return { text: 'Locked', sub: 'Input required' }
    if (draftRunning) return { text: 'In Progress', sub: 'Drafting' }
    if (draftComplete) return { text: 'Completed', sub: 'Drafting' }
    return { text: 'Ready', sub: 'Start drafting' }
  }
  if (stage === 2) {
    if (!draftComplete) return { text: 'Locked', sub: 'Complete drafting first' }
    if (validateRunning) return { text: 'In Progress', sub: 'Validating' }
    if (validateComplete) return { text: 'Completed', sub: 'Validation' }
    return { text: 'Ready', sub: 'Run validation' }
  }
  if (stage === 3) {
    if (!validateComplete) return { text: 'Locked', sub: 'Complete validation first' }
    if (finalRunning) return { text: 'In Progress', sub: 'Finalizing' }
    if (finalComplete) return { text: 'Completed', sub: 'Final output' }
    return { text: 'Ready', sub: 'Resolve feedback' }
  }
  return { text: '—', sub: '' }
}

function currentStatusText(ctx) {
  const {
    hasContent,
    draftRunning,
    draftComplete,
    validateRunning,
    validateComplete,
    finalRunning,
    finalComplete,
  } = ctx

  if (finalComplete) return FINAL_MESSAGE
  if (finalRunning) return 'Finalizing regulatory draft…'
  if (validateComplete && !finalComplete && !finalRunning)
    return 'Validation complete. Resolve feedback to generate the final package.'
  if (validateRunning) return 'Validating in progress…'
  if (draftComplete && !validateComplete) return 'Drafting complete. Proceed to validation.'
  if (draftRunning) return 'Drafting in progress…'
  if (hasContent && !draftComplete) return 'Content ready. Start drafting when ready.'
  return 'Paste or type regulatory content to begin the submission workflow.'
}

export default function App() {
  const chatInputId = useId()
  const timers = useRef([])

  const [regulatoryContent, setRegulatoryContent] = useState('')
  const [chatMessage, setChatMessage] = useState('')
  const [draftSession, setDraftSession] = useState(null)
  const [validationResult, setValidationResult] = useState(null)
  const [finalRevision, setFinalRevision] = useState(null)
  const [draftComplete, setDraftComplete] = useState(false)
  const [validateComplete, setValidateComplete] = useState(false)
  const [finalComplete, setFinalComplete] = useState(false)
  const [draftRunning, setDraftRunning] = useState(false)
  const [validateRunning, setValidateRunning] = useState(false)
  const [finalRunning, setFinalRunning] = useState(false)

  const [theme, setTheme] = useState(getTheme)


  function toggleTheme() {
    setTheme((t) => (t === 'dark' ? 'light' : 'dark'))
  }

  const hasContent = regulatoryContent.trim().length > 0

  function handleRegulatoryContentChange(e) {
    setRegulatoryContent(e.target.value)
    setDraftComplete(false)
    setValidateComplete(false)
    setFinalComplete(false)
  }

  async function handleDownloadPDF() {
  try {
    const res = await exportPDF(finalRevision);

    console.log("PDF path:", res.pdf_file);

    // optional: open file if backend returns URL
    window.open(res.pdf_file, "_blank");
  } catch (err) {
    console.error(err);
  }
}

  function handleChatSend() {
    console.log('[chat send]', chatMessage)
    setChatMessage('')
  }

  async function handleStartDrafting() {
    if (!hasContent || draftRunning || draftComplete) return;

    setDraftRunning(true);

    try {
      const data = await createDraft(regulatoryContent);

      console.log("Draft Response:", data);

      setDraftSession(data);
      setDraftComplete(true);
    } catch (err) {
      console.error("Draft Error:", err);
    } finally {
      setDraftRunning(false);
    }
  }

  async function handleValidate() {
    if (!draftComplete || validateRunning || validateComplete) return;

    setValidateRunning(true);

    try {
      const data = await validateDraft(draftSession);

      console.log("Validation Response:", data);

      setValidationResult(data);
      setValidateComplete(true);
    } catch (err) {
      console.error("Validation Error:", err);
    } finally {
      setValidateRunning(false);
    }
  }

  async function handleResolveFeedback() {
    if (!validateComplete || finalRunning || finalComplete) return;

    setFinalRunning(true);

    try {
      const data = await reviseDraft(draftSession, validationResult);

      console.log("Final Response:", data);

      setFinalRevision(data);
      setFinalComplete(true);
    } catch (err) {
      console.error("Final Error:", err);
    } finally {
      setFinalRunning(false);
    }
  }

  const ctx = {
    hasContent,
    draftRunning,
    draftComplete,
    validateRunning,
    validateComplete,
    finalRunning,
    finalComplete,
  }

  const canDraft = hasContent && !draftRunning && !draftComplete
  const canValidate = draftComplete && !validateRunning && !validateComplete
  const canResolve = validateComplete && !finalRunning && !finalComplete

  function statusSlug(text) {
    if (text === 'In Progress') return 'progress'
    return text.toLowerCase().replace(/\s+/g, '-')
  }

  const s1Active = draftRunning || (hasContent && !draftComplete)
  const s2Active = validateRunning || (draftComplete && !validateComplete)
  const s3Active = finalRunning || (validateComplete && !finalComplete)

  return (
    <div className="app">
      <Navbar theme={theme} onToggleTheme={toggleTheme} />

      <main className="main">
        <div className="main__inner">
          <section className="section-block workflow-section" id="document-review" aria-labelledby="workflow-title">
            <h2 id="workflow-title" className="block-title">
              Document review & submission workflow
            </h2>
            <p className="block-lead">
              Follow the sequence: input content → draft → validate → finalize. Later stages unlock only after the
              previous stage completes.
            </p>

            <div className="upload-wrap">
              <div className="upload-gradient">
                <div className="upload card card--upload card--solid-inner">
                  <div className="upload__head">
                    <span className="upload__badge">Input</span>
                    <h3 id="upload-heading" className="section-title section-title--lg">
                      Regulatory content
                    </h3>
                    <p className="section-desc">
                      Paste or type the controlled document text for this submission package.
                    </p>
                  </div>
                  <textarea
                    className="regulatory-textarea w-full rounded-lg bg-slate-900 text-slate-100 border border-slate-700 p-3"
                    value={regulatoryContent}
                    onChange={handleRegulatoryContentChange}
                    placeholder="Paste or type your regulatory content here..."
                    rows={4}
                    aria-labelledby="upload-heading"
                  />
                </div>
              </div>
            </div>

            <section className="actions" aria-label="Workflow steps">
              <article className="action-card card card--solid">
                <div className="action-card__accent action-card__accent--teal" aria-hidden />
                <h3 className="action-card__title">Drafting</h3>
                <p className="action-card__hint">Generate the initial regulatory draft from your source content.</p>
                <button
                  type="button"
                  className="btn btn--primary btn--teal"
                  disabled={!canDraft}
                  title={!hasContent ? CONTENT_MSG : draftComplete ? 'Stage complete' : undefined}
                  onClick={handleStartDrafting}
                >
                  {draftRunning ? 'Drafting…' : draftComplete ? 'Completed' : 'Start Drafting'}
                </button>
              </article>

              <article className="action-card card card--solid">
                <div className="action-card__accent action-card__accent--blue" aria-hidden />
                <h3 className="action-card__title">Validation</h3>
                <p className="action-card__hint">Verify structure and controls against your internal SOPs.</p>
                <button
                  type="button"
                  className="btn btn--primary btn--blue"
                  disabled={!canValidate}
                  title={
                    validateComplete ? 'Stage complete' : !draftComplete ? PREV_STAGE_MSG : undefined
                  }
                  onClick={handleValidate}
                >
                  {validateRunning ? 'Validating…' : validateComplete ? 'Completed' : 'Validate'}
                </button>
              </article>

              <article className="action-card card card--solid">
                <div className="action-card__accent action-card__accent--violet" aria-hidden />
                <h3 className="action-card__title">Final output</h3>
                <p className="action-card__hint">Apply comments and seal the submission-ready package.</p>
                <button
                  type="button"
                  className="btn btn--primary btn--violet"
                  disabled={!canResolve}
                  title={
                    finalComplete ? 'Stage complete' : !validateComplete ? PREV_STAGE_MSG : undefined
                  }
                  onClick={handleResolveFeedback}
                >
                  {finalRunning ? 'Resolving…' : finalComplete ? 'Completed' : 'Resolve Feedback'}
                </button>
              </article>
            </section>

            <section className="output card card--solid" aria-labelledby="output-heading">
              <div className="output__section-head">
                <div>
                  <h3 id="output-heading" className="section-title section-title--lg">
                    Final output
                  </h3>
                  <p className="section-desc section-desc--tight">
                    Pipeline status across drafting, validation, and final output.
                  </p>
                </div>
                <button
                  type="button"
                  className="btn btn--pdf"
                  disabled={!finalComplete}
                  onClick={handleDownloadPDF}
                  title={
                    finalComplete
                      ? 'Download a stub export (PDF flow simulated)'
                      : 'Complete the final output step to enable download'
                  }
                >
                  <svg className="btn__icon" width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden>
                    <path
                      d="M12 3v12m0 0l4-4m-4 4l-4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  Download as PDF
                </button>
              </div>

              <div className="result-sections">
                {/* Drafting Output */}
                <div className="result-card">
                  <h4>Drafting Output</h4>
                  <div className="result-box">
                    {draftSession ? (
                      <pre>{draftSession?.draft_output}</pre>
                    ) : (
                      <p>No drafting output yet.</p>
                    )}
                  </div>
                </div>

                {/* Validation Output */}
                <div className="result-card">
                  <h4>Validation Output</h4>
                  <div className="result-box">
                    {validationResult ? (
                      <pre>{validationResult?.validation_feedback}</pre>
                    ) : (
                      <p>No validation output yet.</p>
                    )}
                  </div>
                </div>

                {/* Final Output */}
                <div className="result-card">
                  <h4>Final Output</h4>
                  <div className="result-box">
                    {finalRevision ? (
                      <pre>{finalRevision?.improved_draft}</pre>
                    ) : (
                      <p>No final output yet.</p>
                    )}
                  </div>
                </div>
              </div>
             
            </section>

            <section className="chat-panel card card--solid" aria-labelledby="chat-heading">
              <div className="chat-panel__head">
                <div>
                  <h3 id="chat-heading" className="section-title section-title--lg">
                    Keep Yourself Updated
                  </h3>
                  <p className="section-desc section-desc--tight">
                    Ask the assistant about labeling, data integrity, or regional requirements.
                  </p>
                </div>
                <span className="chat-panel__pill">Assistant</span>
              </div>
              <label htmlFor={chatInputId} className="visually-hidden">
                Regulatory guidelines question
              </label>
              <div className="chat__composer">
                <textarea
                  id={chatInputId}
                  className="chat__input chat__input--composer"
                  placeholder="Ask me the current guidelines..."
                  rows={3}
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                />
                <button
                  type="button"
                  className="chat__send"
                  onClick={handleChatSend}
                  aria-label="Send message"
                  title="Send"
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
                    <path
                      d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>
              </div>
            </section>
          </section>
        </div>
      </main>
    </div>
  )
}
