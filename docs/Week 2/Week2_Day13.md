# Week 2 — Day 13 (Code‑Quality Pass & Pre‑Commit Hooks)

> **Target session:** ≈ 3 h (deep work)  **Goal:** enforce consistent style across the repo (Python & TypeScript) using **pre‑commit**, Ruff, Black, isort, and ESLint strict mode—then fix all automatic warnings. *No refactors, logic changes, or API tweaks today.*
>
> **Outcome:** running `git commit` auto‑formats staged files; CI passes with zero lint errors in backend and frontend.

---

## 1 · Install and configure **pre‑commit** (repo root)

```bash
pip install pre-commit
pre-commit install  # adds .git/hooks/pre-commit
```

Create **`.pre-commit-config.yaml`** in repo root:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff
    rev: v0.4.1
    hooks: [id: ruff]

  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile=black"]

  - repo: local
    hooks:
      - id: eslint
        name: eslint (frontend)
        entry: pnpm exec eslint --max-warnings=0 apps/frontend/src
        language: system
        types: [javascript, jsx, ts, tsx]
```

*(We’ll add ESLint config next.)*

Run once to auto‑install hook environments:

```bash
pre-commit run --all-files
```

This will reformat Python with Black, sort imports, and Ruff‑fix trivial errors.

---

## 2 · Frontend ESLint strict mode

```bash
cd apps/frontend
pnpm add -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-react eslint-config-prettier
```

Create **`.eslintrc.cjs`**:

```js
module.exports = {
  parser: "@typescript-eslint/parser",
  parserOptions: { ecmaVersion: "latest", sourceType: "module" },
  plugins: ["@typescript-eslint", "react"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "prettier",
  ],
  settings: { react: { version: "detect" } },
  rules: {
    "react/prop-types": "off",
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
  },
};
```

Generate ignore file:

```bash
echo "dist/\nnode_modules/" > apps/frontend/.eslintignore
```

Run linter:

```bash
pnpm exec eslint apps/frontend/src --fix
```

Fix any remaining warnings manually (rename unused vars, etc.).

---

## 3 · Add dev dependencies to backend

Append to `apps/backend/requirements.txt` (dev section):

```
# dev tools
pre-commit
ruff
black
isort
pytest-asyncio
```

(Backend container doesn’t need these; local dev only.)

---

## 4 · Update CI workflow (`.github/workflows/ci.yml`)

Add a new **pre‑commit** job before lint:

```yaml
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - name: run pre-commit
        uses: pre-commit/action@v3.0.1
```

Remove standalone Ruff step if you like (pre‑commit covers it).

Add ESLint step in frontend-lint job:

```yaml
      - name: eslint strict
        run: pnpm exec eslint apps/frontend/src --max-warnings=0
```

---

## 5 · Fix residual warnings

Run:

```bash
pre-commit run --all-files
pnpm exec eslint apps/frontend/src
```

Manual edits: rename unused vars, add explicit return types, etc. **No functional changes**—if logic tweak seems required, `# noqa` / `// eslint-disable-next-line` and add TODO for Week 3.

---

## 6 · Commit formatted code & configs

```bash
git checkout -b day13-code-quality
# add everything the hooks changed
git add -u
git commit -m "chore: enforce Ruff+Black+isort & ESLint via pre-commit"
git push -u origin day13-code-quality
```

---

## 7 · Pull request & board update

* Open PR → **Closes #Day‑13 issue**.
* CI should run pre‑commit & ESLint—expect all green.
* Merge → delete branch → drag card to **Done**.

---

### ✅ End‑of‑Day 13 Definition

* `.pre-commit-config.yaml` in repo; `pre-commit` installed and active.
* No Ruff/Black/isort or ESLint warnings in CI.
* All code auto‑formats on commit.

*Tomorrow (Day 14):* write Week‑2 retro, open Week‑3 column, optional Redpanda stub.
