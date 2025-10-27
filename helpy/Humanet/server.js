import express from "express";
import cors from "cors";
import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Endpoint para recibir texto del usuario y devolver categorías
app.post("/chat", async (req, res) => {
  const { message } = req.body;
  if (!message) return res.status(400).json({ error: "No message provided" });

  try {
    const prompt = `
    Eres un asistente que sugiere categorías de eventos según la descripción del usuario.
    Responde en formato JSON: {"categorias": ["categoría1","categoría2",...]}.
    Categorías posibles: música, teatro, arte, deporte, naturaleza, comida.
    Usuario: "${message}"
    `;

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: prompt }],
      temperature: 0
    });

    const responseText = completion.choices[0].message.content;
    // Intentar parsear JSON de la respuesta
    const categorias = JSON.parse(responseText).categorias;

    res.json({ categorias });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error al procesar el mensaje" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor corriendo en puerto ${PORT}`));
