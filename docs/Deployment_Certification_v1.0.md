# Family Tree Project
📋
# Deployment Certification v1.0

| Gate | Module | Objective | Status |
|------|--------|-----------|--------|
| ✅ Gate 1 | Environment | Git, Backend, Build, Vite | PASS |
| ✅ Gate 2 | Authentication | Login + ACL | PASS |
| ✅ Gate 3 | Person | CRUD + Family Overview | PASS |
| ✅ Gate 4 | Marriage | CRUD + Permission + Delete Protection | PASS |
| ✅ Gate 5 | Parent Child | AP + AC + Validation | PASS |
| ✅ Gate 6 | Birth Order | Trigger + Pending Action | PASS |
| ✅ Gate 7 | Tree | Access Guard + Navigation | PASS |
| ✅ Gate 8 | Announcement | User + Admin | PASS |
| ✅ Gate 9 | Feedback | User + Admin | PASS |
| ✅ Gate 10 | Role | ACL Verification | PASS |
  ⏳  Gate 11 | Production Configuration | ENV / CORS / Secret Key | IN PROGRESS |
| ⏳ Gate 12 | Production Verification | Final Production Test | TODO |

## Production Endpoints

### Backend (Railway)
https://familytreeproject-avatar-production.up.railway.app

### Frontend Environment Variable (.env.production)
VITE_API_BASE_URL=https://familytreeproject-avatar-production.up.railway.app

### Frontend (Cloudflare)
https://silent-limit-c56a.ngocking56.workers.dev

### Railway Project
harmonious-forgiveness

### Railway Service
familytree_project-avatar

### Railway Production Branch
main

### Current Working Branch
redesign-db

### Recovery Point #1
GitHub commit: 0b0ed70
Date: 2026-06-24
Note: Production deploy paused because Railway was deploying old `main` branch while active code is on `redesign-db`.

Production Deploy Attempt #1 paused after discovering Railway deploys branch 'main' while active development branch is 'redesign-db'.