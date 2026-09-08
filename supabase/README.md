# Supabase setup

1. Create a Supabase project on the free plan.
2. Open **SQL Editor** and run `schema.sql`.
3. From **Project Settings → Database**, copy the pooled or direct PostgreSQL connection string into `DATABASE_URL`. Use the SQLAlchemy form with `postgresql+psycopg2://`.
4. From **Project Settings → API**, copy the project URL into `SUPABASE_URL` and the server-only `service_role` key into `SUPABASE_SERVICE_ROLE_KEY`. Never expose that key to the frontend.
5. Keep `SUPABASE_BUCKET=audio`.

## Vercel projects

Create two Vercel projects from the same GitHub repository:

- `vocalize-api`: Root Directory `backend`, Framework preset FastAPI/Python, environment variables from the backend `.env.example`.
- `vocalize-web`: Root Directory `frontend`, Framework preset Vite, `VITE_API_URL` set to the deployed `vocalize-api` URL.

Set `FRONTEND_URL` in the API project to the deployed web URL. Redeploy the API after changing it.
