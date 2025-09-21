# OMR Evaluation System - Deployment Guide

## 🌐 Web Hosting Options

### Option 1: GitHub Pages (Free & Recommended)

#### Step 1: Prepare Repository
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial OMR Evaluation System"

# Add remote repository
git remote add origin https://github.com/yourusername/omr-evaluator.git

# Push to GitHub
git push -u origin main
```

#### Step 2: Enable GitHub Pages
1. Go to your GitHub repository
2. Click on **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **Deploy from a branch**
5. Choose **main** branch and **/ (root)** folder
6. Click **Save**

#### Step 3: Access Your Site
- Your site will be available at: `https://yourusername.github.io/omr-evaluator/`
- Direct link to results: `https://yourusername.github.io/omr-evaluator/view_final_results.html`

### Option 2: Netlify (Free & Easy)

#### Step 1: Prepare Files
```bash
# Create index.html for redirect
echo '<!DOCTYPE html>
<html>
<head>
    <title>OMR Evaluation System</title>
    <meta http-equiv="refresh" content="0; url=view_final_results.html">
</head>
<body>
    <p>Redirecting to OMR Results...</p>
</body>
</html>' > index.html
```

#### Step 2: Deploy to Netlify
1. Go to [netlify.com](https://netlify.com)
2. Sign up/Login with GitHub
3. Click **New site from Git**
4. Choose **GitHub** and select your repository
5. Click **Deploy site**

#### Step 3: Custom Domain (Optional)
1. In Netlify dashboard, go to **Domain settings**
2. Add your custom domain
3. Configure DNS settings

### Option 3: Vercel (Free & Fast)

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Deploy
```bash
# In your project directory
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name? omr-evaluator
# - Directory? ./
```

#### Step 3: Access Your Site
- Vercel will provide a URL like: `https://omr-evaluator-xxx.vercel.app`

### Option 4: Heroku (Paid but Reliable)

#### Step 1: Create Heroku App
```bash
# Install Heroku CLI first
heroku create your-omr-app
```

#### Step 2: Create Procfile
```bash
echo "web: python -m http.server 8000" > Procfile
```

#### Step 3: Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 📦 Deployment Package

### Required Files for Web Hosting

```
omr_evaluator/
├── view_final_results.html        # Main results viewer
├── index.html                     # Redirect page (create this)
├── requirements.txt               # Python dependencies
├── README.md                      # Documentation
├── DEPLOYMENT_GUIDE.md           # This file
└── [other system files]
```

### Create Deployment Package

```bash
# Create deployment directory
mkdir omr_evaluator_deployment
cd omr_evaluator_deployment

# Copy essential files
cp ../view_final_results.html .
cp ../README.md .
cp ../requirements.txt .

# Create index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OMR Evaluation System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            margin: 0;
            padding: 50px;
            text-align: center;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            color: #a0a0a0;
        }
        .btn {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: bold;
            transition: transform 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-3px);
        }
        .features {
            margin-top: 50px;
            text-align: left;
        }
        .feature {
            margin: 15px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>OMR Evaluation System</h1>
        <p>Automated Optical Mark Recognition with Multiple Correct Answer Support</p>
        
        <a href="view_final_results.html" class="btn">View Results Dashboard</a>
        
        <div class="features">
            <h3>System Features:</h3>
            <div class="feature">✅ Mobile Photo Processing</div>
            <div class="feature">✅ Multiple Correct Answers Support</div>
            <div class="feature">✅ Batch Processing</div>
            <div class="feature">✅ Excel Integration</div>
            <div class="feature">✅ Beautiful Web Interface</div>
            <div class="feature">✅ Detailed Analytics</div>
        </div>
    </div>
</body>
</html>
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
EOF
```

## 🔧 Configuration for Different Hosts

### GitHub Pages Configuration

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

### Netlify Configuration

Create `netlify.toml`:
```toml
[build]
  publish = "."
  command = "echo 'Static site - no build needed'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Vercel Configuration

Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "view_final_results.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/view_final_results.html"
    }
  ]
}
```

## 📱 Mobile Optimization

### Responsive Design
The HTML viewer is already mobile-optimized with:
- Responsive grid layout
- Touch-friendly interface
- Mobile-first design
- Fast loading times

### PWA Support (Optional)

Create `manifest.json`:
```json
{
  "name": "OMR Evaluation System",
  "short_name": "OMR System",
  "description": "Automated OMR evaluation with multiple correct answer support",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#3498db",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## 🔒 Security Considerations

### For Production Deployment

1. **HTTPS Only**: Ensure all deployments use HTTPS
2. **Content Security Policy**: Add CSP headers
3. **Rate Limiting**: Implement if using server-side processing
4. **Input Validation**: Validate all user inputs
5. **File Upload Limits**: Set appropriate limits for file uploads

### Environment Variables

Create `.env` file for sensitive data:
```bash
# Database credentials (if using)
DB_HOST=localhost
DB_USER=username
DB_PASS=password

# API keys (if using external services)
API_KEY=your_api_key

# Security settings
SECRET_KEY=your_secret_key
```

## 📊 Analytics Integration

### Google Analytics

Add to your HTML files:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Custom Analytics

Track usage with custom events:
```javascript
// Track page views
gtag('event', 'page_view', {
  page_title: 'OMR Results Dashboard',
  page_location: window.location.href
});

// Track user interactions
gtag('event', 'click', {
  event_category: 'engagement',
  event_label: 'results_view'
});
```

## 🚀 Performance Optimization

### Image Optimization
- Compress images before upload
- Use WebP format for better compression
- Implement lazy loading for large images

### Caching Strategy
- Set appropriate cache headers
- Use CDN for static assets
- Implement browser caching

### Code Optimization
- Minify CSS and JavaScript
- Use compression (gzip/brotli)
- Optimize database queries (if applicable)

## 📞 Support & Maintenance

### Monitoring
- Set up uptime monitoring
- Monitor performance metrics
- Track error rates

### Updates
- Regular security updates
- Feature enhancements
- Bug fixes

### Backup Strategy
- Regular data backups
- Version control
- Disaster recovery plan

---

## 🎯 Quick Deployment Checklist

- [ ] Choose hosting platform
- [ ] Prepare deployment files
- [ ] Configure domain (if custom)
- [ ] Set up SSL certificate
- [ ] Test all functionality
- [ ] Monitor performance
- [ ] Set up analytics
- [ ] Create backup strategy

**Your OMR Evaluation System is ready for production!** 🚀
