# Amandeep Singh — Django Portfolio

A fully dynamic, single-page portfolio website built with Django.

## 📁 Project Structure

```
portfolio/
├── manage.py
├── requirements.txt
├── portfolio/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main/               # Portfolio app
    ├── models.py       # All data models
    ├── views.py        # Page views + contact endpoint
    ├── urls.py
    ├── admin.py        # Admin panel config
    ├── fixtures/
    │   └── initial_data.json   # Pre-filled CV data
    ├── templates/main/
    │   └── index.html
    └── static/main/
        ├── css/style.css
        └── js/main.js
```

## 🚀 Setup Instructions

### 1. Install Python (3.10+) and pip

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Load your CV data
```bash
python manage.py loaddata main/fixtures/initial_data.json
```

### 5. Create admin account
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**
Admin: **http://127.0.0.1:8000/admin**

---

## ✏️ Updating Your Data

All content is managed via the **Django Admin Panel**:
- Go to `/admin`
- Log in with your superuser credentials
- Update Profile, Projects, Skills, Education, Certificates, Achievements, etc.

### What to update later:
- [ ] Upload your profile photo in Profile
- [ ] Upload your resume PDF in Profile
- [ ] Add GitHub links to each project
- [ ] Add live demo links if you deploy projects
- [ ] Add any work experience when you get one
- [ ] Add open source contributions

---

## 🎨 Design

- **Dark theme** — terminal/data-science aesthetic
- **Font pairing** — Space Mono (headings) + DM Sans (body)
- **Colors** — Cyan (#00d4ff) accent on deep navy background
- **Features** — scroll reveal, typing animation, active nav highlighting, responsive mobile menu

---

## 📦 Sections Implemented

| # | Section | Status |
|---|---------|--------|
| 01 | Hero / Header | ✅ |
| 02 | About Me | ✅ |
| 03 | Skills | ✅ |
| 04 | Projects | ✅ |
| 05 | Experience | ✅ |
| 06 | Education | ✅ |
| 07 | Certifications | ✅ |
| 08 | Achievements | ✅ |
| 09 | Open Source | (add via admin) |
| 10 | Contact | ✅ |

---

## 🌐 Deployment (Optional)

For deploying to platforms like **Railway**, **Render**, or **PythonAnywhere**:

1. Set `DEBUG = False` in settings.py
2. Add your domain to `ALLOWED_HOSTS`
3. Run `python manage.py collectstatic`
4. Set `SECRET_KEY` as an environment variable

---

Built with ❤️ using Django | Amandeep Singh
