# Deployment guide

This project is prepared for a free academic-demo deployment:

- **Frontend:** Vercel
- **API:** Render Free web service
- **Database:** Supabase Free PostgreSQL

This is appropriate for a final-year project demo. It is not a production setup for real government data.

## 1. Create the database

1. Create a free project at [Supabase](https://supabase.com/).
2. In **Connect**, copy the PostgreSQL connection string for a direct connection.
3. Replace `[YOUR-PASSWORD]` in that string with the database password you created.
4. Add `?sslmode=require` to the end if it is not already present.

Keep this value private. It belongs only in the Render `DATABASE_URL` environment variable.

## 2. Deploy the FastAPI backend on Render

1. Push this repository to GitHub.
2. In Render, select **New > Blueprint** and connect the repository. Render detects `render.yaml`.
3. Choose the **Free** plan.
4. When prompted, set:
   - `DATABASE_URL`: the Supabase connection string from step 1.
   - `CORS_ORIGINS`: temporarily use `https://placeholder.vercel.app`; update it after Vercel gives you the real frontend URL.
5. Deploy, then open `https://<your-render-service>.onrender.com/health`. It must return `{"status":"healthy"}`.

The first deployment automatically creates tables and adds the project’s demo accounts.

## 3. Deploy the React frontend on Vercel

1. In Vercel, select **Add New > Project**, import the same GitHub repository, and use the existing root `vercel.json`.
2. In **Environment Variables**, add this variable for Production, Preview, and Development:

   ```text
   VITE_API_BASE_URL=https://<your-render-service>.onrender.com
   ```

3. Deploy. Copy the resulting `https://<your-project>.vercel.app` URL.
4. In Render, change `CORS_ORIGINS` to that exact Vercel URL, save it, and redeploy the API.
5. In Vercel, redeploy once more if you added the API URL after the first build.

## 4. Verify

1. Open the Vercel URL and sign in with `employee@demo.gov.in` and `Demo@1234`.
2. Create a ticket and refresh the page; it should remain.
3. Ask a question from a seeded department document.

## Important free-tier limits

- Render’s free service sleeps after 15 minutes without requests, so the first request can be slow.
- Supabase Free provides 500 MB of database space and pauses low-activity projects after roughly one week; it can be resumed from its dashboard.
- The free Render API deliberately installs the lightweight dependency set. It uses the project’s lexical/document fallback when Ollama and local embeddings are unavailable. Running `llama3.2` needs a paid VM or a separate AI API.
- Do not upload real employee or government data, or use demo passwords, in a public deployment.
