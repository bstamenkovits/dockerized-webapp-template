FROM node:22-slim AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


FROM python:3.14-slim AS final

WORKDIR /app

COPY database/requirements.txt database/requirements.txt
RUN pip install --no-cache-dir -r database/requirements.txt

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY database/ database/
COPY backend/src/ backend/src/
COPY --from=frontend-builder /app/frontend/dist frontend/dist/

EXPOSE 8000

ENTRYPOINT ["database/entrypoint.sh"]
CMD ["fastapi", "run", "backend/src/app.py", "--port", "8000"]
