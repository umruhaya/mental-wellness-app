# Expose Service with Nginx using Certbot for SSL Certificate Guide

### Step 1: Install Nginx

1. Update your package manager:

```bash
sudo apt update
```

2. Install Nginx:

```bash
sudo apt install nginx -y
```

3. Enable and start the Nginx service:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Step 2: Configure Nginx

1. Create a new Nginx server block configuration file:

```bash
sudo vim /etc/nginx/sites-available/mentalwellness.umernaeem.com
```

2. Add the following configuration to set up a reverse proxy from Nginx to your Python server:

```nginx
server {
    listen 80;
    server_name mentalwellness.umernaeem.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Save this file by pressing `Esc`, writing `:wq` and then hitting Enter.

4. Enable the configuration by creating a symbolic link:

```bash
sudo ln -s /etc/nginx/sites-available/mentalwellness.umernaeem.com /etc/nginx/sites-enabled/
```

5. Test the Nginx configuration:

```bash
sudo nginx -t
```

6. Reload Nginx to apply the changes:

```bash
sudo systemctl reload nginx
```

### Step 3: Install Certbot and Obtain an SSL Certificate

1. Install Certbot and the Nginx plugin:

```bash
sudo apt install certbot python3-certbot-nginx -y
```

2. Obtain an SSL certificate:

```bash
sudo certbot --nginx -d mentalwellness.umernaeem.com
```

   Follow the prompts to complete the SSL certificate issuance. Certbot will automatically update your Nginx configuration to redirect HTTP to HTTPS.

### Step 4: Verify the Setup

1. Open your browser and navigate to `https://mentalwellness.umernaeem.com`.
2. You should see your Python application served over HTTPS.

### Step 5: Automate Certificate Renewal

Certbot automatically sets up a cron job to renew the certificates. You can verify this with:

```bash
sudo systemctl status certbot.timer
```

Or, manually test the renewal process with:

```bash
sudo certbot renew --dry-run
```

And that's it! Your Python server should now be securely accessible via HTTPS at `https://mentalwellness.umernaeem.com`.