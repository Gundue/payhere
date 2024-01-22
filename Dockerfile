# Builder stage
FROM python:3.9-slim-buster
# Set the working directory in the container
WORKDIR /app
# Install Poetry and Pillow package
RUN pip install poetry
# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /app/
# Install project dependencies with Poetry
RUN poetry install --no-root --no-interaction --no-ansi
# Copy the entire project directory to the container
COPY . /app/
# Running Docker Files with Poetry
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]