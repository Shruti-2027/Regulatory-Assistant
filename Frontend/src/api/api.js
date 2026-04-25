const BASE_URL = "http://127.0.0.1:8000";

// helper to handle errors properly
async function request(url, options) {
  const res = await fetch(url, options);

  // IMPORTANT: catch backend errors clearly
  const contentType = res.headers.get("content-type");

  let data;

  if (contentType && contentType.includes("application/json")) {
    data = await res.json();
  } else {
    const text = await res.text();
    console.error("Non-JSON response:", text);
    throw new Error(text || "Server error");
  }

  if (!res.ok) {
    console.error("API Error Response:", data);
    throw new Error(data?.detail || "Request failed");
  }

  return data;
}

// --------------------
// 1. Draft
// --------------------
export const createDraft = async (query) => {
  return request(`${BASE_URL}/draft`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
};

// --------------------
// 2. Validate
// --------------------
export const validateDraft = async (draft_session) => {
  return request(`${BASE_URL}/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ draft_session }),
  });
};

// --------------------
// 3. Revise
// --------------------
export const reviseDraft = async (draft_session, validation_result) => {
  return request(`${BASE_URL}/revise`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ draft_session, validation_result }),
  });
};

// --------------------
// 4. Export PDF
// --------------------
export const exportPDF = async (final_revision) => {
  return request(`${BASE_URL}/export`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ final_revision }),
  });
};