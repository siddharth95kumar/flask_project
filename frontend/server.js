import express from "express";
import path from "path";
import axios from "axios";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3001;
const BACKEND_URL = "http://flask-backend:5000";

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// Root → form.html
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "form.html"));
});

// Submit route → forward request to Flask backend
app.post("/submit", async (req, res) => {
  try {
    // Forward form submission as JSON
    const formData = {
      name: req.body.name,
      email: req.body.email,
      message: req.body.message
    };

    await axios.post(`${BACKEND_URL}/api/submit`, formData, {
      headers: { "Content-Type": "application/json" }
    });

    res.redirect("/success");
  } catch (err) {
    console.error("❌ Backend error:", err.message);
    res.status(500).json({ ok: false, error: "Backend unavailable" });
  }
});

// Success page
app.get("/success", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "success.html"));
});

app.listen(PORT, () =>
  console.log(`✅ Frontend running at http://localhost:${PORT}`)
);
