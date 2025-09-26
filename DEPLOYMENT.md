# Deployment README

## Public Deployment Guidelines

### ⚠️ Legal and Ethical Considerations

**IMPORTANT**: This port scanner is for educational purposes only. Before deploying publicly:

1. **Only scan authorized targets** - Never scan systems you don't own or lack permission to test
2. **Respect rate limits** - The included security features help prevent abuse
3. **Check local laws** - Network scanning may be restricted in some jurisdictions
4. **Review hosting ToS** - Many cloud providers prohibit aggressive network scanning

### Deployment Options

#### Option 1: Heroku (Recommended for beginners)
```bash
# Install Heroku CLI, then:
heroku create your-port-scanner-app
git add .
git commit -m "Initial commit"
git push heroku main
```

#### Option 2: Railway
```bash
# Connect your GitHub repo to Railway
# It will automatically deploy from requirements.txt
```

#### Option 3: DigitalOcean App Platform
1. Connect your GitHub repository
2. Select Python as runtime
3. Set run command: `python web_app.py`

#### Option 4: AWS Lambda (Advanced)
- Use Zappa or Serverless framework
- Add API Gateway for HTTP interface

### Security Features Included

1. **Target Whitelist**: Only allows scanning of approved test servers
2. **Rate Limiting**: 5 requests per minute per IP
3. **Port Range Limits**: Maximum 50 ports per scan
4. **Scan Delays**: Built-in delays between port checks
5. **Input Validation**: Validates all inputs

### Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web application:
```bash
python web_app.py
```

3. Visit http://127.0.0.1:5000

### Production Considerations

1. **Use a production WSGI server** (not Flask's dev server):
```bash
pip install gunicorn
gunicorn web_app:app
```

2. **Add proper logging**
3. **Use a database for rate limiting** (Redis recommended)
4. **Add HTTPS/SSL certificates**
5. **Monitor usage and set alerts**
6. **Consider adding authentication**

### Environment Variables for Production

Create a `.env` file:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_PORTS=25
RATE_LIMIT=3
```

### Disclaimer Template

Include this disclaimer prominently:

---
**EDUCATIONAL USE ONLY**

This tool is provided for educational and authorized testing purposes only. Users are responsible for complying with all applicable laws and regulations. Unauthorized network scanning may violate:
- Computer Fraud and Abuse Act (CFAA) in the US
- Computer Misuse Act in the UK  
- Similar laws in other jurisdictions
- Terms of service of hosting providers

By using this tool, you acknowledge that you will only scan systems you own or have explicit permission to test.

---

### Monitoring and Logging

Consider adding:
- Request logging with timestamps and IPs  
- Alerts for suspicious activity
- Usage analytics
- Error tracking (Sentry, etc.)

### Legal Protection

1. **Terms of Service**: Create clear ToS
2. **Privacy Policy**: Explain data handling
3. **User Agreement**: Require users to accept responsible use
4. **Geographic Restrictions**: Consider blocking certain regions
5. **Contact Information**: Provide abuse contact

Remember: You may be liable for how others use your deployed scanner. Deploy responsibly!